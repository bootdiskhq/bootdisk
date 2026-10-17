# Ten-CD format follow-up — 17 October 2026

The unchanged coordinator initially blocked all ten CDs. It extracted 289 entries
and 289 RTFs from seven 2008/2009 discs, but 73 titles were absent from the normalized
view despite existing Norwegian fields. Three 2002 discs exposed multiline Tools
prose and nested metadata. This follow-up fixes formats, not individual records.

## Qualified subset

| CD | Source entries | RTFs |
| --- | ---: | ---: |
| 8/2002 | 67 | 39 |
| 16/2002 | 71 | 42 |
| 10/2008 | 43 | 43 |
| 11/2008 | 42 | 42 |
| 12/2008 | 43 | 43 |
| 14/2008 | 35 | 35 |
| 15/2008 | 42 | 42 |
| 16/2008 | 41 | 41 |
| 5/2009 | 43 | 43 |
| Total | 427 | 370 |

The explicit nine-CD subset completed with no machine tasks. With the rc21 baseline
its local preview contains 1,346 entries and 2,427 image assets. HTTP verification
passes. All 919 old entry documents, baseline history and human review bytes are
unchanged. The nine-disc rerun took 78.30 seconds using already extracted local
source trees; this is not comparable to the original 724.96-second ISO/network run.
No deployment or new release-history event has occurred. The three ready CDs from
the earlier five-CD trial remain a separate unpublished batch.

Ingest preserves 28 workshop lesson documents from 16/2002 separately. They have
original bytes, sections, language hints and same-folder links, and are explicitly
`preserved_only`. No extra programs, launch targets or published courses are inferred.
Unknown lesson/menu sections still block. Complete-disc certification remains false.

## Remaining blocker and limits

4/2002 now parses its repeated multiline Tools.dtx text verbatim. It remains blocked
on the K.DTX section `Flytter`, containing a Danish Pixia 2.4 row alongside the main
Pixia row. Static Director inspection encounters an unsupported compressed resource
codec. Its menu role is unresolved: do not discard it or count it as a second active
program simply to clear the gate. The full ten-disc run remains recorded as blocked;
the nine-disc preview is an explicit subset, not a weakened gate.

Known missing source assets stay in the individual reports. Localized screenshots
such as ShotNO.png are preserved in inventory but are not yet comprehensively mapped
by the legacy asset conventions. Qualify that convention before claiming complete
artwork coverage. Original course playback/publication remains a separate milestone.

## Validation and evidence

- Ingest: 213 tests, 153 passed, 60 private-media/optional skips.
- Catalog: 182 tests, 181 passed, one optional skip; local HTTP tests run with permission.
- Web: 328 tests, 218 passed, 110 browser/optional skips; no browser UI code changed.
- Coordinator: 14 tests, all passed.
- Additional before/after parsing of 3/2002, 7/2001 and 8/2001 preserves raw fields,
  normalized values, file observations and content identities for every prior entry.
- The attempted 15/2001 mounted-media comparison could not read FirstPage/DATA1.CAB
  due to OS access restrictions; it is not counted as a passing regression test.
- Seven newer discs: all 73 title tasks resolve from actual Norwegian fields, with
  no previously nonempty titles changed.

Local evidence: `local-results/intake-format-fixes-2026-10-17/`, especially
`qualification.json`, `qualified-run/report.json`, `all-run/report.json`, regression
results and `flytter-observation.json`. Generated duplicate extraction payloads from
superseded trials were retired to free disk space; source trees, manifests, logs and
receipts are retained. Retired historical runs are not resumable. The final qualified
run retains its outputs. Source media and private fixtures are not committed.

## Components

Ingest owns title normalization, nested Tools paths, prose projection and lesson
observation. Catalog validates new source proofs and emits readiness v4. Web accepts
v4 alongside older rules. The coordinator recognizes the already validated nested
Tools metadata path. Publication remains a separate, explicit release operation.
