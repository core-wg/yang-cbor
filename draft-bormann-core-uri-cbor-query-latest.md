---
docname: draft-bormann-core-uri-cbor-query-latest
stand_alone: true
ipr: trust200902
cat: std
pi:
  toc: 'yes'
  symrefs: 'yes'
  sortrefs: 'yes'
  compact: 'yes'
  subcompact: 'no'
  rfcedstyle: 'yes'
title: >
  Uri-CBOR-Query: A stopgap for working around the lack of FETCH
abbrev: Uri-CBOR-Query
area: General
#wg: Applications Area Working Group
#kw: CoAP
date: 2016-02-17
author:
- ins: C. Bormann
  name: Carsten Bormann
  org: Universitaet Bremen TZI
  street: Postfach 330440
  city: Bremen
  code: D-28359
  country: Germany
  phone: +49-421-218-63921
  email: cabo@tzi.org
normative:
  RFC4648:
  RFC7049:
  RFC7252:
informative:
#  RFC5789:
  RFC7396:
#  RFC7159:

--- abstract

draft-bormann-core-coap-fetch and draft-vanderstok-core-patch define
two (or three) new methods for CoAP that allow read and update
requests with more control than the traditional four CRUD requests.

There is some concern that the FETCH and PATCH operations may not be
ready in time.  In the interest of exploring alternatives, this draft
examines a new CoAP Option, Uri-CBOR-Query.
This option enables the transfer of information similar to a FETCH
request payload with a GET request, and similar to part of the PATCH
request payload with POST, PUT, and/or DELETE.

--- middle

# Introduction {#intro}

(See Abstract for now.)

# The Uri-CBOR-Query Option

The Uri-CBOR-Query Option is an Option analogous to the Uri-Query
Option, with the exception that its value is opaque and not string.
The value is intended to carry a single CBOR data item --
*discussion*: maybe a sequence of these so we can leave off any outer
array markers.


| No. | C | U | N | R | Name           | Format | Length | Default |
|  19 | x | x | - | x | Uri-CBOR-Query | opaque |  0-255 | (none)  |


# HTTP compatibility

Where the Options of a CoAP request need to be translated into a URI
(see Section 6.5 of {{RFC7252}}), e.g. where a request with a
Uri-CBOR-Query Option needs to be translated to an HTTP request, the
Option value is translated to a text string as defined below and
treated like a Uri-Query Option that has this text string as its
Option value and is appended after all other Uri-Query Options.

The specific way the translation is performed is up for *discussion*; as
a strawman: the two characters "??" followed by the base64url encoding
(Section 3.2 of {{RFC4648}}) of the CoAP Option value:

~~~
CoAP:
  Uri-Path: c
  Uri-CBOR-Query: [1, 2, 3]

HTTP:
  /c???gwECAw
~~~

<!-- [[1, 2, 3].to_cbor].pack("m") -->

The two question marks are added as a marker that might also enable the
inverse translation from HTTP to the CoAP Option, assuming that other
uses of this marker are infrequent. (The use of question mark
characters in URI query parts traditionally has been risky and
therefore is not current practice.)

# Usage Guidelines

To emulate a FETCH, what would be the FETCH payload is instead encoded
in a Uri-CBOR-Query Option.
The FETCH payload is assumed to of Content-Format application/cbor, which is not
as specific as it could be -- *discussion*: Should we send along a
Content-Format within the Uri-CBOR-Query???.

To emulate an iPATCH, a POST operation with the same parameters as an
iPATCH is performed; there fundamentally is no need for
Uri-CBOR-Query, except maybe to distinguish the emulated iPATCH from a
real POST operation.
However, an iPATCH that is just a sequence of in-tree deletes can be
mapped to a DELETE operation with a Uri-CBOR-Query Option that
indicates which parts of the tree need to be deleted.
Similarly, an iPATCH that puts new values to several places in the
tree (as in a merge-patch {{RFC7396}}) can be mapped to a PUT with a
Uri-CBOR-Query Option that indicates those places and a payload that is a
CBOR representation of an array of the values for these places.

# Acknowledgements

The idea for this draft was created in discussions with
Alexander Pelov,
Laurent Toutain,
Michel Veillette,
Randy Turner, and
Somaraju Abhinav.
