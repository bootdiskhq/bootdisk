# ADR-0008: Catalog interprets preserved observations without replacing them

## Status

Accepted

## Date

2026-09-14

## Context

Bootdisk separates preservation, provenance and catalog concerns. The ingest and
publication components now make that separation operational:

- `bootdisk-ingest` observes source material and writes manifests;
- preservation extraction materializes explicitly observed bytes while preserving
  their manifest identity;
- provenance records where observations and artifacts came from;
- `bootdisk-publish` consumes manifest-backed preserved material and applies
  publication concerns without rediscovering the original source format.

The remaining domain question is how Bootdisk represents what preserved material
*is*.

An ingest observation may say that a K-CD entry is titled `WinAmp 2.76`, that a
file has a particular path and SHA-256, and that the file occurred on a particular
source. Those are valuable observations, but they do not by themselves establish
that the bytes are definitively a particular software release.

Bootdisk therefore needs a catalog layer that can interpret evidence, relate the
same artifact across many sources, and support later correction without rewriting
preservation history.

The future public archive and frontend also need a stable domain model. They should
not need to understand K.DTX, Director structures, source-specific encodings,
ingest parser details or preservation filesystem layouts merely to present a piece
of software and the sources on which it was found.

## Decision

Bootdisk will maintain a distinct **catalog domain** above preservation and
provenance.

The catalog answers questions such as:

- What software product is this?
- Which release or version does an artifact represent?
- On which sources has the artifact occurred?
- Which editorial entries refer to that software or artifact?
- What evidence supports an identification?
- Is an identification tentative, interpreted or human-curated?

Catalog interpretation MUST NOT replace, normalize away or rewrite preserved
observations. A corrected catalog identification changes the interpretation, not
the historical ingest evidence or artifact identity.

### Core catalog concepts

The initial conceptual model is:

```text
Software
   |
   +-- SoftwareRelease
           |
           +-- Artifact
                   |
                   +-- Occurrence
                           |
                           +-- Source / Entry
```

The concepts have distinct meanings:

- **Software** is the conceptual product, for example `Winamp`.
- **SoftwareRelease** is a particular version, edition or release of that product,
  for example `Winamp 2.76`.
- **Artifact** identifies exact preserved digital content. Content hashes are the
  primary basis for recognizing identical bytes independently of filenames or
  source media.
- **Occurrence** records that an artifact occurred in a particular source context.
  The same artifact may therefore have many occurrences without becoming many
  artifacts.
- **Entry** represents a source/editorial item when such an item exists. Artifacts
  do not require an editorial entry in order to exist in the catalog.
- **Source** represents the provenance context in which an occurrence was
  observed.

These are domain concepts. Their eventual database representation is deliberately
not decided by this ADR.

### Artifact-to-release identification is evidence-bearing

A relationship between an Artifact and a SoftwareRelease is an interpretation,
not an ingest fact merely because a filename, label or source entry resembles a
version string.

The catalog must therefore be able to represent identification separately from the
objects being identified. A future representation may include fields such as:

```text
artifact
software_release
status
confidence
evidence
```

The exact schema is deferred, but the model MUST support retaining the evidence
behind an identification and MUST allow that identification to be corrected
without changing the preserved Artifact or its Occurrences.

### Knowledge kind remains explicit

Catalog data should preserve the distinction between different kinds of knowledge:

- **observed** — recorded directly from a source or ingest observation;
- **derived** — mechanically calculated from observations, such as a hash;
- **interpreted** — a conclusion drawn from evidence, such as mapping an artifact
  to a software release;
- **curated** — an interpretation reviewed or supplied through human curation.

A future implementation may refine statuses or confidence representation, but it
must not collapse observation and interpretation into the same claim.

### Catalog is the semantic basis for the public archive

The public archive, search experience and future frontend will primarily consume
catalog concepts rather than source-format-specific ingest structures.

This does not mean that every preserved observation must be copied into catalog.
Catalog provides semantic relationships and user-facing identity while preserved
manifests remain the evidence record.

The intended responsibility chain is:

> **Ingest tells Catalog what we found. Catalog tells the Frontend what it is.
> Publish tells the Frontend what it may expose.**

Publication policy remains a separate concern. Catalog knowledge that an artifact
is `Winamp 2.76`, for example, does not itself grant redistribution permission for
the preserved executable.

### Component boundary

Catalog is a sufficiently distinct responsibility to justify a component boundary.
The intended component is `bootdiskhq/bootdisk-catalog`.

Creating that repository and choosing its storage technology are implementation
steps, not prerequisites for accepting this domain decision. The domain model and
contract should be understood before persistence, API and frontend choices are
made.

## Consequences

### Positive

- Preservation remains trustworthy even when later interpretation changes.
- Identical artifacts found on multiple sources can share one catalog identity.
- Source-specific parser details do not leak into the future frontend.
- Catalog corrections do not require rewriting ingest manifests.
- Search and browsing can be based on software identity and relationships rather
  than filesystem paths.
- Evidence and uncertainty can remain visible instead of being hidden behind
  premature certainty.
- Publication rights and exposure policy remain independent from identification.

### Negative

- The system gains another explicit domain and likely another component.
- Mapping observations to software releases requires curation and reconciliation
  logic.
- Some concepts will appear in both preservation/provenance and catalog contexts,
  requiring careful identity and reference contracts rather than shared mutable
  records.
- Frontend development depends on establishing a useful catalog projection instead
  of reading ingest manifests directly.

## Alternatives Considered

### Treat ingest entries as the catalog

Rejected because source metadata is evidence, not necessarily normalized software
identity. It would also make catalog behavior dependent on particular source
formats.

### Put catalog interpretation into `bootdisk-publish`

Rejected because publication answers what may be exposed and how derivatives are
materialized. Software identity and historical relationships have a different
lifecycle and remain useful even when nothing may be publicly downloaded.

### Let the frontend interpret ingest manifests directly

Rejected because it would couple the public archive to source formats, parser
history and preservation implementation details. It would also encourage
presentation code to make archival identity decisions.

### Store only artifacts and filenames

Rejected because filenames do not provide stable software identity and the same
artifact may occur under different names and on many different sources.

## Follow-up

Before implementing the catalog component, define a minimal catalog model and the
identity/reference contract for:

- Software;
- SoftwareRelease;
- Artifact;
- Occurrence;
- Source and Entry references;
- evidence-bearing Artifact-to-SoftwareRelease identification.

Database technology, API shape, search technology and frontend framework are
explicitly deferred until that model is sufficiently clear.
