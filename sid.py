"""Tree output plugin

Idea copied from libsmi.
"""

import optparse
import sys
import time
import json
import collections
import re
import os

from pyang import plugin
from collections import OrderedDict

def pyang_plugin_init():
    plugin.register_plugin(SidPlugin())

class SidPlugin(plugin.PyangPlugin):

    def add_opts(self, optparser):
        optlist = [
            optparse.make_option("--sid-help",
                                 dest="sid_help",
                                 action="store_true",
                                 help="Print help on automatic SID generation"),
            optparse.make_option("--generate-sid-file",
                                 action="store",
                                 type="string",
                                 dest="generate_sid_file",
                                 help="Generate a .sid file."),
            optparse.make_option("--update-sid-file",
                                 action="store",
                                 type="string",
                                 dest="update_sid_file",
                                 help="Generate a .sid file based on a previous .sid file."),
            optparse.make_option("--check-sid-file",
                                 action="store",
                                 type="string",
                                 dest="check_sid_file",
                                 help="Check the consistency between a .sid file and the .yang file(s)."),
            optparse.make_option("--list-sid-file",
                                 action="store",
                                 type="string",
                                 dest="list_sid_file",
                                 help="List the .sid file content."),
            ]

        g = optparser.add_option_group("SID file specific options")
        g.add_options(optlist)

    def setup_ctx(self, ctx):
        if ctx.opts.sid_help:
            print_help()
            sys.exit(0)

    def setup_fmt(self, ctx):
        ctx.implicit_errors = False

    def post_validate_ctx(self, ctx, modules):
        if ctx.opts.generate_sid_file is None and ctx.opts.update_sid_file is None and ctx.opts.check_sid_file is None and ctx.opts.list_sid_file is None:
            return

        sid_file = SidFile()

        if ctx.opts.generate_sid_file is not None:
            sid_file.range = ctx.opts.generate_sid_file

        if ctx.opts.update_sid_file is not None:
            sid_file.input_file_name = ctx.opts.update_sid_file

        if ctx.opts.check_sid_file is not None:
            sid_file.input_file_name = ctx.opts.check_sid_file
            sid_file.check_consistency = True
            print("Checking the consistency of '%s'" % sid_file.input_file_name)

        if ctx.opts.list_sid_file is not None:
            sid_file.input_file_name = ctx.opts.list_sid_file
            sid_file.list_content = True

        try:
            sid_file.process_sid_file(modules[0])

        except SidParcingError as e:
            sys.stderr.write("ERROR, %s\n" % e.msg)
            sys.exit(1)
        except SidFileError as e:
            sys.stderr.write("ERROR in '%s', %s\n" % (sid_file.input_file_name, e.msg))
            sys.exit(1)
        except FileNotFoundError as e:
            sys.stderr.write("ERROR, file '%s' not found\n" % e.filename)
            sys.exit(1)
        except json.decoder.JSONDecodeError as e:
            sys.stderr.write("ERROR in '%s', %s\n" % (sid_file.input_file_name, e.msg))
            sys.exit(1)

def print_help():
    print("""
Structure IDentifier (SID) are used to map YANG definitions to
the CBOR encoding. These SIDs can be automatically generated
for a YANG module using the pyang sid plugin.

The first time a .sid file is generated, the entry-point and size
of the registered range of SIDs is provided as argument to
pyang. For more details on registration process, see:
[I-D] veillette-core-yang-cbor-mapping

   pyang --generate-sid-file <entry-point:size> <yang-module> …

For example:
   pyang --generate-sid-file 20000:100 toaster@2009-11-20.yang

The name of the .sid file generated is:

   "<module-name>@<module-revision>.sid"

Each time new thing(s) are added to a YANG module by the
introduction of a new revision of this module, its included
sub-module(s) or imported module(s), the .sid file need to be
updated. This is done by providing the name of the previous
.sid file as argument.

   pyang --update-sid-file <file-name> <yang-module> …

The --check-sid-file option can be used at any time to verify
if the .sid file need to be updated.

   pyang --check-sid-file <file-name> <yang-module> …

The --list-sid-file can also be used at any time to list
the content of a .sid file and verify its consistency.

   pyang --list-sid-file <file-name> <yang-module> …
"""
)

############################################################
class SidFileError(Exception):
    def __init__(self, msg=""):
        self.msg = msg

class SidParcingError(Exception):
    """raised by plugins to fail the emit() function"""
    def __init__(self, msg=""):
        self.msg = msg

############################################################
class SidFile:
    def __init__(self):
        self.is_consistent = True
        self.check_consistency = False
        self.list_content = False
        self.input_file_name = None
        self.range = None

    def process_sid_file(self, module):
        self.module_name = module.i_modulename
        self.module_revision = self.get_module_revision(module)
        self.assigment_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        self.output_file_name = '%s@%s.sid' % (self.module_name, self.module_revision)

        if self.range is not None:
            self.set_initial_range(self.range)

        if self.input_file_name is not None:
            with open(self.input_file_name) as f:
                self.content = json.load(f, object_pairs_hook=collections.OrderedDict)
            self.validate_key_and_value()
            self.sort_ranges()
            self.validate_ovelaping_ranges()
            self.validate_sid()

        self.set_module_information()
        self.collect_module_things(module)
        self.sort_things()
        self.assign_sid()

        if self.check_consistency:
            self.list_deleted_things()
            self.list_new_things()
            if self.is_consistent:
                print("Check completed successfully")
            else:
                print("The .sid file need to be updated.")
            return

        if self.list_content:
            print("SIDs assigned to module '%s', revision '%s':\n" % (self.module_name, self.module_revision))
            self.list_things()
            print("\nDone")
            return

        self.list_deleted_things()
        if self.is_consistent:
            print("No .sid file generated, the current .sid file is already up to date.")
        else:
            print("Generating %s ..." % self.output_file_name)
            self.generate_file()
            print("Done")

    ########################################################
    def set_initial_range(self, range):
        components = range.split(':')
        if len(components) != 2 or not re.match(r'\d+:\d+', range):
            raise SidParcingError("invalid range in argument, must be '<entry-point>:<size>'.")

        self.content = OrderedDict([('assigment-ranges', [])])
        self.content['assigment-ranges'].append(OrderedDict([('entry-point', int(components[0])), ('size', int(components[1]))]))

    ########################################################
    # Retrieve the module revision from the pyang context
    def get_module_revision(self, module):
        revision = None
        for substmt in module.substmts:
            if substmt.keyword == 'revision':
                if revision == None:
                    revision = substmt.arg
                else:
                    if revision < substmt.arg:
                        revision = substmt.arg

        if revision == None:
            raise SidParcingError("no revision found in YANG definition file.")
        return revision

    ########################################################
    # Set the 'module-name' and/or 'module-revision' in the .sid file if require
    def set_module_information(self):
        if 'module-name' not in self.content or self.module_name != self.content['module-name']:
            self.content['module-name'] = self.module_name
            if self.check_consistency == True:
                print("ERROR, Mismatch between the module name defined in the .sid file and the .yang file.")
                self.is_consistent = False

        if 'module-revision' not in self.content or self.module_revision != self.content['module-revision']:
            self.content['module-revision'] = self.module_revision
            if self.check_consistency == True:
                print("ERROR, Mismatch between the module revision defined in the .sid file and the .yang file.")
                self.is_consistent = False

    ########################################################
    # Verify the tag and data type of each .sid file JSON object
    def validate_key_and_value(self):
        for key in self.content:

            if key == 'assigment-ranges':
                if type(self.content[key]) != list:
                    raise SidFileError("key 'assigment-ranges', invalid  value.")
                self.validate_ranges(self.content[key])
                continue

            if key == 'module-name':
                continue

            if key == 'module-revision':
                continue

            if key == 'things':
                if type(self.content[key]) != list:
                    raise SidFileError("key 'things', invalid value.")
                self.validate_things(self.content[key])
                continue

            raise SidFileError("invalid key '%s'." % key)

    def validate_ranges(self, ranges):
        for range in ranges:
            for key in range:
                if key == 'entry-point':
                    if type(range[key]) != int:
                        raise SidFileError("invalid 'entry-point' value '%s'." % range[key])
                    continue

                if key == 'size':
                    if type(range[key]) != int:
                        raise SidFileError("invalid 'size' value '%s'." % range[key])
                    continue

                raise SidFileError("invalid key '%s'." % key)

    def validate_things(self, things):
        for thing in things:
            for key in thing:
                if key == 'type':
                    if type(thing[key]) != str or not re.match(r'identity$|node$|notification$|notification-parameter \S*$|rpc$|rpc-input \S*$|rpc-output \S*$', thing[key]):
                        raise SidFileError("invalid 'type' value '%s'." % thing[key])
                    continue

                if key == 'assigned':
                    if type(thing[key]) != str or not re.match(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ', thing[key]):
                        raise SidFileError("invalid 'assigned' value '%s'." % thing[key])
                    continue

                if key == 'label':
                    if type(thing[key]) != str:
                        raise SidFileError("invalid 'label' value '%s'." % thing[key])
                    continue

                if key == 'sid':
                    if type(thing[key]) != int:
                        raise SidFileError("invalid 'sid' value '%s'." % thing[key])
                    continue

                raise SidFileError("invalid key '%s'." % key)

    ########################################################
    # Sort the range list by 'entry-point'
    def sort_ranges(self):
        if 'assigment-ranges' in self.content:
            self.content['assigment-ranges'].sort(key=lambda range:range['entry-point'])

    ########################################################
    # Verify if each range defined in the .sid file is distinct
    def validate_ovelaping_ranges(self):
        if 'assigment-ranges' in self.content:
            last_highest_sid = 0
            for range in self.content['assigment-ranges']:
                if range['entry-point'] < last_highest_sid:
                    raise SidFileError("overlapping ranges are not allowed.")
                last_highest_sid += range['entry-point'] + range['size']

    ########################################################
    # Verify if each SID listed in things is in range and is not duplicate.
    def validate_sid(self):
        self.content['things'].sort(key=lambda thing:thing['sid'])
        last_sid = -1
        for thing in self.content['things']:
            if self.out_of_ranges(thing['sid']):
                raise SidFileError("'sid' %d not within 'assigment-ranges'" % thing['sid'])
            if thing['sid'] == last_sid:
                raise SidFileError("duplicated 'sid' value %d " % thing['sid'])
                last_sid = thing['sid']

    def out_of_ranges(self, sid):
        for range in self.content['assigment-ranges']:
            if sid >= range['entry-point'] and sid < range['entry-point'] + range['size']:
                return False
        return True

    ########################################################
    # Collection of things defined in .yang file(s)
    def collect_module_things(self, module):
        if 'things' not in self.content:
            self.content['things'] = []

        for thing in self.content['things']:
            thing['status'] = 'd' # Set to 'd' deleted, updated to 'o' if present in .yang file

        for children in module.i_children:
            if children.keyword == 'leaf' or children.keyword == 'leaf-list' or children.keyword == 'anyxml':
                self.merge_thing('node', "/%s" % children.arg)

            if children.keyword == 'container' or children.keyword == 'list':
                self.merge_thing('node', "/%s" % children.arg)
                self.collect_inner_data_nodes(children.i_children, 'node', "/%s/" % children.arg)

            if children.keyword == 'rpc':
                self.merge_thing('rpc', "%s" % children.arg)
                self.collect_rpc_input_and_output(children.i_children, children.arg, "/")

            if children.keyword == 'notification':
                self.merge_thing('notification', "%s" % children.arg)
                self.collect_inner_data_nodes(children.i_children, "notification-parameter %s" % children.arg, "/")

        for identity in module.i_identities:
                self.merge_thing('identity', "%s:%s" % (module.i_modulename, identity))

        for substmt in module.substmts:
            if substmt.keyword == 'augment':
                self.collect_augment_data_nodes(substmt.substmts)

    def collect_inner_data_nodes(self, children, type, label):
        for statement in children:
            if statement.keyword == 'leaf' or statement.keyword == 'leaf-list' or statement.keyword == 'anyxml':
                self.merge_thing(type, "%s%s" % (label, statement.arg))

            if statement.keyword == 'container' or statement.keyword == 'list':
                self.merge_thing(type, "%s%s" % (label, statement.arg))
                self.collect_inner_data_nodes(statement.i_children, type, "%s%s/" % (label, statement.arg))

    def collect_rpc_input_and_output(self, children, rpc_name, label):
        for statement in children:
            if statement.keyword == 'input' or statement.keyword == 'output':
                self.collect_inner_data_nodes(statement.i_children, "rpc-%s %s" % (statement.keyword, rpc_name), label)

    def getPath(self, statement, path = ""):
        if statement.keyword == 'container' or statement.keyword == 'list':
            path = "/" + statement.arg + path
        if statement.parent != None:
            path = self.getPath(statement.parent, path)
        return path

    def collect_augment_data_nodes(self, statement):
        for substmt in statement:
            if substmt.keyword == 'leaf' or substmt.keyword == 'leaf-list' or substmt.keyword == 'anyxml':
                path = self.getPath(substmt.parent)
                self.merge_thing('node', "%s/%s" % (path, substmt.arg))

            if substmt.keyword == 'container' or substmt.keyword == 'list':
                path = self.getPath(substmt.parent)
                self.merge_thing('node', "%s/%s" % (path, substmt.arg))
                self.collect_augment_data_nodes(substmt.i_children)

    def merge_thing(self, type, label):
        for thing in self.content['things']:
            if (type == thing['type'] and label == thing['label']):
                thing['status'] = 'o' # Thing already assigned
                return
        self.content['things'].append(OrderedDict([('type', type),('assigned', self.assigment_time), ('label', label), ('sid', -1), ('status', 'n')]))
        self.is_consistent = False

    ########################################################
    # Sort the things list by 'type', 'assigned' and 'label'
    def sort_things(self):
        self.content['things'].sort(key=lambda thing:thing['label'])
        self.content['things'].sort(key=lambda thing:thing['assigned'])
        self.content['things'].sort(key=lambda thing:thing['type'])

    ########################################################
    # Identifier assignment
    def assign_sid(self):
        last_type = ''
        for i in range(len(self.content['things'])):
            if self.content['things'][i]['type'] != last_type:
                sid = self.get_hihest_sid(i)
                last_type = self.content['things'][i]['type']
            if self.content['things'][i]['sid'] == -1:
                self.content['things'][i]['sid'] = sid
                sid = self.get_next_sid(sid)

    def get_hihest_sid(self, i):
        current_type = self.content['things'][i]['type']
        sid = self.content['assigment-ranges'][0]['entry-point']

        for j in range(i, len(self.content['things'])):
            if (self.content['things'][j]['type'] != current_type):
                return sid
            if (self.content['things'][j]['sid'] >= sid):
                sid = self.content['things'][j]['sid']
                sid = self.get_next_sid(sid)

        return sid

    def get_next_sid(self, sid):
        sid += 1
        for i in range(len(self.content['assigment-ranges'])):
            if sid < self.content['assigment-ranges'][i]['entry-point'] + self.content['assigment-ranges'][i]['size']:
                return sid
            else:
                if i + 1 < len(self.content['assigment-ranges']):
                    if sid < self.content['assigment-ranges'][i+1]['entry-point']:
                        return self.content['assigment-ranges'][i+1]['entry-point']

        raise SidParcingError("SID range(s) exhausted, extend the allocation range or add a new one.")

    ########################################################
    def list_things(self):
        for thing in self.content['things']:
            if thing['status'] == 'd':
                print("WARNING, thing '%s' have been deleted form the .yang files, it should be reintroduced with a 'deprecated' or 'obsolete' status." % thing['label'])
            if thing['status'] == 'n':
                print("WARNING, thing '%s' is not defined in the .sid file." % thing['label'])
            if thing['status'] == 'o':
                print("%s assigned to %s '%s'" % (thing['sid'], thing['type'], thing['label']))

    ########################################################
    def list_deleted_things(self):
        for thing in self.content['things']:
            if thing['status'] == 'd':
                print("WARNING, thing '%s' have been deleted form the .yang files, it should be reintroduced with a 'deprecated' or 'obsolete' status." % thing['label'])

    ########################################################
    def list_new_things(self):
        for thing in self.content['things']:
            if thing['status'] == 'n':
                print("WARNING, thing '%s' is not defined in the .sid file." % thing['label'])

    ########################################################
    def generate_file(self):
        for thing in self.content['things']:
            del thing['status']

        if os.path.exists(self.output_file_name):
            os.remove(self.output_file_name)

        with open(self.output_file_name, 'w') as outfile:
            json.dump(self.content, outfile, indent=2)

