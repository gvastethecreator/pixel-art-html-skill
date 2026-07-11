---
name: pixel-art-html
description: "Create self-contained single-size or multi-resolution pixel-art HTML artifacts from text prompts, local images, or Codex ImageGen outputs. Use when Codex must design, convert, package, compare, edit, or verify pixel art as exact grids, standalone HTML, JSON, or PNG without calling a model API."
---

# Pixel Art HTML

Create exact-grid pixel art through Codex. Keep model generation optional; make conversion, rendering, and validation deterministic.

## Route

- Text only: write a compact scene spec, then compile it.
- Local or attached image: run the local image converter.
- Codex ImageGen: generate a source image with `$imagegen`, save the accepted result in the workspace, then run the same local image converter.
- Existing artifact: edit its spec or canonical JSON, rebuild, and verify.
- Resolution set: generate independent 16x16, 24x24, 32x32, 40x40, 48x48, and 64x64 masters, then package them as one comparison collection.

Do not use an OpenAI API key, an image API script, `$openai-image-gen`, or the upstream converter's API/server layer. If native ImageGen is unavailable, continue with text or a supplied image.

## Workflow

1. Define size or size set, palette limit, background, fit, and dithering. Default to 32x32, 16 colors, transparent background, `contain`, and no dithering. Use `16,24,32,40,48,64` for a full ladder.
2. Read [references/artifact-schema.md](references/artifact-schema.md) before authoring a text-only spec or editing canonical JSON.
3. For visual/art-direction decisions, read [references/quality-contract.md](references/quality-contract.md).
4. Read [references/project-library.md](references/project-library.md) for project-managed output. Build with `scripts/build_pixel_art.py`; use the bundled black proof and hub templates without redesigning them per run.
5. Inspect `index.html` in a real browser. Reject blurry, empty, clipped, low-contrast, or structurally unrecognizable results.
6. Run the CLI validator. Report paths to `index.html`, `pixel-art.json`, `pixel-art.png`, and visual proof.

## Commands

Managed text/spec route; writes to `<project>/pixel-art/YYYY/MM/NNN-slug/` and refreshes the project hub:

```bash
python <skill-dir>/scripts/build_pixel_art.py from-spec <spec.json> --project-root <project> --slug <request-slug>
```

Image route; local Pillow dependency, no model API:

```bash
uv run --with pillow==11.0.0 python <skill-dir>/scripts/build_pixel_art.py from-image <image> --project-root <project> --slug <request-slug> --size 32 --colors 16 --fit contain --dither none --background transparent
```

Full image-derived resolution set; every size converts directly from the original image:

```bash
uv run --with pillow==11.0.0 python <skill-dir>/scripts/build_pixel_art.py from-image <image> --project-root <project> --slug <request-slug> --sizes all --colors 16 --fit contain --dither none --background transparent
```

Text-derived resolution set; author one exact spec per size:

```bash
python <skill-dir>/scripts/build_pixel_art.py collection <16.json> <24.json> <32.json> <40.json> <48.json> <64.json> --project-root <project> --slug <request-slug> --title "Resolution set"
```

Omit `--project-root` to use the current project. Use `--output <dir>` for an explicit unindexed destination. Rebuild a project hub manually with:

```bash
python <skill-dir>/scripts/build_pixel_art.py hub --project-root <project>
```

Validate an output directory:

```bash
python <skill-dir>/scripts/build_pixel_art.py validate <output-dir>
```

Useful options:

- `--size N` or `--width N --height N`
- `--sizes 16,24,32,40,48,64` or `--sizes all`
- `--colors 4|8|16|32`
- `--fit contain|cover|stretch`
- `--dither none|floyd`
- `--background transparent|#RRGGBB`
- `--alpha-threshold 0..255`
- `--scale N` for the exported preview PNG

## Text-only authoring

Prefer palette aliases plus `rects`, `runs`, and sparse `pixels`; use a full `grid` only when exact per-cell control is useful. Build large shapes first, then silhouette, interior contrast, and identity details. Keep every coordinate in bounds.

For complex text-only subjects, make one coherent low-resolution composition rather than simulating a high-resolution illustration. Generate with ImageGen first only when visual exploration materially helps.

For a text-only resolution set, author each size independently. Preserve subject, palette roles, and pose across specs, but deliberately add or remove details per grid. Never resize a 64x64 grid downward and call the results responsive masters.

## ImageGen handoff

Ask for a centered subject, clean silhouette, simple value groups, controlled palette, flat or removable background, no readable text, no watermark, and framing that survives the target grid. Treat ImageGen as source acquisition only. Always repixelize to enforce exact dimensions and palette limits.

Save the accepted raw image inside the user's project before conversion. Never leave the only copy in a temporary or generated-images directory.

## Output contract

Each completed single-artifact directory contains:

```text
index.html
pixel-art.json
pixel-art.png
```

A completed resolution collection contains:

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

Managed project mode additionally writes `iteration.json` beside the artifact and regenerates `pixel-art/catalog.json` plus `pixel-art/index.html`. The hub discovers all chronological requests from metadata and links to their standalone proof pages.

Every `index.html` must use the bundled black proof-workbench system, remain standalone, and make no network requests. `pixel-art.json` is the canonical exact grid. `pixel-art.png` is a nearest-neighbor preview/export. A collection root compares masters without replacing the exact per-size proofs.

For spritesheets or animation atlases, finish individual frames here, then hand off to `$spritesheet-expert`.

## Verification gates

- Canonical dimensions equal the request.
- Every non-transparent cell is `#RRGGBB` and belongs to the emitted palette.
- HTML has no unresolved placeholders or remote URLs.
- Browser canvas is non-empty and uses hard pixel edges.
- Subject remains readable at native size and at 2x/4x.
- Every requested collection size exists and was generated from the original source or its own text spec.
- Transparent edges, palette, crop, and focal details match the requested contract.

Use `$browser-ui-verification` when available for browser proof. Source inspection or a successful CLI exit is not sufficient visual proof.
