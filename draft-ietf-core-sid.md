---
stand_alone: true
ipr: trust200902
docname: draft-ietf-core-sid-latest
title: YANG Schema Item iDentifier (YANG SID)
area: Applications and Real-Time Area (art)
wg: Internet Engineering Task Force
kw: CBOR
cat: std
pi:
  strict: 'yes'
  toc: 'yes'
  tocdepth: '4'
  symrefs: 'yes'
  sortrefs: 'yes'
  compact: 'yes'
  subcompact: 'no'
author:
- role: editor
  ins: M. V. Veillette
  name: Michel Veillette
  org: Trilliant Networks Inc.
  street: 610 Rue du Luxembourg
  code: J2J 2V2
  city: Granby
  region: Quebec
  country: Canada
  phone: "+14503750556"
  email: michel.veillette@trilliant.com
- role: editor
  ins: A. P. Pelov
  name: Alexander Pelov
  org: Acklio
  street: 1137A avenue des Champs Blancs
  code: '35510'
  city: Cesson-Sevigne
  region: Bretagne
  country: France
  email: a@ackl.io
- role: editor
  ins: I. Petrov
  name: Ivaylo Petrov
  org: Google Switzerland GmbH
  street: Brandschenkestrasse 110
  code: 8002
  city: Zurich
  region: Zurich
  country: Switzerland
  email: ivaylopetrov@google.com
- ins: C. Bormann
  name: Carsten Bormann
  org: Universität Bremen TZI
  street: Postfach 330440
  city: D-28359 Bremen
  country: Germany
  phone: "+49-421-218-63921"
  email: cabo@tzi.org

normative:
  RFC3688:
  RFC6991:
#  RFC7120: BCP100
  BCP100:
  RFC7950:
  RFC7951:
  RFC8040:
  I-D.ietf-core-yang-cbor:
informative:
  RFC6020:
  RFC6241:
  RFC7224:
  RFC7317:
  RFC8126:
  RFC8341:
  RFC8343:
  RFC8344:
  RFC8366:
  RFC7317:
  I-D.ietf-core-comi: comi
  I-D.ietf-core-yang-library: yang-library
  I-D.ietf-anima-constrained-voucher: constrained-voucher

--- abstract

YANG Schema Item iDentifiers (YANG SID) are globally unique 63-bit unsigned integers used to identify YANG items.  This document defines the semantics, the registration, and assignment processes of YANG SIDs.  To enable the implementation of these processes, this document also defines a file format used to persist and publish assigned YANG SIDs.

--- middle

# Introduction

Some of the items defined in YANG {{RFC7950}} require the use of a unique identifier.  In both Network Configuration Protocol(NETCONF) {{RFC6241}} and RESTCONF {{RFC8040}}, these identifiers are implemented using names.  To allow the implementation of data models defined in YANG in constrained devices and constrained networks, a more compact method to identify YANG items is required. This compact identifier, called YANG SID or simply SID in this document and when the context is clear, is encoded using a 63-bit unsigned integer. The limitation to 63-bit unsigned integers allows SIDs to be manipulated more easily on platforms that might otherwise lack native 64-bit unsigned arithmetic. The loss of a single bit of range is not significant given the size of the remaining space.

The following items are identified using SIDs:

* identities

* data nodes (Note: including those nodes defined by the 'yang-data' extension.)

* remote procedure calls (RPCs) and associated input(s) and output(s)

* actions and associated input(s) and output(s)

* notifications and associated information

* YANG modules, submodules and features

It is possible that some protocols use only a subset of the assigned SIDs, for
example, for protocols equivalent to NETCONF {{RFC6241}} like {{-comi}} the
transportation of YANG module SIDs might be unnecessary. Other protocols
might need to be able to transport this information, for example protocols
related to discovery such as Constrained YANG Module Library {{-yang-library}}.

SIDs are globally unique integers.  A registration system is used in order to
guarantee their uniqueness. SIDs are registered in blocks called "SID ranges".

Assignment of SIDs to YANG items can be automated. For more details how this
can be achieved, please consult {{sid-auto-generation}}.

SIDs are assigned permanently, items introduced by a new revision of a YANG
module are added to the list of SIDs already assigned. If the meaning of an
item changes, for example as a result from a non-backward compatible update of
the YANG module, a new SID SHOULD be assigned to it. A new SID MUST always be
assigned if the new meaning of the item is going to be referenced using a SID.

{{sid-lifecycle}} provides more details about the registration process of YANG
modules and associated SIDs. To enable the implementation of this registry,
{{sid-file-format}} defines a standard file format used to store and publish
SIDs.

# Terminology and Notation

{::boilerplate bcp14-tagged}

The following terms are defined in {{RFC7950}}:

* action
* feature
* module
* notification
* RPC
* schema node
* schema tree
* submodule

The following term is defined in {{RFC8040}}:

* yang-data extension

This specification also makes use of the following terminology:

* item:  A schema node, an identity, a module, a submodule or a feature defined using the YANG modeling language.
* schema-node path: A schema-node path is a string that identifies a schema node within the schema tree. A path consists of the list of consecutive schema node identifier(s) separated by slashes ("/"). Schema node identifier(s) are always listed from the top-level schema node up to the targeted schema node and could contain namespace information. (e.g. "/ietf-system:system-state/clock/current-datetime")
* Namespace-qualified form - a schema node identifier is prefixed with the name of the module in which the schema node is defined, separated from the schema node identifier by the colon character (":").
* YANG Schema Item iDentifier (YANG SID or simply SID): Unsigned integer used to identify different YANG items.

# ".sid" file lifecycle  {#sid-lifecycle}

YANG is a language designed to model data accessed using one of the compatible
protocols (e.g. NETCONF {{RFC6241}}, RESTCONF {{RFC8040}} and CORECONF {{-comi}}). A
YANG module defines hierarchies of data, including configuration, state data,
RPCs, actions and notifications.

Many YANG modules are not created in the context of constrained
applications. YANG modules can be implemented using NETCONF {{RFC6241}} or
RESTCONF {{RFC8040}} without the need to assign SIDs.

As needed, authors of YANG modules can assign SIDs to their YANG modules. In
order to do that, they should first obtain a SID range from a registry and use
that range to assign or generate SIDs to items of their YANG module. The
assignments can then be stored in a ".sid" file. For
example on how this could be achieved, please refer to {{sid-lifecycle-ex}}.

Registration of the ".sid" file associated to a YANG module is optional but
recommended to promote interoperability between devices and to avoid duplicate
allocation of SIDs to a single YANG module. Different registries might have
different requirements for the registration and publication of the ".sid"
files. For a diagram of one of the possibilities, please refer to the activity
diagram on {{fig-sid-file-creation}} in {{sid-lifecycle-ex}}.

Each time a YANG module or one of its imported module(s) or included
sub-module(s) is updated, a new ".sid" file MAY be created if the new or
updated items will need SIDs. All the SIDs present in the previous version of
the ".sid" file MUST be present in the new version as well. The creation of
this new version of the ".sid" file SHOULD be performed using an automated
tool.

If a new revision requires more SIDs than initially allocated, a new SID range
MUST be added to the 'assignment-range' as defined in {{sid-file-format}}.
These extra SIDs are used for subsequent assignments.

For an example of this update process, see activity diagram
{{fig-sid-file-update}} in {{sid-lifecycle-ex}}.

# ".sid" file format  {#sid-file-format}

".sid" files are used to persist and publish SIDs assigned to the different
YANG items of a specific YANG module. It has the following structure.

~~~~
module: ietf-sid-file
  +-- sid-file
     +-- module-name?              yang:yang-identifier
     +-- module-revision?          revision-identifier
     +-- sid-file-version?         sid-file-version-identifier
     +-- description?              string
     +-- dependency-revision* [module-name]
     |  +-- module-name        yang:yang-identifier
     |  +-- module-revision    revision-identifier
     +-- assignment-range* [entry-point]
     |  +-- entry-point    sid
     |  +-- size           uint64
     +-- item* [namespace identifier]
        +-- namespace     enumeration
        +-- identifier    union
        +-- sid           sid
~~~~

The following YANG module defined the structure of this file, encoding is
performed using the rules defined in {{RFC7951}}. It references ietf-yang-types
defined in {{RFC6991}} and ietf-restconf defined in {{RFC8040}}.

RFC Ed.: please update the date of the module and Copyright if needed and remove this note.

~~~~
<CODE BEGINS> file "ietf-sid-file@2020-02-05.yang"
module ietf-sid-file {
  yang-version 1.1;
  namespace "urn:ietf:params:xml:ns:yang:ietf-sid-file";
  prefix sid;

  import ietf-yang-types {
    prefix yang;
    reference "RFC 6991: Common YANG Data Types.";
  }
  import ietf-restconf {
    prefix rc;
    reference "RFC 8040: RESTCONF Protocol.";
  }

  organization
    "IETF Core Working Group";

  contact
    "WG Web:   <http://datatracker.ietf.org/wg/core/>

     WG List:  <mailto:core@ietf.org>

     Editor:   Michel Veillette
               <mailto:michel.veillette@trilliant.com>

     Editor:   Andy Bierman
               <mailto:andy@yumaworks.com>

     Editor:   Alexander Pelov
               <mailto:a@ackl.io>

     Editor:   Ivaylo Petrov
               <mailto:ivaylopetrov@google.com>";

  description
    "Copyright (c) 2021 IETF Trust and the persons identified as
     authors of the code.  All rights reserved.

     Redistribution and use in source and binary forms, with or
     without modification, is permitted pursuant to, and subject to
     the license terms contained in, the Simplified BSD License set
     forth in Section 4.c of the IETF Trust's Legal Provisions
     Relating to IETF Documents
     (https://trustee.ietf.org/license-info).

     This version of this YANG module is part of RFC XXXX
     (https://www.rfc-editor.org/info/rfcXXXX); see the RFC itself
     for full legal notices.

     The key words 'MUST', 'MUST NOT', 'REQUIRED', 'SHALL', 'SHALL
     NOT', 'SHOULD', 'SHOULD NOT', 'RECOMMENDED', 'NOT RECOMMENDED',
     'MAY', and 'OPTIONAL' in this document are to be interpreted as
     described in BCP 14 (RFC 2119) (RFC 8174) when, and only when,
     they appear in all capitals, as shown here.

     This module defines the structure of the .sid files.

     Each .sid file contains the mapping between the different
     string identifiers defined by a YANG module and a
     corresponding numeric value called YANG SID.";

  revision 2020-02-05 {
    description
      "Initial revision.";
    reference
      "[I-D.ietf-core-sid] YANG Schema Item iDentifier (YANG SID)";
  }

  typedef revision-identifier {
    type string {
      pattern '\d{4}-\d{2}-\d{2}';
    }
    description
      "Represents a date in YYYY-MM-DD format.";
  }

  typedef sid-file-version-identifier {
    type uint64;
    description
      "Represents the version of a .sid file.";
  }

  typedef sid {
    type uint64 {
      range "0..9223372036854775807";
    }
    description
      "YANG Schema Item iDentifier";
    reference
      "[I-D.ietf-core-sid] YANG Schema Item iDentifier (YANG SID)";
  }

  typedef schema-node-path {
    type string {
      pattern
        '/[a-zA-Z_][a-zA-Z0-9\-_.]*:[a-zA-Z_][a-zA-Z0-9\-_.]*' +
        '(/[a-zA-Z_][a-zA-Z0-9\-_.]*(:[a-zA-Z_][a-zA-Z0-9\-_.]*)?)*';
    }
    description
      "A schema-node path is an absolute YANG schema node identifier
      as defined by the YANG ABNF rule absolute-schema-nodeid,
      except that module names are used instead of prefixes.

      This string additionally follows the following rules:

       o  The leftmost (top-level) data node name is always in the
          namespace-qualified form.
       o  Any subsequent schema node name is in the
          namespace-qualified form if the node is defined in a module
          other than its parent node, and the simple form is used
          otherwise. No predicates are allowed.";
    reference
      "RFC 7950, The YANG 1.1 Data Modeling Language;
       Section 6.5: Schema Node Identifier;";
  }

  rc:yang-data sid-file {
      uses sid-file;
  }

  grouping sid-file {
    description "A grouping that contains a YANG container
      representing the file structure of a .sid files.";

    container sid-file {
      description
        "A Wrapper container that together with the rc:yang-data
        extension marks the YANG data structures inside as not being
        intended to be implemented as part of a configuration
        datastore or as an operational state within the server.";
      leaf module-name {
        type yang:yang-identifier;
        description
          "Name of the YANG module associated with this .sid file.";
      }

      leaf module-revision {
        type revision-identifier;
        description
          "Revision of the YANG module associated with this .sid
          file.
          This leaf is not present if no revision statement is
          defined in the YANG module.";
      }

      leaf sid-file-version {
        type sid-file-version-identifier;
        default 0;
        description
          "Optional leaf that specifies the version number of the
          .sid file.  .sid files and the version sequence are
          specific to a given YANG module revision. This number
          starts at zero when there is a new YANG module revision and
          increases monotonically.  This number can distinguish
          updates to the .sid file which are the result of new
          processing, or the result of reported errata.";
      }

      leaf description {
        type string;
        description
          "Free-form meta information about the generated file. It
          might include .sid file generation tool and time among
          other things.";
      }

      list dependency-revision {
        key "module-name";

        description
          "Information about the used revision during the .sid file
          generation of each YANG module that the module in
          'module-name' imported.";

        leaf module-name {
          type yang:yang-identifier;
          description
            "Name of the YANG module, dependency of 'module-name',
            for which revision information is provided.";
        }
        leaf module-revision {
          type revision-identifier;
          mandatory true;
          description
            "Revision of the YANG module, dependency of
            'module-name', for which revision information is
            provided.";
        }
      }

      list assignment-range {
        key "entry-point";
        description
          "YANG SID range(s) allocated to the YANG module identified
          by 'module-name' and 'module-revision'.

          - The YANG SID range first available value is entry-point
            and the the last available value in the range is
            (entry-point + size - 1).
          - The YANG SID ranges specified by all assignment-rages
            MUST NOT overlap.";

        leaf entry-point {
          type sid;
          description
            "Lowest YANG SID available for assignment.";
        }

        leaf size {
          type uint64;
          mandatory true;
          description
            "Number of YANG SIDs available for assignment.";
        }
      }

      list item {
        key "namespace identifier";
        unique "sid";

        description
          "Each entry within this list defined the mapping between
          a YANG item string identifier and a YANG SID. This list
          MUST include a mapping entry for each YANG item defined by
          the YANG module identified by 'module-name' and
          'module-revision'.";

        leaf namespace {
          type enumeration {
            enum module {
              value 0;
              description
                "All module and submodule names share the same
                global module identifier namespace.";
            }
            enum identity {
              value 1;
              description
                "All identity names defined in a module and its
                submodules share the same identity identifier
                namespace.";
            }
            enum feature {
              value 2;
              description
                "All feature names defined in a module and its
                submodules share the same feature identifier
                namespace.";
            }
            enum data {
              value 3;
              description
                "The namespace for all data nodes, as defined in
                YANG.";
            }
          }
          description
            "Namespace of the YANG item for this mapping entry.";
        }

        leaf identifier {
          type union {
            type yang:yang-identifier;
            type schema-node-path;
          }
          description
            "String identifier of the YANG item for this mapping
            entry.

            If the corresponding 'namespace' field is 'module',
            'feature', or 'identity', then this field MUST
            contain a valid YANG identifier string.

            If the corresponding 'namespace' field is 'data',
            then this field MUST contain a valid schema node
            path.";
        }

        leaf sid {
          type sid;
          mandatory true;
          description
            "YANG SID assigned to the YANG item for this mapping
            entry.";
        }
      }
    }
  }
}
<CODE ENDS>
~~~~
{: align="left"}

# Content-Types {#content-type}

The following Content-Type has been defined in {{I-D.ietf-core-yang-cbor}}:

application/yang-data+cbor; id=sid:

: This Content-Type represents a CBOR YANG document containing one or multiple data node values.
  Each data node is identified by its associated SID.

: FORMAT: CBOR map of SID, instance-value

: The message payload of Content-Type 'application/yang-data+cbor' is encoded using a CBOR map.
  Each entry within the CBOR map contains the data node identifier (i.e. SID) and the associated instance-value.
  Instance-values are encoded using the rules defined in {{Section 4 of I-D.ietf-core-yang-cbor}}.

# Security Considerations

This document defines a new type of identifier used to encode data models defined in YANG {{RFC7950}}. As such, this identifier does not contribute to any new security issues in addition of those identified for the specific protocols or contexts for which it is used.

# IANA Considerations  {#IANA}

## YANG Namespace Registration

This document registers the following XML namespace URN in the "IETF XML
Registry", following the format defined in {{RFC3688}}:

URI: please assign urn:ietf:params:xml:ns:yang:ietf-sid-file

Registrant Contact: The IESG.

XML: N/A, the requested URI is an XML namespace.

Reference:    RFC XXXX

// RFC Ed.: please replace XXXX with RFC number and remove this note

## Register ".sid" File Format Module {#iana-module-registration}

This document registers one YANG module in the "YANG Module Names" registry {{RFC6020}}:

* name:         ietf-sid-file
* namespace:    urn:ietf:params:xml:ns:yang:ietf-sid-file
* prefix:       sid
* reference:    [[RFC XXXX]]

// RFC Ed.: please replace XXXX with RFC number and remove this note

## CoAP Content-Formats Registry

A Content-Format for `application/yang-data+cbor; id=sid` has been
added to the "CoAP Content-Formats" within the "Constrained RESTful
Environments (CoRE) Parameters" registry, in
{{I-D.ietf-core-yang-cbor}}.

## Create new IANA Registry: "YANG SID Mega-Range" registry {#mega-range-registry}

The name of this registry is "YANG SID Mega-Range". This registry is used to record the delegation of the management of a block of SIDs to third parties (such as SDOs or registrars).

### Structure

Each entry in this registry must include:

* The entry point (first SID) of the registered SID block.
* The size of the registered SID block. The size MUST be one million (1 000 000) SIDs.
* The contact information of the requesting organization including:
  * The policy of SID range allocations: Public, Private or Both.
  * Organization name
  * URL

The information associated to the Organization name should not be publicly
visible in the registry, but should be available. This information includes
contact email and phone number and change controller email and phone number.

### Allocation policy

The IANA policy for future additions to this registry is "Expert Review" {{RFC8126}}.

An organization requesting to manage a YANG SID Range (and thus have an entry in the YANG SID Mega-Range Registry), must ensure the following capacities:

* The capacity to manage and operate a YANG SID Range Registry. A YANG SID Range Registry MUST provide the following information for all YANG SID Ranges allocated by the Registry:
    * Entry Point of allocated YANG SID Range
    * Size of allocated YANG SID Range
    * Type: Public or Private
        * Public Ranges MUST include at least a reference to the YANG module and ".sid" files for that YANG SID Range.
        * Private Ranges MUST be marked as "Private"
* A Policy of allocation, which clearly identifies if the YANG SID Range allocations would be Private, Public or Both.
* Technical capacity to ensure the sustained operation of the registry for a period of at least 5 years. If Private Registrations are allowed, the period must be of at least 10 years.


#### First allocation

For a first allocation to be provided, the requesting organization must demonstrate a functional registry infrastructure.

#### Consecutive allocations

On subsequent allocation request(s), the organization must demonstrate the
exhaustion of the prior range. These conditions need to be asserted by the
assigned expert(s).

If that extra-allocation is done within 3 years from the last allocation, the
experts need to discuss this request on the CORE working group mailing list and
consensus needs to be obtained before allocating a new Mega-Range.


### Initial contents of the Registry

The initial entry in this registry is allocated to IANA:

| Entry Point | Size    | Allocation | Organization name | URL      |
|-------------+---------+------------|-------------------|----------|
| 0           | 1000000 | Public     | IANA              | iana.org |
{: align="left"}

## Create a new IANA Registry: IETF YANG SID Range Registry (managed by IANA) {#ietf-iana-sid-range-allocation}

### Structure {#ietf-iana-sid-range-structure}

Each entry in this registry must include:

* The SID range entry point.
* The SID range size.
* The YANG module name.
* Document reference.

### Allocation policy {#ietf-iana-sid-range-allocation-policy}

The first million SIDs assigned to IANA is sub-divided as follows:

* The range of 0 to 999 (size 1000) is subject to "IESG Approval" as defined in {{RFC8126}}; of these, SID value 0 has been reserved for implementations to internally signify the absence of a SID number and does not occur in interchange.
* The range of 1000 to 59,999 (size 59,000) is designated for YANG modules defined in RFCs.
    * The IANA policy for additions to this registry is either:
        * "Expert Review" {{RFC8126}} in case the ".sid" file comes from a YANG module from an existing RFC, or
        * "RFC Required" {{RFC8126}} otherwise.
    * The Expert MUST verify that the YANG module for which this allocation is made has an RFC (existing RFC) OR is on track to become RFC (early allocation with a request from the WG chairs as defined by {{BCP100}}).
* The range of 60,000 to 99,999 (size 40,000) is reserved for experimental YANG modules. This range MUST NOT be used in operational deployments since these SIDs are not globally unique which limit their interoperability. The IANA policy for this range is "Experimental use" {{RFC8126}}.
* The range of 100,000 to 999,999 (size 900,000) is "Reserved" as defined in {{RFC8126}}.

| Entry Point | Size    | IANA policy              |
|-------------|---------|--------------------------|
| 0           | 1,000   | IESG Approval            |
| 1,000       | 59,000  | RFC Required             |
| 60,000      | 40,000  | Experimental/Private use |
| 100,000     | 900,000 | Reserved                 |
{: align="left"}

The size of the SID range allocated for a YANG module is recommended to be a multiple of 50 and to be at least 33% above the current number of YANG items. This headroom allows assignment within the same range of new YANG items introduced by subsequent revisions. The maximum SID range size is 1000. A larger size may be requested by the authors if this recommendation is considered insufficient. It is important to note that an additional SID range can be allocated to an existing YANG module if the initial range is exhausted.

In case a SID range is allocated for an existing RFC through the "Expert
Review" policy, the Document reference field for the given allocation should
point to the RFC that the YANG module is defined in.

In case a SID range is required before publishing the RFC due to
implementations needing stable SID values, early allocation as defined in
{{BCP100}} can be employed. As specified in {{Section 4.6 of RFC8126}}, RFCs
and by extension documents that are expected to become an RFC fulfill the
requirement for "Specification Required" stated in Section 2 of
{{BCP100}}, <!-- XXX xml2rfc bug-->
which allows for the early allocation process to be employed.

### Initial contents of the registry {#ietf-iana-sid-range-initial-contents}

Initial entries in this registry are as follows:

| Entry Point | Size | Module name                      | Document reference     |
|-------------|------|----------------------------------|------------------------|
|           0 |    1 | (Reserved: not a valid SID)      | RFCXXXX                |
|        1000 |  100 | ietf-coreconf                    | {{-comi}}                |
|        1100 |   50 | ietf-yang-types                  | {{RFC6991}}              |
|        1150 |   50 | ietf-inet-types                  | {{RFC6991}}              |
|        1200 |   50 | iana-crypt-hash                  | {{RFC7317}}              |
|        1250 |   50 | ietf-netconf-acm                 | {{RFC8341}}              |
|        1300 |   50 | ietf-sid-file                    | RFCXXXX                |
|        1500 |  100 | ietf-interfaces                  | {{RFC8343}}              |
|        1600 |  100 | ietf-ip                          | {{RFC8344}}              |
|        1700 |  100 | ietf-system                      | {{RFC7317}}              |
|        1800 |  400 | iana-if-type                     | {{RFC7224}}              |
|        2400 |   50 | ietf-voucher                     | {{RFC8366}}              |
|        2450 |   50 | ietf-constrained-voucher         | {{-constrained-voucher}} |
|        2500 |   50 | ietf-constrained-voucher-request | {{-constrained-voucher}} |
{: align="left" cols="5r 4r 26l 22l"}

// RFC Ed.: replace XXXX with RFC number assigned to this draft.

For allocation, RFC publication of the YANG module is required as per {{RFC8126}}. The YANG module must be registered in the "YANG module Name" registry according to the rules specified in {{Section 14 of RFC6020}}.

## Create new IANA Registry: "IETF YANG SID Registry" {#ietf-sid-registry}

The name of this registry is "IETF YANG SID Registry".  This registry is used to
record the allocation of SIDs for individual YANG module items.

### Structure

Each entry in this registry must include:

* The YANG module name. This module name must be present in the "Name" column of the "YANG Module Names" registry.
* A link to the associated ".yang" file.  This file link must be present in the "File" column of the "YANG Module Names" registry.
* The link to the ".sid" file which defines the allocation. The ".sid" file is stored by IANA.
* The number of actually allocated SIDs in the ".sid" file.

### Allocation policy

The allocation policy is Expert review. The Expert MUST ensure that the following conditions are met:

* The ".sid" file has a valid structure:
    * The ".sid" file MUST be a valid JSON file following the structure of the
      module defined in RFCXXXX (RFC Ed: replace XXX with RFC number assigned
      to this draft).
* The ".sid" file allocates individual SIDs ONLY in the YANG SID Ranges for this
  YANG module (as allocated in the IETF YANG SID Range Registry):
    * All SIDs in this ".sid" file MUST be within the ranges allocated to this
      YANG module in the "IETF YANG SID Range Registry".
* If another ".sid" file has already allocated SIDs for this YANG module (e.g.
  for older or newer versions of the YANG module), the YANG items are assigned
  the same SIDs as in the other ".sid" file.
* If there is an older version of the ".sid" file, all allocated SIDs from that
  version are still present in the current version of the ".sid" file.

### Recursive Allocation of YANG SID Range at Document Adoption {#recursive-allocation-at-adoption}

Due to the difficulty in changing SID values during IETF document processing,
it is expected that most documents will ask for SID allocations using Early
Allocations {{BCP100}}. The details of the Early Allocation should be included
in any Working Group Adoption call. Prior to Working Group Adoption, an internet
draft authors can use the experimental SID range (as per
{{ietf-iana-sid-range-allocation-policy}}) for their SIDs allocations or
other values that do not create ambiguity with other SID uses (for example
they can use a range that comes from a non-IANA managed "YANG SID Mega-Range"
registry).

After Working Group Adoption, any modification of a ".sid" file is expected to be
discussed on the mailing list of the appropriate Working Groups. Specific
attention should be paid to implementers' opinion after Working Group Last Call
if a SID value is to change its meaning. In all cases, a ".sid" file and the SIDs
associated with it are subject to change before the publication of an internet
draft as an RFC.

During the early use of SIDs, many existing, previously published YANG modules
will not have SID allocations.  For an allocation to be useful the included
YANG modules may also need to have SID allocations made.

The Expert Reviewer who performs the (Early) Allocation analysis will need to
go through the list of included YANG modules and perform SID allocations for
those modules as well.

* If the document is a published RFC, then the allocation of SIDs for its
  referenced YANG modules is permanent.  The Expert Reviewer provides the
  generated SID file to IANA for registration.  This process may be time
  consuming during a bootstrap period (there are over 100 YANG modules to date,
  none of which have SID allocations), but should quiet down once needed
  entries are allocated.
* If the document is an unprocessed Internet-Draft adopted in a WG, then an
  Early Allocation is performed for this document as well. Early Allocations
  require approval by an IESG Area Director.  An early allocation which
  requires additional allocations will list the other allocations in it's
  description, and will be cross-posted to the any other working group mailing
  lists.
* A YANG module which references a module in an document which has not yet been
  adopted by any working group will be unable to perform an Early Allocation
  for that other document until it is adopted by a working group.  As described
  in {{BCP100}}, an AD Sponsored document acts as if it had a working group.  The
  approving AD may also exempt a document from this policy by agreeing to AD
  Sponsor the document.

At the end of the IETF process all the dependencies of a given module for which
SIDs are assigned, should also have SIDs assigned. Those dependencies'
assignments should be permanent (not Early Allocation).

A previously SID-allocated YANG module which changes its references to include
a YANG module for which there is no SID allocation needs to repeat the Early
Allocation process.

Early Allocations are made with a one-year period, after which they are
expired.  {{BCP100}} indicates that at most one renewal may be made.  For the
SID allocation a far more lenient stance is desired.

1. An extension of a referencing documents Early Allocation should update any
   referenced Early Allocations to expire no sooner than the referencing
   document.
2. The {{BCP100}} mechanism allows the IESG to provide a second renewal,
   and such an event may prompt some thought about how the collection of
   documents are being processed.

This is driven by the very generous size of the SID space and the often complex
and deep dependencies of YANG modules.  Often a core module with many
dependencies will undergo extensive review, delaying the publication of other
documents.

{{BCP100}} also says:

    Note that if a document is submitted for review to the IESG and at
    the time of submission some early allocations are valid (not
    expired), these allocations should not be expired while the document
    is under IESG consideration or waiting in the RFC Editor's queue
    after approval by the IESG.

### Initial contents of the registry

None.

--- back

# ".sid" file example  {#sid-file-example}

The following ".sid" file (ietf-system@2014-08-06.sid) have been generated using the following yang modules:

* ietf-system@2014-08-06.yang (defined in {{RFC7317}})

* ietf-yang-types@2013-07-15.yang (defined in {{RFC6991}})

* ietf-inet-types@2013-07-15.yang (defined in {{RFC6991}})

* ietf-netconf-acm@2018-02-14.yang (defined in {{RFC8341}})

* iana-crypt-hash@2014-08-06.yang (defined in {{RFC7317}})

~~~~
{
  "ietf-sid-file:sid-file" : {
    "module-name": "ietf-system",
    "module-revision": "2020-02-05",
    "dependency-revision": [
      {
        "module-name": "ietf-yang-types",
        "module-revision": "2013-07-15"
      },
      {
        "module-name": "ietf-inet-types",
        "module-revision": "2013-07-15"
      },
      {
        "module-name": "ietf-netconf-acm",
        "module-revision": "2018-02-14"
      },
      {
        "module-name": "iana-crypt-hash",
        "module-revision": "2014-08-06"
      }
    ],
    "description": "Example sid file",
    "assignment-range": [
      {
        "entry-point": 1700,
        "size": 100
      }
    ],
    "item": [
      {
        "namespace": "module",
        "identifier": "ietf-system",
        "sid": 1700
      },
      {
        "namespace": "identity",
        "identifier": "authentication-method",
        "sid": 1701
      },
      {
        "namespace": "identity",
        "identifier": "local-users",
        "sid": 1702
      },
      {
        "namespace": "identity",
        "identifier": "radius",
        "sid": 1703
      },
      {
        "namespace": "identity",
        "identifier": "radius-authentication-type",
        "sid": 1704
      },
      {
        "namespace": "identity",
        "identifier": "radius-chap",
        "sid": 1705
      },
      {
        "namespace": "identity",
        "identifier": "radius-pap",
        "sid": 1706
      },
      {
        "namespace": "feature",
        "identifier": "authentication",
        "sid": 1707
      },
      {
        "namespace": "feature",
        "identifier": "dns-udp-tcp-port",
        "sid": 1708
      },
      {
        "namespace": "feature",
        "identifier": "local-users",
        "sid": 1709
      },
      {
        "namespace": "feature",
        "identifier": "ntp",
        "sid": 1710
      },
      {
        "namespace": "feature",
        "identifier": "ntp-udp-port",
        "sid": 1711
      },
      {
        "namespace": "feature",
        "identifier": "radius",
        "sid": 1712
      },
      {
        "namespace": "feature",
        "identifier": "radius-authentication",
        "sid": 1713
      },
      {
        "namespace": "feature",
        "identifier": "timezone-name",
        "sid": 1714
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:set-current-datetime",
        "sid": 1715
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:set-current-datetime/
                      current-datetime",
        "sid": 1716
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system",
        "sid": 1717
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-restart",
        "sid": 1718
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-shutdown",
        "sid": 1719
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-state",
        "sid": 1720
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-state/clock",
        "sid": 1721
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-state/clock/boot-datetime",
        "sid": 1722
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-state/clock/
                      current-datetime",
        "sid": 1723
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-state/platform",
        "sid": 1724
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-state/platform/machine",
        "sid": 1725
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-state/platform/os-name",
        "sid": 1726
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-state/platform/os-release",
        "sid": 1727
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system-state/platform/os-version",
        "sid": 1728
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/authentication",
        "sid": 1729
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/authentication/user",
        "sid": 1730
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/authentication/
                      user-authentication-order",
        "sid": 1731
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/authentication/user/
                      authorized-key",
        "sid": 1732
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/authentication/user/
                      authorized-key/algorithm",
        "sid": 1733
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/authentication/user/
                      authorized-key/key-data",
        "sid": 1734
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/authentication/user/
                      authorized-key/name",
        "sid": 1735
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/authentication/user/
                      name",
        "sid": 1736
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/authentication/user/
                      password",
        "sid": 1737
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/clock",
        "sid": 1738
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/clock/timezone-name",
        "sid": 1739
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/clock/timezone-utc-offset",
        "sid": 1740
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/contact",
        "sid": 1741
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/dns-resolver",
        "sid": 1742
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/dns-resolver/options",
        "sid": 1743
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/dns-resolver/options/
                      attempts",
        "sid": 1744
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/dns-resolver/options/
                      timeout",
        "sid": 1745
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/dns-resolver/search",
        "sid": 1746
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/dns-resolver/server",
        "sid": 1747
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/dns-resolver/server/name",
        "sid": 1748
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/dns-resolver/server/
                      udp-and-tcp",
        "sid": 1749
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/dns-resolver/server/
                      udp-and-tcp/address",
        "sid": 1750
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/dns-resolver/server/
                      udp-and-tcp/port",
        "sid": 1751
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/hostname",
        "sid": 1752
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/location",
        "sid": 1753
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/ntp",
        "sid": 1754
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/ntp/enabled",
        "sid": 1755
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/ntp/server",
        "sid": 1756
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/ntp/server/
                      association-type",
        "sid": 1757
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/ntp/server/iburst",
        "sid": 1758
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/ntp/server/name",
        "sid": 1759
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/ntp/server/prefer",
        "sid": 1760
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/ntp/server/udp",
        "sid": 1761
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/ntp/server/udp/address",
        "sid": 1762
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/ntp/server/udp/port",
        "sid": 1763
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius",
        "sid": 1764
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius/options",
        "sid": 1765
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius/options/attempts",
        "sid": 1766
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius/options/timeout",
        "sid": 1767
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius/server",
        "sid": 1768
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius/server/
                      authentication-type",
        "sid": 1769
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius/server/name",
        "sid": 1770
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius/server/udp",
        "sid": 1771
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius/server/udp/
                      address",
        "sid": 1772
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius/server/udp/
                      authentication-port",
        "sid": 1773
      },
      {
        "namespace": "data",
        "identifier": "/ietf-system:system/radius/server/udp/
                      shared-secret",
        "sid": 1774
      }
    ]
  }
}
~~~~

# SID auto generation {#sid-auto-generation}

Assignment of SIDs to YANG items can be automated, the recommended process to assign SIDs is as follows:

1. A tool extracts the different items defined for a specific YANG module.
2. The list of items is sorted in alphabetical order, 'namespace' in descending order, 'identifier' in ascending order. The 'namespace' and 'identifier' formats are described in the YANG module 'ietf-sid-file' defined in {{sid-file-format}}.
3. SIDs are assigned sequentially from the entry point up to the size of the registered SID range. This approach is recommended to minimize the serialization overhead, especially when delta between a reference SID and the current SID is used by protocols aiming to reduce message size.
4. If the number of items exceeds the SID range(s) allocated to a YANG module, an extra range is added for subsequent assignments.
5. The "dependency-revision" should reflect the revision numbers of each
   YANG module that the YANG module imports at the moment of the generation.

In case of an update to an existing ".sid" file, an additional step is needed
that increments the ".sid" file version number. If there was no version number
in the previous version of the ".sid" file, 0 is assumed as the version number
of the old version of the ".sid" file and the version number is 1 for the new
".sid" file. Apart from that, changes of ".sid" files can also be automated using
the same method described above, only unassigned YÀNG items are processed at
step #3. Already existing items in the ".sid" file should not be given new SIDs.

Note that ".sid" file versions are specific to a YANG module revision. For each
new YANG module or each new revision of an existing YANG module, the version
number of the initial ".sid" file should either be 0 or should not be present.

Note also that RPC or action "input" and "output" data nodes MUST always be
assigned SID even if they don't contain data nodes. The reason for this
requirement is that other modules can augment the given module and those SIDs
might be necessary.

# ".sid" file lifecycle {#sid-lifecycle-ex}

Before assigning SIDs to their YANG modules, YANG module authors must acquire a
SID range from a "YANG SID Range Registry". If the YANG module is part of an IETF
draft or RFC, the SID range need to be acquired from the "IETF YANG SID Range
Registry" as defined in {{ietf-iana-sid-range-allocation}}. For the other YANG
modules, the authors can acquire a SID range from any "YANG SID Range Registry" of
their choice.

Once the SID range is acquired, the owner can use it to generate ".sid" file/s
for his YANG module/s.  It is recommended to leave some unallocated SIDs
following the allocated range in each ".sid" file in order to allow better
evolution of the YANG module in the future.  Generation of ".sid" files should
be performed using an automated tool.  Note that ".sid" files can only be
generated for YANG modules and not for submodules.

## ".sid" File Creation

The following activity diagram summarizes the creation of a YANG module and its associated ".sid" file.

~~~~ goat
        +---------------+
  o     | Creation of a |
 -+- -->| YANG module   |
 / \    +------+--------+
               |
               v
         .-------------.
        / Standardized  \     yes
        \ YANG module ? /------------+
         '-----+-------'             |
               |  no                 |
               v                     v
         .-------------.      +---------------+
   +--> / Constrained   \ yes | SID range     |
   |    \ application ? /---->| registration  |<---------+
   |     '-----+-------'      +------+--------+          |
   |           |  no                 |                   |
   |           v                     v                   |
   |    +---------------+    +---------------+           |
   +----+ YANG module   |    | SID sub-range |           |
        | update        |    | assignment    |<----------+
        +---------------+    +-------+-------+           |
                                     |                   |
                                     v                   |
                             +---------------+    +------+------+
                             | ".sid" file   |    | Rework YANG |
                             | generation    |    |    model    |
                             +-------+-------+    +-------------+
                                     |                   ^
                                     v                   |
                                .----------.  yes        |
                               /  Work in   \ -----------+
                               \  progress  /
                                '----+-----'
                                     |  no
                                     v
                               .-------------.       .-------------.
                              /      RFC      \ no  /     Open      \ no
                              \  publication? /---> \ specification?/---+
                               '------+------'       '------+------'    |
                                 yes  |                     | yes       |
                                      |       .------------'            |
                                      |      /                          |
                                      v     v                           v
                              +---------------+               +---------------+
                              |     IANA      |               | Third party   |
                              | registration  |               | registration  |
                              +-------+-------+               +---------+-----+
                                      |                                 |
                                      +---------------------------------+
                                      v
                                    [DONE]
~~~~
{: #fig-sid-file-creation title='SID Lifecycle' align="left"}

## ".sid" File Update

The following Activity diagram summarizes the update of a YANG module and its associated ".sid" file.

~~~~ goat
        +---------------+
  o     | Update of the |
 -+- -->| YANG module   |
 / \    | or include(s) |
        | or import(s)  |
        +------+--------+
               |
               v
           .-------------.
          /  New items    \ yes
          \  created  ?   /------+
           '------+------'       |
                  |  no          v
                  |       .-------------.      +----------------+
                  |      /  SID range    \ yes | Extra sub-range|
                  |      \  exhausted ?  /---->| assignment     |
                  |       '------+------'      +-------+--------+
                  |              |  no                 |
                  |              +---------------------+
                  |              |
                  |              v
                  |      +---------------+
                  |      | ".sid" file   |
                  |      | update based  |
                  |      | on previous   |
                  |      | ".sid" file   |
                  |      +-------+-------+
                  |              |
                  |              v
                  |       .-------------.      +---------------+
                  |      /  Publicly     \ yes | YANG module   |
                  |      \  available ?  /---->| registration  |
                  |       '------+------'      +-------+-------+
                  |              | no                  |
                  +--------------+---------------------+
                                 |
                               [DONE]

~~~~
{: #fig-sid-file-update title="YANG and \".sid\" file update" align="left"}



# Acknowledgments
{: numbered="false"}

The authors would like to thank {{{Andy Bierman}}}, {{{Michael Richardson}}}, {{{Abhinav Somaraju}}}, {{{Peter van der Stok}}}, {{{Laurent Toutain}}} and {{{Randy Turner}}} for their help during the development of this document and their useful comments during the review process.
