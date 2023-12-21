Once draft-ietf-core-sid is published as an RFC there will be a process for new YANG modules that need SID allocations.

There will be an interval when the ~100 published YANG modules that don't have SID files.

This document just documents among the IESG, RFC Editor and IANA, and "SID designated  experts" what the process should be.

One conclusion may be do nothing and create the SID files reactively (as currently proposed in the draft).
An alternative conclusion may be to have a designated expert create all the SID files and ask IANA to add them to the registry.

This document concludes that the Designated Experts will create a list of dependencies and then work through the needed SID allocations in a bottom-up, or depth-first manner.
The list of files/modules to be processed will be appended to this file.

This is likely to take a number of months for a few reasons:

* number of cycles of designated expert time will be limited.
* round trips to IANA to get ranges allocated
* discovery of bugs in pyang (or other tools) while processing modules

During this process, a WG that has a document with unresolved SID dependancies may petition the Designated Experts to reprioritize which part of the dependancy tree they are working on.




