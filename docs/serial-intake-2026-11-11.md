# Serial intake qualification — 11 November 2026

Inventory across Kjøpt and Original found 79 image files / 77 byte-unique images:
33 published issues, 40 unpublished regular K-CD issues, 3 special discs and one
unrelated Windows-magazine disc. Equal-size candidates were fully SHA-256 hashed;
published issue matching was by filename/directory label, not fresh historical
image fingerprint verification. The full inventory is local-results/disc-inventory-2026-11-11.

37 remaining ordinary discs use HTML/cdindex (2013–2015); three use DTX
(13/2001, 14/2001, 4/2002). A family match is not a complete qualification.
The first six-disc qualification uses those three DTX issues and 1/2013, 1/2014,
1/2015. The 14/2001 image also contains KNUSER.DTX; coverage gates must decide
whether it is supported. No silent omission is acceptable.

The coordinator now supports an explicit bsdtar driver with one temporary source
at a time. This avoids accumulating roughly 25 GB of extracted program payloads
on a Mac with approximately 5.5 GiB free. Original images and published rc25 are
preserved. Component results still consume disk and must remain for traceability.

Synthetic verification: 21 tests passed, including successful disposal, disposal
on pipeline failure, traversal rejection, absolute path rejection, symlink
rejection, existing checkpoint resumption and blocked-member continuation.
The existing macOS path test now compares the resolved expected path, matching
production normalization (/var is a symlink to /private/var).

Real qualification results are recorded separately when the run finishes. This
note does not claim success for any of the six images or authorize publication.
