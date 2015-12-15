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
  RFC2119:
  RFC6020:
  RFC7049:
informative:
  RFC7223:
  RFC7277:
  RFC7317:
  RFC7159:
  RFC7228:
  I-D.ietf-netmod-rfc6020bis:
  I-D.ietf-netmod-yang-json:

--- abstract

This document defines encoding rules for representing configuration, state
data, RPC input and output parameters, and notifications defined using YANG
as Concise Binary Object Representation (CBOR, RFC7049).

--- middle

# Introduction

The specification of YANG 1.1 data modelling language [I-D.ietf-netmod-rfc6020bis] defines only XML encoding for data instances, i.e. contents of configuration datastores, state data, RPC operation or action input and output parameters, and event notifications.

A new set of encoding rules has been defined to allow the use of the same data models in environments based on the JavaScript Object Notation (JSON) Data Interchange Format [RFC7159]. This is accomplished in the JSON Encoding of Data Modeled with YANG specification [I-D.ietf-netmod-yang-json].

The aim of this document is to define a set of encoding rules for the Concise Binary Object Representation (CBOR) [RFC7049]. The resulting encoding is more compact compared to XML and JSON and more suitable of Constrained Nodes and/or Constrained Networks as defined by [RFC7228].

# Terminology and Notation

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to
be interpreted as described in {{RFC2119}}.

This specification makes use of the following terminology:

* Data node: A node in the YANG schema that can be instantiated in a datastore.
One of container, leaf, leaf-list, list, or anyxml.

* Child data node: A data node defined within a container or a list is a child
of this container or list. The container or list is the parent of the data
node.

* Identifier: An identifier embodies the information required to distinguish
what is being identified from all other things within its scope of identification.

* Parent data node: See Child data node.

## CBOR diagnostic notation

Within this document, CBOR binary contents are represented using an equivalent textual form called CBOR diagnostic notation. This notation is used strictly for documentation purposes and is never transmitted as such.

| CBOR content     | CBOR type | Text representation                                                     | Example            | CBOR encoding      |
|------------------+-----------+-------------------------------------------------------------------------+--------------------+--------------------|
| Unsigned integer |         0 | Decimal digits                                                          | 123                | 18 7b              |
| Negative integer |         1 | Decimal digits prefixed by a minus sign                                 | -123               | 38 7a              |
| Byte string      |         2 | Hexadecimal value enclosed between single quotes and prefixed by an 'h' | h'f15c'            | 42 f15c            |
| Text string      |         3 | String of Unicode characters enclosed between double quotes             | "txt"              | 63 747874          |
| Array            |         4 | Comma separated list of values within square brackets                   | [ 1, 2 ]           | 82 01 02           |
| Map              |         5 | Comma separated list of name/value pairs within curly braces            | { 1: 123, 2: 456 } | a2 01187b 021901c8 |
| Boolean          |      7/20 | false                                                                   | false              | f4                 |
|                  |      7/21 | true                                                                    | true               | f5                 |
| Null             |      7/22 | null                                                                    | null               | f6                 |
| Not assigned     |      7/23 | undefined                                                               | undefined          | f7                 |
{: align="left"}

# Properties of the CBOR Encoding

TO DO

# Structured IDentifiers (SID)

TO DO

# Encoding of YANG Data Node Instances

Objects defined using the YANG modeling language are encoded using CBOR {{RFC7049}} based on the rules defined in this section. We assume that the reader is
already familiar with both YANG {{RFC6020}} and CBOR {{RFC7049}}.

## The "leaf" Data Node 

TO DO

## The "container" Data Node

A container MUST be encoded using a CBOR map data item (major type 5). A
map is comprised of pairs of data items, with each data item consisting of
a key and a value.
CBOR map keys MUST be encoded using a CBOR unsigned integer (major type 0)
and set to a data node ID or a fully-qualified data node ID.  Data node IDs
MUST be used when a parent node exists and this parent shares the same module
ID as the current data node.
CBOR map values MUST be encoded using the rules associated with the data
node type.

Definition example [RFC7317]:

~~~~ YANG
typedef date-and-time {
  type string {
    pattern '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[\+\-]
             \d{2}:\d{2})';
  }
}

container clock {
  leaf current-datetime {
    type date-and-time;
  }

  leaf boot-datetime {
        type date-and-time;
  }
}
~~~~
{: align="left"}

CBOR diagnostic notation:

~~~~ CBORdiag
{
  69667 : {
    36 : "2015-10-02T14:47:24Z-05:00",
    37 : "2015-09-15T09:12:58Z-05:00"
  }
}
~~~~
{: align="left"}

CBOR encoding:

~~~~ CBORbytes
a1
  1a 00011023
  a2
    18 24
    78 1a 323031352d31302d30325431343a34373a32345a2d30353a3030
    18 25
    78 1a 323031352d30392d31355430393a31323a35385a2d30353a3030
~~~~
{: align="left"}

In this example, we assume that the module ID = 68, data node IDs clock =
35, current-datetime = 36 and boot-datetime 37.

## The "leaf-list" Data Node

A leaf-list MUST be encoded using a CBOR array data item (major type 4).
Each entry MUST be encoded using the rules defined by the type specified.

Definition example [RFC7317]:

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

## The "list" Data Node 

A list MUST be encoded using a CBOR array data item (major type 4). Each
entry of this array is encoded using a CBOR map data item (major type 5)
following the same rules as a YANG container.

Definition example [RFC7317]:

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

CBOR diagnostic notation:

~~~~ CBORdiag
{
  69642 : [
    {
      11: "NRC TIC server",
      12 : {
        13: "tic.nrc.ca",
        14: 123
      },
      15 : 0,
      16 : false,
      17 : true
    },
    {
      11: "NRC TAC server",
      12 : {
        13: "tac.nrc.ca"
      }
    }
  ]
}
~~~~
{: align="left"}

CBOR encoding:

~~~~ CBORbytes
a1
   1a 0001100a
   82
      a5
         0b 6e 4e52432054494320736572766572
         0c a2
            0d 6a 7469632e6e72632e6361
            0e 18 7b
         0f 00
         10 f4
         11 f5
      a2
         0b 6f 4e5243205441432073657276657220
         0c a1
            0d 6a 7461632e6e72632e6361
~~~~
{: align="left"}

In this example, we assume that the module ID = 68, data node IDs server
= 10, name = 11,  udp = 12, address = 13, port = 14, association-type = 15,
iburst = 16, prefer = 17.

## The "choice" Statement

YANG allows the data model to segregate incompatible nodes into distinct
choices using the "choice" and "case" statements. Encoded payload MUST carry
data nodes defined in only one of the possible cases.

Definition example [RFC7317]:

~~~~ YANG
typedef timezone-name {
  type string;
}

choice timezone {
  case timezone-name {
    leaf timezone-name {
      type timezone-name;
    }
  }
  case timezone-utc-offset {
    leaf timezone-utc-offset {
      type int16 {
        range "-1500 .. 1500";
      }
      units "minutes";
    }
  }
}
~~~~
{: align="left"}

CBOR diagnostic notation:

~~~~ CBORdiag
{
  69638 : "Europe/Stockholm"
}
~~~~
{: align="left"}

CBOR encoding:

~~~~ CBORbytes
a1
   1a 00011006
   70
      4575726f70652f53746f636b686f6c6d
~~~~
{: align="left"}

## The "anydata" Data Node

TO DO


## The "anyxml" Data Node  

TO DO

# Representing YANG Data Types in CBOR {#data_types_mapping}

## The unsigned integer Types

Leafs of type uint8, uint16, uint32 and uint64 MUST be encoded using a CBOR
unsigned integer data item (major type 0).

Definition example [RFC7277]:

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

Definition example [RFC7317]:

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
value.

Definition example [RFC7317]:

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

Definition example [RFC7223]:

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

Definition example [RFC7317]:

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

Definition example [RFC7317]:

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

Definition example [RFC6020]:

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

Leafs of type leafref MUST be encoded using the rules of the data node referenced
by the "path" YANG statement.

Definition example [RFC7223]:

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

Leafs of type identityref MUST be encoded using a CBOR text string data item
(major type 3). Unlike XML, CBOR does not support namespaces. To overcome
this limitation, identities are encoded using a concatenation of the identity
name(s) of the referenced identities, excluding the base identity and separated
by dot(s).

Definition example [RFC7223]:

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

CBOR diagnostic notation: "iana-interface-type.ethernetCsmacd"

CBOR encoding: 78 22 69616e612d696e746572666163652d747970652e65746865726e657443736d616364

## The "empty" Type  

Leafs of type empty MUST be encoded using the CBOR null value (major type
7, additional information 22).

Definition example [RFC7277]:

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

Definition example [RFC7317]:

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

When a leaf node of type instance-identifier identifies a single instance
data node (data node not part of a list), its value MUST be encoded using
a CBOR unsigned integer data item (major type 0) containing the targeted
data node ID.

Definition example [RFC7317]:

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

CBOR diagnostic notation: 69635

CBOR encoding: 1a 00011003

In this example, the value 69635 identifies the instance of the data node
"hostname" within the ietf-system module. Assuming module ID = 68 and data
node ID = 3.

When a leaf node of type instance-identifier identifies a data node supporting
multiple instances (data node part of a list), its value MUST be encoded
using a CBOR array data item (major type 4) containing the following entries:

* a CBOR unsigned integer data item (major type 0) containing the fully-qualified
data node ID of the targeted data node.

* a CBOR array data item (major type 4) containing the value of each key required
to identify the instance of the targeted data node. These keys MUST be ordered
as defined in the "key" YANG statement, starting from top level list, and
follow by each of the subordinate list(s).

Definition example [RFC7317]:

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

CBOR diagnostic notation: [69679, ["bob", "admin"]]

CBOR encoding: 82  1a 0001102f  82  63 626f62  65 61646d696e

This example identifies the instance of the data node "key-data" within the
ietf-system module, associated with user name "bob" and authorized-key name
"admin". Assuming module ID = 68 and data node ID = 47.

# CBOR Compliance

TO DO

# Security Considerations

This document defines an alternative encoding for data modeled in the YANG data modeling language. As such, this encoding doesn’t contribute any new security issues in addition of those identified for the specific protocol or context for which it is used.

To minimize security risks, software on the receiving side SHOULD reject all messages that do not comply to the rules of this document and reply with an appropriate error message to the sender.

* Acknowledgments

The authors would like to acknowledge the review, feedback, and comments from Andy Bierman, Ladislav Lhotka, Juergen Schoenwaelder, Peter van der Stok.

--- back
