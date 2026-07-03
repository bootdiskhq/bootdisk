# Bootdisk Roadmap

Bootdisk is a long-term project to preserve, document and make Norwegian PC history searchable and accessible.

This roadmap describes the current direction of the project. It is not a fixed promise, but a living document that will evolve as the project grows.

## Roadmap Status

| Phase | Status | Focus |
| --- | --- | --- |
| Phase 0 | In progress | Foundation, documentation and project structure |
| Phase 1 | Planned | Public landing page and basic project identity |
| Phase 2 | Planned | Core archive model and searchable metadata |
| Phase 3 | Planned | Software and cover CD catalog |
| Phase 4 | Planned | LetoLAN archive |
| Phase 5 | Future | OCR, import tools and contributor workflows |

---

## Phase 0: Foundation

**Status:** In progress

The goal of this phase is to establish a solid foundation before implementation begins.

### Goals

- Register and configure the domain
- Establish the GitHub organization
- Create the main repository
- Define project principles
- Write the project manifesto
- Create the first ADRs
- Agree on repository structure
- Define the initial roadmap
- Start documenting the domain model

### Deliverables

- `bootdisk.no`
- GitHub organization: `bootdiskhq`
- Main repository: `bootdisk`
- Documentation-first project structure
- Initial Architecture Decision Records
- Public roadmap
- Project manifesto

---

## Phase 1: Public Presence

**Status:** Planned

The goal of this phase is to create the first public-facing version of Bootdisk.

This does not need to be a full product. It should clearly explain what Bootdisk is, why it exists and what we are building.

### Goals

- Create a simple landing page
- Explain the project vision
- Publish the roadmap
- Publish the manifesto
- Set up basic deployment
- Connect `bootdisk.no`
- Establish visual direction and tone

### Possible Deliverables

- Public website
- About page
- Manifesto page
- Roadmap page
- Development log
- Basic design language

---

## Phase 2: Core Archive Model

**Status:** Planned

The goal of this phase is to define the core information model for the archive.

Bootdisk should not only store files. It should describe relationships between software, magazines, cover CDs, hardware, events and stories.

### Goals

- Define the first domain model
- Identify core entities
- Define metadata fields
- Define relationships between entities
- Decide how archival objects should be identified
- Decide how sources and uncertainty should be documented

### Candidate Entities

- Software
- Software version
- Magazine
- Magazine issue
- Cover CD
- File
- Screenshot
- Hardware
- Event
- LAN party
- Person or contributor
- Organization
- Source
- Story

### Possible Deliverables

- Domain model documentation
- Initial data model
- Metadata guidelines
- Source and citation guidelines
- ADRs for data and archive structure

---

## Phase 3: Software and Cover CD Catalog

**Status:** Planned

The goal of this phase is to create the first useful archive experience.

A visitor should be able to browse and search early Bootdisk content.

### Goals

- Add initial software entries
- Add initial magazine and cover CD entries
- Support basic search
- Support basic filtering
- Document file origins and metadata
- Add checksums where relevant
- Add screenshots or scans where available

### Possible Deliverables

- Browse software
- Browse cover CDs
- Browse magazine issues
- Basic search
- Entry pages for software
- Entry pages for cover CDs
- Initial metadata import workflow

---

## Phase 4: LetoLAN Archive

**Status:** Planned

The goal of this phase is to preserve and publish the history of LetoLAN as part of Norwegian LAN culture.

LetoLAN is one of the founding stories behind Bootdisk.

### Goals

- Document the history of LetoLAN
- Identify years, locations and organizers
- Digitize and publish available material
- Prepare and preserve existing video material
- Add photos, posters, stories and other artifacts if available
- Create a public LetoLAN archive page

### Possible Deliverables

- LetoLAN history page
- Timeline
- Video archive
- Photo gallery
- Organizer notes
- Technical setup notes
- Stories from participants

---

## Phase 5: Tools, Import and Preservation Workflows

**Status:** Future

The goal of this phase is to make Bootdisk scalable as an archive project.

As the amount of material grows, manual work should be supported by tools and repeatable workflows.

### Goals

- Build import tools
- Scan ISO and CD contents
- Generate file inventories
- Extract metadata where possible
- Support OCR for scanned material
- Support contributor submissions
- Support moderation and review workflows
- Export structured archive data

### Possible Deliverables

- ISO scanner
- Metadata importer
- OCR pipeline
- Contributor guide
- Submission workflow
- Admin/review interface
- Public data export

---

## Guiding Principles

The roadmap should follow the project principles:

- Documentation first
- Simplicity before complexity
- Open standards where possible
- Preserve history before presenting it
- Make decisions traceable
- Build for long-term sustainability
- Prefer small, useful iterations over large unfinished plans

---

## Not Yet Prioritized

These ideas are valuable, but are not part of the immediate roadmap.

- Public API
- Advanced full-text search
- User accounts
- Comments and community features
- Emulation in browser
- Interactive timelines
- AI-assisted tagging
- Large-scale OCR
- Hardware database
- Norwegian LAN party directory
- Public contribution portal

---

## Current Focus

The current focus is:

1. Establish the project foundation
2. Write the manifesto
3. Document core architectural decisions
4. Define the first archive/domain model
5. Prepare for the first public landing page
