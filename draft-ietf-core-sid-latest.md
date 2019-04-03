---
stand_alone: true
ipr: trust200902
docname: draft-ietf-core-sid-06
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
  ins: I. I. Petrov
  name: Ivaylo Petrov
  org: Acklio
  street: 1137A avenue des Champs Blancs
  code: '35510'
  city: Cesson-Sevigne
  region: Bretagne
  country: France
  email: ivaylo@ackl.io
normative:
  RFC7950:
  RFC7951:
  RFC2119:
  RFC7049:
  RFC7120:
informative:
  RFC8126:
  RFC6020:
  RFC6021:
  RFC6241:
  RFC6536:
  RFC7223:
  RFC7224:
  RFC7277:
  RFC7317:
  RFC8040:
  I-D.ietf-core-comi: comi

--- abstract

YANG Schema Item iDentifiers (SID) are globally unique 64-bit unsigned numbers used to identify YANG items.  This document defines the semantics, the registration, and assignment processes of SIDs.  To enable the implementation of these processes, this document also defines a file format used to persist and publish assigned SIDs.

--- middle

# Introduction

Some of the items defined in YANG {{RFC7950}} require the use of a unique identifier.  In both NETCONF {{RFC6241}} and RESTCONF {{RFC8040}}, these identifiers are implemented using names.  To allow the implementation of data models defined in YANG in constrained devices and constrained networks, a more compact method to identify YANG items is required. This compact identifier, called SID, is encoded using a 64-bit unsigned integer. The following items are identified using SIDs:

* identities

* data nodes (Note: including those part of a YANG template as defined by the 'yang-data' extension.)

* RPCs and associated input(s) and output(s)

* actions and associated input(s) and output(s)

* notifications and associated information

* YANG modules, submodules and features

To minimize their size, in certain positions, SIDs could be represented using a
(signed) delta from a reference SID and the current SID (for example during
transmissions). Such difference is itself called "delta", shorthand for
"delta-encoded SID". Conversion from SIDs to deltas and back to SIDs is a
stateless process. Each protocol implementing deltas must unambiguously define
the reference SID for each YANG item.

SIDs are globally unique numbers, a registration system is used in order to
guarantee their uniqueness. SIDs are registered in blocks called "SID ranges".

Assignment of SIDs to YANG items can be automated. For more details how this
could be achieved, please consult {{sid-auto-generation}}.

SIDs are assigned permanently, items introduced by a new revision of a YANG
module are added to the list of SIDs already assigned.

{{sid-lifecycle}} provides more details about the registration process of YANG
modules and associated SIDs. To enable the implementation of this registry,
{{sid-file-format}} defines a standard file format used to store and publish
SIDs.

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

The following term is defined in {{RFC8040}}:

* yang-data extension

This specification also makes use of the following terminology:

* delta : Difference between the current SID and a reference SID. Each protocol that uses delta encoded SIDs MUST define how the reference SID is obtained.
* item:  A schema node, an identity, a module, a submodule or a feature defined using the YANG modeling language.
* path: A path is a string that identifies a schema node within the schema tree. A path consists of the list of schema node identifier(s) separated by slashes ("/"). Schema node identifier(s) are always listed from the top-level schema node up to the targeted schema node. (e.g. "/ietf-system:system-state/clock/current-datetime")
* YANG Schema Item iDentifier (SID): Unsigned integer used to identify different YANG items.

# ".sid" file lifecycle  {#sid-lifecycle}

YANG is a language designed to model data accessed using one of the compatible
protocols (e.g. NETCONF {{RFC6241}}, RESCONF {{RFC8040}} and CoMI {{-comi}}). A
YANG module defines hierarchies of data, including configuration, state data,
RPCs, actions and notifications.

YANG modules are not necessarily created in the context of constrained
applications. YANG modules can be implemented using NETCONF {{RFC6241}} or
RESTCONF {{RFC8040}} without the need to assign SIDs.

As needed, authors of YANG modules can assign SIDs to their YANG modules. In
order to do that, they should first obtain a SID range from a registry and use
that range to assign or generate SIDs to items of their YANG module. For
example how this could be achieved, please refer to {{sid-lifecycle-ex}}.

Registration of the .sid file associated to a YANG module is optional but
recommended to promote interoperability between devices and to avoid duplicate
allocation of SIDs to a single YANG module. Different registries might have
different requirements for the registration and publication of the “.sid“
files. For diagram of one of the possibilities, please refer to the activity
diagram on {{fig-sid-file-creation}} in {{sid-lifecycle-ex}}.


Each time a YANG module or one of its imported module(s) or included
sub-module(s) is updated, the ".sid" file MAY need to be updated. This update
SHOULD also be performed using an automated tool.

If a new revision requires more SIDs than initially allocated, a new SID range
MUST be added to the 'assignment-ranges' as defined in {{sid-file-format}}.
These extra SIDs are used for subsequent assignments.

For an example of this update process, see activity diagram
{{fig-sid-file-update}} in {{sid-lifecycle-ex}}.

# ".sid" file format  {#sid-file-format}

".sid" files are used to persist and publish SIDs assigned to the different YANG items of a specific YANG module. The following YANG module defined the structure of this file, encoding is performed using the rules defined in {{RFC7951}}.

~~~~
<CODE BEGINS> file "ietf-sid-file@2017-11-26.yang"
module ietf-sid-file {
  namespace "urn:ietf:params:xml:ns:yang:ietf-sid-file";
  prefix sid;

  import ietf-yang-types {
    prefix yang;
  }

  organization
    "IETF Core Working Group";

  contact
    "Michel Veillette
     <mailto:michel.veillette@trilliant.com>

     Andy Bierman
     <mailto:andy@yumaworks.com>

     Alexander Pelov
     <mailto:a@ackl.io>";

  description
    "This module defines the structure of the .sid files.
    
     Each .sid file contains the mapping between the different
     string identifiers defined by a YANG module and a
     corresponding numeric value called SID.";

  revision 2017-11-26 {
    description
      "Initial revision.";
    reference
      "[I-D.ietf-core-sid] YANG Schema Item iDentifier (SID)";
  }

  typedef revision-identifier {
    type string {
      pattern '\d{4}-\d{2}-\d{2}';
    }
    description
      "Represents a date in YYYY-MM-DD format.";
  }

  typedef sid {
    type uint64;
    description
      "YANG Schema Item iDentifier";
    reference
      "[I-D.ietf-core-sid] YANG Schema Item iDentifier (SID)";
  }

  typedef schema-node-path {
    type string {
      pattern
        '/[a-zA-Z_][a-zA-Z0-9\-_.]*:[a-zA-Z_][a-zA-Z0-9\-_.]*' +
        '(/[a-zA-Z_][a-zA-Z0-9\-_.]*(:[a-zA-Z_][a-zA-Z0-9\-_.]*)?)*';
    }
    description
      "Identifies a schema-node path string for use in the
       SID registry. This string format follows the rules
       for an instance-identifier, as defined in RFC 7959,
       except that no predicates are allowed.

       This format is intended to support the YANG 1.1 ABNF
       for a schema node identifier, except module names
       are used instead of prefixes, as specified in RFC 7951.";
    reference
      "RFC 7950, The YANG 1.1 Data Modeling Language;
       Section 6.5: Schema Node Identifier;
       RFC 7951, JSON Encoding of YANG Data;
       Section 6.11: The instance-identifier type";
  }

  leaf module-name {
    type yang:yang-identifier;
    description
      "Name of the YANG module associated with this .sid file.";
  }

  leaf module-revision {
    type revision-identifier;
    description
      "Revision of the YANG module associated with this .sid file.
       This leaf is not present if no revision statement is
       defined in the YANG module.";
  }

  list assigment-ranges {
    key "entry-point";
    description
      "SID range(s) allocated to the YANG module identified by
       'module-name' and 'module-revision'.";

    leaf entry-point {
      type sid;
      mandatory true;
      description
        "Lowest SID available for assignment.";
    }

    leaf size {
      type uint64;
      mandatory true;
      description
        "Number of SIDs available for assignment.";
    }
  }

  list items {
    key "namespace identifier";
    description
      "Each entry within this list defined the mapping between
       a YANG item string identifier and a SID. This list MUST
       include a mapping entry for each YANG item defined by
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
            "The namespace for all data nodes, as defined in YANG.";
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
        "String identifier of the YANG item for this mapping entry.
        
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
        "SID assigned to the YANG item for this mapping entry.";
    }
  }
}
<CODE ENDS>
~~~~
{: align="left"}

# Security Considerations

The security considerations of {{RFC7049}} and {{RFC7950}} apply.

This document defines a new type of identifier used to encode data models defined in YANG {{RFC7950}}. As such, this identifier does not contribute to any new security issues in addition of those identified for the specific protocols or contexts for which it is used.

# IANA Considerations  {#IANA}

## Register SID File Format Module {#iana-module-registration}

This document registers one YANG modules in the "YANG Module Names" registry {{RFC6020}}:

* name:         ietf-sid-file
* namespace:    urn:ietf:params:xml:ns:yang:ietf-sid-file
* prefix:       sid
* reference:    [[THISRFC]]

## Create new IANA Registry: "SID Mega-Range" registry {#mega-range-registry}

The name of this registry is "SID Mega-Range". This registry is used to record the delegation of the management of a block of SIDs to third parties (e.g. SDOs, registrars, etc).

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

The IANA policies for future additions to this registry are "Expert Review" {{RFC8126}}.

An organization requesting to manage a SID Range (and thus have an entry in the SID Mega-Range Registry), must ensure the following capacities:

* The capacity to manage and operate a SID Range Registry. A SID Range Registry MUST provide the following information for all SID Ranges allocated by the Registry:
    * Entry Point of allocated SID Range
    * Size of allocated SID Range
    * Type: Public or Private
        * Public Ranges MUST include at least a reference to the YANG module and ".sid" files for that SID Range.
        * Private Ranges MUST be marked as "Private"
* A Policy of allocation, which clearly identifies if the SID Range allocations would be Private, Public or Both.
* Technical capacity to ensure the sustained operation of the registry for a period of at least 5 years. If Private Registrations are allowed, the period must be of at least 10 years.


#### First allocation

For a first allocation to be provided, the requesting organization must demonstrate a functional registry infrastructure.

#### Consecutive allocations

On subsequent allocation request(s), the organization must demonstrate the
exhaustion of the prior range. These conditions need to be asserted by the
assigned expert(s).

If that extra-allocation is done within 3 years from the last allocation, the
experts need to discuss this request on the CORE working group mailing list and
consensus needs to be obtained before allocating new Mega-Range.


### Initial contents of the Registry

The initial entry in this registry is allocated to IANA:

| Entry Point | Size    | Allocation | Organization name | URL      |
|-------------+---------+------------|-------------------|----------|
| 0           | 1000000 | Public     | IANA              | iana.org |
{: align="left"}

## Create a new IANA Registry: IETF SID Range Registry (managed by IANA) {#ietf-iana-sid-range-allocation}

### Structure {#ietf-iana-sid-range-structure}

Each entry in this registry must include:

* The SID range entry point.
* The SID range size.
* The YANG module name.
* Document reference.

### Allocation policy {#ietf-iana-sid-range-allocation-policy}

The first million SIDs assigned to IANA is sub-divided as follows:

* The range of 0 to 999 (size 1000) is "Reserved" as defined in {{RFC8126}}.
* The range of 1000 to 59,999 (size 59,000) is reserved for YANG modules defined in RFCs. The IANA policy for additions to this registry is "Expert Review" {{RFC8126}}.
    * The Expert MUST verify that the YANG module for which this allocation is made has an RFC (existing RFC) OR is on track to become RFC (early allocation with a request from the WG chairs).

* The SID range allocated for a YANG module can follow in one of the four categories:
    * SMALL (50 SIDs)
    * MEDIUM (100 SIDs)
    * LARGE (250 SIDs)
    * CUSTOM (requested by the YANG module author, with a maximum of 1000 SIDs).
  In all cases, the size of a SID range assigned to a YANG module should be at least 33% above the current number of YANG items. This headroom allows assignment within the same range of new YANG items introduced by subsequent revisions. A larger SID range size may be requested by the authors if this recommendation is considered insufficient. It is important to note that an additional SID range can be allocated to an existing YANG module if the initial range is exhausted.
* The range of 60,000 to 99,999 (size 40,000)is reserved for experimental YANG modules. This range MUST NOT be used in operational deployments since these SIDs are not globally unique which limit their interoperability. The IANA policy for this range is "Experimental use" {{RFC8126}}.
* The range of 100,000 to 999,999 (size 900,000) is "Reserved" as defined in {{RFC8126}}.

| Entry Point   | Size       | IANA policy                       |
|---------------+------------+-----------------------------------|
| 0             | 1,000      | Reserved                          |
| 1,000         | 59,000     | Expert Review                     |
| 60,000        | 40,000     | Experimental use                  |
| 100,000       | 900,000    | Reserved                          |
{: align="left"}


### Initial contents of the registry {#ietf-iana-sid-range-initial-contents}

Initial entries in this registry are as follows:

| Entry Point | Size | Module name      | Document reference     |
|-------------+------+------------------+------------------------|
| 1000        | 100  | ietf-comi        | {{-comi}}              |
| 1100        |  50  | ietf-yang-types  | {{RFC6021}}            |
| 1150        |  50  | ietf-inet-types  | {{RFC6021}}            |
| 1200        |  50  | iana-crypt-hash  | {{RFC7317}}            |
| 1250        |  50  | ietf-netconf-acm | {{RFC6536}}            |
| 1300        |  50  | ietf-sid-file    | RFCXXXX                |
| 1500        | 100  | ietf-interfaces  | {{RFC7223}}            |
| 1600        | 100  | ietf-ip          | {{RFC7277}}            |
| 1700        | 100  | ietf-system      | {{RFC7317}}            |
| 1800        | 400  | iana-if-type     | {{RFC7224}}            |
{: align="left"}

// RFC Ed.: replace XXXX with RFC number assigned to this draft.

For allocation, RFC publication of the YANG module is required as per {{RFC8126}}. The YANG module must be registered in the "YANG module Name" registry according to the rules specified in section 14 of {{RFC6020}}.

## Create new IANA Registry: “IETF SID Registry” {#ietf-sid-registry}

The name of this registry is "IETF SID Registry".  This registry is used to
record the allocation of individual SIDs YANG module items.

### Structure

Each entry in this registry must include:

* The YANG module name. This module name must be present in the "Name" column of the “YANG Module Names” registry.
* A link to the associated ".yang" file.  This file link must be present in the "File" column of the “YANG Module Names” registry.
* The link to the ".sid" file which defines the allocation.
* The number of actually allocated SIDs in the “.sid” file.

The “.sid” file is stored by IANA.

### Allocation policy

The allocation policy is Expert review. The Expert MUST ensure that the following conditions are met:

* The ".sid" file has a valid structure:
    * The “.sid” file MUST be a valid JSON file following the structure of the
      module defined in RFCXXXX (RFC Ed: replace XXX with RFC number assigned
      to this draft).
* The ".sid" file allocates individual SIDs ONLY in the SID Ranges for this
  YANG module (as allocated in the IETF SID Range Registry):
    * All SIDs in this “.sid” file MUST be within the ranges allocated to this
      YANG module in the “IETF SID Range Registry”.
* If another ".sid" file has already allocated SIDs for this YANG module (e.g.
  for older or newer versions of the YANG module), the YANG items are assigned
  the same SIDs as in the the other ".sid" file.
* SIDs never change.

### Initial contents of the registry

None.

# Acknowledgments

The authors would like to thank Andy Bierman, Carsten Bormann, Abhinav Somaraju, Laurent Toutain, Randy Turner and Peter van der Stok for their help during the development of this document and their useful comments during the review process.

--- back

# ".sid" file example  {#sid-file-example}

The following .sid file (ietf-system@2014-08-06.sid) have been generated using the following yang modules:

* ietf-system@2014-08-06.yang

* ietf-yang-types@2013-07-15.yang

* ietf-inet-types@2013-07-15.yang

* ietf-netconf-acm@2012-02-22.yang

* iana-crypt-hash@2014-04-04.yang

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
~~~~

# SID auto generation {#sid-auto-generation}

Assignment of SIDs to YANG items can be automated, the recommended process to assign SIDs is as follows:

1. A tool extracts the different items defined for a specific YANG module.

2. The list of items is sorted in alphabetical order, 'namespace' in descending order, 'identifier' in ascending order. The 'namespace' and 'identifier' formats are described in the YANG module 'ietf-sid-file' defined in {{sid-file-format}}.

3. SIDs are assigned sequentially from the entry point up to the size of the registered SID range. This approach is recommended to minimize the serialization overhead, especially when delta encoding is implemented.

4. If the number of items exceeds the SID range(s) allocated to a YANG module, an extra range is added for subsequent assignments.

Changes of SID files can also be automated using the same method described above, only unassigned YÀNG items are processed at step #3.

# ".sid" file lifecycle {#sid-lifecycle-ex}

Before assigning SIDs to their YANG modules, YANG module authors must acquire a
SID range from a "SID Range Registry". If the YANG module is part of an IETF
draft or RFC, the SID range need to be acquired from the "IETF SID Range
Registry" as defined in {{ietf-iana-sid-range-allocation}}. For the other YANG
modules, the authors can acquire a SID range from any "SID Range Registry" of
their choice.

Once the SID range is acquired, the owner can use it to generate ".sid" file/s
for his YANG module/s.  It is recommended to leave some unallocated SIDs
following the allocated range in each ".sid" file in order to allow better
evolution of the YANG module in the future.  Generation of ".sid" files should
be performed using an automated tool.  Note that ".sid" files can only be
generated for YANG modules and not for submodules.

## SID File Creation

The following activity diagram summarizes the creation of a YANG module and its associated .sid file.

~~~~
       +---------------+
  O    | Creation of a |
 -|- ->| YANG module   |
 / \   +---------------+
               |
               V
        /-------------\
       / Standardized  \     yes
       \ YANG module ? /-------------+
        \-------------/              |
               | no                  |
               V                     V
        /-------------\      +---------------+
       / Constrained   \ yes | SID range     |
   +-->\ application ? /---->| registration  |<----------+
   |    \-------------/      +---------------+           |
   |           | no                  |                   |
   |           V                     V                   |
   |   +---------------+     +---------------+           |
   +---| YANG module   |     | SID sub-range |           |
       | update        |     | assignment    |<----------+
       +---------------+     +---------------+           |
                                     |                   |
                                     V                   |
                             +---------------+    +-------------+
                             | .sid file     |    | Rework YANG |
                             | generation    |    |    model    |
                             +---------------+    +-------------+
                                     |                   ^
                                     V                   |
                                /----------\  yes        |
                               /  Work in   \ -----------+
                               \  progress  /
                                \----------/
                                     | no
                                     V
                               /-------------\       /-------------\
                              /      RFC      \ no  /     Open      \ no
                              \  publication? /---->\ specification?/---+
                               \-------------/       \-------------/    |
                                      | yes                 | yes       |
                                      |     +---------------+           |
                                      V     V                           V
                              +---------------+                 +---------------+
                              |     IANA      |                 | Third party   |
                              | registration  |                 | registration  |
                              +-------+-------+                 +-------+-------+
                                      |                                 |
                                      +---------------------------------+
                                      V
                                    [DONE]
~~~~
{: #fig-sid-file-creation title='SID Lifecycle' align="left"}

## SID File Update

The following Activity diagram summarizes the update of a YANG module and its associated .sid file.

~~~~
       +---------------+
  O    | Update of the |
 -|- ->| YANG module   |
 / \   | or include(s) |
       | or import(s)  |
       +---------------+
               |
               V
           /-------------\
          /  New items    \ yes
          \  created  ?   /------+
           \-------------/       |
                  | no           V
                  |       /-------------\      +----------------+
                  |      /  SID range    \ yes | Extra sub-range|
                  |      \  exhausted ?  /---->| assignment     |
                  |       \-------------/      +----------------+
                  |              | no                  |
                  |              +---------------------+
                  |              |
                  |              V
                  |      +---------------+
                  |      | .sid file     |
                  |      | update based  |
                  |      | on previous   |
                  |      | .sid file     |
                  |      +---------------+
                  |              |
                  |              V
                  |       /-------------\      +---------------+
                  |      /  Publicly     \ yes | YANG module   |
                  |      \  available ?  /---->| registration  |
                  |       \-------------/      +---------------+
                  |              | no                  |
                  +--------------+---------------------+
                                 |
                               [DONE]

~~~~
{: #fig-sid-file-update title="YANG and SID file update" align="left"}
