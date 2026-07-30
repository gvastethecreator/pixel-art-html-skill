---
name: pixel-art-html
description: "Create, repixelize, repair, review, and package exact-grid pixel art as editable JSON, parity-checked PNG, and standalone HTML. Use for authored pixel icons, sprites, tiles, props, small scenes, image-to-grid recovery, or visual-quality repair; not for animation atlases or painterly image generation."
---

# Pixel Art HTML

Build art that reads on its exact native grid. A valid file, a clean metric report, or a title-assisted preview is not evidence that the art works.

## Route

- Text or grid edit: brief -> direction study when needed -> authored spec.
- Local image: classify -> exact draft -> same-grid authored repair when recognition collapses.
- Existing bad output: keep it as the losing baseline -> study three new directions -> rebuild.
- Resolution set: author or repair every size independently, then use `collection`.
- Related assets: keep one family contract, author distinct silhouettes, then use `pack`.
- Animation or atlas work: create individual frame masters here, then hand them to `$spritesheet-expert`.
- Painterly or concept image generation: use `$imagegen`; return here only to author the final exact grid.

The runner is local and deterministic. Do not add an API key or call a hosted converter.

## Native-read ladder

### 1. BRIEF

Fix the use, exact grid, background, palette limit, display context, projection, light, subject/action, material, focal cue, and one intended signature. Honor a runtime grid; otherwise start at 32x32 and enlarge only when a same-brief prototype proves the information cannot fit.

Choose `fixture` for mechanics-only output or `draft` for art under review. Source specs and image conversion may author only those two tiers.

Load only the matching reference:

- characters or creatures: [characters-creatures.md](references/subjects/characters-creatures.md)
- icons, props, or UI: [props-ui.md](references/subjects/props-ui.md)
- vehicles or architecture: [vehicles-architecture.md](references/subjects/vehicles-architecture.md)
- environments, materials, or tiles: [environments-tiles.md](references/subjects/environments-tiles.md)
- uncertain image lattice or 8x8-32x32 recovery: [source-recovery.md](references/source-recovery.md)
- spec syntax: [artifact-schema.md](references/artifact-schema.md)

Done when the grid contract and intended blind read fit in one short direction card.

### 2. STUDY

For rejected work, quality claims, or uncertain visual direction, author exactly three `draft` specs against the same brief and exact grid. Change silhouette thesis, shape language, orientation, or material construction. Palette swaps and ornament variants are duplicates.

Run `study`, then open `blind.html` before the named `index.html`. Select one sample from its native read; record why the other two lose. Preserve one useful signature and name one element to remove. Do not default to a hybrid.

Routine mechanical fixtures may skip the study. Record the skip reason; never use that output as art-quality evidence.

Done when one direction wins without its title or provenance.

### 3. BLOCK

Build the selected silhouette as a full local grid or coherent motifs. Rectangles and runs are scaffolds, not a finished style. At native 1x, the flat shape must communicate subject, orientation, and action.

For image input, keep automatic conversion as a draft. If an 8x8 or 16x16 result loses the read, preserve it and use `repair` with explicit `silhouette`, `identity_cue`, and `subtraction` decisions.

Done when removing every interior color still leaves the intended read.

### 4. LIGHT

Add only dark, mid, light, and accent jobs. Establish projection and one light before texture. Separate major planes in grayscale; then make material readable through plane shape, edge behavior, highlight shape, and cluster rhythm—not hue alone.

Keep a buildable checkpoint after silhouette and value. If either fails, revise structure rather than adding detail. Read [craft-workflow.md](references/craft-workflow.md) for the pass checks.

Done when volume, material, and focal hierarchy work without decorative pixels.

### 5. FINISH, THEN CUT

Add the selected signature and a small reusable cluster vocabulary. Protect one focal cue. Remove every cell that helps only while zoomed, creates an orphan, weakens negative space, or competes with the focus.

For tiles, inspect the automatic 3x repeat proof. For packs, compare silhouettes, baseline, padding, palette roles, projection, and light as a family.

Done when another subtraction pass no longer improves the native read.

### 6. PROVE

Run `validate` and `critique`, then inspect the generated HTML in a real browser at native 1x, 2x, 4x, silhouette, and value. Treat bounds, singleton, value-span, and contrast output as risk prompts, never as a score.

Enable blind review before reading the title, source, evidence tier, metrics, or direction card. Record the actual subject, orientation/action, material, focal cue, remembered signature, and mismatch. Inspect the final generated grid in its real background or repeated/set context.

Use `$browser-ui-verification`; CLI success and a non-empty canvas do not prove visual quality. Read [quality-contract.md](references/quality-contract.md) and [visual-review.md](references/visual-review.md).

Done when structural parity and the title-free perceptual record both pass.

### 7. PROMOTE OR KEEP DRAFT

Copy [visual-review-input.json](assets/visual-review-input.json) and fill it from the blind review. `representative` requires a real non-builder reviewer. `production-candidate` requires the project owner. If that reviewer did not inspect the raw proof, the artifact stays `draft`.

Run `promote`. It writes `visual-review.json`, fingerprints the exact canonical grid, changes the tier, and makes later grid drift fail validation. For a pack or collection, include one non-empty blind observation per manifest item and pass `set_context`.

Hand back the source spec/image, checkpoints or study, final `index.html`, `pixel-art.json`, `pixel-art.png`, review record, browser evidence, and any remaining limitation. Read [command-reference.md](references/command-reference.md) for exact commands and layouts.

Done when another agent can rebuild, inspect, challenge, and validate the same pixels without hidden state.

## Stop conditions

Revise instead of shipping when any applies:

- the native read needs the title or source image;
- the three directions share one silhouette thesis;
- a generic rectangle, ellipse, or automatic thumbnail survives as the main construction;
- material is inferred only from color;
- texture or extra colors compensate for weak structure;
- browser proof is missing, clipped, blurry, empty, or not the final output;
- a source spec claims `representative` or `production-candidate`;
- a self-review is presented as independent acceptance.
