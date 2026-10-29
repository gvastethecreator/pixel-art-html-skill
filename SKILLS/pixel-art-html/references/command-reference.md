# Command and artifact reference

## Contents

- [Prerequisites](#prerequisites)
- [Reference and repair lab](#reference-and-repair-lab)
- [Build and repair commands](#build-and-repair-commands)
- [Compose a scene](#compose-a-scene)
- [Inspect and maintain outputs](#inspect-and-maintain-outputs)
- [Image options](#image-options)
- [Artifact layouts](#artifact-layouts)

## Prerequisites

- `from-spec`, `study`, `repair`, `collection`, `pack`, `promote`, `validate`, `critique`, `hub`: Python, no extra deps.
- Interpretation and conditional method selection: `tutorial_bridge.py`, Python 3.11+ without extra dependencies. See the [structured input and diagnosis contract](interpretation-contract.md).
- Local image conversion + small-grid benchmark: Pillow. `uv run --with pillow==12.3.0` keeps it local to the command.
- Reference indexing, boards, and coordinate loupes: Pillow. Video metadata/samples additionally use local `ffprobe`/`ffmpeg`. Technique search, indexed text search, and pixel inspection, diff, and patch need only Python 3.11+.
- `--output`: unindexed scratch. `--project-root` plus `--slug`: managed iteration.

## Reference and repair lab

```bash
python <skill-dir>/scripts/reference_library.py techniques "tree volume"
python <skill-dir>/scripts/reference_library.py index --root "wiki=<local-directory>" --output <private-work-dir>/library.json
python <skill-dir>/scripts/reference_library.py search <private-work-dir>/library.json "leaf" --kind image --limit 6
python <skill-dir>/scripts/reference_library.py board <private-work-dir>/library.json --ids <reference-id> --fractions 0,0.5,0.95 --output <private-work-dir>/study.png
python <skill-dir>/scripts/pixel_lab.py inspect <baseline>/pixel-art.json --region 8 6 12 10
python <skill-dir>/scripts/pixel_lab.py loupe <baseline>/pixel-art.json --region 8 6 12 10 --compare <new-repair>/pixel-art.json --output <private-work-dir>/comparison.png
python <skill-dir>/scripts/pixel_lab.py patch <baseline>/pixel-art.json <patch.json> --output <new-repair> --scale 1
python <skill-dir>/scripts/pixel_lab.py diff <baseline>/pixel-art.json <new-repair>/pixel-art.json
```

Reference provenance and sampling limits: [reference-library.md](reference-library.md). Patch fields, coordinates, and construction decisions: [construction-workflow.md](construction-workflow.md). `patch` requires a new output directory and always writes a draft with the compiler's repair provenance; it never changes the baseline. `inspect` accepts a canonical JSON file or a validated single-artifact directory.

`loupe` writes a new diagnostic PNG and JSON receipt with native context, coordinate labels, shared palette aliases, exact ROI rows, and source fingerprints. Limit the ROI to 32 by 32 cells; omit `--region` for a smaller whole grid. `--compare` requires the same dimensions and declared background. Labels and cell gaps belong only to the diagnostic. The command does not alter either artifact or decide whether a repair improves it.

## Build and repair commands

Masters accept integer width and height from 8 through 512, including rectangular grids. The default PNG export is 16× for masters up to 128 pixels per side and native 1× for larger masters. Explicit `--scale` accepts 1–32, with a maximum exported side of 4096 pixels. Display zoom never changes the source grid.

Authoring CLI commands require a new output directory. Keep earlier drafts; `promote` is the separate reviewed update to an existing draft.

`pack` also builds a compact standalone showcase with integer scale, color/value/silhouette views, background controls, and links to each proof, PNG, and JSON. It supports mixed master sizes. Large previews scroll at native scale instead of shrinking below one pixel per cell. A named showcase is not an anonymous review or a promotion.

For native assets and direction studies, use the existing compiler commands below.

### Compose a scene

```bash
python <skill-dir>/scripts/compose_scene.py build <scene-source.json> --output <new-scene>
python <skill-dir>/scripts/compose_scene.py validate <new-scene>
```

The compositor needs only Python. It combines validated native masters without changing the single-asset size limit. It writes standalone HTML with pan/zoom, embedded scene JSON, and a native PNG. Use its own `validate` command for these scene outputs. Read [scene-composition.md](scene-composition.md) for placement, groups, contact height, and camera proof. The city example's authoring script additionally uses Pillow.

### Single-master and study commands

Managed text/spec:

```bash
python <skill-dir>/scripts/build_pixel_art.py from-spec <spec.json> --project-root <project> --slug <request-slug>
```

Scratch build:

```bash
python <skill-dir>/scripts/build_pixel_art.py from-spec <spec.json> --output <scratch-output>
```

Same-grid three-way study, only for explicitly requested alternatives:

```bash
python <skill-dir>/scripts/build_pixel_art.py study <a.json> <b.json> <c.json> --output <study-output> --title "Direction study"
```

Open `<study-output>/blind.html` before named overview. Three materially different draft grids, identical dimensions.

Image route; Pillow; no model API:

```bash
uv run --with pillow==12.3.0 python <skill-dir>/scripts/build_pixel_art.py from-image <image> --project-root <project> --slug <request-slug> --size 32 --colors 16 --fit contain --dither none --background transparent --evidence-tier draft
```

Small-grid recovery ladder, same source:

```bash
uv run --with pillow==12.3.0 python <skill-dir>/scripts/build_pixel_art.py from-image <image> --output <scratch-output> --sizes 8,16,24,32 --colors 8 --source-class auto --reconstruction auto
```

Image-derived resolution set:

```bash
uv run --with pillow==12.3.0 python <skill-dir>/scripts/build_pixel_art.py from-image <image> --project-root <project> --slug <request-slug> --sizes all --colors 16 --fit contain --dither none --background transparent
```

Same-grid repair from one draft:

```bash
python <skill-dir>/scripts/build_pixel_art.py repair <draft-output>/pixel-art.json <repair-spec.json> --output <repair-output> --scale 16
```

Text-derived resolution set:

```bash
python <skill-dir>/scripts/build_pixel_art.py collection <16.json> <24.json> <32.json> <40.json> <48.json> <64.json> --project-root <project> --slug <request-slug> --title "Resolution set"
```

Same- or mixed-size pack:

```bash
python <skill-dir>/scripts/build_pixel_art.py pack <potion.json> <key.json> <shield.json> <crystal.json> --project-root <project> --slug pickups --title "RPG pickups"
```

Promote after blind review:

```bash
python <skill-dir>/scripts/build_pixel_art.py promote <draft-output> <review-input.json> --tier representative
```

`--tier production-candidate` only with owner review. Authoring commands reject promoted tiers. Schema + set-level item observations: [visual-review.md](visual-review.md).

Recovery benchmark:

```bash
uv run --with pillow==12.3.0 python <skill-dir>/scripts/benchmark_small_grids.py --output <benchmark-output>
```

## Inspect and maintain outputs

Validate, then craft-risk:

```bash
python <skill-dir>/scripts/build_pixel_art.py validate <output-dir>
python <skill-dir>/scripts/build_pixel_art.py critique <output-dir>
```

Rebuild managed hub:

```bash
python <skill-dir>/scripts/build_pixel_art.py hub --project-root <project>
```

## Image options

Options the brief needs: `--size N`, `--width N --height N`, `--sizes all`, `--colors 4|8|16|32`, `--fit contain|cover|stretch`, `--source-class auto|exact-grid|pseudo-pixel|painterly`, `--reconstruction auto|two-stage|legacy`, `--structure-colors 0|2..64`, `--resample lanczos|nearest`, `--min-cluster 1..8`, `--dither none|floyd`, `--background transparent|#RRGGBB`, `--alpha-threshold 0..255`, `--scale N`.

`auto` uses nearest only for an exact source lattice matching the target; otherwise two-stage packing. Keep `min-cluster` at `1` unless image-derived singleton noise is visible. Cleanup stays a draft. Optional detector: `--pixel-fixer-bin <path> --pixel-fixer-mode full|fast` — advisory lattice metadata; once per resolution set.

## Artifact layouts

Single artifact:

```text
index.html
pixel-art.json
pixel-art.png
visual-review.json  # generated only after reviewed promotion
```

Direction study:

```text
index.html
blind.html
manifest.json
sample-a/{index.html,pixel-art.json,pixel-art.png}
sample-b/{index.html,pixel-art.json,pixel-art.png}
sample-c/{index.html,pixel-art.json,pixel-art.png}
```

Resolution collection:

```text
index.html
manifest.json
16x16/{index.html,pixel-art.json,pixel-art.png}
24x24/{index.html,pixel-art.json,pixel-art.png}
32x32/{index.html,pixel-art.json,pixel-art.png}
40x40/{index.html,pixel-art.json,pixel-art.png}
48x48/{index.html,pixel-art.json,pixel-art.png}
64x64/{index.html,pixel-art.json,pixel-art.png}
```

Asset pack:

```text
index.html
manifest.json
<asset-slug>/{index.html,pixel-art.json,pixel-art.png}
```

Promoted collection/pack: root `visual-review.json` plus one bound `visual-review.json` per child.

Managed mode writes `iteration.json` and regenerates `pixel-art/catalog.json` plus `pixel-art/index.html`. Contract: [project-library.md](project-library.md). Proof HTML is standalone, network-free. `pixel-art.json` is the canonical editable grid; `pixel-art.png` is nearest-neighbor preview/export. Validation checks dimensions and every RGBA cell still match the canonical grid. Repair artifacts embed the exact baseline grid, authored decisions, and recomputed delta evidence. Promoted output proves review fingerprints still match the final grid.

## Named construction parts

```bash
python <skill-dir>/scripts/construct.py build block-source.json --output work/block
python <skill-dir>/scripts/construct.py review work/block review-input.json --output work/block-review.json
python <skill-dir>/scripts/construct.py build planes-source.json --previous work/block --review work/block-review.json --output work/planes
python <skill-dir>/scripts/construct.py edit source.json part-edit.json --output revised-source.json
python <skill-dir>/scripts/construct.py validate work/planes
```

Read [executable-construction.md](executable-construction.md) for the source schema, stage contract, real review requirements, and part-preserving repair route. Outputs add `construction.json`, `construction-report.json`, and `parts.html` to the standard exact-grid bundle. Replay the [recorded original studies](../examples/part-construction/README.md) to inspect parts, failure lessons, and the pan/zoom scene; replay does not grant a fresh review.
