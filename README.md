# Bootdisk

Bootdisk is a long-term digital-preservation and catalog project for historical software and Norwegian PC culture.

The project preserves source evidence first, keeps provenance explicit, and lets catalog interpretation and publication evolve without rewriting what was originally observed.

> **Ingest observes more than it interprets.**

## What Bootdisk is building

Bootdisk is intended to support material such as:

- magazine cover CDs and DVDs;
- floppy disks and disk images;
- extracted archives and software collections;
- standalone software;
- screenshots, scans and editorial metadata;
- documentation and stories from Norwegian PC and LAN culture.

K-CD from *Komputer for alle* is the first deeply qualified source format, not the Bootdisk data model.

## Architecture

Bootdisk separates four related concerns:

- **Preservation** — What do we have?
- **Provenance** — Where did it come from?
- **Catalog** — What is it?
- **Publication** — What may be exposed, and in what form?

The current top-level repository structure is:

```text
bootdiskhq/bootdisk
    project documentation, governance and cross-repository architecture

bootdiskhq/bootdisk-ingest
    source observation, preservation identities, adapters and extraction

bootdiskhq/bootdisk-catalog
    JSON-first catalog identity, interpretation and relationships

bootdiskhq/bootdisk-publish
    manifest-driven publication, stable objects and derivatives
```

The ingest manifest is the semantic boundary between source understanding and downstream components. `bootdisk-catalog` interprets preserved observations through stable catalog IDs, while `bootdisk-publish` consumes manifest observations and verified preservation extraction bytes without rediscovering source-specific formats from original media.

See [docs/architecture.md](docs/architecture.md) for the project architecture.

## Current state

The project has moved beyond the original documentation-only foundation:

- `bootdisk-ingest` has a tested K-CD ingest pipeline;
- K-CD metadata can be observed through both K.DTX and Director-based paths;
- preservation extraction materializes explicit verified manifest references;
- `bootdisk-catalog` has a JSON-first ID-addressed reference graph implementation;
- `bootdisk-publish` consumes ingest manifests without source-specific parsing;
- original publication objects are stored content-addressably;
- WebP thumbnails can be generated as traceable publication derivatives;
- the end-to-end path from real K-CD media through ingest and publication has been demonstrated.

Catalog enrichment, broad source coverage and the public archive experience remain active future work.

## Project documentation

- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Architecture Decision Records](docs/adr/README.md)

Important project-wide decisions include preservation/provenance/catalog separation, source-adapter boundaries, ADR ownership and the move from the initial monorepo plan to explicit component repositories.

## Repository responsibilities

### `bootdisk`

This repository is the coordination layer for the overall project. It owns project-wide documentation, roadmap, governance and architectural decisions that affect multiple components.

### `bootdisk-ingest`

Ingest understands historical sources. It inventories bytes, calculates identities, records source observations, isolates source-specific interpretation in adapters, and may create verified preservation extractions for explicit manifest references.

### `bootdisk-catalog`

Catalog interprets preserved evidence without replacing it. It owns software and release identity, artifact-to-release identification, occurrence relationships and stable catalog IDs. Authoritative catalog data is JSON-first; indexes and projections are derived.

### `bootdisk-publish`

Publish consumes the ingest contract. It materializes publication objects from verified preserved bytes, creates derivatives according to publication policy, and emits its own publication metadata without reinterpreting original source formats.

## Principles

Bootdisk favors:

- preservation before presentation;
- lossless observation before interpretation;
- explicit provenance;
- traceable architectural decisions;
- small, testable increments;
- source-agnostic core concepts;
- open and sustainable formats where practical;
- preserving unknown and incomplete knowledge rather than inventing certainty.

## Status

Bootdisk is under active development. The current repositories and schemas are still evolving, and no claim is made that the archive or source coverage is complete.
