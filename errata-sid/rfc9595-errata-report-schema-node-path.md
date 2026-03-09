In:
     typedef schema-node-path {

OLD:

      "A schema-node path is an absolute YANG schema-node
       identifier as defined by the YANG ABNF rule
       'absolute-schema-nodeid', except that module names are used
       instead of prefixes.

NEW:

      "A schema-node path is an absolute YANG schema-node
       identifier as defined by the YANG ABNF rule
       'absolute-schema-nodeid', except that module names are used
       instead of prefixes. In addition, choice and case schema nodes
       are not represented in a path string.

In:

       list item {

OLD:

      description
        "Each entry within this list defines the mapping between
         a YANG item string identifier and a YANG SID.  This list
         MUST include a mapping entry for each YANG item defined
         by the YANG module identified by 'module-name' and
         'module-revision'.";

NEW:

      description
        "Each entry within this list defines the mapping between
         a YANG item string identifier and a YANG SID.  This list
         MUST include a mapping entry for each YANG item defined
         by the YANG module identified by 'module-name' and
         'module-revision'. YANG choice and case nodes are not included.

Note that both changes simply add a single sentence at the end of the description.

(Should there be a change to "revision 2024-07-31"?)
