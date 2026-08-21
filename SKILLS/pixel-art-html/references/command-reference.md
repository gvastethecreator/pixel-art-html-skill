# Command and artifact reference

## Contents

- [Prerequisites](#prerequisites)
- [Build and repair commands](#build-and-repair-commands)
- [Inspect and maintain outputs](#inspect-and-maintain-outputs)
- [Image options](#image-options)
- [Artifact layouts](#artifact-layouts)

## Prerequisites

- `from-spec`, `study`, `repair`, `collection`, `pack`, `promote`, `validate`, `critique`, `hub`: Python, no extra deps.
- Local image conversion + small-grid benchmark: Pillow. `uv run --with pillow==12.3.0` keeps it local to the command.
- `--output`: unindexed scratch. `--project-root` plus `--slug`: managed iteration.

## Build and repair commands

Managed text/spec:

```bash
python <skill-dir>/scripts/build_pixel_art.py from-spec <spec.json> --project-root <project> --slug <request-slug>
```

Scratch build:

```bash
python <skill-dir>/scripts/build_pixel_art.py from-spec <spec.json> --output <scratch-output>
```

Same-grid three-way study:

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
