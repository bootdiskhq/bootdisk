# HTML-disc acceptance — 8 November 2026

Local preparation, not publication. Live baseline remains rc23 (1551 posts/26 CDs).
The previous prepared batch adds 154 posts on three CDs; this batch adds:

| Medium | Source posts | Source images |
|---|---:|---:|
| K-CD 5/2012 | 37 | 37 |
| K-CD 14/2012 | 104 | 104 |
| K-CD 16/2012 | 36 | 36 |
| K-CD 18/2012 | 35 | 35 |

Combined preview: **1917 posts / 33 CDs**. All 1705 preceding entry documents
are byte-identical. Human review-state SHA-256 remains
`16e4307226d20011c706de9abe5627c714b9844cbf933db0adda0a07fa80cbd2`.
No missing explicit references or missing images; no machine investigation tasks.
Original image hashes are retained in manifests. All 212 descriptions and image
hashes match their parsed source observations. Three Windows-1252 en dashes on
16/2012 are retained correctly. No human curation or product identification was
created. There are no RTFs in this HTML source projection.

Evidence: `local-results/intake-2012-2026-11-08/run4/report.json`,
`acceptance.json`, `verify-intake.py`, component test logs and `verify-preview.log`.
The earlier run directories are failed/interrupted qualification attempts, not
accepted releases. Their generated extraction copies may be removed; diagnostic
manifests/logs remain. `snapshot-5.json` records the unsuccessful mounted-file copy,
not the final tar extraction. Final sources were extracted from original images
with system bsdtar; the problematic installer is present and hashed.

Intake and Catalog changes require separate component PRs. Frontend remains the
existing design while Claude works independently. Public history must be generated
from rc23 at publication time, including the three earlier prepared CDs; a preview
has no public history and is not evidence of publication.

Coverage: current CD index plus software/article/video menu pages. Historical
article-search XML, membership/navigation pages and runtime functionality are not
claimed as newly catalogued programs. Fourteen article and nine video descriptions
are included; PDF/SWF payloads remain unserved. Source version/license observations
are preserved in manifests but the current frontend still displays curated
product fields; exposing source-reported versions separately is a follow-up.
