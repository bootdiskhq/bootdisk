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
