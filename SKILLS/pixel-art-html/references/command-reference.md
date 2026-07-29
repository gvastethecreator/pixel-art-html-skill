# Command And Artifact Reference

## Contents

- [Prerequisites](#prerequisites)
- [Build and repair commands](#build-and-repair-commands)
- [Inspect and maintain outputs](#inspect-and-maintain-outputs)
- [Image options](#image-options)
- [Artifact layouts](#artifact-layouts)

## Prerequisites

- Run the dependency-free `from-spec`, `repair`, `collection`, `pack`, `validate`, `critique`, and `hub` commands with Python.
- Run local image conversion and the small-grid benchmark with Pillow. `uv run --with pillow==11.0.0` keeps that dependency local to the command.
- Use `--output` for an unindexed scratch artifact. Use `--project-root` plus `--slug` for a managed project iteration.

## Build And Repair Commands

Managed text/spec route:

```bash
python <skill-dir>/scripts/build_pixel_art.py from-spec <spec.json> --project-root <project> --slug <request-slug>
```

Iterative scratch build:

```bash
python <skill-dir>/scripts/build_pixel_art.py from-spec <spec.json> --output <scratch-output>
```

Image route; local Pillow dependency, no model API:

```bash
uv run --with pillow==11.0.0 python <skill-dir>/scripts/build_pixel_art.py from-image <image> --project-root <project> --slug <request-slug> --size 32 --colors 16 --fit contain --dither none --background transparent --evidence-tier draft
```

Small-grid recovery ladder from the same original source:

```bash
uv run --with pillow==11.0.0 python <skill-dir>/scripts/build_pixel_art.py from-image <image> --output <scratch-output> --sizes 8,16,24,32 --colors 8 --source-class auto --reconstruction auto
```

Full image-derived resolution set:

```bash
uv run --with pillow==11.0.0 python <skill-dir>/scripts/build_pixel_art.py from-image <image> --project-root <project> --slug <request-slug> --sizes all --colors 16 --fit contain --dither none --background transparent
```

Authored same-grid repair from one canonical draft:

```bash
python <skill-dir>/scripts/build_pixel_art.py repair <draft-output>/pixel-art.json <repair-spec.json> --output <repair-output> --scale 16
```

Text-derived resolution set:

```bash
python <skill-dir>/scripts/build_pixel_art.py collection <16.json> <24.json> <32.json> <40.json> <48.json> <64.json> --project-root <project> --slug <request-slug> --title "Resolution set"
```

Same-size or mixed-size asset pack:

```bash
python <skill-dir>/scripts/build_pixel_art.py pack <potion.json> <key.json> <shield.json> <crystal.json> --project-root <project> --slug pickups --title "RPG pickups"
```

Deterministic recovery benchmark:

```bash
uv run --with pillow==11.0.0 python <skill-dir>/scripts/benchmark_small_grids.py --output <benchmark-output>
```

## Inspect And Maintain Outputs

Validate structure, then emit craft-risk signals:

```bash
python <skill-dir>/scripts/build_pixel_art.py validate <output-dir>
python <skill-dir>/scripts/build_pixel_art.py critique <output-dir>
```

Rebuild a managed project hub:

```bash
python <skill-dir>/scripts/build_pixel_art.py hub --project-root <project>
```

## Image Options

Use only the options needed by the brief: `--size N`, `--width N --height N`, `--sizes all`, `--colors 4|8|16|32`, `--fit contain|cover|stretch`, `--source-class auto|exact-grid|pseudo-pixel|painterly`, `--reconstruction auto|two-stage|legacy`, `--structure-colors 0|2..64`, `--resample lanczos|nearest`, `--min-cluster 1..8`, `--dither none|floyd`, `--background transparent|#RRGGBB`, `--alpha-threshold 0..255`, and `--scale N`.

`auto` chooses nearest only for an exact source lattice that matches the target and otherwise uses two-stage packing. Keep `min-cluster` at `1` unless image-derived singleton noise is visible; cleanup remains a draft for manual review. A compatible local detector can be supplied with `--pixel-fixer-bin <path> --pixel-fixer-mode full|fast`; it adds advisory lattice metadata only and runs once for a resolution set.

## Artifact Layouts

Single artifact:

```text
index.html
pixel-art.json
pixel-art.png
visual-review.md  # required beside representative / production-candidate evidence
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

Managed mode also writes `iteration.json` and regenerates `pixel-art/catalog.json` plus `pixel-art/index.html`; read [project-library.md](project-library.md) for that contract. Every proof HTML remains standalone and network-free. `pixel-art.json` is the canonical editable grid; `pixel-art.png` is its nearest-neighbor preview/export, and validation proves its dimensions and every RGBA cell still match the canonical grid. A repair artifact also embeds its exact baseline grid, authored decisions, and recomputed delta evidence. The proof page displays the declared evidence tier so a fixture or draft cannot masquerade as accepted art.
