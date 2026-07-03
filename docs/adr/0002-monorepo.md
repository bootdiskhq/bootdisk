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

```text
bootdiskhq/bootdisk
