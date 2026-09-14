# Minimal Catalog Domain Model

This document defines the first deliberately small catalog model for Bootdisk.

It implements the direction established by:

- ADR-0004: separate Preservation, Provenance and Catalog domains;
- ADR-0008: Catalog interprets preserved observations without replacing them;
- ADR-0009: JSON is the initial authoritative catalog storage format.

The purpose of this model is not to describe every future archive concept. It is to
establish the smallest useful set of identities and relationships needed to say
what preserved software appears to be, why we believe that, and where it occurred.

## Design rules

The first catalog model follows these rules:

1. Preserved observations are never rewritten by catalog interpretation.
2. Artifact identity is based on content identity, not filename or source.
3. The same Artifact may occur in many Sources.
4. Software identity and release identity are separate concepts.
5. Mapping an Artifact to a SoftwareRelease is an evidence-bearing interpretation.
6. Unknown and incomplete knowledge are valid states.
7. Catalog records use stable explicit IDs and references rather than embedding
   duplicated copies of other records.
8. JSON records are authoritative; indexes and database projections are derived.

## Minimal entities

The first model contains five record types:

```text
Software
SoftwareRelease
Artifact
Occurrence
Identification
```

`Source` and `Entry` remain provenance references supplied by preserved ingest data
rather than becoming duplicated catalog-owned objects in this first model.

This keeps the catalog small while still allowing a future catalog record to point
back to the evidence from which it was derived.

---

## Software

Software represents the conceptual product independent of any particular version,
package or source occurrence.

Examples include:

```text
Winamp
CPU-Z
WinZip
Paint Shop Pro
```

Minimal record:

```json
{
  "schema": "bootdisk-catalog-0.1",
  "type": "software",
  "id": "software:winamp",
  "name": "Winamp"
}
```

### Required fields

- `schema`
- `type`
- `id`
- `name`

### Notes

`name` is the preferred catalog display name. It is curated catalog data and must
not overwrite differently spelled names preserved from historical sources.

Aliases, developer/publisher relationships, descriptions and dates are useful but
are intentionally deferred from the minimal model.

---

## SoftwareRelease

SoftwareRelease represents one particular release, edition or version of Software.

Minimal record:

```json
{
  "schema": "bootdisk-catalog-0.1",
  "type": "software_release",
  "id": "release:winamp:2.76",
  "software_id": "software:winamp",
  "version": "2.76",
  "display_name": "Winamp 2.76"
}
```

### Required fields

- `schema`
- `type`
- `id`
- `software_id`
- `version`

### Notes

`version` is catalog interpretation. It is not inferred merely because a source
filename contains a version-like string.

`display_name` is optional convenience metadata and must not be part of identity.

Release date, language, platform, edition and build metadata are deliberately
deferred until real material demonstrates how they should be represented.

---

## Artifact

Artifact represents exact preserved digital content.

For file artifacts, the canonical identity is currently SHA-256.

Minimal record:

```json
{
  "schema": "bootdisk-catalog-0.1",
  "type": "artifact",
  "id": "artifact:sha256:abc123...",
  "sha256": "abc123...",
  "size": 1234567
}
```

### Required fields

- `schema`
- `type`
- `id`
- `sha256`
- `size`

### Identity rule

For the current model:

```text
artifact ID = artifact:sha256:<digest>
```

Filename is not part of Artifact identity.

Two byte-identical files observed under different filenames or on different media
represent one Artifact with multiple Occurrences.

Catalog should normally derive Artifact records from trusted preservation data
rather than accepting manually invented content identities.

---

## Occurrence

Occurrence records that an Artifact was observed in a particular preserved source
context.

It connects catalog identity back to provenance without making the Source part of
Artifact identity.

Minimal record:

```json
{
  "schema": "bootdisk-catalog-0.1",
  "type": "occurrence",
  "id": "occurrence:kcd-15-2001:0018:winamp276",
  "artifact_id": "artifact:sha256:abc123...",
  "source_ref": {
    "manifest": "sha256:<ingest-manifest-digest>",
    "entry": "0018",
    "path": "Tools/Winamp/winamp276_full.exe"
  }
}
```

### Required fields

- `schema`
- `type`
- `id`
- `artifact_id`
- `source_ref`

### Source reference

The exact long-term reference mechanism to ingest manifests may evolve, but an
Occurrence must be traceable to preserved evidence.

The reference must not silently depend on a local machine path.

Where possible it should identify the ingest manifest or other preservation record
by immutable content identity plus a stable record/entry reference within it.

`path` may be repeated as a useful observed locator but is not itself sufficient as
the source identity.

---

## Identification

Identification is the critical interpretation record that says an Artifact is
believed to represent a SoftwareRelease.

This relationship is deliberately a first-class object instead of a field directly
on Artifact.

Minimal record:

```json
{
  "schema": "bootdisk-catalog-0.1",
  "type": "identification",
  "id": "identification:abc123:winamp-2.76",
  "artifact_id": "artifact:sha256:abc123...",
  "software_release_id": "release:winamp:2.76",
  "status": "curated",
  "evidence": [
    {
      "kind": "observed",
      "source_ref": {
        "manifest": "sha256:<ingest-manifest-digest>",
        "entry": "0018"
      },
      "field": "title",
      "value": "WinAmp 2.76"
    },
    {
      "kind": "observed",
      "source_ref": {
        "manifest": "sha256:<ingest-manifest-digest>",
        "entry": "0018"
      },
      "field": "path",
      "value": "Tools/Winamp/winamp276_full.exe"
    }
  ]
}
```

### Required fields

- `schema`
- `type`
- `id`
- `artifact_id`
- `software_release_id`
- `status`
- `evidence`

### Initial status values

The minimal model uses:

```text
interpreted
curated
```

`interpreted` means Bootdisk has made a catalog conclusion from available evidence.

`curated` means the conclusion has received explicit human review.

These statuses describe the catalog claim. They do not change the knowledge kind
of the underlying evidence.

### Confidence

Numeric confidence is intentionally NOT required in the first model.

A value such as `0.95` looks precise without necessarily having a defensible
calibration. Evidence plus explicit status is preferable until Bootdisk has a real
need for scored automated matching.

A future matching system may introduce confidence through a separate ADR or schema
revision.

---

## Relationships

The minimal relationship graph is:

```text
Software
    |
    +-- SoftwareRelease
            ^
            |
      Identification
            |
            v
         Artifact
            |
            +-- Occurrence --> preserved Source / Entry
            |
            +-- Occurrence --> preserved Source / Entry
            |
            +-- Occurrence --> preserved Source / Entry
```

This gives Bootdisk several useful properties immediately.

One Artifact can occur on many sources.

One SoftwareRelease can eventually have many Artifacts, such as localized builds,
installer variants or repackaged byte streams.

An Artifact can temporarily exist without any Identification.

An Identification can be corrected or replaced without changing the Artifact or
Occurrence records.

---

## Example catalog layout

The authoritative JSON catalog could initially look like:

```text
catalog/
    software/
        winamp.json

    releases/
        winamp-2.76.json

    artifacts/
        sha256-abc123.json

    occurrences/
        kcd-15-2001-0018-winamp276.json
        hjemmepc-example-winamp276.json

    identifications/
        abc123-winamp-2.76.json
```

The filenames are for human convenience. The `id` inside each record is the catalog
identity.

## Complete example

Together, the records may express:

```text
Winamp
  |
  +-- Winamp 2.76
          ^
          |
       curated identification
          |
          +-- artifact:sha256:abc123...
                    |
                    +-- K-CD 15/2001 occurrence
                    +-- HjemmePC occurrence
```

The historical K-CD title may remain exactly `WinAmp 2.76` in ingest evidence while
the preferred catalog name is `Winamp 2.76`.

Neither representation overwrites the other.

## What is deliberately not in version 0.1

The following concepts are intentionally deferred:

- developer and publisher entities;
- people and organizations;
- genres and categories;
- operating systems and platforms;
- languages and localization;
- release/build dates;
- licenses and redistribution rights;
- descriptions and editorial copy;
- screenshots and presentation assets;
- tags;
- arbitrary relationships between software;
- automated confidence scores;
- database mappings;
- API representations;
- search indexes;
- frontend-specific fields.

They may all become valuable. None is required to prove the core catalog identity
model.

## First implementation target

The first implementation should be able to:

1. load catalog JSON records;
2. validate their structure and IDs;
3. resolve references between the five record types;
4. reject broken references and duplicate IDs;
5. trace each Occurrence and Identification evidence item back to preservation
   evidence;
6. answer simple in-memory questions such as:
   - Which release is this artifact identified as?
   - Which artifacts belong to this release?
   - On which sources has this artifact occurred?
   - What evidence supports this identification?

It does not need a database, server or API to do any of this.

A later frontend or search layer may generate a disposable index from these records
without changing the catalog source of truth.
