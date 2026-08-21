---
name: pixel-art-html
description: "Pixel art HTML: create, repixelize, repair, review, package JSON, PNG, HTML. Icons, sprites, tiles, props, scenes, image-to-grid recovery, visual-quality repair. Not animation atlases or painterly generation."
---

# Pixel Art HTML

Art must read on its exact native grid. A valid file, metric report, or title-assisted preview is not evidence.

## Route

- Text or grid edit: brief -> direction study if needed -> authored spec.
- Local image: classify -> exact draft -> same-grid authored repair if recognition collapses.
- Existing bad output: keep as losing baseline -> study three new directions -> rebuild.
- Resolution set: author or repair every size independently, then `collection`.
- Related assets: one family contract, distinct silhouettes, then `pack`.
- Animation or atlas: individual frame masters here, then `$spritesheet-expert`.
- Painterly or concept image generation: `$imagegen`. Return here only to author the final exact grid.

Runner is local and deterministic. Do not add an API key or call a hosted converter.

## Native-read ladder

### 1. BRIEF

Fix use, exact grid, background, palette limit, display context, projection, light, subject/action, material, focal cue, one intended signature. Honor a runtime grid if present; else 32x32. Enlarge only if a same-brief prototype proves the information cannot fit.

`fixture` for mechanics-only; `draft` for art under review. Source specs and image conversion author only those two tiers.

Load the matching reference:

- characters/creatures: [characters-creatures.md](references/subjects/characters-creatures.md)
- icons, props, UI: [props-ui.md](references/subjects/props-ui.md)
- vehicles/architecture: [vehicles-architecture.md](references/subjects/vehicles-architecture.md)
- environments, materials, tiles: [environments-tiles.md](references/subjects/environments-tiles.md)
- uncertain image lattice, 8x8-32x32 recovery: [source-recovery.md](references/source-recovery.md)
- spec syntax: [artifact-schema.md](references/artifact-schema.md)

Done: grid contract and intended blind read fit in one short direction card.

### 2. STUDY

If rejected, quality claim, or direction uncertain: author exactly three `draft` specs. Same brief and exact grid. Change silhouette thesis, shape language, orientation, or material construction. Palette swaps and ornament variants are duplicates.

Run `study`. Open `blind.html` before named `index.html`. Pick one sample from native read. Record why the other two lose. Keep one useful signature. Name one element to remove. Do not default to a hybrid.

Routine mechanical fixtures can skip study; record skip reason. Never use that output as art-quality evidence.

Done: one direction wins without title or provenance.

### 3. BLOCK

Build selected silhouette as a full local grid or coherent motifs. Rectangles and runs are scaffolds, not a finished style. At native 1x the flat shape must communicate subject, orientation, action.

For image input, keep automatic conversion as a draft. If an 8x8 or 16x16 result loses the read, preserve it. Then `repair` with explicit `silhouette`, `identity_cue`, and `subtraction`.

Done: removing every interior color still leaves the intended read.

### 4. LIGHT

Add only dark, mid, light, accent jobs. Establish projection and one light before texture. Separate major planes in grayscale. Make material readable via plane shape, edge behavior, highlight shape, cluster rhythm — not hue alone.

Checkpoint after silhouette and value. If either fails, revise structure rather than adding detail. Pass checks: [craft-workflow.md](references/craft-workflow.md).

Done: volume, material, focal hierarchy work without decorative pixels.

### 5. FINISH, THEN CUT

Add selected signature and a small reusable cluster vocabulary. Protect one focal cue. Remove every cell that helps only zoomed, creates an orphan, weakens negative space, or competes with focus.

For tiles, inspect the automatic 3x repeat proof. For packs, compare silhouettes, baseline, padding, palette roles, projection, light as a family.

Done: another subtraction pass no longer improves the native read.

### 6. PROVE

Run `validate` and `critique`. Inspect generated HTML in a real browser at native 1x, 2x, 4x, silhouette, value. Treat bounds, singleton, value-span, contrast as risk prompts, never a score. Blind-review before title, source, evidence tier, metrics, or direction card. Record actual subject, orientation/action, material, focal cue, remembered signature, mismatch. Inspect the final grid in its real background or repeated/set context.

Use `$browser-ui-verification`. CLI success and a non-empty canvas do not prove visual quality. Read [quality-contract.md](references/quality-contract.md) and [visual-review.md](references/visual-review.md).

Done: structural parity and the title-free perceptual record both pass.

### 7. PROMOTE OR KEEP DRAFT

Copy [visual-review-input.json](assets/visual-review-input.json). Fill from the blind review. `representative` requires a real non-builder reviewer; `production-candidate` requires the project owner. Stay `draft` if that reviewer did not inspect the raw proof.

Run `promote`: writes `visual-review.json`, fingerprints the exact canonical grid, changes the tier, later grid drift fails validation. Pack or collection: one non-empty blind observation per manifest item, then `set_context`.

Hand back source spec/image, checkpoints or study, final `index.html`, `pixel-art.json`, `pixel-art.png`, review record, browser evidence, remaining limitations. Commands/layouts: [command-reference.md](references/command-reference.md).

Done: another agent can rebuild, inspect, challenge, and validate the same pixels without hidden state.

## Stop conditions

If any apply, do not ship:

- native read needs the title or source image
- three directions share one silhouette thesis
- generic rectangle, ellipse, or automatic thumbnail survives as the main construction
- material inferred only from color
- texture or extra colors compensate for weak structure
- browser proof missing, clipped, blurry, empty, or not the final output
- source spec claims `representative` or `production-candidate`
- self-review presented as independent acceptance
