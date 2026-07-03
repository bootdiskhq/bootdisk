# ADR-0002: Monorepo

## Status

Accepted

## Date

2026-07-03

## Context

Bootdisk is expected to grow into a long-term digital archive with multiple parts:

- A public website
- Documentation
- Import tools
- Metadata tools
- Possible OCR pipelines
- Possible APIs
- Design assets
- Infrastructure configuration

At this stage, the project is small and should remain easy to understand, navigate and maintain.

## Problem

Splitting the project into multiple repositories too early would create unnecessary overhead:

- Multiple issue trackers
- Multiple README files
- More repository administration
- Harder onboarding
- More difficult coordination between documentation, code and tooling

Bootdisk should start with a structure that supports growth without adding unnecessary complexity.

## Decision

Bootdisk will use a monorepo.

The main repository will be:

    bootdiskhq/bootdisk

The repository may eventually contain folders such as:

    docs/
    apps/
    packages/
    tools/
    infrastructure/

These folders should be added when there is a real need for them, not before.

## Alternatives Considered

### Multiple repositories

Example:

    bootdisk-web
    bootdisk-api
    bootdisk-docs
    bootdisk-tools

This was rejected for now because it adds coordination overhead before the project needs it.

### Documentation-only repository first

This was considered, but rejected because the main repository should become the long-term home of both documentation and implementation.

## Consequences

### Positive

- One place for project history
- One issue tracker
- One roadmap
- Easier onboarding
- Easier to keep documentation and implementation aligned
- Lower operational complexity in the early phase

### Negative

- The repository may become large over time
- Some tools may eventually need clearer boundaries
- We may need stronger conventions as the project grows

## Review Date

2027-07-03
