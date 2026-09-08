---
name: pixel-art-html
description: "Author and repair exact-grid pixel art through reference study, shape construction, material clusters, and coordinate-level visual iteration. Export editable JSON, PNG, and standalone HTML. For sprites, icons, tiles, props, scenes, and image-to-grid recovery; animation atlases belong to spritesheet-expert."
---

# Pixel Art HTML

Build a visual idea as deliberate pixel relationships. Work from references to a construction plan, then from visible errors to small, testable edits. A valid file or a favorable metric does not prove good art.

## Choose the route

- New asset: brief -> retrieve -> construct -> inspect -> repair -> prove.
- Rejected output or uncertain direction: keep the baseline, then a three-direction `study` before construction.
- Local image: classify -> exact draft -> authored repair when recognition or cluster structure fails.
- Related assets: shared family contract and distinct silhouettes, then `pack`.
- A composed world or camera: native masters -> shared contacts and depth -> `compose_scene.py`; read [scene-composition.md](references/scene-composition.md).
- Multiple resolutions: author each master independently, then `collection`.
- Animation: construct individual frame masters here; hand timing, pivots, and atlas work to `$spritesheet-expert`.
- Painterly concepts: use an available image-generation tool when requested; return here to author the final exact grid.

The compiler and study tools run locally. They need no model API, hosted converter, or external service. Command details: [command-reference.md](references/command-reference.md).

## 1. Fix the visual contract

Record use, exact dimensions, background, palette budget, projection, light, subject/action, material, and one identifying cue. Honor the runtime grid; otherwise start at 32x32. Increase dimensions only when a same-brief trial shows what cannot fit.

Describe the intended native read in one sentence. Decide what can be omitted. At 8x8, relationships such as head/body, handle/blade, or cockpit/engines are usually worth more than surface detail.

Author `draft` for art and `fixture` for mechanics. Neither label is acceptance.

## 2. Retrieve a construction method

Search the bundled technique library for the actual problem:

```bash
python <skill-dir>/scripts/reference_library.py techniques "tree foliage volume"
```

Read only the returned techniques and the matching subject guide:

- [Characters and creatures](references/subjects/characters-creatures.md)
- [Props, icons, and UI](references/subjects/props-ui.md)
- [Vehicles and architecture](references/subjects/vehicles-architecture.md)
- [Environments and tiles](references/subjects/environments-tiles.md)

When local references exist, use [reference-library.md](references/reference-library.md) to retrieve a few relevant images or process frames. Open the selected originals. A filename match or contact sheet locates evidence; it does not explain pixel construction.

For each useful reference, record **observed construction -> transferable decision -> application on this grid**. Prefer evidence for form, material, or projection over a gallery of similar colors. Keep source IDs and frame positions. Separate an artist's example, a wiki interpretation, and your own inference.

For original work, design your own silhouette, composition, motifs, and palette. State what will differ from the reference. Do not trace, recolor, rearrange, or downscale source art and present it as a new design.

No suitable local corpus is required: the bundled techniques are portable. If visual references were unavailable, state that limitation; do not claim reference inspection.

## 3. Plan the forms and choose a direction

For multipart assets, use [executable construction](references/executable-construction.md) when a pose, attachment, or overlap needs controlled revision. `construct.py` compiles named part masks and anchors, exposes ownership, and binds stage transitions to observed reviews. For a simple flat asset, [construction-plan.json](assets/construction-plan.json) remains a brief working note.

Map geometry before details: a body dummy for anatomy, shared corners for architecture, functional modules for machines, crown bundles for trees, depth bands for scenes. See [construction-workflow.md](references/construction-workflow.md).

For quality work, read [artistic-construction.md](references/artistic-construction.md). Give the design a visual thesis, then solve main masses, form clusters, and edge pixels at their appropriate scales. Recognition alone does not establish finish.

For rejected art, a quality comparison, or unresolved direction, author exactly three same-grid drafts. Change mass allocation, gesture, contour, orientation, or material construction. Palette swaps are not new directions. Run `study`; inspect `blind.html` before `index.html`. Choose one direction, explain the losses, and retain one useful signature. Do not merge all three by default.

Name the construction question each candidate tests. A few width changes or shifted marks can pass the topology validator while exploring too little. Review the structural differences visually; record weak exploration instead of claiming three strong directions.

A clear approved direction or a diagnosed repair can proceed directly. This includes rebuilding a structural relationship whose failure is already understood. Record the construction hypothesis and the reason a new direction study is unnecessary.

## 4. Construct in visible passes

**Block:** build the dominant mass, secondary masses, and negative space. Flat silhouette must carry the subject and orientation. Rectangles, circles, and runs are valid scaffolds; refine their junctions into the intended form.

**Planes:** map light onto surfaces and overlaps. Use the few value groups that explain the volume; three is a useful trial, not a universal minimum. Inspect grayscale before adding texture.

**Material:** select a small cluster vocabulary. Give each cluster a purpose, direction, scale, and quiet region. Reuse `motifs` and `stamps` where they preserve structure. Repair their overlap artifacts. Do not fill a surface just because space remains.

Check whether value regions actually turn the surface. Horizontal bands can flatten a bottle or canopy. Small roof marks can contradict a roof plane. A load above legs can read as a head. Correct the responsible construction before adding texture.

**Edges and subtraction:** inspect staircase rhythm, doubled elbows, tangencies, banding, and competing highlights. Remove details that weaken the native read. Manual antialiasing or dithering can be deliberate palette-bound choices; automatic smoothing must not change the exact grid or create fringes.

Inspect each construction pass before authoring the next. A set of checkpoints exported after finishing the image does not show decisions between passes. In the executable route, a reviewed block permits planes, then reviewed planes permit material. A changed mask, anchor, or placement returns to block; an old review cannot authorize new structure. These records do not authenticate the reviewer or grant artistic acceptance. Use [craft-workflow.md](references/craft-workflow.md) for pass criteria and [artifact-schema.md](references/artifact-schema.md) for flat grids, motifs, and paint order.

## 5. Repair an observed problem

State one hypothesis: **visible symptom -> responsible region -> pixel operation -> expected native change**. Inspect the region:

```bash
python <skill-dir>/scripts/pixel_lab.py inspect <output>/pixel-art.json --region 8 6 12 10
```

Use the returned rows, palette legend, cluster locations, and fingerprint. For a constructed asset, edit its named source parts with `construct.py edit`; rebuild a color-only revision from its reviewed predecessor, or return to block when structure changes. Flat repairs reject constructed artifacts because they would discard editable parts. For a small flat-grid repair, fill [pixel-patch.json](assets/pixel-patch.json) and run `pixel_lab.py patch`. It checks the original grid, expected cell colors, protected regions, and palette budget before writing a new draft. For a flat-grid structural rebuild, edit the source spec and use `build_pixel_art.py repair`.

For ambiguous local relationships, `pixel_lab.py loupe` renders a labeled ROI with native context and an optional before/after comparison. Its receipt binds coordinates and palette aliases to both grids. The loupe supports inspection; it does not replace the final browser view.

For a diagnosed construction failure, select one matching [original visual lesson](examples/part-construction/README.md). Transfer its decision and test it on the new form; do not copy its geometry.

Compare before/after at 1x and use `pixel_lab.py diff` to locate the changes. Keep an edit only if the visible hypothesis holds. If silhouette or value still fails after two focused attempts, reconsider the construction or direction. Do not keep adding detail.

For image input, retain the automatic draft and its provenance. Small-grid recovery has additional requirements in [source-recovery.md](references/source-recovery.md).

## 6. Prove the final pixels

At closeout, run `validate` and `critique`. Inspect the generated HTML in a real browser at native 1x, 2x, 4x, silhouette, and value. Use the available browser tooling; `$browser-ui-verification` gives the verification procedure when installed.

Review without title, provenance, metrics, or the direction card first. Record actual subject, orientation/action, material, focus, signature, and mismatch. A builder who knows the brief can inspect an anonymous page, but cannot claim an independent blind test.

Judge the current piece alone before showing its weaker baseline. Critique meaning, construction, material/light, then finish; locate the most important failures on the grid. Only then compare revisions. A relative preference does not satisfy a requirement the preferred piece still fails.

Inspect the actual background. For tiles, inspect both the 3x repeat and required mixed transitions. For packs, compare distinctive silhouettes plus shared baseline, padding, projection, light, and palette roles.

Bounds, singleton counts, contrast, and changed-cell totals locate risks. They never rank art quality. Read [quality-contract.md](references/quality-contract.md) and [visual-review.md](references/visual-review.md).

## 7. Deliver with the correct evidence tier

Keep the result `draft` without the required reviewer. `representative` requires a real non-builder review; `production-candidate` requires the owner. Copy [visual-review-input.json](assets/visual-review-input.json) only when that review occurs. `promote` binds it to the exact canonical grid. Later drift invalidates the review.

Return the source spec, relevant reference decisions, selected study/checkpoints, final HTML/JSON/PNG, material repair evidence, browser proof, and remaining limitations. Reuse the project's iteration record. Do not copy a private reference corpus into the output package.

Stop a quality claim when the native read needs its label, the main construction is unresolved, the final browser proof is missing, or self-review is being presented as independent acceptance. Return the useful draft and the specific remaining problem.
