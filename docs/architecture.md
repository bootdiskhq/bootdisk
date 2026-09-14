# Bootdisk Architecture

Bootdisk is a digital-preservation and catalog project for historical software and related Norwegian PC history. The architecture is designed to preserve evidence first, keep provenance explicit, and allow catalog interpretation and publication to evolve without rewriting original observations.

The project principle is:

> **Ingest observes more than it interprets.**

## Project domains

Bootdisk separates three core questions:

- **Preservation:** What do we have?
- **Provenance:** Where did it come from?
- **Catalog:** What is it?

Publication is a separate downstream capability: what preserved and described material should be exposed, and in what form?

The same byte-identical Artifact can occur in several Sources without becoming several different Artifacts. Catalog interpretation may improve later without changing the preserved evidence.

## Repository architecture

Bootdisk currently uses four top-level repositories with explicit responsibilities:

```text
bootdiskhq/bootdisk
        |
        +-- project governance
        +-- cross-repository architecture
        +-- ADR registry
        +-- roadmap and project documentation

bootdiskhq/bootdisk-ingest
        |
        +-- source inventory and hashing
        +-- media and filesystem observations
        +-- source adapters such as K-CD
        +-- reusable format readers such as Director
        +-- ingest manifest
        +-- preservation extraction

bootdiskhq/bootdisk-catalog
        |
        +-- JSON-first authoritative catalog records
        +-- stable catalog IDs and relationships
        +-- software and release identity
        +-- artifact-to-release identification
        +-- occurrence relationships
        +-- derived in-memory indexes and projections

bootdiskhq/bootdisk-publish
        |
        +-- consume ingest manifests
        +-- bind observations to preserved bytes
        +-- content-addressed publication store
        +-- derivatives such as thumbnails
        +-- publish manifest
```

Repository boundaries follow architectural responsibility and independent lifecycle, as defined by ADR-0007. They are not intended to create a repository for every small tool.

## Data flow

The current preservation-to-catalog/publication flow is:

```text
historical source / image
          |
          v
   bootdisk-ingest
          |
          +----------------------+----------------------+
          |                      |                      |
          v                      v                      v
   ingest manifest       preservation extraction   observed evidence
          |                      |                      |
          |                      |                      v
          |                      |              bootdisk-catalog
          |                      |                      |
          |                      |              catalog identities
          |                      |              and relationships
          |                      |
          +----------+-----------+
                     |
                     v
              bootdisk-publish
                     |
             +-------+-------+
             |               |
             v               v
       original objects   derivatives
             |               |
             +-------+-------+
                     |
                     v
              publish manifest
```

`bootdisk-catalog` is deliberately source-format agnostic. It consumes preserved evidence and expresses interpretation through stable IDs; it must not reinterpret K.DTX, Director structures or other source formats directly.

`bootdisk-publish` is also deliberately source-format agnostic. It should not parse `K.DTX`, Director movies or future source formats to rediscover what ingest observed. The ingest manifest is the semantic contract, and preservation extraction supplies verified bytes for explicitly preserved references.

If a publication-required observation cannot be resolved to preserved bytes with matching identity, the contract fails explicitly. Publish must not silently reopen original media as a fallback.

## Preservation and catalog model

The central conceptual entities are:

```text
Source / Collection
        |
        v
    Occurrence --------------------+
        |                           |
        v                           v
     Artifact                SoftwareRelease
                                  |
                                  v
                               Software
```

`Media`, editorial `Entry` and publication-specific structures provide context where they exist, but they are not prerequisites for an Artifact.

Artifact identity should be based on byte identity where appropriate, normally SHA-256, rather than filename, magazine issue, path or editorial title.

Catalog relationships are expressed with stable IDs rather than JSON filenames or directory paths. Authoritative catalog JSON may be reorganized physically without changing the semantic graph. Reverse indexes and frontend/search projections are derived rather than duplicated into the authoritative records.

Unknown and incomplete relationships are valid states.

## Evidence classes

Bootdisk distinguishes different kinds of knowledge:

- **Observed:** directly present on or in source material.
- **Derived:** deterministically calculated from observations, such as hashes.
- **Interpreted:** inferred from available evidence.
- **Curated:** explicitly reviewed or confirmed catalog information.

Interpretation must not overwrite original evidence.

## Source and format boundaries

Source-specific meaning belongs in source adapters. Generic preservation operations belong in the ingest core.

For example:

```text
K.DTX -----------------> K-CD adapter ----+
Director structures --> K-CD adapter ----+----> ingest observations
                          ^
                          |
                  generic Director
                    format reader
```

A format reader describes reusable structural facts about a format. A source adapter decides what those facts mean for a particular historical source. A medium or filesystem format is not the same thing as a publication or source.

The architecture therefore avoids assuming:

```text
source == publication == medium == filesystem
```

## Publication policy

Preservation and publication are not equivalent.

The fact that bytes were observed, hashed or preserved does not itself establish permission to redistribute them. Publication policy must decide what may be exposed and which derivatives may be generated or served.

Original preserved bytes, generated derivatives and publication metadata remain distinguishable and traceable.

## Responsibility chain

The intended responsibility chain is:

> **Ingest tells Catalog what we found. Catalog tells the Frontend what it is. Publish tells the Frontend what it may expose.**

The frontend should therefore consume catalog identity and publication outputs rather than source-format-specific ingest structures.

## Decision ownership

Project-wide and cross-repository architecture is documented in `bootdisk/docs/adr`. Component-local decisions live beside the component they govern. The central ADR index links important component decisions without copying their accepted text.

See [the ADR index](adr/README.md) for current decisions and ownership.
