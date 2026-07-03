# ADR-0003: GitHub as Source of Truth

## Status

Accepted

## Date

2026-07-03

## Context

Bootdisk will have many types of project knowledge:

- Code
- Documentation
- Architecture decisions
- Roadmap
- Issues
- Development log
- Contribution guidelines
- Historical notes
- Metadata discussions

To keep the project sustainable, this information must not be scattered across private notes, chat logs or temporary documents.

## Problem

If project knowledge is spread across many places, Bootdisk becomes harder to maintain and contribute to.

Important decisions may be forgotten, repeated or misunderstood.

## Decision

GitHub will be the source of truth for Bootdisk project work.

This includes:

- Repository structure
- Documentation
- ADRs
- Issues
- Roadmap
- Pull requests
- Development discussions
- Contribution process

External tools may be used, but important decisions and project knowledge should eventually be reflected in GitHub.

## Alternatives Considered

### Private notes

Rejected because they are not transparent and are hard for future contributors to access.

### Chat history as source of truth

Rejected because chat is useful for exploration, but not suitable as long-term project memory.

### Separate project management tool

May be considered later, but rejected for now to reduce complexity.

## Consequences

### Positive

- Clear project memory
- Transparent decision-making
- Easier onboarding
- Better long-term maintainability
- Publicly visible project progress

### Negative

- Requires discipline to keep GitHub updated
- Some early discussions must be summarized manually
- GitHub becomes a dependency for project coordination

## Review Date

2027-07-03
