---
name: pixel-art-html
description: "Pixel-art HTML artifacts: direct, repixelize, critique, and package exact grids with explicit evidence tiers, title-free visual review, editable palette JSON, PNG parity, and browser proof."
---

# Pixel Art HTML

Create authored pixel art, not merely valid low-resolution files. Keep model generation optional; make exact grids, conversion, rendering, diagnostics, and packaging deterministic.

## Route

- Text-only art or edits: direction card -> silhouette/value passes -> exact spec -> critique -> browser proof.
- Local/attached image: source brief -> direct conversion -> manual repixelization -> critique -> browser proof.
- Codex ImageGen: generate a clean source with `$imagegen`, save it in the project, then follow the image route.
- Existing artifact: edit its source spec or canonical grid, rebuild, and compare the final render.
- Resolution set: author each text master independently, or convert every size from the original image, then clean each size.
- Same-size asset set: author each item independently, then compile the specs with `pack` so names, proofs, and canonical files stay together.
- Animation/spritesheet request: use this skill for individual frame masters; hand atlas, sequencing, and runtime registration to `$spritesheet-expert` with explicit state workflow, frame order/timing, runtime cell, pivot/baseline, and pose geometry.
- Quality claim or rejected output: label the evidence tier, compare three materially different directions, select one signature, then prove the final exact grid without titles. Read [visual-review.md](references/visual-review.md).

Do not use an OpenAI API key, image API script, `$openai-image-gen`, or an external converter service. If native ImageGen is unavailable, continue from text or a supplied image.

## Workflow

1. Set the contract.
   - Define use, exact grid, palette limit, background, fit, and dithering.
   - Declare `evidence_tier`: `fixture`, `draft`, `representative`, or `production-candidate`. Default is `draft`; a fixture proves mechanics only.
   - Write a direction card: subject/action, projection, silhouette cue, focal cue, light, value groups, palette ramps, material grammar, and padding/overlap.
   - Default to 32x32, at most 16 colors, transparent background, `contain`, and no dithering only when the request does not decide them. Treat 32x32 as a starting point, not a badge: move to 48x48 when a representative direction needs several readable materials or a structural signature and a 32x32 prototype proves they collapse. Never override a fixed runtime grid.
   - Read [craft-workflow.md](references/craft-workflow.md) for text authoring, cleanup, or critique. Done when the silhouette, projection, light, and palette decisions are explicit.

2. Load only the relevant branch.
   - Read [subject-recipes.md](references/subject-recipes.md) for the matching subject: character, prop, vehicle, architecture, landscape, material, tile, isometric, retro, or gameplay-readable asset.
   - Read [image-source-brief.md](references/image-source-brief.md) before ImageGen or conversion when the source is not already pixel-clean.
   - Read [artifact-schema.md](references/artifact-schema.md) before authoring or editing a spec.
   - Done when subject-specific construction and rejection rules are known without loading unrelated branches.

3. Search direction before committing.
   - For recovery, standout work, or `representative` / `production-candidate` output with direction risk, produce exactly three cheap candidates against the same brief and grid. Change silhouette thesis, shape language, or material story; palette swaps do not count.
   - Compare native-size read, user value, useful signature, feasibility, and proof path. Choose one explicitly; reject the other two and do not default to a hybrid.
   - Name one signature to preserve and one generic or diluting element to remove. ImageGen may supply concept evidence, never the final exact grid.
   - For a concrete recovery benchmark, inspect [cursed-salvage](examples/cursed-salvage/README.md); use its process and gates, not its visual theme.
   - `fixture` and routine `draft` work may skip this search only when no artistic-quality claim is made.
   - Done when [visual-review.md](references/visual-review.md) has a direction record or an explicit, valid skip reason.

4. Build structure before detail.
   - Author the flat silhouette and major negative space first. Render it at native 1x.
   - Add projection/volume and dark-mid-light groups. Render again; reject pillow shading, mixed projection, or a title-dependent read.
   - Add hue-shifted palette roles, directional light, material clusters, and one focal accent.
   - Use rectangles/runs only for broad scaffolds. Use a full local grid for unique silhouettes and reusable `motifs`/`stamps` for coherent repeated clusters.
   - Done when silhouette and value proofs work before texture or decorative detail.

5. Compile through the public script.
   - Use a scratch `--output` while iterating. Use managed project output only for the accepted artifact/iteration.
   - Keep every operation in bounds and keep palette aliases semantic: outline, shadow, base, light, accent, environment bridge.
   - Done when JSON, PNG, and standalone HTML are generated from one canonical grid.

6. Critique and repair.
   - Run `critique`; inspect bounds, singleton clusters, value span, and low-contrast boundaries as risk signals, not a score.
   - Open the HTML in a browser. Inspect native 1x, 2x, 4x, silhouette, value hierarchy, crop, alpha edges, cluster rhythm, focal contrast, and subject-specific context.
   - Tile, texture, and seamless specs automatically add a 3x repeat proof when their direction card identifies that use. Inspect the repeated proof for seams, landmarks, diagonals, and visual fatigue.
   - Resolve every warning visually or record why it is intentional. Remove details that help only while zoomed in.
   - For `representative` or `production-candidate` output, copy the visual-review template beside the output. Hide titles, shuffle pack items, and record what is actually identified, which materials read, what signature is remembered, and every mismatch.
   - Never call an author self-review independent judgment. A `production-candidate` label means approval is still pending.
   - Use `$browser-ui-verification` for live proof; a successful CLI exit or non-empty canvas does not prove art quality.
   - Done when the final generated artifact, not an earlier preview, passes [quality-contract.md](references/quality-contract.md).

7. Handle resolution sets deliberately.
   - Text route: preserve subject, pose, palette roles, and framing, but add/remove detail per independently authored grid.
   - Image route: convert each target directly from the original source, then clean silhouette, palette, and clusters per size.
   - Compare every master at native size. Never downscale the largest grid and call the results responsive masters.
   - Done when every requested size communicates the same identity with resolution-appropriate information.

8. Package related assets deliberately.
   - Use `pack` for icons, pickups, props, palette variants, tile variants, or other sets that may share dimensions.
   - Keep a shared direction card for projection, light, palette roles, baseline, padding, and material grammar; preserve item-specific silhouettes and focal cues.
   - Review both each exact proof and the pack overview. Same dimensions are valid in a pack and invalid in a resolution collection.
   - Done when the set reads as one family without making the individual assets interchangeable.

9. Hand animation frames over without losing authored geometry.
   - Keep identity palette, light, outline, focal cues, and native cell size stable across frame specs. Name the animation workflow and key phase represented by every frame.
   - Supply frame order, unequal durations when intentional, loop intent, runtime cell, safe margin, and the ground/contact pivot. For grounded rows, declare the receiving sprite contract as grounded rather than allowing extraction to recenter each changing bbox.
   - Require `$spritesheet-expert` to prove `frame_layout`, baseline/root alignment, identity consistency, exact timing, and live runtime playback. Deterministic/scripted animation remains a labeled fixture unless its source provenance satisfies the production-art contract.
   - Done when the final atlas reproduces the authored baseline and timing rather than merely containing all frames.

10. Hand back reproducible proof.
   - Report paths to `index.html`, `pixel-art.json`, `pixel-art.png`, source spec/image, evidence tier, screenshots or browser evidence, and `visual-review.md` when required.
   - For managed output, also report the project hub and iteration path.
   - Done when another agent can inspect, edit, rebuild, critique, and verify the artifact without hidden state.

## Commands

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

Full image-derived resolution set:

```bash
uv run --with pillow==11.0.0 python <skill-dir>/scripts/build_pixel_art.py from-image <image> --project-root <project> --slug <request-slug> --sizes all --colors 16 --fit contain --dither none --background transparent
```

Text-derived resolution set:

```bash
python <skill-dir>/scripts/build_pixel_art.py collection <16.json> <24.json> <32.json> <40.json> <48.json> <64.json> --project-root <project> --slug <request-slug> --title "Resolution set"
```

Same-size or mixed-size asset pack:

```bash
python <skill-dir>/scripts/build_pixel_art.py pack <potion.json> <key.json> <shield.json> <crystal.json> --project-root <project> --slug pickups --title "RPG pickups"
```

Validate structure, then emit craft-risk signals:

```bash
python <skill-dir>/scripts/build_pixel_art.py validate <output-dir>
python <skill-dir>/scripts/build_pixel_art.py critique <output-dir>
```

Rebuild a project hub:

```bash
python <skill-dir>/scripts/build_pixel_art.py hub --project-root <project>
```

Useful image options: `--size N`, `--width N --height N`, `--sizes all`, `--colors 4|8|16|32`, `--fit contain|cover|stretch`, `--resample lanczos|nearest`, `--min-cluster 1..8`, `--dither none|floyd`, `--background transparent|#RRGGBB`, `--alpha-threshold 0..255`, and `--scale N`. Use nearest only for an already pixel-clean source. Keep min-cluster at 1 unless image-derived singleton noise is visible; cleanup is still a draft for manual review.

## Output contract

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

Managed mode also writes `iteration.json` and regenerates `pixel-art/catalog.json` plus `pixel-art/index.html`; read [project-library.md](references/project-library.md) for that contract. Every proof HTML remains standalone and network-free. `pixel-art.json` is the canonical editable grid; `pixel-art.png` is its nearest-neighbor preview/export, and validation proves its dimensions and every RGBA cell still match the canonical grid. The proof page displays the declared evidence tier so a fixture or draft cannot masquerade as accepted art.
