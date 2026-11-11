# Resumable local intake

Run from this repository with Python 3.10+ on macOS/Linux:

```sh
python3 tools/intake.py intake.json --workspace /absolute/path/to/new-intake
```

Use exactly the same command after interruption. The workspace must initially be
empty or absent, and separate from source media, component repositories, the
baseline release and the human review workspace. Finished stages are verified and
reused. Only the interrupted partial stage is rebuilt. Changed source bytes,
configuration, component files or runner code require a new workspace. Keep all
sources and checkouts unchanged throughout a run. Do not edit generated stages.

Copy [the example configuration](../examples/intake.json), then select explicit
paths to qualified component checkouts and source media. Relative paths resolve
against the configuration file. Install each component's documented dependencies
in the Python environment used to launch the coordinator.

- `dtx-workshop`: qualified DTX main menu plus the legacy Director workshop reader.
- `dtx`: qualified DTX menus, including root Tools.dtx where supported.
- `source_root`: a mounted or previously extracted CD directory, read only.
- `iso`: alternative to source_root; requires an explicit `seven_zip` executable.
- `collections`: optional Web collection registry. The example uses an explicitly
  labelled local preview. When preparing an existing archive release, omit it to
  use Web's public registry, which requires its cited entries in the baseline.
- `baseline`: optional existing release; its entries and objects are preserved.

Profiles must be qualified for the source format. Unknown metadata is a stop
condition, not permission to publish only the subset the reader understands.
No historical program is executed.

## Results

`report.md` is the per-CD overview and `report.json` its machine-readable equivalent.
Both state whether the batch is ready for review. Each stage contains `commands.log`
and component manifests with detailed evidence. A failed stage remains in
`.STAGE.partial` for diagnosis. Exit 0 means a local preview is ready; exit 2 means
blocked or interrupted. A blocked member prevents a combined preview, while other
members can still complete their own extraction.

`collection/preview/` is the static site for local inspection. Serve it with a local
HTTP server. `collection/baseline-public-updates.json` preserves existing history
separately: the preview does not claim that new entries have been published.
Before deployment, follow the Web release workflow to record the release's history,
rebuild its package, validate it and publish. The coordinator has no upload action.

Source readiness is distinct from exact product identification. Missing versions
remain unknown. The report includes observed coverage and source/asset issues;
readiness does not certify all possible CD menus, workshop RTF completeness or
executable compatibility. Unqualified formats remain a component-level backlog.

## Verification

```sh
python3 -m unittest discover -s tests -v
```

CI runs these synthetic safety tests without private CDs. Real-media acceptance is
recorded separately in [the acceptance report](intake-acceptance-2026-10-17.md).
`--stop-after kcd-7-2001-observe` deliberately stops after a committed checkpoint;
repeat without that option to test resumption.

## Serial ISO input with a disposable source

For ISO9660 images that 7-Zip misdetects as an embedded archive, set an explicit
`"bsdtar": "/usr/bin/tar"` at the top level and `"archive_driver": "bsdtar"`
on each ISO member. Use the same qualified `html`, `dtx` or `dtx-workshop` profile
as for an extracted source. Driver selection is explicit, not guessed from year.

The driver checks member paths and rejects links/special files before extraction.
One source directory at a time is unpacked under the owned workspace, then removed
on success, normal failure or interruption. Original images are read only. Stage
outputs, observations and command logs remain. Source extraction itself is repeated
on resume; existing committed processing stages are still checksum-verified and
reused. A hard process kill may leave a `.source-*` temporary directory; these are
not silently deleted on restart. A new workspace is required if code or inputs change.

The original image and archive executable are pinned alongside the component
checkouts. A free-space check reserves the image size plus 512 MiB before extraction;
this is a minimum guard, not a guarantee for arbitrary compressed archives. This
mode is intended for ISO images. A failed disc continues to the next one and blocks
combined publication, just as other profiles do. Inspect report.json/report.md.

No source readiness result means verified product identity. No automatic upload is
introduced. Keep specialist/unknown discs in a separate explicitly configured run.
