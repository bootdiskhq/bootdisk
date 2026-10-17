# Bootdisk Roadmap

Bootdisk is a long-term project to preserve, document and make historical software and Norwegian PC culture searchable and accessible.

This roadmap describes the current direction of the project. It is not a fixed promise; phases may overlap and priorities may change as source material and architectural needs become clearer.

## Verified status — 17 October 2026

Public release **1.2.0-rc21** contains **919 source posts across fourteen K-CDs**.
K-CD 7/2001 adds 29 main-menu and 33 workshop posts, plus 29 original RTF documents.
All 857 rc20 entry documents and human review decisions are preserved. The new CD
has no missing explicit launch references or unprocessed DTX metadata; workshop
RTF completeness and executable compatibility remain unverified. Release evidence:
[rc21 validation](https://github.com/bootdiskhq/bootdisk-web/blob/main/docs/1.2.0-rc21-validation.md).

[Web PR 70](https://github.com/bootdiskhq/bootdisk-web/pull/70) makes all readable
original RTF text expandable, including text identical to the menu description.
Original downloads remain separate. Unreadable files get an explanation, not a
fabricated transcription. Freesaver's Symbol-font text is an Ingest follow-up.

**Coverage exceptions remain explicit:** Tools/Knuser.dtx on 12/2001 contains
36 alternate metadata rows not yet qualified against actual menu behavior.
They are preserved but not published or declared redundant. Both 11/2001 and 12/2001 have a
K9 row without a content folder and three missing workshop launch references.
These source rows remain visible; no replacement files or identity claims are
invented. Supplemental workshop RTF coverage is not certified.

Intake attempts on 4/2002, 8/2002 and 16/2002 exposed unindented multiline text.
[Ingest draft PR 24](https://github.com/bootdiskhq/bootdisk-ingest/pull/24) contains
partial nested-menu support, but fails real-media acceptance and is not merged
or used for rc19/rc20. This is a format-level follow-up, not manual curation of each
program. Original source text must not be silently repaired.

13/2001 and 14/2001 were attempted but not published. The former has an unresolved
Firewall workshop destination, unprocessed Quiz/Knuser metadata and a missing
Championship installer. The latter has inconsistent external-cast DRCF/MCsL bounds
and unprocessed Knuser metadata. Preserve these observations and qualify the
formats before adding either CD; do not weaken validation to force publication.

[Further source inspection](director-source-exceptions-2026-10-17.md) identifies
two FireWall labels on 13/2001. On 14/2001, 95 active score references require 46
cast members absent from the supplied Norwegian cast, which is byte-identical
to 13/2001. Both remain unpublished; this is not repaired with another CD's files.

Automatic source documentation is delivered. It does **not** establish executable
compatibility, exact product identity or complete coverage of every possible menu.
The latest intake produced no new machine investigation tasks. Product enrichment
remains optional; missing versions do not create mandatory manual review queues.

The [resumable intake command](intake.md) now coordinates extraction, projection
and local packaging, reuses verified checkpoints and reports per-CD exceptions.
Selecting qualified inputs, resolving format exceptions and publication still require
an operator. A fully unattended intake/deploy service is not delivered.
Next: qualify remaining metadata formats, extend workshop document coverage, and
exercise larger batches before expanding the accepted profile set.

This status and the current focus below supersede older planning labels. Detailed
component plans and release reports remain supporting records, not independent
project-wide priority lists.

## Roadmap status

| Phase | Status | Focus |
| --- | --- | --- |
| Phase 0 | Completed / maintained | Foundation, governance and architectural boundaries |
| Phase 1 | In progress | Preservation ingest and source qualification |
| Phase 2 | In progress | Manifest-driven publication pipeline |
| Phase 3 | Core delivered / enrichment ongoing | Catalog model and identity resolution |
| Phase 4 | Published / evolving | Public archive experience |
| Phase 5 | Planned | Additional sources and preservation workflows |
| Phase 6 | Future | LetoLAN and broader Norwegian PC-history collections |
| Phase 7 | Future | Contributor, OCR and large-scale enrichment workflows |

---

## Phase 0: Foundation and architecture

**Status:** Completed / maintained

The initial foundation established Bootdisk as a documentation-first preservation project and defined the boundaries needed for later implementation.

### Established

- `bootdisk.no`
- GitHub organization `bootdiskhq`
- project-wide ADR process
- preservation / provenance / catalog separation
- source-adapter architecture
- repository ownership rules
- explicit component repositories for project, ingest and publication
- public project roadmap

Architecture remains a maintained concern rather than a permanently finished task.

---

## Phase 1: Preservation ingest and source qualification

**Status:** In progress

The goal of this phase is to observe historical sources reproducibly without making catalog identity a prerequisite for preservation.

### Current capabilities

- deterministic regular-file inventory
- SHA-256 identities
- logical collection identity
- media-image observations and ISO9660 metadata
- K-CD adapter with K.DTX, Tools.dtx and J.DTX calendar parsing
- reusable Director format reader
- K-CD Director adapter when K.DTX is absent
- explicit validation and unresolved/conflicting observations
- reproducible ingest manifests
- verified preservation extraction for explicit manifest references

### Current qualification source

*Komputer for alle* K-CD 15/2001 is the primary real-media regression source for the current ingest path.

### Next goals

- qualify additional available K-CDs using the current repeatable pipeline
- investigate additional menu variants only when a concrete source requires it
- document manifest evolution rules
- add new source adapters only when actual source material establishes their requirements
- keep preservation core behavior independent of publication-specific formats

---

## Phase 2: Manifest-driven publication

**Status:** In progress

The goal of this phase is to turn preserved observations into publication-ready objects without teaching publication tooling how historical source formats work.

### Current capabilities

- ingest manifest validation
- strict binding between manifest observations and preservation extraction bytes
- no fallback to original source media
- content-addressed storage for original publication objects
- stable publication object keys
- WebP thumbnail derivatives
- publication manifest describing originals and derivatives
- end-to-end image publication from real K-CD observations

### Next goals

- broaden derivative support where useful
- define publication policy explicitly, including redistribution constraints
- refine publish-manifest contracts
- support additional presentation assets without weakening provenance
- keep originals, derivatives and publication metadata independently traceable

---

## Phase 3: Catalog model and identity resolution

**Status:** Core delivered; optional identity enrichment continues

The goal of this phase is to answer the question that preservation intentionally does not answer automatically: **what is this?**

### Core concepts

- Software
- SoftwareRelease
- Artifact
- Occurrence
- Source / Collection
- editorial Entry where applicable

### Goals

- establish persistent catalog identities
- associate preserved Artifacts with software releases using evidence
- represent uncertain or incomplete identification
- distinguish observed, derived, interpreted and curated knowledge
- recognize byte-identical Artifacts across different Sources
- avoid making filename, magazine issue or editorial title part of Artifact identity

### Delivered foundations, maintained as the model evolves

- catalog schema
- curation workflow
- identity-resolution guidelines
- provenance-aware matching tools
- ADRs for catalog-specific decisions

---

## Phase 4: Public archive experience

**Status:** Published; further content access planned

The goal of this phase is to expose useful archive material through `bootdisk.no` while preserving the distinction between evidence, catalog interpretation and publication policy.

### Delivered public capabilities

- collection and CD pages, source-post browsing, search and filters
- original menu descriptions, images and linked RTF text/downloads
- public added/changed history and source-status explanations

### Continuing goals

- maintain the project landing page
- browse preserved/cataloged material
- basic search and filtering
- source and occurrence pages
- software and release pages
- thumbnails and other approved derivatives
- visible provenance and checksums where useful
- clear explanation of uncertainty and source evidence

The public site should consume stable publication/catalog contracts rather than parse historical source media directly.

---

## Phase 5: Additional sources and preservation workflows

**Status:** Planned

The goal of this phase is to broaden source coverage without allowing the first source format to define the architecture.

### Candidate source classes

- additional magazine cover CDs and DVDs
- HjemmePC and similar publications
- floppy disks and disk images
- extracted archives
- standalone software
- private software collections
- user-contributed source material

### Goals

- add source adapters when source-specific interpretation is required
- reuse generic hashing, inventory, identity and provenance behavior
- qualify media/filesystem readers independently of source adapters
- preserve source-specific metadata without promoting it into the generic core

---

## Phase 6: LetoLAN and broader Norwegian PC history

**Status:** Future

The goal of this phase is to preserve material that is historically important even when it is not primarily a software-distribution source.

LetoLAN is one of the founding stories behind Bootdisk and is a natural first collection in this direction.

### Goals

- document LetoLAN history, years, locations and organizers
- preserve available video and photographic material
- record posters, technical notes, stories and related artifacts
- model events and collections without forcing them into magazine/software assumptions
- create a public historical collection when rights and source context allow

---

## Phase 7: Contributor and enrichment workflows

**Status:** Future

As collection size grows, manual archival work should be supported by repeatable tools without obscuring provenance.

### Candidate capabilities

- OCR for scans and printed material
- contributor submissions
- moderation and review workflows
- structured import/export
- duplicate and identity assistance
- catalog-curation tools
- public data exports or APIs when the underlying contracts are mature

Automation may propose interpretations, but source observations and curated decisions must remain distinguishable.

---

## Guiding principles

The roadmap follows these principles:

- preserve history before presenting it
- ingest should be lossless where practical
- parser observes more than it interprets
- preservation does not depend on successful catalog identification
- provenance does not define Artifact identity
- publication does not imply redistribution permission
- source-specific formats belong at component edges
- unknown and incomplete information are valid states
- make decisions traceable through ADRs
- prefer small, testable increments over large unfinished rewrites

---

## Current focus

1. **Qualify observed format exceptions, then consolidate intake.** Resolve the
   2002 multiline text with preserved raw evidence and matching Catalog validation;
   verify nested Tools paths and all original regression media. Determine the role
   of Knuser.dtx before claiming complete coverage of 12/2001. Do not turn these
   format investigations into per-program manual approvals. Also qualify the new
   13/2001 workshop destination and 14/2001 external-cast boundary variants.

   **Repeatable intake: first coordinator delivered.** The [command](intake.md)
   resumes verified checkpoints and reports each CD separately. Real-media tests
   cover main/workshop menus, images, RTFs, interrupted runs and blocked batches.
   Expand qualification to larger batches and the unresolved source variants;
   this does not certify complete-disc or workshop-RTF coverage.
2. **Keep documentation aligned with each release.** Update this roadmap and link
   component ADRs when behavior changes; retain release evidence and distinguish
   source documentation from optional product identification.
3. **Courses and original attachments.** Pilot one source-bound PDF course with
   file type, size, provenance and an explicit publication decision. Define the
   attachment contract before general rollout. The Videoskolen PDF on 3/2002 is a
   candidate; rc18 publishes its description/RTF, not the PDF itself.

## Planned milestones beyond the current intake work

### CD covers

Use available scanned PDF covers first. Verify issue/year visually, show a cover
on the CD page and retain the original scan. Record missing scans for a separate
completion milestone; a complete scan collection is not a prerequisite.

### RTF coverage and wording

RTF publication is delivered, but exhaustive coverage across all source formats
and clearer wording remain work to qualify. Distinguish linked/readable, identical
to menu text, unreadable, investigated without a match, and not yet investigated.
Never equate an absent reading panel with proof that no RTF exists on the CD.

### Video courses

Wait for a disc containing actual video lessons. Preserve original media and
source bindings independently of any YouTube copy. Before a pilot, resolve rights,
channel and visibility; define lesson ordering and a click-to-load embedded player.
A PDF about video editing does not qualify as a video lesson. No upload is authorized
by this roadmap entry alone.

### Try historical software in the browser

**Status: future exploratory pilot, requested 16 October 2026. No implementation
or emulator choice has been approved. No delivery date or mandatory place ahead
of intake, courses or covers is assigned.**

Goal: a source post can eventually offer “Prøv i nettleseren”, opening a disposable
emulated session while preserving the original artifact unchanged.

Start with one small, well-understood program. Select the candidate and verify
current emulator capabilities at that time; do not assume the Windows programs on
our CDs work in a browser. Record an ADR before implementation covering:

- emulator/runtime choice and hosting ownership across Catalog, Publish and Web;
- permitted redistribution of the program, OS/runtime images and dependencies;
- an isolated temporary session, no guest network or host-file access by default;
- immutable source objects and separate disposable session writes;
- a launch profile bound to exact source hashes, with OS, dependencies and settings;
- compatibility evidence, supported devices, startup/download budgets and clear
  failure states; known 3D/driver limitations must remain visible;
- disabling the feature independently of the public catalog and source preservation.

Pilot acceptance: one permitted program starts and responds on explicitly tested
browsers/devices; reset restores a clean session; isolation and source integrity
are verified; failures leave the catalog usable; a reproducible launch recipe and
limitations are documented. Expand only after the pilot is evaluated. A launch
profile must not turn an unverified catalog identity into a confirmed one.

### Deferred exploration

Do not spend broadly on AI enrichment or old menu formats without a concrete
need. Investigate actual intake exceptions and preserve unknowns. Broader sources,
LetoLAN and contributor workflows remain in phases 5–7 above.
