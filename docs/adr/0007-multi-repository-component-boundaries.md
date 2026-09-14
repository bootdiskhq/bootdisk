# ADR-0007: Use component repositories with explicit architectural boundaries

## Status

Accepted

## Date

2026-09-14

## Supersedes

[ADR-0002: Monorepo](0002-monorepo.md)

## Context

Bootdisk originally adopted a monorepo while the project was small and primarily documentation-driven. That decision reduced early coordination overhead and provided one obvious place to start.

The project has since developed independently deployable and independently evolving components with different responsibilities:

- `bootdiskhq/bootdisk` for project-wide documentation, governance, roadmap and cross-repository architecture;
- `bootdiskhq/bootdisk-ingest` for source observation, preservation identities, source adapters and preservation extraction;
- `bootdiskhq/bootdisk-publish` for manifest-driven publication, content-addressed publication objects and derivatives.

These are no longer hypothetical future components. They have distinct dependency sets, tests, release concerns and architectural contracts. In particular, `bootdisk-publish` is intentionally forbidden from reimplementing source parsing performed by `bootdisk-ingest`; the ingest manifest and verified preservation extraction form the boundary between those components.

Keeping all implementation in one repository would no longer simplify the architecture. It would instead blur ownership boundaries that are now useful and intentional.

## Decision

Bootdisk will use multiple repositories for components that have a clear independent responsibility and lifecycle.

The current top-level repository model is:

```text
bootdiskhq/bootdisk
    project governance
    cross-repository architecture
    roadmap and project documentation

bootdiskhq/bootdisk-ingest
    source understanding
    preservation observations and identities
    source adapters and format readers
    preservation extraction

bootdiskhq/bootdisk-publish
    manifest-driven publication
    verified publication objects
    derivatives and publish manifests
```

Repository boundaries should follow architectural responsibility, not arbitrary code size.

A new repository should be created only when a capability has a meaningful independent contract, ownership boundary or lifecycle. Small helper modules and closely coupled code should remain with the component they serve.

The project repository remains the coordination point for decisions that affect multiple repositories. Under ADR-0006, component-local ADRs remain authoritative in their component repositories, while project-wide and cross-repository decisions are authoritative in `bootdisk`.

## Cross-repository contracts

Splitting components does not authorize hidden coupling.

Components communicate through explicit, documented contracts. Current examples include:

- the ingest manifest as the semantic contract from `bootdisk-ingest` toward publication;
- preservation extraction as the source of verified bytes for explicitly preserved manifest references;
- publish manifests and stable object keys as publication outputs rather than reinterpretations of ingest evidence.

A component must not compensate for a broken upstream contract by silently reaching across repository boundaries and rediscovering implementation-specific state.

For example, `bootdisk-publish` must not reopen original media to recover a missing asset that ingest failed to preserve.

## Alternatives considered

### Continue the monorepo

This would preserve one repository and one issue tracker, but would no longer reflect the actual component boundaries. It would also make it easier for source-specific ingest implementation details to leak into publication tooling.

### Repository per feature or tool

This would create too much operational overhead and fragment closely related code. Repository boundaries are therefore reserved for durable architectural components, not every executable or module.

## Consequences

### Positive

- Component responsibilities are visible in repository structure.
- Ingest and publication can evolve and be tested independently.
- Dependencies and release concerns remain local to the component that needs them.
- Cross-repository contracts become explicit architectural concerns.
- Source-specific parsing is less likely to leak into downstream publication code.
- The project repository remains a lightweight coordination and governance layer.

### Negative

- There are multiple repositories, test suites and release histories to maintain.
- Cross-repository changes require deliberate coordination.
- Documentation must link across repositories rather than assuming one filesystem tree.
- Contributors must understand which repository owns a decision or implementation.

These costs are accepted because the boundaries now correspond to real architectural responsibilities rather than speculative future decomposition.

## Migration from ADR-0002

ADR-0002 remains in the repository as historical evidence of the project's initial decision. It is not deleted or rewritten to pretend that the project always used multiple repositories.

This ADR supersedes ADR-0002 from 2026-09-14 onward.
