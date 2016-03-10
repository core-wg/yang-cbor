---
stand_alone: true
ipr: trust200902
docname: draft-turner-cool-problem-00
cat: bcp
pi:
  toc: 'yes'
  comments: 'yes'
  inline: 'yes'
title: CoOL Problem Statement
abbrev: CoOL Problem
area: Internet Area
wg: CoRE
kw: Draft
author:
- role: editor
  ins: R. Turner
  name: Randy Turner
  org: Landis+Gyr
  street: 30000 Mill Creek Ave
  city: Alpharetta
  region: Georgia
  code: '30022'
  country: USA
  phone: 678-258-1292
  email: randy.turner@landisgyr.com

--- abstract

A significant part of the next tens of billion of devices that will be connected to the Internet will be constrained devices, connecting over constrained networks. Managing these devices and the networks they form in a consistent, scalable, extensible, secure, energy-efficient manner with low computational and protocol complexity cannot be done in an ad-hoc manner. This document outlines the problem at hand and provides a roadmap of the possible solutions develped at the IETF. The description includes the basic constrained management problem, as well as properties of the solution. Details as to the Constrained Objecs Language (CoOL) protocol itself can be found in companion documents.

--- middle

# Introduction

The need exists for a unified approach to network management of constrained devices as well as constrained networks. Constrained devices imply the solution should require minimal resources (CPU, memory) from the device platform; constrained networks imply the network management solution should impose minimal traffic on the network to accomplish a particular management objective.

# Problem Statement {#ref_for_later}

The problem of network management for constrained networks and devices includes a number of requirements not necessarily addressed by existing solutions. Any solution must be conservative with "when" network traffic is required, as well as "how much" traffic is required in order to fulfill network management functions. In addition, a solution should support "traditional" network management functions that have been useful in a variety of legacy use-cases, as well as new functionality that address the evolving constrained device and constrained device scenarios. In this context, the term "constrained" implies limited resources (RAM, FLASH), as well as limited CPU resources.  Therefore, the amount of code necessary to achieve network management functionality will need to be as small as possible, as well as the amount of RAM necessary to achieve the functionality will be limited. Likewise, minimal network bandwidth should be required to support a solution.

An ideal solution SHOULD therefore possess the following characteristics:
* Simple and efficient
** Low memory footprint (RAM)
** Low binary footprint (flash)
** Low protocol complexity (simple state machine)
* Scalable
** Thing-to-thing management
** Zero feature negotiation required
* Compact on the air/wire 
* Secure
* Extensible
** Possibility to modify 
* Interoperable

The IETF is coalescing around a set of solutions for transport of applications on constrained networks (CoAP).  Since constrained devices will likely include support for this constrained "stack", it would be advantageous to reuse this constrained device stack for network management as well, to address the constrained device property of limited resources.

Additionally, the IETF is moving towards YANG as a data modeling language for configuration and state data often attributed to network management problems. Therefore, any constrained device/network management solution should attempt to reuse this information when and where possible.

YANG is a data modeling language used to model configuration and state data manipulated by the NETCONF protocol (RFC 6241), NETCONF remote procedure calls, and NETCONF notifications. YANG was originally designed to work with the NETCONF configuration protocol; however, the idea of constrained networks and devices was not a factor in the design of NETCONF/YANG.  Any solution that attempts to use YANG in a constrained environment should consider constrained device and networking properties to the application of YANG in these scenarios.

It would be advantageous to model the particular constrained network management functionality on the evolving NETCONF/RESTCONF operations, since some level of semantic interoperability might be expected by management systems that mix constrained and non-constrained management domains.

One design element that could reduce the amount of traffic "on the wire" is requiring less metadata in management transactions. Instead of endpoints semantically parsing the meaning of the data and/or traffic, the knowledge of the data and how it is expected to be used is, instead, required on the endpoints, a priori.


# Why CoOL?

Currently proposed solutions for constrained management do not specifically address the requirements previously suggested in this memo.  The solution introduced by CoOL seeks to remedy this by introducing an alternative method for operations and encoding "on the wire". CoOL will address these requirements while still utilizing the IETF application "stack" and management data modeling language (YANG). The alternative method employed by CoOL utilizes a more concise representation of management transactions (specifically management "data").

The evolution of the CoOL solution will recognize the proliferation of the "pub/sub" design pattern by relying on extensions both at the CoAP, as well as CoOL protocol layers where needed. Incorporating the pub/sub design pattern will assist in the application of CoOL into larger scale networks (both constrained and non-constrained).

# Roadmap

Within the CORE group, there are currently two threads of development of a management interface for constrained devices and networks. They both converge on the common grounds of using CoAP as fundamental transport protocol. Both solutions bring the YANG modeling language to the world of constrained networks and devices, thus bridging the gap to core network management.

Both solutions address most of the ideal solution characteristics as outlined in the previous section, with the major difference situateed in the runtime--vs--compile time complexity and efficiency. The first approach is based on unmanaged identifiers (YANG hashes), which require zero compile-time efforts in exchange for decreased runtime efficiency. The second approach is based on managed identifiers (SID), which takes the opposite direction, requiring more upfront preparation, aiming at maximal efficiency, deterministic behavior and improved scalability.

Both solutions converge around the YANG data representation expressed in CBOR, as well as the common comprehension of the problem statement. The managed and unmanaged identifier spaces have their specific underlaying function sets. A function set is the specification of CoAP method mapping to NETCONF/RESTCONF functions. 

The following drafts are currently available:

|                   | Managed, Unmanaged                                |
|-------------------+---------------------------------------------------+
| Problem statement | I-D.turner-core-cool-problem-statement            |
| Data presentation | I-D.veillette-core-yang-cbor-mapping              |
| Identifiers       | I-D.somaraju-core-sid, I-D.bierman-core-yang-hash |
| Function set      | I-D.veillette-core-cool, I-D.vanderstok-core-comi |
{: align="left"}

          +----------------------------------------+
          |          Problem statement             |
          | I-D.turner-core-cool-problem-statement |
          +----------------------------------------+
                               |
                               V
          +----------------------------------------+
          |          Data representation           |
          |  I-D.veillette-core-yang-cbor-mapping  |
          +----------------------------------------+
                   |                      |
                   V                      V
+---------------------------+  +----------------------------+
|       Managed IDs         |  |       Unmanaged IDs        |
|   I-D.somaraju-core-sid   |  | I-D.bierman-core-yang-hash |
+---------------------------+  +----------------------------+
                   |                      |
                   V                      V
+---------------------------+  +----------------------------+
|       Function set        |  |       Function set         |
|  I-D.veillette-core-cool  |  |  I-D.vanderstok-core-comi  |
+---------------------------+  +----------------------------+
{: align="left"}


# Security Considerations

The security considerations applicable to network management of enterprise networks is similar but different to that of constrained networks given the potential risk involved.  The risk involved to enterprise networks could be local to an organization (assets, reputation). However, in the case of constrained networks, it is reasonable to assume significant risk due to the types of application domains constrained devices would be applied (sensors controlling everything from home automation to medical devices).  With this risk should come a more strict understanding of the attack vectors and vulnerabilities of any and all protocols in use in constrained networks, especially those protocols tasked with the management of a device. The CoOL working group will attempt to reuse applicable ideas and technology originating from other IETF working groups to address the problem of security. The initial focus of security will involve the integrity and trustworthiness of information originating from CoOL managed endpoints. The confidentiality of this information will also be considered.

--- back
