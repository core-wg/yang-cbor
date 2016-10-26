---
stand_alone: true
ipr: trust200902
docname: draft-ietf-core-sid-00
title: YANG Schema Item iDentifier (SID)
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
  ins: A.  S. Somaraju
  name: Abhinav Somaraju
  org: Tridonic GmbH & Co KG
  street: Farbergasse 15
  code: '6850'
  city: Dornbirn
  region: Vorarlberg
  country: Austria
  phone: "+43664808926169"
  email: abhinav.somaraju@tridonic.com
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
- ins: A. P. Pelov
  name: Alexander Pelov
  org: Acklio
  street: 2bis rue de la Chataigneraie
  code: '35510'
  city: Cesson-Sevigne
  region: Bretagne
  country: France
  email: a@ackl.io
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
  street: 2bis rue de la châtaigneraie
  code: '35510'
  city: Cesson-Sévigné
  region: Bretagne
  country: France
  email: ana@ackl.io
normative:
  RFC7950:
  RFC7951:
  RFC2119:
  RFC7049:
informative:
  RFC6241:
  RFC7223:
  RFC7224:
  RFC7277:
  RFC7317:
  I-D.ietf-netconf-restconf: restconf

--- abstract

YANG Schema Item iDentifiers (SID) are used to identify different YANG items using a numeric identifier. This document defines the registration and assignment processes of SIDs. To enable the implementation of these processes, this document also defines a file format used to persist and publish assigned SIDs.

--- middle

# Introduction

YANG identifiers are typically implemented using unmanaged strings. This is the approach used by both NETCONF {{RFC6241}} and RESTCONF {{-restconf}}. In order to implement YANG in constrained devices and constrained networks, a more efficient representation is required. YANG Schema Item iDentifier (SID) is a compact numeric identifier assigned to the following YANG items:

* schema node identifier

* identity identifier

* module name

* submodule name

* feature name

To guarantee uniqueness, SIDs SHALL be assigned within a registered range. This document describes the registries required to manage SIDs and a file format used to persist and publish the assigned SIDs.

# Terminology and Notation

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to
be interpreted as described in {{RFC2119}}.

The following terms are defined in {{RFC7950}}:

* action

* feature

* module

* notification

* RPC

* schema node

* schema tree

* submodule

This specification also makes use of the following terminology:

* identifier: An identifier embodies the information required to distinguish what is being identified from all other things within its scope of identification.

* delta : Difference between the current SID and a reference SID. A reference SID is defined for each context for which deltas are used.

* item:  A schema node, an identity, a module, a submodule or a feature defined using the YANG modeling language.

* path: A path is a string that identifies a schema node within the schema tree. A path consists of the list of schema node identifier(s) separated by slashes ("/"). Schema node identifier(s) are always listed from the top-level schema node up to the targeted schema node. (e.g. "/system-state/clock/current-datetime")

# YANG Schema Item iDentifier (SID)

Some of the items defined in YANG {{RFC7950}} require the use of a unique identifier. In both NETCONF and RESTCONF, these identifiers are implemented using names. To allow the implementation of data models defined in YANG in constrained devices and constrained networks, a more compact method to identify YANG items is required.

This compact identifier, called SID, is encoded using an unsigned integer. To minimize its size, SIDs are often implemented using a delta from a reference SID and the current SID. To guaranty the uniqueness of each assigned SID, SID ranges MUST be registered. {{sid-range-registry}} provide more details about the registration process of SID range(s).

To avoid duplicate assignment of SIDs, the registration of the SIDs assigned to YANG module(s) is recommended. {{module-registry}} provide more details about the registration process of YANG modules.

The following items are identified using SIDs:

*	identities

*	data nodes

*	RPCs and associated input(s) and output(s)

*	actions and associated input(s) and output(s)

*	notifications and associated information

*	YANG modules, submodules and features

Assignment of SIDs can be automated, the recommended process to assign SIDs is as follows:

*	A tool extracts the different items defined for a specific YANG module.

*	The list of items is ordered by type and label.

*	SIDs are assigned sequentially for the entry point up to the size of the registered SID range. This approach is recommended to minimize the serialization overhead, especially when delta encoding is implemented.

*	If the number of items exceeds the SID range(s) allocated to a YANG module, an extra range is added for subsequent assignments.

SIDs are assigned permanently, items introduced by a new revision of a YANG module are added to the list of SIDs already assigned. This process can also be automated using the same method described above except that the assignment need to be restarted from the highest SID already assigned.

{{sid-file-format}} defines a standard file format used to store and publish SIDs.

# ".sid" file lifecycle  {#sid-lifecycle}

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
                            /  Publicly     \ yes | YANG module   |
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

YANG modules are not necessary created in the context of constrained applications. YANG modules can be implemented using NETCONF or RESTCONF without the need to assign SIDs.

As needed, authors of YANG modules can assign SIDs to their modules. This process starts by the registration of a SID range. Once a SID range is registered, the owner of this range assigns sub-ranges to each YANG module in order to generate the associated “.sid” files. Generation of “.sid” files SHOULD be performed using an automated tool.

Registration of the .sid file associated to a YANG module is optional but recommended to promote interoperability between devices and to avoid duplicate allocation of SIDs to a single YANG module.

Each time a YANG module or one of its imported module(s) or included sub-module(s) is updated, the ".sid" file MAY need to be updated. This update SHOULD also be performed using an automated tool.

If a new revision requires more SIDs than initially allocated, a new SID range MUST be added to the assignment ranges as defined in the ".sid" file header. These extra SIDs are used for subsequent assignments.

# ".sid" file format  {#sid-file-format}

".sid" files are used to persist and publish SIDs assigned to the different YANG items of a specific YANG module. The following YANG module defined the structure of this file, encoding is performed using the rules defined in {{RFC7951}}.

~~~~
<CODE BEGINS> file "ietf-sid-file@2015-12-16.yang"
module ietf-sid-file {
  namespace "urn:ietf:params:xml:ns:yang:ietf-sid-file";
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
      "RFC XXXX";
      // RFC Ed.: replace XXXX with RFC number assigned to draft-ietf-core-yang-cbor and remove this note
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
      type uint32;
      mandatory true;
      description
        "Lowest SID available for assignment.";
    }

    leaf size {
      type uint16;
      mandatory true;
      description
        "Number of SIDs available for assignment.";
    }
  }

  list items {
    key "type label";
    description
      "List of items defined by the associated YANG module.";

    leaf type {
      type string {
        pattern 'Module|Submodule|feature|' +
                'identity$|node$|notification$|rpc$|action$';
      }
      mandatory true;
      description
        "Item type assigned, this field can be set to:
          - 'Module'
          - 'Submodule'
          - 'feature'
          - 'identity'
          - 'node'
          - 'notification'
          - 'rpc'
          - 'action'";
    }

    leaf label {
      type string;
      mandatory true;
      description
        "Label associated to this item, can be set to:
          - a module name
          - a submodule name
          - a feature name
          - a base identity encoded as '/<base identity name>'
          - an identity encoded as '/<base identity name>/<identity name>'
          - a schema node path";
    }

    leaf sid {
      type uint32;
      mandatory true;
      description "Identifier assigned to this YANG item.";
    }
  }
}
<CODE ENDS>
~~~~
{: align="left"}

# Security Considerations

The security considerations of {{RFC7049}} and {{RFC7950}} apply.

This document defines an new type of identifier used to encode data models defined in YANG {{RFC7950}}. As such, this identifier does not contribute to any new security issues in addition of those identified for the specific protocols or contexts for which it is used.

# IANA Considerations  {#IANA}

## "SID" range registry  {#sid-range-registry}

IANA is requested to create a registry for YANG Schema Item iDentifier (SID) ranges. This registry needs to guarantee that the ranges registered do not overlap. The registry SHALL record for each entry:

*	The entry point (first entry) of the registered SID range.

*	The size of the registered SID range.

*	The contact information of the owner of the range such as name, email address, and phone number.

The IANA policy for this registry is split into four tiers as follows:

*	The range of 0 to 999 and 0x40000000 to 0xFFFFFFFFFFFFFFFF are reserved for future extensions of this protocol. Allocation within these ranges require IETF review or IESG approval.

*	The range of 1000 to 59999 is reserved for standardized YANG modules. Allocation within this range requires publishing of the associated ".yang" and ".sid" files.  (Specification required.)

*	The range of 60000 to 99999 is reserved for experimental YANG modules. Use of this range MUST NOT be used in operational deployments since these SIDs are not globally unique which limit their interoperability.

*	The range of 100000 to 0x3FFFFFFF is available on a first come first served basis. The only information required from the registrant is a valid contact information. The recommended size of the SID ranges allocated is 1,000 for private use and 10,000 for standard development organizations (SDOs). Registrants MAY request fewer or more SIDs based on their expected, sat needs. Allocation of a significantly larger SID range MAY required IETF review or IESG approval. IANA MAY delegate this registration process to one or multiple sub-registries. The recommended size of the SID range allocation for a sub-registry is 1,000,000.


| Entry Point | Size            | Registration Procedures                                                                                                   |
|-------------+-----------------+---------------------------------------------------------------------------------------------------------------------------|
| 0           | 1,000           | IETF review or IESG approval                                                                                              |
| 1,000       | 59,000          | Specification and associated ".yang" and ".sid" files required                                                            |
| 60,000      | 40,000          | Experimental use                                                                                                          |
| 100,000     | 0x3ffe7960      | Contact information is required. Registration of the module name(s) and associated ".yang" and ".sid" files are optional. |
| 0x40000000  | 2^64-0x40000000 | Specification required, expert review                                                                                     |
{: align="left"}

## YANG module registry {#module-registry}

Each registered SID range can be used to assign SIDs to one or more YANG modules. To track which YANG modules have been assigned and to avoid duplicate allocation, IANA is requested to provide a method to register and query the following information:

*	The YANG module name

*	The contact information of the author

*	The specification reference

*	The associated ".yang" file(s) (Optional)

*	The associated ".sid" file (Optional)

Registration of YANG modules is optional. When a YANG module is registered, the registrant MUST provide the module name and contact information and/or a specification reference.

The registration of the associated ".yang" and ".sid" files is optional. When provided, the validity of the files MUST be verified. This can be accomplished by a YANG validation tool specially modified to support ".sid" file verification. The SID range specified within the ".sid" file SHOULD also be checked against the "SID" range registry ({{sid-range-registry}}) and against the other YANG modules registered to detect any duplicate use of SIDs.

Initial entries in this registry are as follows:

| Entry Point | Size | Module name     | Reference               |
|-------------+------+-----------------+-------------------------+
|        1000 |  100 |                 | Reserved for CoMI       |
|        1100 |  400 | iana-if-type    | {{RFC7224}}             |
|        1500 |  100 | ietf-interfaces | {{RFC7223}}             |
|        1600 |  100 | ietf-ip         | {{RFC7277}}             |
|        1700 |  100 | ietf-system     | {{RFC7317}}             |
{: align="left"}

# Acknowledgments

The authors would like to thank Carsten Bormann for his help during the development of this document and his useful comments during the review process.

--- back

# ".sid" file example  {#sid-file-example}

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
      "type": "Module",
      "label": "ietf-system",
      "sid": 1700
    },
    {
      "type": "feature",
      "label": "authentication",
      "sid": 1701
    },
    {
      "type": "feature",
      "label": "dns-udp-tcp-port",
      "sid": 1702
    },
    {
      "type": "feature",
      "label": "local-users",
      "sid": 1703
    },
    {
      "type": "feature",
      "label": "ntp",
      "sid": 1704
    },
    {
      "type": "feature",
      "label": "ntp-udp-port",
      "sid": 1705
    },
    {
      "type": "feature",
      "label": "radius",
      "sid": 1706
    },
    {
      "type": "feature",
      "label": "radius-authentication",
      "sid": 1707
    },
    {
      "type": "feature",
      "label": "timezone-name",
      "sid": 1708
    },
    {
      "type": "identity",
      "label": "/authentication-method",
      "sid": 1709
    },
    {
      "type": "identity",
      "label": "/authentication-method/local-users",
      "sid": 1710
    },
    {
      "type": "identity",
      "label": "/authentication-method/radius",
      "sid": 1711
    },
    {
      "type": "identity",
      "label": "/radius-authentication-type",
      "sid": 1712
    },
    {
      "type": "identity",
      "label": "/radius-authentication-type/radius-chap",
      "sid": 1713
    },
    {
      "type": "identity",
      "label": "/radius-authentication-type/radius-pap",
      "sid": 1714
    },
    {
      "type": "node",
      "label": "/system",
      "sid": 1715
    },
    {
      "type": "node",
      "label": "/system-state",
      "sid": 1716
    },
    {
      "type": "node",
      "label": "/system-state/clock",
      "sid": 1717
    },
    {
      "type": "node",
      "label": "/system-state/clock/boot-datetime",
      "sid": 1718
    },
    {
      "type": "node",
      "label": "/system-state/clock/current-datetime",
      "sid": 1719
    },
    {
      "type": "node",
      "label": "/system-state/platform",
      "sid": 1720
    },
    {
      "type": "node",
      "label": "/system-state/platform/machine",
      "sid": 1721
    },
    {
      "type": "node",
      "label": "/system-state/platform/os-name",
      "sid": 1722
    },
    {
      "type": "node",
      "label": "/system-state/platform/os-release",
      "sid": 1723
    },
    {
      "type": "node",
      "label": "/system-state/platform/os-version",
      "sid": 1724
    },
    {
      "type": "node",
      "label": "/system/authentication",
      "sid": 1725
    },
    {
      "type": "node",
      "label": "/system/authentication/user",
      "sid": 1726
    },
    {
      "type": "node",
      "label": "/system/authentication/user-authentication-order",
      "sid": 1727
    },
    {
      "type": "node",
      "label": "/system/authentication/user/authorized-key",
      "sid": 1728
    },
    {
      "type": "node",
      "label": "/system/authentication/user/authorized-key/algorithm",
      "sid": 1729
    },
    {
      "type": "node",
      "label": "/system/authentication/user/authorized-key/key-data",
      "sid": 1730
    },
    {
      "type": "node",
      "label": "/system/authentication/user/authorized-key/name",
      "sid": 1731
    },
    {
      "type": "node",
      "label": "/system/authentication/user/name",
      "sid": 1732
    },
    {
      "type": "node",
      "label": "/system/authentication/user/password",
      "sid": 1733
    },
    {
      "type": "node",
      "label": "/system/clock",
      "sid": 1734
    },
    {
      "type": "node",
      "label": "/system/clock/timezone/timezone-name/timezone-name",
      "sid": 1735
    },
    {
      "type": "node",
      "label": "/system/clock/timezone/timezone-utc-offset/timezone-utc-offset",
      "sid": 1736
    },
    {
      "type": "node",
      "label": "/system/contact",
      "sid": 1737
    },
    {
      "type": "node",
      "label": "/system/dns-resolver",
      "sid": 1738
    },
    {
      "type": "node",
      "label": "/system/dns-resolver/options",
      "sid": 1739
    },
    {
      "type": "node",
      "label": "/system/dns-resolver/options/attempts",
      "sid": 1740
    },
    {
      "type": "node",
      "label": "/system/dns-resolver/options/timeout",
      "sid": 1741
    },
    {
      "type": "node",
      "label": "/system/dns-resolver/search",
      "sid": 1742
    },
    {
      "type": "node",
      "label": "/system/dns-resolver/server",
      "sid": 1743
    },
    {
      "type": "node",
      "label": "/system/dns-resolver/server/name",
      "sid": 1744
    },
    {
      "type": "node",
      "label": "/system/dns-resolver/server/transport/udp-and-tcp/udp-and-tcp",
      "sid": 1745
    },
    {
      "type": "node",
      "label": "/system/dns-resolver/server/transport/udp-and-tcp/udp-and-tcp/address",
      "sid": 1746
    },
    {
      "type": "node",
      "label": "/system/dns-resolver/server/transport/udp-and-tcp/udp-and-tcp/port",
      "sid": 1747
    },
    {
      "type": "node",
      "label": "/system/hostname",
      "sid": 1748
    },
    {
      "type": "node",
      "label": "/system/location",
      "sid": 1749
    },
    {
      "type": "node",
      "label": "/system/ntp",
      "sid": 1750
    },
    {
      "type": "node",
      "label": "/system/ntp/enabled",
      "sid": 1751
    },
    {
      "type": "node",
      "label": "/system/ntp/server",
      "sid": 1752
    },
    {
      "type": "node",
      "label": "/system/ntp/server/association-type",
      "sid": 1753
    },
    {
      "type": "node",
      "label": "/system/ntp/server/iburst",
      "sid": 1754
    },
    {
      "type": "node",
      "label": "/system/ntp/server/name",
      "sid": 1755
    },
    {
      "type": "node",
      "label": "/system/ntp/server/prefer",
      "sid": 1756
    },
    {
      "type": "node",
      "label": "/system/ntp/server/transport/udp/udp",
      "sid": 1757
    },
    {
      "type": "node",
      "label": "/system/ntp/server/transport/udp/udp/address",
      "sid": 1758
    },
    {
      "type": "node",
      "label": "/system/ntp/server/transport/udp/udp/port",
      "sid": 1759
    },
    {
      "type": "node",
      "label": "/system/radius",
      "sid": 1760
    },
    {
      "type": "node",
      "label": "/system/radius/options",
      "sid": 1761
    },
    {
      "type": "node",
      "label": "/system/radius/options/attempts",
      "sid": 1762
    },
    {
      "type": "node",
      "label": "/system/radius/options/timeout",
      "sid": 1763
    },
    {
      "type": "node",
      "label": "/system/radius/server",
      "sid": 1764
    },
    {
      "type": "node",
      "label": "/system/radius/server/authentication-type",
      "sid": 1765
    },
    {
      "type": "node",
      "label": "/system/radius/server/name",
      "sid": 1766
    },
    {
      "type": "node",
      "label": "/system/radius/server/transport/udp/udp",
      "sid": 1767
    },
    {
      "type": "node",
      "label": "/system/radius/server/transport/udp/udp/address",
      "sid": 1768
    },
    {
      "type": "node",
      "label": "/system/radius/server/transport/udp/udp/authentication-port",
      "sid": 1769
    },
    {
      "type": "node",
      "label": "/system/radius/server/transport/udp/udp/shared-secret",
      "sid": 1770
    },
    {
      "type": "rpc",
      "label": "/set-current-datetime",
      "sid": 1771
    },
    {
      "type": "rpc",
      "label": "/set-current-datetime/input/current-datetime",
      "sid": 1772
    },
    {
      "type": "rpc",
      "label": "/system-restart",
      "sid": 1773
    },
    {
      "type": "rpc",
      "label": "/system-shutdown",
      "sid": 1774
    }
  ]
}
~~~~
{: align="left"}

--- back
