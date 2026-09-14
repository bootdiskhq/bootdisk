# Bootdisk Roadmap

Bootdisk is a long-term project to preserve, document and make historical software and Norwegian PC culture searchable and accessible.

This roadmap describes the current direction of the project. It is not a fixed promise; phases may overlap and priorities may change as source material and architectural needs become clearer.

## Roadmap status

| Phase | Status | Focus |
| --- | --- | --- |
| Phase 0 | Completed / maintained | Foundation, governance and architectural boundaries |
| Phase 1 | In progress | Preservation ingest and source qualification |
| Phase 2 | In progress | Manifest-driven publication pipeline |
| Phase 3 | Planned | Catalog model and identity resolution |
| Phase 4 | Planned | Public archive experience |
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
- K-CD adapter with K.DTX parsing
- reusable Director format reader
- K-CD Director adapter when K.DTX is absent
- explicit validation and unresolved/conflicting observations
- reproducible ingest manifests
- verified preservation extraction for explicit manifest references

### Current qualification source

*Komputer for alle* K-CD 15/2001 is the primary real-media regression source for the current ingest path.

### Next goals

- stabilize the current release candidate
- continue qualifying older Director-based K-CD variants
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

**Status:** Planned

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

### Possible deliverables

- catalog schema
- curation workflow
- identity-resolution guidelines
- provenance-aware matching tools
- ADRs for catalog-specific decisions

---

## Phase 4: Public archive experience

**Status:** Planned

The goal of this phase is to expose useful archive material through `bootdisk.no` while preserving the distinction between evidence, catalog interpretation and publication policy.

### Goals

- project landing page
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

The current focus is:

1. finish documentation and contract cleanup around the existing ingest/publish architecture;
2. stabilize preservation ingest and publication boundaries;
3. continue real-media qualification;
4. define the catalog layer that can build on preserved Artifacts and Occurrences;
5. prepare the first public archive experience on top of those stable contracts.
