# Architecture Decision Records

This directory contains the authoritative project-wide and cross-repository
architectural decisions for Bootdisk.

ADRs are numbered sequentially **within this repository** and are not renumbered
after acceptance. Component repositories may maintain their own ADR sequences for
component-local decisions. The repository therefore forms part of an ADR's
identity; for example, `bootdisk ADR-0006` and `bootdisk-ingest ADR-0006` are
separate records.

The ownership rule is defined by
[ADR-0006: ADR ownership follows architectural scope](0006-adr-ownership-across-repositories.md):

- project-wide and cross-repository decisions are authoritative here;
- component-local decisions are authoritative beside the component they govern;
- an ADR has one authoritative copy;
- other repositories should link rather than duplicate accepted decision text.

## Project ADRs

| ADR | Decision | Scope |
| --- | --- | --- |
| [0001](0001-documentation-first.md) | Documentation first | Project |
| [0002](0002-monorepo.md) | Monorepo — superseded by ADR-0007 | Historical repository structure |
| [0003](0003-github-as-source-of-truth.md) | GitHub as source of truth | Project |
| [0004](0004-separate-preservation.md) | Separate preservation, provenance and catalog domains | Project domain model |
| [0005](0005-Source-adapters-isolate-source-specific-parsing-from-the-preservation-core.md) | Source adapters isolate source-specific parsing | Project ingest boundary |
| [0006](0006-adr-ownership-across-repositories.md) | ADR ownership follows architectural scope | Project governance |
| [0007](0007-multi-repository-component-boundaries.md) | Use component repositories with explicit architectural boundaries | Project / repository structure |
| [0008](0008-catalog-interprets-preserved-observations.md) | Catalog interprets preserved observations without replacing them | Project catalog boundary |
| [0009](0009-json-first-catalog-storage.md) | Use JSON as the authoritative catalog storage format | Project catalog persistence |

## Component ADR registry

The records below are authoritative in their component repositories and are linked
here only to make important architectural boundaries discoverable from the project
repository.

### bootdisk-ingest

- [ADR-0006: Preserve metadata evidence and write observations safely](https://github.com/bootdiskhq/bootdisk-ingest/blob/main/docs/adr/ADR-0006-evidence-and-publication.md)
- [ADR-0007: Director structure is a format layer, not a source adapter](https://github.com/bootdiskhq/bootdisk-ingest/blob/main/docs/adr/ADR-0007-director-format-observations.md)
- [ADR-0008: Manifest is the contract for publication](https://github.com/bootdiskhq/bootdisk-ingest/blob/main/docs/adr/ADR-0008-manifest-publication-contract.md)

ADR-0008 currently records a cross-repository contract discovered during ingest
work. Its accepted record remains valid. Under ADR-0006, future changes to that
cross-repository contract should be captured by a project-level ADR here, with
component documentation linking to it.

## Catalog ADR registry (reviewed 16 October 2026)

- [ADR 001: Curated descriptions are catalog knowledge](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-001-curated-descriptions.md)
- [ADR 002: Public metadata is versioned in Git](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-002-public-metadata-in-git.md)
- [ADR-003: Identify source-entry packages separately from files](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-003-source-entry-packages.md)
- [ADR-004: Local curator with a Catalog-owned write boundary](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-004-local-curator-boundary.md)
- [ADR-005: Drafts, explicit decisions and append-only review history](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-005-review-state-and-decisions.md)
- [ADR-006: gate hosted curation on approved-user access](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-006-hosted-curator-access.md)
- [ADR-007: Receive unidentified Director candidates outside the review workspace](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-007-candidate-intake.md)
- [ADR-008: Keep first-pass suggestions outside authoritative decisions](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-008-automatic-first-pass.md)
- [ADR-009: Automatic source-attributed identification](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-009-machine-source-identification.md)
- [ADR-010: Machine decisions backed by decoded program metadata](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-010-machine-payload-identification.md)
- [ADR 011: Katalogfør kilden uavhengig av programidentitet](https://github.com/bootdiskhq/bootdisk-catalog/blob/main/docs/adr-011-source-catalog-readiness.md)

These are existing component-owned records; this index does not change their
status or transfer ownership. In particular, ADR 011 separates source catalog
readiness from optional product identification. Its initial acceptance figures
are historical; current release counts belong in the roadmap and release reports.

## Decisions still to make

Browser execution is a roadmap proposal, not an accepted architecture decision.
Create a project-level ADR before implementation because runtime isolation,
launch-profile provenance and public hosting cross component boundaries. Likewise,
the generic course/attachment contract needs an explicit decision before rollout.
