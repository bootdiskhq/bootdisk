# ADR-0010: Coordinate intake through resumable local checkpoints

## Status

Accepted — 17 October 2026

## Context

Qualified components already extract and project most CD content automatically.
An operator still coordinates several commands, repeats interrupted work and
assembles exception reports. That does not scale to dozens of discs.

## Decision

The project repository owns a narrow local coordinator, `tools/intake.py`, which
invokes existing component CLIs. This extends the coordination role in ADR-0007;
it does not transfer source parsing, catalog decisions or publication policy.
The coordinator owns checkpoint integrity, batch selection, collection assembly
and a combined report. Components remain responsible for their own contracts.

Each run uses a separate workspace. The run pins input bytes, component Git heads
and nonignored working files, runner bytes and Python version. Completed stages
have hashed receipts and become visible by atomic rename. A process lock excludes
concurrent writers. Resuming verifies completed results before reuse; changed
inputs or completed results require investigation and a new workspace. Interrupted
partial stages may be rebuilt, but existing human curator work is never an input
or a write target. An existing public baseline is copied without rewriting its
entry documents.

Unknown metadata coverage blocks that CD. Other CDs may finish observation, but
no combined preview is produced when any member is blocked. Source defects remain
explicit evidence; they do not create invented software identities or a mandatory
manual queue for missing versions.

This command prepares a local preview, never deploys it. Public history from the
baseline is retained separately; a new release must record its own history before
packaging and deployment. This prevents a preview from inventing publication dates.

## Consequences

A standard intake and its resumption use the same command. Source-format exceptions
are collected per CD and fixed in the owning component instead of bypassed.
Hashing and isolated output copies cost disk space and time. POSIX locking limits
this first version to macOS/Linux. Qualified component checkouts and their Python
dependencies remain required; this is not an installer or a hosted service.
Source mutation during processing invalidates the run; the original source must
remain read-only. Checkpoint hashes protect against accidents, not a hostile owner
who can rewrite both state and receipts.

## Alternatives

Per-disc shell scripts duplicate orchestration and lack consistent resumption.
A new service/repository adds lifecycle overhead before there is an independent
service contract. Automatic deployment is excluded until a separate deployment
and rollback contract is agreed.
