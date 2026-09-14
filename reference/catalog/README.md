# Catalog reference implementation

This directory contains the deliberately small reference implementation for the
Bootdisk JSON catalog model.

It is not intended to make the project repository the permanent home of catalog
runtime code. ADR-0008 defines `bootdisk-catalog` as the intended component
boundary. Until that repository exists, this implementation lives here so the
domain contract can be exercised and reviewed next to the project ADRs.

The implementation has no third-party dependencies.

## Core rule

Catalog relationships are expressed through stable record IDs, never through JSON
filenames or directory paths.

For example:

```text
software:winamp
        ^
        |
release:winamp:2.76
        ^
        |
identification:...
        |
        v
artifact:sha256:...
        |
        v
occurrence:...
```

The JSON files may be reorganized without changing those relationships.

Filesystem paths are retained only when they are themselves observed historical
metadata, such as an artifact path within a preserved source. Such a path is not a
catalog identity or an internal catalog reference.

## What the code does

`bootdisk_catalog.Catalog` currently:

- recursively loads JSON catalog records;
- validates schema, record type and stable ID form;
- rejects duplicate catalog IDs;
- verifies that an Artifact ID matches its SHA-256 content identity;
- resolves and type-checks internal references;
- requires Occurrence and Identification evidence to use immutable manifest
  content references rather than local filesystem identity;
- provides simple in-memory navigation in both forward and reverse directions.

Reverse relationships are derived at load time. They are not written back into the
authoritative JSON, avoiding duplicated relationship state.

## Running the tests

From this directory:

```bash
python -m unittest discover -s tests -v
```

No virtual environment or package installation is required.

## Deliberately not implemented

This reference implementation does not provide:

- a database;
- an ORM;
- an HTTP API;
- a search engine;
- a frontend projection;
- source-format parsing;
- external preservation-manifest loading.

It validates the shape of immutable preservation references but does not yet open
those external manifests. Cross-repository resolution can be added once the
catalog input contract is defined precisely enough to do so without coupling the
catalog to source-specific ingest behavior.

The goal is to prove that the domain can be navigated correctly from authoritative
JSON using stable IDs alone.
