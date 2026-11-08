# HTML-disc intake

The coordinator accepts `profile: "html"` and requires the observed manifest to
be `kcd-html-1`; a DTX/HTML mismatch stops. Existing DTX/workshop behavior remains.
A source_root may additionally specify `image` as independent original-image
evidence. Both inputs are fingerprinted before and after the run, and Ingest gets
`--image`. This does not by itself certify directory/image equivalence.

For 2012 images use a fresh directory extracted with the system bsdtar, then the
normal resumable intake command. Do not use 7-Zip autodetection for these images:
it opens an embedded archive. All extraction and pipeline commands are static;
no vintage software is executed. Future automatic archive-driver selection is
not implemented by this profile.

The profile projects indexed software, article and video menu posts with images.
It does not upload PDF courses/video files, reinterpret distribution/version as
verified product identity, or change the human review workspace. Existing public
posts are copied byte-for-byte; public update history is added at release time.
