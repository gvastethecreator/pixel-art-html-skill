---
name: pixel-art-html
description: "Pixel-art HTML artifacts: direct, repixelize, critique, and package exact grids with explicit evidence tiers, title-free visual review, editable palette JSON, PNG parity, and browser proof."
---

# Pixel Art HTML

Create authored pixel art, not merely valid low-resolution files. Keep model generation optional; make exact grids, conversion, rendering, diagnostics, and packaging deterministic.

## Route

- Text-only art or edits: direction card -> silhouette/value passes -> exact spec -> critique -> browser proof.
- Local/attached image: source brief -> source classification -> target-aware draft -> authored same-grid repair -> critique -> blind before/after browser proof.
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
   - Read [source-recovery.md](references/source-recovery.md) when the source has an uncertain lattice, the target is 8x8-32x32, or conversion quality is the problem.
   - Read [artifact-schema.md](references/artifact-schema.md) before authoring or editing a spec.
   - Done when subject-specific construction and rejection rules are known without loading unrelated branches.

3. Search direction before committing.
   - For recovery, standout work, or `representative` / `production-candidate` output with direction risk, produce exactly three cheap candidates against the same brief and grid. Change silhouette thesis, shape language, or material story; palette swaps do not count.
   - Compare native-size read, user value, useful signature, feasibility, and proof path. Choose one explicitly; reject the other two and do not default to a hybrid.
   - Name one signature to preserve and one generic or diluting element to remove. ImageGen may supply concept evidence, never the final exact grid.
   - For a concrete recovery benchmark, inspect [cursed-salvage](examples/cursed-salvage/README.md); use its process and gates, not its visual theme.
   - For severe-grid image recovery, inspect [small-grid-repair](examples/small-grid-repair/README.md); preserve its same-grid baseline/repair proof and omission discipline, not its potion theme.
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
   - For image input, leave `--source-class auto` unless visual evidence disproves the detector. The default `--reconstruction auto` preserves an exact source lattice only when it matches the requested target; pseudo-pixel and painterly inputs use target-aware two-stage packing. `--reconstruction legacy` exists for comparison and regression work, not as the preferred path.

6. Critique and repair.
   - Run `critique`; inspect bounds, singleton clusters, value span, and low-contrast boundaries as risk signals, not a score.
   - Open the HTML in a browser. Inspect native 1x, 2x, 4x, silhouette, value hierarchy, crop, alpha edges, cluster rhythm, focal contrast, and subject-specific context.
   - For image-derived work, inspect source class/confidence and toggle the recovered source-lattice overlay. Treat a plausible lattice as diagnosis, not proof that the final target grid is good.
   - When an 8x8/16x16 image draft loses the native read, author an independent exact spec and compile it with `repair <baseline-pixel-art.json> <repair-spec.json>`. Record non-empty `silhouette`, `identity_cue`, and `subtraction` decisions. A repair must keep dimensions and change at least one cell.
   - Use the generated same-scale baseline/authored comparison and enable `Hide title for blind review`. Changed-cell count proves intervention only; it is not a quality score.
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
   - At 8x8 and 16x16, the automatic result is always a draft. Re-author the silhouette, remove secondary forms, and spend the remaining cells on one identity/focal cue. Do not promote it because reconstruction metrics improved.
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

## Commands And Artifact Layouts

Read [command-reference.md](references/command-reference.md) before invoking the CLI or interpreting generated output. It centralizes supported command forms, image options, managed-versus-scratch behavior, and the canonical artifact layouts.
