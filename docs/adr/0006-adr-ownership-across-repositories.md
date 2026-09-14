# ADR-0006: ADR ownership follows architectural scope

- **Status:** Accepted
- **Date:** 2026-09-14

## Context

Bootdisk now spans multiple repositories, including the project-level `bootdisk`
repository and implementation repositories such as `bootdisk-ingest` and
`bootdisk-publish`.

Architectural decisions have so far been recorded both centrally and inside
component repositories. In particular, ADR-0004 and ADR-0005 exist in both
`bootdisk` and `bootdisk-ingest`, while later ingest-related ADRs exist only in the
component repository. Copying full ADR text between repositories creates unclear
ownership, risks divergence and makes it difficult to know which copy is the
authoritative record.

At the same time, forcing every implementation detail into the central repository
would make component-local evolution unnecessarily cumbersome and would separate
technical decisions from the code they govern.

## Decision

ADR ownership follows the scope of the decision.

Project-wide and cross-repository decisions are authoritative in
`bootdisk/docs/adr`. These include decisions that define Bootdisk domain boundaries,
repository relationships, contracts between components, or rules that multiple
components must obey.

Component-local decisions are authoritative in that component's own `docs/adr`
directory. These include implementation and architecture choices that can change
inside one component without redefining a contract for the rest of Bootdisk.

An ADR has one authoritative copy. Other repositories should link to that ADR
instead of copying its full decision text. Historical duplicates are not silently
deleted or renumbered; they may be retained with an explicit note identifying the
authoritative record.

ADR numbering is repository-local. An ADR number is therefore meaningful together
with its repository, for example `bootdisk ADR-0006` or `bootdisk-ingest ADR-0007`.
Accepted ADRs are not renumbered solely to create organization-wide numbering.

Cross-repository contracts should be recorded centrally even when the work that
revealed the need for the decision happened in a component repository. Component
ADRs may document implementation consequences and link to the central contract.

The central ADR index may also list authoritative component ADRs when they are
important for understanding the overall architecture. Such links are a registry,
not duplicate ownership.

## Existing records

The existing project-level ADR-0004 and ADR-0005 remain the authoritative records
for their project-wide decisions. The corresponding files in `bootdisk-ingest`
are historical duplicates and should be marked as such rather than evolved
independently.

`bootdisk-ingest` ADR-0006 and ADR-0007 remain component-owned because they govern
safe ingest manifest writing/evidence handling and the internal Director
format-layer boundary respectively.

The publication contract currently described by `bootdisk-ingest` ADR-0008 is a
cross-repository contract between ingest and publication. Its current accepted
record remains valid, but future changes to that contract should be represented by
a project-level ADR in `bootdisk`, with component documentation linking to the
project decision rather than creating another independent copy.

## Consequences

There is a single place to edit each architectural decision, reducing the chance of
contradictory ADR copies.

Component repositories retain autonomy for implementation-level architecture while
project-wide contracts remain visible from the central repository.

Existing accepted ADR numbers do not need to be rewritten. References must include
repository context when ambiguity is possible.

Some historical duplicate ADR files remain for traceability. Their status must be
clear, and they must not be treated as independently evolving sources of truth.

Future cross-repository decisions require a small amount of coordination in the
central `bootdisk` repository, which is accepted in exchange for clearer ownership.
