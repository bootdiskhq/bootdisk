# Intake coordinator acceptance — 17 October 2026

This is local intake qualification, not a new public release. rc21 remains live.

## Toolchain

| Component | Git head |
| --- | --- |
| Ingest | `5e9191a01108215cef1f5387880024beb0fb2fe4` |
| Catalog | `9f5b6c1000e0bf71e6e62fc053a31d61bf571461` |
| Publish | `8eae44dee42dbd5c3537fffe9bd557176c1b7382` |
| Web | `aae0799c2b4c8a691f43c6c9df1fbdc404b67c06` |

Run markers additionally retain hashes of all tracked and nonignored local files,
source input bytes, runner bytes and the Python version. The ISO path uses the
explicit local 7zz executable; no historical executable is launched.

## Results

- Fourteen synthetic tests pass without skips: interruption/resumption, atomic
  checkpoint reuse, concurrent writer exclusion, changed configuration/tool files,
  changed completed results, unsafe workspace/symlink refusal, preserved human
  documents, route/media/store collisions, inconsistent baseline ordering,
  batch isolation and source mutation during processing.
- K-CD 7/2001 from ISO: controlled stop after extraction returns exit 2; the same
  command without `--stop-after` resumes and finishes with exit 0. It produces
  29 main-menu plus 33 workshop posts and 29 original RTF documents.
- With rc20 as baseline: 919 posts, all 857 previous entry files byte-identical.
  Existing public history is byte-identical in the separate baseline copy.
  The human review workspace hash is unchanged.
- Repeating the finished ISO command reuses all eight stages, with every
  checkpoint file byte-identical and no duplicated entries.
- HTTP verification of that preview passes: 919 entries and 1,694 image assets.
- K-CD 3/2002 (`dtx`, including root Tools.dtx) produces 78 posts and 51 RTFs.
  HTTP verification passes for all 78 entries and 285 image assets. Its missing
  discovered assets remain explicit in the report. A local preview collection
  registry avoids presenting citations to entries outside this isolated sample.
- A mixed batch starts with K-CD 13/2001 and continues with 7/2001. Unprocessed
  metadata blocks 13/2001; 7/2001 still finishes its 62 posts. Exit 2 and no
  combined collection directory confirm that a partial batch is not marked ready.

The first packaging trial exposed that public history from an old projection
cannot accompany new data. The coordinator now preserves that history separately
for the explicit release workflow. Another trial correctly rejected public
collection citations missing from a single-CD sample; the configuration now
accepts an explicit local preview registry. Neither validation was bypassed.

## Evidence and limits

Local evidence is under `local-results/intake-acceptance-2026-10-17/` in the Bootdisk
workspace: `acceptance.json`, `iso-qualified/`, `dtx-verified/` and
`blocked-accepted/`. Each run contains its pinned inputs, receipts, logs, component
manifests and per-CD reports. Private source media are not committed.

This qualifies these paths and checkpoint behavior. It does not establish every
CD format, complete-disc coverage, supplemental workshop RTF completeness,
executable compatibility, publication rights or unattended deployment. Installed
Python dependencies must remain stable in addition to the pinned component files.
The larger-batch and unresolved-format work remains on the roadmap.
