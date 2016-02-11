---
stand_alone: true
ipr: trust200902
docname: draft-veillette-core-yang-cbor-mapping-latest
title: CBOR Encoding of Data Modeled with YANG
area: Applications and Real-Time Area (art)
wg: Internet Engineering Task Force
kw: CBOR
cat: info
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
  email: michel.veillette@trilliantinc.com
- role: editor
  ins: A. P. Pelov
  name: Alexander Pelov
  org: Acklio
  street: 2 Rue de la Chataigneraie
  code: '35510'
  city: Cesson-Sevigne
  region: Bretagne
  country: France
  phone: "+33299127004"
  email: a@ackl.io
- ins: A.  S. Somaraju
  name: Abhinav Somaraju
  org: Tridonic GmbH & Co KG
  street: Farbergasse 15
  code: '6850'
  city: Dornbirn
  region: Vorarlberg
  country: Austria
  phone: "+43664808926169"
  email: abhinav.somaraju@tridonic.com
- ins: R. T. Turner
  name: Randy Turner
  org: Landis+Gyr
  street:
  - 30000 Mill Creek Ave
  - Suite 100
  code: '30022'
  city: Alpharetta
  region: GA
  country: US
  phone: "++16782581292"
  email: randy.turner@landisgyr.com
  uri: http://www.landisgyr.com/
- ins: A. M.  Minaburo
  name: Ana Minaburo
  org: Acklio
  street: 2 rue de la châtaigneraie
  code: '35510'
  city: Cesson-Sévigné
  region: Bretagne
  country: France
  phone: "+33299127026"
  email: ana@ackl.io
normative:
  I-D.ietf-netmod-rfc6020bis:
  RFC2119:
  RFC7049:
informative:
  I-D.ietf-netmod-yang-json:
  RFC7159:
  RFC7223:
  RFC7228:
  RFC7277:
  RFC7317:

--- abstract

This document defines encoding rules for serializing configuration data, state data, RPC input and RPC output, Action input, Action output and notifications defined within YANG modules using the Concise Binary Object Representation (CBOR) {{RFC7049}}.

--- middle

# Introduction

The specification of YANG 1.1 data modelling language {{I-D.ietf-netmod-rfc6020bis}} defines only XML encoding for data instances, i.e. contents of configuration datastores, state data, RPC inputs and outputs, action inputs and outputs, and event notifications.

A new set of encoding rules have been defined to allow the use of the same data models in environments based on the JavaScript Object Notation (JSON) Data Interchange Format {{RFC7159}}. This is accomplished in the JSON Encoding of Data Modeled with YANG specification {{I-D.ietf-netmod-yang-json}}.

The aim of this document is to define a set of encoding rules for the Concise Binary Object Representation (CBOR) {{RFC7049}}. The resulting encoding is more compact compared to XML and JSON and more suitable for Constrained Nodes and/or Constrained Networks as defined by {{RFC7228}}.

# Terminology and Notation

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to
be interpreted as described in {{RFC2119}}.

The following terms are defined in {{I-D.ietf-netmod-rfc6020bis}}:

* action

* anydata

* anyxml

* data node

* data tree

* module

* notification

* RPC

* schema node

* schema tree

* submodule

This specification also makes use of the following terminology:

* child: A schema node defined within a collection such as a container, a list, a case, a notification, a RPC input, a RPC output, an action input, an action output.

* parent: The collection in which a schema node is defined.

* path: A path is a string that identifies a schema node within the schema tree. A path consists of the list of schema node identifier(s) separated by slashes ("/"). Schema node identifier(s) are always listed from the top-level schema node up to the targeted schema node. (e.g. "/system-state/clock/current-datetime")

* structured identifier or SID: Unsigned integer used to identify different YANG items.


## CBOR diagnostic notation

Within this document, CBOR binary contents are represented using an equivalent textual form called CBOR diagnostic notation as define in {{RFC7049}} section 6. This notation is used strictly for documentation purposes and is never used in the data serialization.

| CBOR content     | CBOR type | Diagnostic notation                                                     | Example            | CBOR encoding      |
|------------------+-----------+-------------------------------------------------------------------------+--------------------+--------------------|
| Unsigned integer |         0 | Decimal digits                                                          | 123                | 18 7b              |
| Negative integer |         1 | Decimal digits prefixed by a minus sign                                 | -123               | 38 7a              |
| Byte string      |         2 | Hexadecimal value enclosed between single quotes and prefixed by an 'h' | h'f15c'            | 42 f15c            |
| Text string      |         3 | String of Unicode characters enclosed between double quotes             | "txt"              | 63 747874          |
| Array            |         4 | Comma separated list of values within square brackets                   | [ 1, 2 ]           | 82 01 02           |
| Map              |         5 | Comma separated list of tag : value pairs within curly braces           | { 1: 123, 2: 456 } | a2 01187b 021901c8 |
| Boolean          |      7/20 | false                                                                   | false              | f4                 |
|                  |      7/21 | true                                                                    | true               | f5                 |
| Null             |      7/22 | null                                                                    | null               | f6                 |
| Not assigned     |      7/23 | undefined                                                               | undefined          | f7                 |
{: align="left"}

Within this document, comments are allowed in CBOR diagnostic notation. Any characters after a Pound sign ('#') up to the end of the line is treated as a comment.

# Properties of the CBOR Encoding

This document defines CBOR encoding rules for YANG schema trees and their subtrees.

Basic schema nodes such leaf, leaf-list, anydata and anyxml can be encoded standalone. In this case, only the value of this schema node is encoded in CBOR. Identification of this value need to be provided by some external means when needed.

Collections like container, list, notification, RPC input, RPC output, action input and action output are serialized using a CBOR map in which each child schema node is encode using a tag and a value. Section 4 defines how the tag part is encoded, and the following sections deal with the value part.

In order to minimize the size of the encoded data, the propose mapping do not make use of any meta-information beyond those natively supported by CBOR. This include the use of CBOR tags which are not used for any of the proposed mapping. It is expected that entities generating and decoding CBOR contents have enough knowledge about the information processed in order to perform the expected task, and this without the need of such extra meta-information.

# Structured IDentifiers (SID)

Some of the items defined within YANG data models are identified using a unique unsigned integer called structured identifier (SID). The following items are identified using SIDs:

* identity

* data node

* rpc

* action

* notification

SIDs are globally unique and need to be registered, see section 9 and appendix A for more details about the registration process of SIDs.

Assignment of SIDs can be automated, the recommended process to assign SIDs is as follow:

* The tools extract the different items defined for a specific YANG module.

* The list of items is ordered by type, assignment date and label.

* SIDs are assigned sequentially for the entry point up to the size of the registered SID range. It is important to note that sequentially assigned SIDs optimizes the CBOR serialization due to the use of delta encoding.

* If the number of items exceed the SID range(s) associated to a YANG module, an extra range is added for subsequent assignments.

* SID are assigned permanently, items introduced by a new revision of a YANG module are added to the list of SIDs already assigned.

Appendix B define a standard file format used to store and publish SIDs.

# Encoding of YANG Schema Node Instances

Objects defined using the YANG modeling language are encoded using CBOR {{RFC7049}} based on the rules defined in this section. We assume that the reader is
already familiar with both YANG {{I-D.ietf-netmod-rfc6020bis}} and CBOR {{RFC7049}}.

## The "leaf" Schema Node 

Leaf MUST be encoded based on the encoding rules specific in section 6.

## The "container" Schema Node

A container MUST be encoded using a CBOR map data item (major type 5). A map is comprised of pairs of data items, with each data item consisting of a key and a value. 
Keys MUST be encoded using a CBOR unsigned integer (major type 0) and set to the delta value of the associated SID. Delta values are computed as follow:

*	The delta value is equal the SID of the current schema node minus the SID of the parent schema node. When no parent exists in the context of use of this container, the delta is set to the SID of the current schema node (a parent with SID equal to zero is assumed).

*	Delta values may result in a negative number, CoOL clients and servers MUST support negative deltas.

Values MUST be encoded using the appropriate rules defined in section 5 and section 6.

Definition example {{RFC7317}}:

~~~~ YANG
typedef date-and-time {
  type string {
    pattern '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[\+\-]
             \d{2}:\d{2})';
  }
}

container system {
  leaf hostname {
    type inet:domain-name;

  container clock {
    leaf current-datetime {
      type date-and-time;
    }

    leaf boot-datetime {
      type date-and-time;
    }
  }
}
~~~~
{: align="left"}

The ".sid" file used in this example is available in appendix C.

CBOR diagnostic notation:

~~~~ CBORdiag
{
  1708 : {                              # clock
    2 : "2015-10-02T14:47:24Z-05:00",   # current-datetime, SID 1710
    1 : "2015-09-15T09:12:58Z-05:00"    # boot-datetime, SID 1709
  }
}
~~~~
{: align="left"}

CBOR encoding:

~~~~ CBORbytes
a1                                      # map(1)
   19 06ac                              # unsigned(1708)
   a2                                   # map(2)
      02                                # unsigned(2)
      78 1a                             # text(26)
      323031352d31302d30325431343a34373a32345a2d30353a3030
      01                                # unsigned(1)
      78 1a                             # text(26)
      323031352d30392d31355430393a31323a35385a2d30353a3030
~~~~
{: align="left"}

## The "leaf-list" Schema Node

A leaf-list MUST be encoded using a CBOR array data item (major type 4).
Each entry MUST be encoded using the rules defined by the YANG type specified.

Definition example {{RFC7317}}:

~~~~ YANG
typedef domain-name {
  type string {
    length "1..253";
    pattern '((([a-zA-Z0-9_]([a-zA-Z0-9\-_]){0,61})?[a-zA-Z0-9].)
             *([a-zA-Z0-9_]([a-zA-Z0-9\-_]){0,61})?[a-zA-Z0-9]\.?
             )|\.';
  }
}

leaf-list search {
  type domain-name;
  ordered-by user;
}
~~~~
{: align="left"}

CBOR diagnostic notation: [ "ietf.org", "ieee.org" ]

CBOR encoding: 82  68 696574662e6f7267  68 696565652e6f7267

## The "list" Schema Node 

A list MUST be encoded using a CBOR array data item (major type 4). Each entry of this array is encoded using a CBOR map data item (major type 5) based on the same rules as a YANG container, see section 5.2.

Definition example {{RFC7317}}:

~~~~ YANG
list server {
  key name;

  leaf name {
    type string;
  }
  choice transport {
    case udp {
      container udp {
        leaf address {
          type host;
          mandatory true;
        }
        leaf port {
          type port-number;
        }
      }
    }
  }
  leaf association-type {
    type enumeration {
      enum server;
      enum peer;
      enum pool;
    }
    default server;
  }
  leaf iburst {
    type boolean;
    default false;
  }
  leaf prefer {
    type boolean;
    default false;
  }
}
~~~~
{: align="left"}

The .sid file used in this example is available in appendix C.

CBOR diagnostic notation:

~~~~ CBORdiag
[
  {
    1746 : "NRC TIC server",          # name
    1748 : {                          # udp
      1 : "tic.nrc.ca",               # address, SID 1749
      2 : 123                         # port, SID 1750
    }, 
    1744 : 0,                         # association-type
    1745 : false,                     # iburst
    1747 : true                       # prefer
  },
  {
    1746 : "NRC TAC server",          # name
    1748 : {                          # udp
      1 : "tac.nrc.ca"                # address, SID 1749
    }
  }
]
~~~~
{: align="left"}

CBOR encoding:

~~~~ CBORbytes
82                                    # array(2)
   a5                                 # map(5)
      19 06d2                         # unsigned(1746)
      6e                              # text(14)
         4e52432054494320736572766572 # "NRC TIC server"
      19 06d4                         # unsigned(1748)
      a2                              # map(2)
         01                           # unsigned(1)
         6a                           # text(10)
            7469632e6e72632e6361      # "tic.nrc.ca"
         02                           # unsigned(2)
         18 7b                        # unsigned(123)
      19 06d0                         # unsigned(1744)
      00                              # unsigned(0)
      19 06d1                         # unsigned(1745)
      f4                              # primitive(20)
      19 06d3                         # unsigned(1747)
      f5                              # primitive(21)
   a2                                 # map(2)
      19 06d2                         # unsigned(1746)
      6e                              # text(14)
         4e52432054414320736572766572 # "NRC TAC server"
      19 06d4                         # unsigned(1748)
      a1                              # map(1)
         01                           # unsigned(1)
         6a                           # text(10)
            7461632e6e72632e6361      # "tac.nrc.ca"
~~~~
{: align="left"}

## The "anydata" Schema Node

An anydata serves as a container for an arbitrary set of schema nodes that otherwise appear as normal YANG-modeled data. An anydata instance is encoded using the same rules as a container, i.e., CBOR map. The requirement that anydata content can be modeled by YANG implies the following:

*	Tags MUST be set to valid SIDs, this include the tag of the anydata node and the tag of any inner schema node.

*	CBOR array MUST contain either unique scalar values (as a leaf-list, see Section 5.3), or maps (as a list, see Section 5.4).

*	Values MUST follow the encoding rules of one of the datatype listed in section 6.

## The "anyxml" Schema Node  

An anyxml instance is encoded as a CBOR tag/value pair. The tag of the anyxml schema node MUST be a valid SID but the value is unrestricted, i.e., the value can be any CBOR encoded content.

# Representing YANG Data Types in CBOR {#data_types_mapping}

## The unsigned integer Types

Leafs of type uint8, uint16, uint32 and uint64 MUST be encoded using a CBOR
unsigned integer data item (major type 0).

Definition example {{RFC7277}}:

~~~~ YANG
leaf mtu {
  type uint16 {
    range "68..max";
  }
}
~~~~
{: align="left"}

CBOR diagnostic notation: 1280

CBOR encoding: 19 0500

## The integer Types

Leafs of type int8, int16, int32 and int64 MUST be encoded using either CBOR
unsigned integer (major type 0) or CBOR signed integer (major type 1), depending
on the actual value.

Definition example {{RFC7317}}:

~~~~ YANG
leaf timezone-utc-offset {
  type int16 {
    range "-1500 .. 1500";
  }
}
~~~~
{: align="left"}

CBOR diagnostic notation: -300

CBOR encoding: 39 012b

## The "decimal64" Type 

Leafs of type decimal64 MUST be encoded using either CBOR unsigned integer
(major type 0) or CBOR signed integer (major type 1), depending on the actual
value. The position of the decimal point is defined by the fraction-digits YANG statement and not available in the CBOR encoding.

Definition example {{RFC7317}}:

~~~~ YANG
leaf my-decimal {
  type decimal64 {
    fraction-digits 2;
    range "1 .. 3.14 | 10 | 20..max";
  }
}
~~~~
{: align="left"}

CBOR diagnostic notation: 257 (Represents decimal value 2.57)

CBOR encoding: 19 0101

## The "string" Type 

Leafs of type string MUST be encoded using a CBOR text string data item (major
type 3).

Definition example {{RFC7223}}:

~~~~ YANG
leaf name {
  type string;
}
~~~~
{: align="left"}

CBOR diagnostic notation: "eth0"

CBOR encoding: 64 65746830

## The "boolean" Type  

Leafs of type boolean MUST be encoded using a CBOR true (major type 7, additional
information 21) or false data item (major type 7, additional information
20).

Definition example {{RFC7317}}:

~~~~ YANG
leaf enabled {
  type boolean;
}
~~~~
{: align="left"}

CBOR diagnostic notation: true

CBOR encoding: f5

## The "enumeration" Type  

Leafs of type enumeration MUST be encoded using a CBOR unsigned integer data
item (major type 0).

Definition example {{RFC7317}}:

~~~~ YANG
leaf oper-status {
  type enumeration {
    enum up { value 1; }
    enum down { value 2; }
    enum testing { value 3; }
    enum unknown { value 4; }
    enum dormant { value 5; }
    enum not-present { value 6; }
    enum lower-layer-down { value 7; }
  }
}
~~~~
{: align="left"}

CBOR diagnostic notation: 3 (Represents enumeration value "testing")

CBOR encoding: 03

## The "bits" Type 

Leafs of type bits MUST be encoded using a CBOR byte string data item (major
type 2). Bits position 0 to 7 are assigned to the first byte within the byte
string, bits 8 to 15 to the second byte, and subsequent bytes are assigned
similarly. Within each byte, bits are assigned from least to most significant.

Definition example {{I-D.ietf-netmod-rfc6020bis}}:

~~~~ YANG
leaf mybits {
  type bits {
    bit disable-nagle {
      position 0;
    }
    bit auto-sense-speed {
      position 1;
    }
    bit 10-Mb-only {
      position 2;
    }
  }
}
~~~~
{: align="left"}

CBOR diagnostic notation: h'05' (Represents bits disable-nagle and 10-Mb-only set)

CBOR encoding: 41 05

## The "binary" Type 

Leafs of type binary MUST be encoded using a CBOR byte string data item (major
type 2).

Definition example:

~~~~ YANG
leaf aes128-key {
  type binary {
    length 16;
  }
}
~~~~
{: align="left"}

CBOR diagnostic notation: h'1f1ce6a3f42660d888d92a4d8030476e'

CBOR encoding: 50 1f1ce6a3f42660d888d92a4d8030476e

## The "leafref" Type  

Leafs of type leafref MUST be encoded using the rules of the schema node referenced
by the "path" YANG statement.

Definition example {{RFC7223}}:

~~~~ YANG
typedef interface-state-ref {
  type leafref {
    path "/interfaces-state/interface/name";
  }
}

container interfaces-state {
  list interface {
    key "name";
    leaf name {
      type string;
    }
    leaf-list higher-layer-if {
      type interface-state-ref;
    }
  }
}
~~~~
{: align="left"}

CBOR diagnostic notation: "eth1.10"

CBOR encoding: 67 657468312e3130

## The "identityref" Type  

Leafs of type identityref MUST be encoded using a CBOR unsigned integer data item (major type 0) and MUST contain a registered SID.

Definition example {{RFC7223}}:

~~~~ YANG
identity interface-type {
}

identity iana-interface-type {
  base interface-type;
}

identity ethernetCsmacd {
  base iana-interface-type;
}

leaf type {
  type identityref {
    base interface-type;
  }
}
~~~~
{: align="left"}

Assuming that the identity "iana-if-type:ethernetCsmacd" have been assigned to the SID value 1179.

CBOR diagnostic notation: 1179

CBOR encoding: 19 049b

## The "empty" Type  

Leafs of type empty MUST be encoded using the CBOR null value (major type
7, additional information 22).

Definition example {{RFC7277}}:

~~~~ YANG
leaf is-router {
  type empty;
}
~~~~
{: align="left"}

CBOR diagnostic notation: null

CBOR encoding: f6

## The "union" Type  

Leafs of type union MUST be encoded using the rules associated with one of
the type listed.

Definition example {{RFC7317}}:

~~~~ YANG
typedef ipv4-address {
  type string {
  pattern '(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}
           ([0-9][1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])(%[\p{N}
           \p{L}]+)?';
  }
}

typedef ipv6-address {
  type string {
    pattern '((:|[0-9a-fA-F]{0,4}):)([0-9a-fA-F]{0,4}:){0,5}((([0-9a
             -fA-F]{0,4}:)?(:|[0-9a-fA-F]{0,4}))|(((25[0-5]|2[0-4][0
             -9]|[01]?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0
             -9]?[0-9])))(%[\p{N}\p{L}]+)?';
    pattern '(([^:]+:){6}(([^:]+:[^:]+)|(.*\..*)))|((([^:]+:)*[^:]+)
             ?::(([^:]+:)*[^:]+)?)(%.+)?';
  }
}

typedef ip-address {
  type union {
    type ipv4-address;
    type ipv6-address;
  }
}

leaf address {
  type inet:ip-address;
}
~~~~
{: align="left"}

CBOR diagnostic notation: "[2001:db8:0:1]:80"

CBOR encoding: 71 5b323030313a6462383a303a315d3a3830

## The "instance-identifier" Type  

Leafs of type instance-identifier MUST be encoded using either a CBOR unsigned integer data item (major type 0) or a CBOR array data item (major type 4).
When a leaf node of type instance-identifier identifies a single instance schema node (schema node not part of a list), its value MUST be encoded using a CBOR unsigned integer set to the targeted data node SID.

Definition example {{RFC7317}}:

~~~~ YANG
container system {

  leaf contact {
    type string;
  }

  leaf hostname {
    type inet:domain-name;
  }
}
~~~~
{: align="left"}

In this example, we assume that the leaf "/system/contact" is assigned to SID 1728.

CBOR diagnostic notation: 1728

CBOR encoding: 19 06c0

In this example, the value 69635 identifies the instance of the data node
"hostname" within the ietf-system module. Assuming module ID = 68 and data
node ID = 3.

When a leaf node of type instance-identifier identifies a data node supporting
multiple instances (data node part of a list), its value MUST be encoded
using a CBOR array data item (major type 4) containing the following entries:

* The first entry MUST be encoded as a CBOR unsigned integer data item (major type 0) and set to the targeted data node SID. 

* The following entries MUST contain the value of each key required to identify the instance of the targeted data node. These keys MUST be ordered as defined in the "key" YANG statement, starting from top level list, and follow by each of the subordinate list(s).

Definition example {{RFC7317}}:

~~~~ YANG
list user {
  key name;

  leaf name {
    type string;
  }
  leaf password {
    type ianach:crypt-hash;
  }

  list authorized-key {
    key name;

    leaf name {
      type string;
    }
    leaf algorithm {
      type string;
    }
    leaf key-data {
      type binary;
  }
}
~~~~
{: align="left"}

In this example, we assume that the leaf "/system/authentication/user/authorized-key/key-data" is assigned to SID 1721.

CBOR diagnostic notation: [1721, "bob", "admin"]

CBOR encoding: 82 19 06b9 63 626f62 65 61646d696e

# Security Considerations

This document defines an alternative encoding for data modeled in the YANG data modeling language. As such, this encoding doesn’t contribute any new security issues in addition of those identified for the specific protocol or context for which it is used.

To minimize security risks, software on the receiving side SHOULD reject all messages that do not comply to the rules of this document and reply with an appropriate error message to the sender.

# IANA Considerations

## "SID" range registry

This document defines a registry for Structure Identifier (SID) ranges. This registry guaranty that each SID assigned is globally unique. The registry SHALL record for each entry:

*	The entry point of the registered SID range.

*	The size of the registered SID range.

*	The contact information of the owner of the range such as name, email address, and phone number.
The IANA policy for this registry is split into four tiers as follows:

*	The range of 0 to 9999 and 0x40000000 to 0xFFFFFFFFFFFFFFFF are reserved for future extensions of this protocol. Allocation within these ranges require IETF review or IESG approval.

*	The range of 1000 to 59999 is reserved for standardized YANG modules. Allocation within this range require publishing of the associated ".yang" and ".sid" files.

*	The range of 60000 to 99999 is reserved for experimental or private YANG modules. Use of this range SHOUD NOT be used in operational deployments since these SIDs are not globally unique which limit their interoperability.

*	The range of 100000 to 0x3FFFFFFF is available as first come first served basis. The only information require from the registrant is a valid contact information. The recommended size of the SID ranges allocated is 1,000 for private use and 10,000 for standard development organizations (SDOs). Registrants MAY request less or more SIDs based on their expected needs. Allocation of a significant larger SID range MAY required IETF review or IESG approval.

| Entry Point | Size       | Registration Procedures                                                 |
|-------------+------------+-------------------------------------------------------------------------+
|      0      |      1 000 | Specification required, expert review                                   |
|  1 000      |     59 000 | Specification and associated ".yang" and ".sid" files required          |
| 60 000      |     40 000 | Experimental or private use                                             |
| 100 000     | 0x3FFE7960 | Contact information is required. Registration of the module name(s) and associated ".yang" and ".sid" files are optional.  |
| 0x40000000  |      2^64  | Specification required, expert review                                   |
{: align="left"}

## YANG module registry

Each registered SID range can be used to assign SIDs multiple YANG modules. To track which YANG module have been assigned and to avoid duplicate allocation, IANA SHALL provide a method to register and query the following information:

*	The YANG module name

*	The contact information of the author

*	The specification reference

*	The associated ".yang" file(s) (Optional)

*	The associated ".sid" file(Optional)

Registration of YANG modules is optional. When a YANG module is registered, the registrant MUST provide the module name and its contact information and/or a specification reference.

The registration of the associated ".yang" and ".sid" files is optional. When provided, the validity of the files SHOULD be verified. This can be accomplished by a YANG validation tool specially modified to support ".sid" file verification. The SID range specified within the ".sid" file SHOULD also be checked against the "SID" range registry (section 9.1) and against the other YANG modules registered to detect any duplicate use of SIDs.

Initial entries in this registry are as follows:

| Entry Point | Size | Module name     | Module revision  | Reference               |
|-------------+------+-----------------+------------------+-------------------------+
|        1000 |  100 | ietf-cool       |    2016-01-01    | I.D-veillette-core-cool |
|        1100 |  400 | iana-if-type    |    2014-05-08    | RFC 7224                |
|        1500 |  100 | ietf-interfaces |    2014-05-08    | RFC 7223                |
|        1600 |  100 | ietf-ip         |    2014-06-16    | RFC 7277                |
|        1700 |  100 | ietf-system     |    2014-08-06    | RFC 7317                |
{: align="left"}

# Acknowledgments

This document have been largely inspired by the extensive works done by Andy Bierman and Peter van der Stok on {{I-D.vanderstok-core-comi}}. {{I-D.ietf-netmod-yang-json}} have also been a critical input to this work. The authors would like to thank the authors and contributors to these two drafts.

The authors would also like to acknowledge the review, feedback, and comments from Ladislav Lhotka and Juergen Schoenwaelder.

# Appendix A. ".sid" file lifecycle

The following activity diagram summarize the life cycle of ".sid" files.

~~~~
      +---------------+
 O    | Creation of a |
-|- ->| YANG module   |
/ \   +---------------+
              |
              V
       /-------------\
      / Standardized  \ yes
      \ YANG module ? /-------------+
       \-------------/              |
              | no                  |
              V                     V
       /-------------\      +---------------+
      / Constrained   \ yes | SID range     |
  +-->\ application ? /---->| registration  |
  |    \-------------/      +---------------+
  |           | no                  |
  |           V                     V
  |   +---------------+     +---------------+
  +---| YANG module   |     | .sid file     |
      | update        |     | generation    |
      +---------------+     +---------------+
                                    |
                                    V
                             /-------------\      +---------------+
                            /  Publicaly    \ yes | YANG module   |
              +------------>\  available ?  /---->| registration  |
              |              \-------------/      +---------------+
              |                     | no                  |
              |                     +---------------------+
              |                     V
      +---------------+     +---------------+
      | .sid file     |     | Update of the |
      | update based  |     | YANG module   |
      | on previous   |     | or include(s) |
      | .sid file     |     | or import(s)  |
      +---------------+     +---------------+
              ^                     |
              |                     V
              |              /-------------\      +---------------+
              |             /  More SIDs    \ yes | Extra range   |
              |             \  required ?   /---->| assignment    |
              |              \-------------/      +---------------+
              |                     | no                  |
              +---------------------+---------------------+
~~~~
{: align="left"}

YANG modules are not necessary created in the context of constrained applications. YANG modules can be implemented using NETCONF or RESTCONF without the need for assigning SIDs to the deferent items within these YANG modules.

Assignment of SIDs of a YANG module defined by an RFC is the responsibility of the authors of this RFC or IANA in the case of already existing modules. In the case of the non-standardized YANG module, authors or implementers MAY register for a SID range at any point in their development cycle.

Once a SID range is registered, the owner of this range assign sub-ranges to each YANG module in order to generate the associated ".sid" files. Generation of ".sid" files SHOULD be performed using an automated tool.

Registration of the .sid file associated to a YANG module is optional but recommended to promote interoperability between devices and to avoid duplicate allocation of SIDs to a single YANG module.

Each time a YANG module or one of its imported module(s) or included sub-module(s) is updated, the ".sid" file MAY need to be updated. This update SHOULD also be performed using an automated tool.

If a new revision requires more SIDs than initially allocated, a new SID range MUST be added to the assignment ranges as defined in the ".sid" file header. These extra SIDs are used for subsequent assignment.

# Appendix B. ".sid" file format

".sid" files are used to persist and publish SIDs assigned to the different YANG items of a specific YANG module. The following YANG module defined the structure of this file, encoding is performed using the rules defined in {{I-D.ietf-netmod-yang-json}}.

~~~~
module sid-file {
  namespace "urn:ietf:ns:cool:sid-file";
  prefix sid;

  organization
    "IETF Core Working Group";

  contact
    "Ana Minaburo
     <ana@ackl.io>
     
     Alexander Pelov
     <mailto:a@ackl.io>

     Abhinav Somaraju
     <mailto:abhinav.somaraju@tridonic.com>

     Laurent Toutain
     <Laurent.Toutain@telecom-bretagne.eu>

     Randy Turner
     <mailto:Randy.Turner@landisgyr.com>

     Michel Veillette
     <mailto:michel.veillette@trilliantinc.com>";

  description
    "This module define the structure of the .sid files.
     .sid files contains the identifiers (SIDs) assigned 
     to the different items defined in a YANG module.
     SIDs are used to encode a data model defined in YANG
     using CBOR.";

  revision 2015-12-16 {
    description
      "Initial revision.";
    reference
      "draft-veillette-core-yang-cbor-mapping";
  }

  typedef yang-identifier {
    type string {
      length "1..max";
      pattern '[a-zA-Z_][a-zA-Z0-9\-_.]*';
      pattern '.|..|[^xX].*|.[^mM].*|..[^lL].*';
    }
    description
      "A YANG identifier string as defined by the 'identifier'
       rule in Section 12 of RFC 6020.";
  }

  typedef revision-identifier {
    type string {
      pattern '\d{4}-\d{2}-\d{2}';
    }
    description
      "Represents a date in YYYY-MM-DD format.";
  }


  typedef date-and-time {
    type string {
      pattern '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?' +
              '(Z|[\+\-]\d{2}:\d{2})';
    }
    description
      "The date-and-time type is a profile of the ISO 8601
      standard for representation of dates and times using the
      Gregorian calendar.  The profile is defined by the
      date-time production in section 5.6 of RFC 3339.";
  }
  
  leaf module-name {
    type yang-identifier;
    description
      "Name of the module associated with this .sid file.";
  }

  leaf module-revision {
    type revision-identifier;
    description
      "Revision of the module associated with this .sid file.
       This leaf is not present if no revision statement is
       defined in the YANG module.";
  }

  list assigment-ranges {
    key "entry-point";
    description
      "Range(s) of SIDs available for assignment to the
       different items defined by the associated module.";

    leaf entry-point {
      mandatory true;
      type uint32;
      description
        "Lowest SID available for assignment.";
    }

    leaf size {
      mandatory true;
      type uint16;
      description
        "Number of SIDs available for assignment.";
    }
  }
 
  list items {
    key "type assigned label";
    description
      "List of items defined by the associated YANG module.";

    leaf type {
      description
        "Item type assigned, this field can be set to:
          - 'identity'
          - 'node'
          - 'notification'
          - 'rpc'
          - 'action'";
      mandatory true;
      type string {
        pattern 'identity$|node$|notification$|rpc$|action$';
      }
    }

    leaf assigned {
      mandatory true;
      type date-and-time;
      description
        "Date and time when this entry has been created.";
    }

    leaf label {
      mandatory true;
      type string;
      description
        "Label associated to this item, can be set to:
          - an identity encoded as: '<module name>:<entity name>'
          - a schema node path";
    }

    leaf sid {
      mandatory true;
      type uint32;
      description "Identifier assigned to this YANG item.";
    }
  }
}
~~~~
{: align="left"}

# Appendix C. ".sid" file example

The following .sid file (ietf-system@2014-08-06.sid) have been generated using the following yang modules:

*	ietf-system@2014-08-06.yang

*	ietf-yang-types@2013-07-15.yang

*	ietf-inet-types@2013-07-15.yang

*	ietf-netconf-acm@2012-02-22.yang

*	iana-crypt-hash@2014-04-04.yang

~~~~
{
  "assignment-ranges": [
    {
      "entry-point": 1700,
      "size": 100
    }
  ],
  "module-name": "ietf-system",
  "module-revision": "2014-08-06",
  "items": [
    {
      "type": "identity",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "ietf-system:authentication-method",
      "sid": 1700
    },
    {
      "type": "identity",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "ietf-system:local-users",
      "sid": 1701
    },
    {
      "type": "identity",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "ietf-system:radius",
      "sid": 1702
    },
    {
      "type": "identity",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "ietf-system:radius-authentication-type",
      "sid": 1703
    },
    {
      "type": "identity",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "ietf-system:radius-chap",
      "sid": 1704
    },
    {
      "type": "identity",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "ietf-system:radius-pap",
      "sid": 1705
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system",
      "sid": 1706
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-state",
      "sid": 1707
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-state/clock",
      "sid": 1708
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-state/clock/boot-datetime",
      "sid": 1709
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-state/clock/current-datetime",
      "sid": 1710
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-state/platform",
      "sid": 1711
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-state/platform/machine",
      "sid": 1712
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-state/platform/os-name",
      "sid": 1713
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-state/platform/os-release",
      "sid": 1714
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-state/platform/os-version",
      "sid": 1715
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/authentication",
      "sid": 1716
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/authentication/user",
      "sid": 1717
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/authentication/user-authentication-order",
      "sid": 1718
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/authentication/user/authorized-key",
      "sid": 1719
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/authentication/user/authorized-key/algorithm",
      "sid": 1720
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/authentication/user/authorized-key/key-data",
      "sid": 1721
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/authentication/user/authorized-key/name",
      "sid": 1722
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/authentication/user/name",
      "sid": 1723
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/authentication/user/password",
      "sid": 1724
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/clock",
      "sid": 1725
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/clock/timezone/timezone-name/timezone-name",
      "sid": 1726
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/clock/timezone/timezone-utc-offset/timezone-utc-offset",
      "sid": 1727
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/contact",
      "sid": 1728
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/dns-resolver",
      "sid": 1729
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/dns-resolver/options",
      "sid": 1730
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/dns-resolver/options/attempts",
      "sid": 1731
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/dns-resolver/options/timeout",
      "sid": 1732
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/dns-resolver/search",
      "sid": 1733
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/dns-resolver/server",
      "sid": 1734
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/dns-resolver/server/name",
      "sid": 1735
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/dns-resolver/server/transport/udp-and-tcp/udp-and-tcp",
      "sid": 1736
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/dns-resolver/server/transport/udp-and-tcp/udp-and-tcp/address",
      "sid": 1737
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/dns-resolver/server/transport/udp-and-tcp/udp-and-tcp/port",
      "sid": 1738
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/hostname",
      "sid": 1739
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/location",
      "sid": 1740
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/ntp",
      "sid": 1741
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/ntp/enabled",
      "sid": 1742
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/ntp/server",
      "sid": 1743
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/ntp/server/association-type",
      "sid": 1744
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/ntp/server/iburst",
      "sid": 1745
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/ntp/server/name",
      "sid": 1746
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/ntp/server/prefer",
      "sid": 1747
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/ntp/server/transport/udp/udp",
      "sid": 1748
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/ntp/server/transport/udp/udp/address",
      "sid": 1749
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/ntp/server/transport/udp/udp/port",
      "sid": 1750
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius",
      "sid": 1751
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius/options",
      "sid": 1752
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius/options/attempts",
      "sid": 1753
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius/options/timeout",
      "sid": 1754
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius/server",
      "sid": 1755
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius/server/authentication-type",
      "sid": 1756
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius/server/name",
      "sid": 1757
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius/server/transport/udp/udp",
      "sid": 1758
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius/server/transport/udp/udp/address",
      "sid": 1759
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius/server/transport/udp/udp/authentication-port",
      "sid": 1760
    },
    {
      "type": "node",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system/radius/server/transport/udp/udp/shared-secret",
      "sid": 1761
    },
    {
      "type": "rpc",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/set-current-datetime",
      "sid": 1762
    },
    {
      "type": "rpc",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/set-current-datetime/input/current-datetime",
      "sid": 1763
    },
    {
      "type": "rpc",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-restart",
      "sid": 1764
    },
    {
      "type": "rpc",
      "assigned": "2016-01-13T21:00:19Z",
      "label": "/system-shutdown",
      "sid": 1765
    }
  ]
}
~~~~
{: align="left"}

--- back
