# ADR-0009: Use JSON as the authoritative catalog storage format

## Status

Accepted

## Date

2026-09-14

## Context

ADR-0008 establishes Catalog as the semantic interpretation layer above
preservation and provenance. The next implementation question is how catalog data
should be stored.

A traditional relational database could represent software, releases, artifacts,
occurrences and evidence. It would also introduce operational state, migrations,
backup/restore concerns and another persistence technology before Bootdisk has a
proven need for them.

Bootdisk already relies heavily on explicit, versioned JSON contracts. Ingest
produces manifests, Publish consumes manifests and produces its own manifest, and
the project values reproducibility, inspectability and long-term preservation over
premature infrastructure complexity.

The initial catalog is expected to be curated and relatively small. Human review,
clear history and deterministic representation matter more at this stage than
high-volume transactional writes.

## Decision

Bootdisk Catalog will use **JSON as its authoritative storage format initially**.

Catalog records will be stored as normal files under version control or equivalent
preserved storage, with explicit schema/version identifiers and stable object IDs.

A database is not required for the first catalog implementation.

This decision does **not** prohibit databases later. If search volume, concurrent
editing, operational workflows or performance eventually justify one, a database
may be introduced as:

1. a derived index built from authoritative JSON; or
2. a new authoritative persistence layer through a future ADR and explicit
   migration plan.

Until such a decision is made, JSON remains the source of truth for catalog data.

## Why JSON

JSON fits Bootdisk's current priorities:

- human-readable and inspectable;
- easy to diff and review in Git;
- trivial to archive and copy;
- language- and framework-neutral;
- consistent with existing ingest and publish contracts;
- easy to validate with JSON Schema or application-level validation;
- no database server, migration framework or runtime service required;
- suitable for deterministic builds of search indexes and frontend projections;
- preserves a clear historical record of curation changes.

## Storage shape

This ADR does not require one giant catalog file.

The preferred direction is **small records with stable identities**, for example:

```text
catalog/
    software/
        winamp.json
    releases/
        winamp-2.76.json
    artifacts/
        sha256-abc123.json
    occurrences/
        occurrence-kcd15-2001-0018.json
    identifications/
        identification-abc123-winamp-2.76.json
```

Exact filenames and directory layout may evolve, but object identity must not depend
on filenames alone.

## Stable identifiers

Catalog objects need explicit IDs because paths and human-readable names may change.

Examples:

```text
software:winamp
release:winamp:2.76
artifact:sha256:<digest>
occurrence:<stable-id>
identification:<stable-id>
```

The final identifier syntax may be refined by the minimal catalog model, but IDs
must be stable, unique within their namespace and independent of display labels.

## References instead of duplication

Catalog JSON should prefer references between canonical records rather than copying
whole objects into each other.

For example, a release record may reference:

```json
{
  "software_id": "software:winamp"
}
```

rather than embedding a complete copy of the Software record.

This keeps records small and prevents divergent duplicated metadata.

## Validation

Catalog JSON MUST be validated before it is accepted as authoritative catalog data.

Validation should cover at least:

- supported schema version;
- required IDs and object type;
- valid references where resolvable;
- immutable artifact content identity semantics;
- allowed knowledge/status values;
- evidence structure for interpreted identifications.

JSON Schema may be used for structural validation, but domain validation may remain
application code where cross-record rules are required.

## Derived indexes are disposable

Search indexes, SQLite databases, static site projections, caches and similar
structures may be generated from the JSON catalog.

Such derived state must be reproducible and replaceable. It is not authoritative
unless a future ADR explicitly changes the persistence model.

Conceptually:

```text
Authoritative catalog JSON
          |
          +--> validation
          |
          +--> search index
          |
          +--> SQLite cache
          |
          +--> frontend/API projection
```

Deleting and rebuilding a derived index must not lose catalog knowledge.

## Consequences

### Positive

- Very low operational complexity.
- Catalog history is naturally reviewable in Git.
- No database service is required to preserve or edit the catalog.
- Backups are ordinary file backups.
- Data remains portable across future implementations.
- Static-site and offline workflows remain possible.
- The project can learn its real query patterns before choosing database technology.

### Negative

- Cross-record queries require loading/indexing files or building a derived index.
- Concurrent multi-user editing is less convenient than transactional database
  writes.
- Referential integrity is not automatically enforced by a database engine.
- Large-scale catalog growth may eventually require generated indexes for
  acceptable performance.

These costs are accepted because Bootdisk currently values simplicity,
inspectability and preservation more highly than database-backed operational
features.

## Alternatives Considered

### Relational database as the initial source of truth

Rejected for now because the catalog is not yet large enough to justify the added
operational and migration complexity.

### One monolithic `catalog.json`

Rejected as the preferred design because large files create noisy diffs and make
independent curation harder. Multiple small JSON records remain easier to review
and evolve.

### YAML

Not selected because JSON already forms the project's machine contracts and has
stronger interoperability with validation and generated tooling. Human readability
is sufficient for the intended records.

## Follow-up

Define the minimal catalog record model and example JSON for Software,
SoftwareRelease, Artifact, Occurrence and evidence-bearing identification.
