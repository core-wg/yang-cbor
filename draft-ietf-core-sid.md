---
stand_alone: true
ipr: trust200902
docname: draft-ietf-core-sid-latest
title: YANG Schema Item iDentifier (YANG SID)
area: Applications and Real-Time Area (art)
wg: Internet Engineering Task Force
kw: CBOR
cat: std
consensus: true
submissiontype: IETF
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
  name: Ivaylo Petrov
  org: Google Switzerland GmbH
  street: Brandschenkestrasse 110
  code: 8002
  city: Zurich
  region: Zurich
  country: Switzerland
  email: ivaylopetrov@google.com
- name: Carsten Bormann
  org: Universität Bremen TZI
  street: Postfach 330440
  city: D-28359 Bremen
  country: Germany
  phone: "+49-421-218-63921"
  email: cabo@tzi.org

- name: Michael Richardson
  org: Sandelman Software Works
  email: mcr+ietf@sandelman.ca
  country: Canada

contributor:
- name: Andy Bierman
  org: YumaWorks
  street:
  - 685 Cochran St.
  - 'Suite #160'
  city: Simi Valley
  region: CA
  code: '93065'
  country: USA
  email: andy@yumaworks.com


normative:
  RFC3688:
  RFC6991:
  BCP100:
  RFC7950: yang
  RFC7951: yang-json
  RFC8040: rc
  RFC8259: json
  RFC8791: sx
informative:
  RFC6020:
  RFC6241:
  RFC7224:
  RFC7228: constrained
  RFC7317:
  RFC8126:
  RFC8341:
  RFC8343:
  RFC8344:
  RFC8366:
  RFC7317:
  RFC8792: break
  I-D.ietf-core-comi: comi
  I-D.ietf-core-yang-library: yang-library
  I-D.ietf-anima-constrained-voucher: constrained-voucher
  RFC9254: yang-cbor
  PYANG:
    target: https://github.com/mbj4668/pyang
    title: An extensible YANG validator and converter in python
    author:
      - name: Martin Bjorklund
    date: false
  I-D.bormann-t2trg-deref-id: deref-id

--- abstract

YANG Schema Item iDentifiers (YANG SID) are globally unique 63-bit unsigned integers used to identify YANG items, as a more compact method to identify YANG items that can be used for efficiency and in constrained environments (RFC 7228).
This document defines the semantics, the registration, and assignment processes of YANG SIDs for IETF managed YANG modules.
To enable the implementation of these processes, this document also defines a file format used to persist and publish assigned YANG SIDs.



[^status]

[^status]:
    The present version (–21) updates the `ietf-system.sid` example to
    correctly provide SIDs for the RPCs in `ietf-system.yang`.

--- middle

# Introduction

Some of the items defined in YANG {{RFC7950}} require the use of a
unique identifier.
In both Network Configuration Protocol (NETCONF) {{RFC6241}} and RESTCONF {{RFC8040}}, these identifiers are implemented using names.
To allow the implementation of data models defined in YANG in constrained devices {{RFC7228}} and constrained networks, a more compact method to identify YANG items is required.
This compact identifier, called YANG Schema Item iDentifier or YANG SID (or simply SID in this document and when the context is clear), is encoded using a 63-bit unsigned integer.
The limitation to 63-bit unsigned integers allows SIDs to be manipulated more easily on platforms that might otherwise lack 64-bit unsigned arithmetic.
The loss of a single bit of range is not significant given the size of the remaining space.

The following items are identified using SIDs:

* identities

* data nodes (Note: including those nodes defined by the
  'rc:yang-data' {{-rc}} and 'sx:structure' {{-sx}} extensions.)

* remote procedure calls (RPCs) and associated input(s) and output(s)

* actions and associated input(s) and output(s)

* notifications and associated information

* YANG modules and features

It is possible that some protocols use only a subset of the assigned SIDs, for
example, for protocols equivalent to NETCONF {{RFC6241}} like {{-comi}} the
transportation of YANG module SIDs might be unnecessary. Other protocols
might need to be able to transport this information, for example protocols
related to discovery such as Constrained YANG Module Library {{-yang-library}}.

SIDs are globally unique integers.  A registration system is used in order to
guarantee their uniqueness. SIDs are registered in blocks called "SID ranges".
SIDs are assigned permanently.
Items introduced by a new revision of a YANG
module are added to the list of SIDs already assigned.
This is discussed in more detail in {{objectives}}.

Assignment of SIDs to YANG items is usually automated as
discussed in {{sid-auto-generation}}, which also discusses some cases
where manual interventions may be appropriate.

{{sid-lifecycle}} provides more details about the registration process of YANG
modules and associated SIDs. To enable the implementation of this registry,
{{sid-file-format}} defines a standard file format used to store and publish
SIDs.

IETF managed YANG modules that need to allocate SIDs use the IANA mechanism specified in this document.
YANG modules created by other parties allocate SID ranges using the IANA allocation mechanisms via Mega-Ranges (see {{mega-range-registry}}); within the Mega-Range allocation, those other parties are free to make up their own mechanism.

Among other uses, YANG SIDs are particularly useful to obtain a
compact encoding for YANG-CBOR {{-yang-cbor}}.
At the time of writing, a tool for automated ".sid" file generation is
available as part of the open-source project PYANG {{PYANG}}.

## Terminology and Notation

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

This specification also makes use of the following terminology:

* item:  A schema node, an identity, a module, or a feature defined using the YANG modeling language.

* YANG Schema Item iDentifier (YANG SID or simply SID): Unsigned
  integer used to identify different YANG items (cf. {{Section 3.2 of RFC9254}}).

* YANG Name: Text string used to identify different YANG items
  (cf. {{Section 3.3 of RFC9254}}).

# Objectives

The overriding objective of the SID assignment and registration system is to
ensure global interoperability of protocols that employ SIDs in order
to communicate about data modeled in YANG.
This objective poses certain requirements on the stability of SIDs
while at the same time not hindering active evolution of the YANG
modules the SIDs are intended to support.

Additional objectives include:

* enabling the developer of a YANG module to also be the originating
  entity for the SIDs pertaining to that module.
* making it easy for YANG developers to obtain SIDs.
* enabling other developers to define SIDs for a module where the
  developer of the module is not interested in assigning the SIDs.
* keeping an assignment regime that keeps short (2..4 byte) SIDs
  readily available for the applications that would benefit from them
  while at the same time employing the vast 63-bit SID space to
  facilitate permissionless actions.
* enabling multiple entities to provide services that support the
  assignment of SIDs.
* maintaining some locality in the assignment of SIDs so the
  efficiencies of the SID delta mechanism can be fully employed.
* enabling various software components to deal in terms of SIDs
  without having complete information about other parties in the
  communication process.

While IANA ultimately maintains the registries that govern SIDs for
IETF-defined modules, various support tools such as yangcatalog.org
need to provide the support to enable SID assignment and use for
modules still in IETF development.  Developers of open-source or
proprietary YANG modules also need to be able to serve as such
entities autonomously, possibly forming alliances independent of the
IETF, while still fitting in the overall SID number space managed by
IANA.  Obviously, this process has a number of parallels to the
management of IP addresses, but also is very different.

## Technical Objectives

As discussed in the introduction, SIDs are intended as globally unique
(unsigned) integers.

Specifically, this means that:

**Objective 1** (MUST):
:  any 63-bit unsigned integer is either
unassigned as a SID or immutably maps to EXACTLY one YANG name.
Only the transition from unassigned to that immutable mapping is
defined.

This enables a recipient of a data structure employing SIDs to
translate them into the globally meaningful YANG names that the
existing encodings of YANG data such as YANG-XML {{RFC7950}} and
YANG-JSON {{RFC7951}} employ today.

The term YANG name is not defined outside this document, and YANG has
a complex system of names and entities that can have those names.
Instead of defining the term technically, this set of objectives uses
it in such a way that the overall objectives of YANG-SID can be
achieved.

A desirable objective is that:

**Objective 2** (SHOULD):
: any YANG name in active use has one SID assigned.

This means that:

1. There should not be YANG names without SIDs assigned
2. YANG names should not have multiple SIDs assigned

These objectives are unattainable in full, because YANG names are not
necessarily born with a SID assignment, and because entirely autonomous
entities might decide to assign SIDs for the same YANG name like ships
in the night.
Note that as long as this autonomy is maintained, any single observer
will have the impression that Objective 2 is attained.
Only when entities that have acted autonomously start communicating, a
deviation is observed.

## Module evolution, versioning

YANG modules evolve.
The technical objectives listed above are states in terms that are
independent of this evolution.

However, some modules are still in a very fluid state, and the
assignment of permanent SIDs to the YANG names created in them is less
desirable.  This is not only true for new modules, but also for
emerging new revisions of existing stable modules.

**Objective 3** (MUST):
: the SID management system is independent from any module versioning.



## Solution Components and Derived Objectives

A registration system is used in order to guarantee the uniqueness of
SIDs.
To be able to provide some autonomy in allocation (and avoid
information disclosure where it is not desirable), SIDs are registered
in blocks called "SID ranges".

SIDs are assigned permanently.

Items introduced by a new revision of a YANG
module are added to the list of SIDs already assigned.

## Parties and Roles {#parties-roles}

In the YANG development process, we can discern a number of parties
that are concerned with a YANG module:

{:vspace}
module controller:
: The owner of the YANG module, i.e., the controller
  about its evolution.

registration entity:
: The controller of the module namespace, specifically also of the
  prefixes that are in common use.  (This is not a required party.)

module repository:
: An entity that supplies modules to module users.  This can be
  "official" (e.g., IANA for IETF modules) or unofficial (e.g.,
  yangcatalog.org).  Not all repositories are in a position to act as
  a registry, i.e., as a permanent record for the information they
  supply; these repositories need to recur to module owners as a
  stable source.

module user:
: An entity that uses a module, after obtaining it from the module
  controller or a module repository.

This set of parties needs to evolve to take on the additional roles
that the SID assignment process requires:

{:vspace}
SID assigner:
: An entity that assigns SIDs for a module.  Objective 2 requires that
  there is only one SID assigner for each module.  SID assigners
  preferably stay the same over a module development process; however
  this specification provides SID files to ensure an organized handover.

SID range registries:
: The entities that supply a SID assigner with SID ranges that they can
  use in assigning SIDs for a module.  (In this specification, there
  is a structure with mega-ranges and individual SID ranges; this is
  not relevant here.)

SID repository:
: An entity that supplies SID assignments to SID users, usually in the
  form of a SID file.

SID users:
: The module user that uses the SIDs provided by a SID assigner for a YANG
  module.  SID users need to find SID assigners (or at least their SID
  assignments).

During the introduction of SIDs, the distribution of the SID roles to
the existing parties for a YANG module will evolve.

The desirable end state of this evolution is shown in {{roles-parties}}.

| Role               | Party                                |
| SID assigner       | module developer                     |
| SID range registry | (as discussed in this specification) |
| SID repository     | module repository                    |
| SID user           | module user (naturally)              |
{: #roles-parties title="Roles and Parties: Desired End State"}

This grouping of roles and parties puts the module developer into a
position where it can achieve the objectives laid out in this section
(a "type-1", "SID-guiding" module controller).
(While a third party might theoretically assign additional SIDs and
conflict with objective 2, there is very little reason to do so if SID
files are always provided by the module developer with the module.)

The rest of this section is concerned with the transition to this end
state.

For existing modules, there is no SID file.  The entity that stands in
as the SID assigner is not specified.  This situation has the highest
potential of a conflict with objective 2.

Similarly, for new module development, the module owner may not have
heard about SIDs or not be interested in assigning them (e.g., because
of lack of software or procedures within their organization).

For these two cases (which we will call type-3, "SID-oblivious" module
controller), module repositories can act as a mediator, giving SID
users access to a SID assigner that is carefully chosen to be a likely
choice by other module repositories as well, maximizing the likelihood
of achieving objective 2.

If the module controller has heard about SIDs, but is not assigning
them yet, it can designate a SID assigner instead.  This can lead to a
stable, unique set of SID assignments being provided indirectly by a
(type-2, "SID-aware") module developer.  Entities offering designated
SID assigner services could make these available in an easy-to-use
way, e.g., via a Web interface.

The entity acting as a SID assigner minimally needs to record the SID
range it uses for the SID assignment.  If the SID range registry can
record the module name and revision, and the assignment processes
(including the software used) are stable, the SID assigner can
theoretically reconstruct its assignments, but this is an invitation
for implementation bugs.

SID assigners attending to a module in development (not yet stable)
need to decide whether SIDs for a new revision are re-assigned from
scratch ("clean-slate") or use existing assignments from a previous
revision as a base, only assigning new SIDs for new names.
Once a module is declared stable, its SID assignments SHOULD be
declared stable as well (the exception being that, for existing YANG
modules, some review may be needed before this is done).

This specification does not further discuss how mediating entities
such as designated SID assigners or SID repositories could operate;
instead, it supplies objectives for their operation.

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

Items introduced by a new revision of a YANG module are added to the list of SIDs already assigned.
When this is done during development of a new protocol document, it may be necessary to make provisional assignments.
They may get changed, revised or withdrawn during the development of a new standard.
These provisional assignments are marked with a status of "unstable",
so that they can be removed and the SID number possibly be reassigned
for a different YANG schema name/path later during development.
When the specification is advanced to a final document, then
the assignment is marked with a status of "stable".
During a period of development starting from a published
specification, two variants of the SID file should
be made available by the tooling involved in that development: (1) a
"published" SID file with the existing stable SID assignments only
(which the development effort should keep stable), as
well as (2) an "unpublished" SID file that also contains the unstable
SID assignments.

Registration of the ".sid" file associated to a YANG module is optional but
recommended  <!-- sic. --> to promote interoperability between devices and to avoid duplicate
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
YANG items of a specific YANG module.

It has the following structure:

~~~~ yangtree
{::include code/ietf-sid-file.yangtree}
~~~~
{: align="left" title="YANG tree for ietf-sid-file"}

The following YANG module defines the structure of this file, encoding is
performed in JSON {{-json}} using the rules defined in {{RFC7951}}.
It references ietf-yang-types defined in {{RFC6991}} and ietf-yang-structure-ext defined in {{RFC8791}}.

RFC Ed.: please update the date of the module and Copyright if needed and remove this note.

~~~~ yang
{::include code/ietf-sid-file.yang}
~~~~
{: align="left" sourcecode-markers="true" sourcecode-name="ietf-sid-file@2023-10-23.yang" title="YANG module ietf-sid-file"}

# Security Considerations

This document defines a new type of identifier used to encode data that are modeled in YANG {{RFC7950}}.
This new identifier maps semantic concepts to integers, and if the
source of this mapping is not trusted, then new security risks might
occur if an attacker can control the mapping.

At the time of writing, it is expected that the SID files will be
processed by a software developer, within a software development
environment.  Developers are advised to only import SID files from
authoritative sources.  IANA is the authoritative source for IETF
managed YANG modules.

Conceptually, SID files could be processed by less-constrained target
systems such as network management systems.  Such systems need to take
extra care to make sure that they are only processing SID files from
authoritative sources, as authoritative as the YANG modules that they
are using.

The privacy considerations in {{Section 6 of -deref-id}} apply.

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
* reference:    RFC XXXX

// RFC Ed.: please replace XXXX with RFC number and remove this note

## Create new IANA Registry: "YANG SID Mega-Range" registry {#mega-range-registry}

The name of this registry is "YANG SID Mega-Range". This registry is used to record the delegation of the management of a block of SIDs to third parties (such as SDOs or registrars).

### Structure

Each entry in this registry must include:

* The entry point (first SID) of the registered SID block.
* The size of the registered SID block.
  The size SHOULD be one million (1 000 000) SIDs,
  it MAY exceptionally be a multiple of 1 000 000.
* The contact information of the requesting organization including:
  * The policy of SID range allocations: Public, Private or Both.
  * Organization name
  * URL

### Allocation policy

The IANA policy for future additions to this registry is "Expert Review" {{RFC8126}}.

An organization requesting to manage a YANG SID Range (and thus have an entry in the YANG SID Mega-Range Registry), must ensure the following capacities:

* The capacity to manage and operate a YANG SID Range Registry. A YANG SID Range Registry MUST provide the following information for all YANG SID Ranges allocated by the Registry:
    * Entry Point of allocated YANG SID Range
    * Size of allocated YANG SID Range
    * Type: Public or Private
        * Public Ranges MUST include at least a reference to the YANG module and ".sid" files for that YANG SID Range (e.g., compare {{publink}} for the IETF YANG SID registry).
        * Private Ranges MUST be marked as "Private"
* A Policy of allocation, which clearly identifies if the YANG SID Range allocations would be Private, Public or Both.
* Technical capacity to ensure the sustained operation of the registry for a period of at least 5 years. If Private Registrations are allowed, the period must be of at least 10 years.

If a size of the allocation beyond 1 000 000 is desired, the
organization must demonstrate the sustainability of the technical
approach for utilizing this size of allocation and how it does not
negatively impact the overall usability of the SID allocation
mechanisms; such allocations are preferably placed in the space above
4 295 000 000 (64-bit space).

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

The size of the SID range allocated for a YANG module is recommended to be a multiple of 50 and to be at least 33% above the current number of YANG items. This headroom allows assignment within the same range of new YANG items introduced by subsequent revisions. The SID range size SHOULD NOT exceed 1000; a larger size may be requested by the authors if this recommendation is considered insufficient. It is important to note that an additional SID range can be allocated to an existing YANG module if the initial range is exhausted; this then just leads to slightly less efficient representation.

In case a SID range is allocated for an existing RFC through the "Expert
Review" policy, the Document reference field for the given allocation should
point to the RFC that the YANG module is defined in.

In case a SID range is required before publishing the RFC due to
implementations needing stable SID values, early allocation as defined in
{{BCP100}} can be employed for the "RFC Required" range (Section 2 of
{{BCP100}}). <!-- XXX xml2rfc bug-->


### Publication of the ".sid" file {#publink}

During publication of an RFC, IANA contacts the designated expert team
("the team"), who are responsible for delivering a final SID file for
each module defined by the RFC.
For a type-3 developer ({{parties-roles}}), the team
creates a new SID file from each YANG module, see below.
For a type-2 developer, the team first obtains the existing draft SID
file from a stable reference in the approved draft; for a type-1
developer, the team extracts the SID file from the approved draft.

The team uses a tool to generate a final SID file from each YANG
module; the final SID file has all SID assignments set to "stable" and
the SID file status set to "published".
A published ".sid" file MUST NOT contain SID assignments with an
unstable status.

For the cases other than type-3, the team feeds the existing draft SID
file as an input to the tool so that the changes resulting from
re-generation are minimal.
In any case, the team checks the generated file, including for
validity as a SID file, for consistency with the SID range
allocations, for full coverage of the YANG items in YANG module, and
for the best achievable consistency with the existing draft SID file.

The designated experts then give the SID file to IANA to publish into
the YANG SID Registry ({{ietf-sid-registry}}) along with the YANG
module.

The ".sid" file MUST NOT be published as part of the RFC: the IANA
Registry is authoritative and a link to it is to be inserted in the RFC.
(Note that the present RFC is an exception to this rule as the SID
file also serves as an example for exposition.)
RFCs that need SIDs assigned to their new modules for use in the text
of the document, e.g., for examples, need to alert the RFC editor in
the draft text that this is the case.
Such RFCs cannot be produced by type-3 developers:
the SIDs used in the text need to be assigned in the existing draft
SID file, and the designated expert team needs to check that the
assignments in the final SID file are consistent with the usage in the
RFC text or that the approved draft test is changed appropriately.


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
draft author can use the experimental SID range (as per
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
YANG modules may also need to have SID allocations made, in a process
that will generally analogous to that in {{publink}} for the type-3 case.

The Expert Reviewer who performs the (Early) Allocation analysis will need to
go through the list of included YANG modules and perform SID allocations for
those modules as well.

* If the document is a published RFC, then the allocation of SIDs for its
  referenced YANG modules is permanent.  The Expert Reviewer provides the
  generated ".sid" file to IANA for registration.
* If the document is an unprocessed Internet-Draft adopted in a WG, then an
  Early Allocation is performed for this document as well. Early Allocations
  require approval by an IESG Area Director.  An early allocation which
  requires additional allocations will list the other allocations in its
  description, and will be cross-posted to the any other working group mailing
  lists.
* A YANG module which references a module in a document which has not yet been
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

Early Allocations are made with a one-year period, after which they
need to be renewed or will expire.

{{BCP100}} also says:

    Note that if a document is submitted for review to the IESG and at
    the time of submission some early allocations are valid (not
    expired), these allocations should not be expired while the document
    is under IESG consideration or waiting in the RFC Editor's queue
    after approval by the IESG.

### Initial contents of the registry

None.

## Register Media Type and Content-Format

### Media Type application/yang-sid+json

This document adds the following Media-Type to the "Media Types" registry.

| Name          | Template                  | Reference |
| yang-sid+json | application/yang-sid+json | RFC XXXX  |
{: align="left" title="SID File Media-Type Registration"}

// RFC Ed.: please replace RFC XXXX with this RFC number and remove this note.

{: spacing="compact"}
Type name:
: application

Subtype name:
: yang-sid+json

Required parameters:
: N/A

Optional parameters:
: N/A

Encoding considerations:
: binary (UTF-8)

Security considerations:
: see {{security-considerations}} of RFC XXXX

Published specification:
: RFC XXXX

Applications that use this media type:
: applications that need to obtain YANG SIDs to interchange
  YANG-modeled data in a concise and efficient representation

Fragment identifier considerations:
: The syntax and semantics of
      fragment identifiers specified for "application/yang-sid+json" is
      as specified for "application/json".  (At publication of this
      document, there is no fragment identification syntax defined for
      "application/json".)

Additional information:
: <br>
  Magic number(s):
  : N/A

  File extension(s):
  : .sid

  Macintosh file type code(s):
  : N/A

Person & email address to contact for further information:
: CORE WG mailing list (core@ietf.org),
  or IETF Applications and Real-Time Area (art@ietf.org)

Intended usage:
: COMMON

Restrictions on usage:
: none

Author/Change controller:
: IETF


### CoAP Content-Format

This document adds the following Content-Format to the "CoAP Content-Formats",
within the "Constrained RESTful Environments (CoRE) Parameters"
registry, where TBD1 comes from the "IETF Review" 256-999 range.

| Content Type              | Content Coding | ID   | Reference |
| application/yang-sid+json | -              | TBD1 | RFC XXXX  |
{: align="left" title="SID File Content-format Registration"}

// RFC Ed.: please replace TBDx with assigned IDs, remove the
requested ranges, and remove this note.\\
// RFC Ed.: please replace RFC XXXX with this RFC number and remove this note.


--- back

# ".sid" file example  {#sid-file-example}

The following ".sid" file (ietf-system@2014-08-06.sid) has been generated using the following yang modules:

* ietf-system@2014-08-06.yang (defined in {{RFC7317}})

* ietf-yang-types@2013-07-15.yang (defined in {{RFC6991}})

* ietf-inet-types@2013-07-15.yang (defined in {{RFC6991}})

* ietf-netconf-acm@2018-02-14.yang (defined in {{RFC8341}})

* iana-crypt-hash@2014-08-06.yang (defined in {{RFC7317}})

For purposes of exposition, line breaks have been introduced below in
some JSON strings that represent overly long identifiers.

<!-- /^ *[^" ]+"/ -->

~~~~ yang-sid
{::include-fold code/ietf-system.sid}
~~~~
{: #sid-example-pretty title="Example .sid file (ietf-system, with extra line-breaks)"}

# SID auto generation {#sid-auto-generation}

Assignment of SIDs to YANG items SHOULD be automated.
The recommended process to assign SIDs is as follows:

1. A tool extracts the different items defined for a specific YANG module.
2. The list of items is sorted in alphabetical order, 'namespace' in descending order, 'identifier' in ascending order. The 'namespace' and 'identifier' formats are described in the YANG module 'ietf-sid-file' defined in {{sid-file-format}}.
3. SIDs are assigned sequentially from the entry point up to the size of the registered SID range. This approach is recommended to minimize the serialization overhead, especially when delta between a reference SID and the current SID is used by protocols aiming to reduce message size.
4. If the number of items exceeds the SID range(s) allocated to a YANG module, an extra range is added for subsequent assignments.
5. The "dependency-revision" should reflect the revision numbers of each
   YANG module that the YANG module imports at the moment of the generation.

When updating a YANG module that is in active use, the existing SID assignments are maintained.
(In contrast, when evolving an early draft that has not yet been adopted by a community of developers, SID assignments are often better done from scratch after a revision.)
If the name of a schema node changes, but the data remain structurally and semantically similar to what was previously available under an old name, the SID that was used for the old name MAY continue to be used for the new name.
If the meaning of an item changes, a new SID MAY be assigned to it; this is particularly useful to allow the new SID to identify the new structure or semantics of the item.
If the YANG data type changes in a new revision of a published module,
such that the resulting CBOR encoding is changed, then implementations will be aided significantly if a new SID is assigned.
Note that these decisions are generally at the discretion of the YANG module author, who should decide if the benefits of a manual intervention are worth the deviation from automatic assignment.

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

Note also that RPC or action "input" and "output" YANG items MUST always be
assigned SID even if they don't contain further YANG items. The reason for this
requirement is that other modules can augment the given module and those SIDs
might be necessary.

# ".sid" file lifecycle {#sid-lifecycle-ex}

Before assigning SIDs to their YANG modules, YANG module authors must acquire a
SID range from a "YANG SID Range Registry". If the YANG module is part of an IETF
draft or RFC, the SID range need to be acquired from the "IETF YANG SID Range
Registry" as defined in {{ietf-iana-sid-range-allocation}}. For the other YANG
modules, the authors can acquire a SID range from any "YANG SID Range Registry" of
their choice.

Once the SID range is acquired, owners can use it to generate ".sid" file/s
for their YANG module/s.  It is recommended to leave some unallocated SIDs
following the allocated range in each ".sid" file in order to allow better
evolution of the YANG module in the future.  Generation of ".sid" files should
be performed using an automated tool.  Note that ".sid" files can only be
generated for YANG modules and not for submodules.

## ".sid" File Creation

The following activity diagram summarizes the creation of a YANG module and its associated ".sid" file.

~~~~ aasvg
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
|    \ application ? /---->| registration  |<--------+
|     '-----+-------'      +------+--------+         |
|           |  no                 |                  |
|           v                     v                  |
|    +---------------+    +---------------+          |
+----+ YANG module   |    | SID sub-range |          |
     | update        |    | assignment    |<---------+
     +---------------+    +-------+-------+          |
                                  |                  |
                                  v                  |
                         +---------------+    +------+------+
                         | ".sid" file   |    | Rework YANG |
                         | generation    |    |    module   |
                         +-------+-------+    +-------------+
                                 |                   ^
                                 v                   |
                           .----------.  yes         |
                          /  Work in   \ ------------+
                          \  progress  /
                           '----+-----'
                                |  no
                                v
                       .-------------.
                      /      RFC      \ no
                      \  publication? /--------------+
                       '------+------'               |
                         yes  |                      |
                              v                      v
                    +---------------+        +---------------+
                    |     IANA      |        | Third party   |
                    | registration  |        | registration  |
                    +-------+-------+        +-------+-------+
                            |                        |
                            +------------------------+
                            v
                          [DONE]
~~~~
{: #fig-sid-file-creation title='SID Lifecycle' align="left"}

## ".sid" File Update

The following Activity diagram summarizes the update of a YANG module and its associated ".sid" file.

~~~~ aasvg
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
                                 v
                               [DONE]

~~~~
{: #fig-sid-file-update title="YANG and \".sid\" file update" align="left"}

# Keeping a SID File in a YANG Instance Data file

{{?RFC9195}} defines a format for "YANG Instance Data".
This essentially leads to an encapsulation of the instance data within
some metadata envelope.

If a SID file needs to be stored in a YANG Instance Data file, this
can be achieved by embedding the value of the SID file as the value of the
`content-data` member in the following template, and copying over the
second-level members as indicated with the angle brackets:

~~~ yang-instance-data
{
  "ietf-yang-instance-data:instance-data-set": {
    "name": "<module-name>@<module-revision>.sid",
    "description":  ["<description>"],
    "content-schema": {
      "module": "ietf-sid-file@2023-10-23"
    },
    "content-data": {  <replace this object>
      "ietf-sid-file:sid-file" : {
        "module-name": ...
      }
    }
  }
}
~~~

[^rfced]

[^rfced]: RFC editor: Please replace the module date by the correct
    one for the ietf-sid-file module.


# Acknowledgments
{: numbered="false"}

The authors would like to thank {{{Andy Bierman}}}, {{{Michael Richardson}}},
{{{Abhinav Somaraju}}}, {{{Peter van der Stok}}}, {{{Laurent Toutain}}} and
{{{Randy Turner}}} for their help during the development of this document and
their useful comments during the review process.
Special thanks go to the IESG members who supplied very useful
comments during the IESG processing phase, in particular to
{{{Benjamin Kaduk}}} and {{{Rob Wilton}}}.
