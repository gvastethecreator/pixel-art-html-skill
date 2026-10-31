---
name: pixel-art-html
description: "Author and repair exact-grid pixel art through reference study, explicit visual interpretation, shape construction, material clusters, and a single construction pass. Export editable JSON, PNG, and standalone HTML. For sprites, icons, tiles, props, scenes, and image-to-grid recovery; animation atlases are out of scope."
---

# Pixel Art HTML

Build a visual idea as deliberate pixel relationships. Observe before diagnosing; preserve the design's identity while repairing the relationship that fails. A valid file, retrieved technique, preferred revision, or favorable metric does not prove good art.

## Choose the route

- New asset: interpret -> choose one direction -> construct and inspect stages -> export -> verify -> deliver.
- Explicit repair request: diagnose one relationship -> make one bounded intervention -> compare -> deliver.
- Local image: classify -> exact draft -> inspect -> deliver; report any authored recovery still required.
- Direction variants: only when the user explicitly requests alternatives; use the existing `study` command.

## Single-pass delivery

Default to one direction and one delivery. Plan before drawing. Construct progressively and inspect each stage once before advancing; this is one construction pass, not a set of alternative finished images. Record at most two identity relationships to preserve.

Do not generate competing drafts, restart the design, repeat artistic repairs, or add a finishing loop after final inspection. Technical fixes needed to export are allowed; preserve the intended pixels and record the cause. An explicit repair request authorizes one bounded intervention, not repeated attempts.

If an inspection blocks the next stage, retain the failed review and deliver the incomplete draft with its specific limitation. Do not fabricate an advance review. Final inspection records what failed; it does not start another repair. These execution limits also apply when a linked reference describes a repair technique.

## 1. Fix the visual contract and interpretation

Record use, exact dimensions, actual background, palette budget, projection, light, subject/action, material, and one or two identifying relationships. Honor the runtime grid; otherwise trial 32x32. Rectangular grids are valid. Increase dimensions only when a same-brief trial shows what cannot fit.

Describe the intended native read in one sentence. Decide what can be omitted. At 8x8, relationships such as head/body, handle/blade, or cockpit/engines are usually worth more than surface detail. Protect the function of an identity cue, not automatically every coordinate that currently expresses it.

Keep **observed**, **ruled out**, **uncertain**, and **preserve** separate. Distinguish a technical defect, a construction/readability failure, and a style preference. A quoted tutorial, a previously fixed problem, or “no noise” is not a current defect. A preference for clean art does not authorize removing a defining cloth pattern. Before applying a repair or resolving an ambiguous brief, read [the interpretation contract](references/interpretation-contract.md). Reuse [interpretation-input.json](assets/interpretation-input.json) when the distinction needs a durable record; it is not an artifact or review receipt.

Use a subject-specific contract: copy shared lighting conventions only, never unrelated emitters or subject instructions. Resolve whether “top-down” means true overhead or an oblique RPG view. Record palette limits separately for a source asset and a composited scene. UI, portraits and the world may have different coherent display conventions.

Author `draft` for art and `fixture` for mechanics. Neither label is acceptance. Calibration work remains draft until the required review; completing a candidate is not permission to expand a weak family.

## 2. Retrieve a construction method, not a diagnosis

For a technique/topic query, use the existing library:

```bash
python <skill-dir>/scripts/reference_library.py techniques "tree foliage volume"
```

For a concrete defect report, use explicit interpretation before contextual retrieval:

```bash
python <skill-dir>/scripts/tutorial_bridge.py diagnose --context <work>/interpretation.json
```

The bridge distinguishes bounded ES/EN negation and uncertainty, filters by subject/stage/projection, and falls back to actual bundled technique IDs. It does not inspect images or understand arbitrary language. Read its preserved text, exclusions, conflicts and stage mismatches. No compatible result means revisit the observation or stage, not apply a generic texture cleanup. Ordinary `reference_library.py` topic search remains lexical and unchanged.

Read only the returned techniques and matching subject guide:

- [Characters and creatures](references/subjects/characters-creatures.md)
- [Props, icons, and UI](references/subjects/props-ui.md)
- [Vehicles and architecture](references/subjects/vehicles-architecture.md)
- [Environments and tiles](references/subjects/environments-tiles.md)

When local references exist, use [reference-library.md](references/reference-library.md) to retrieve a few relevant images or process frames. Open the selected originals. A filename match or contact sheet locates evidence; it does not explain pixel construction.

For each useful reference, record **observed construction -> transferable decision -> application on this grid**, including what is inferred and what will deliberately differ. Keep source IDs and frame positions. Separate an artist's example, a wiki interpretation, and your inference. A reconstructed teaching sequence is not evidence of the author's historical process, and cannot fill your stage reviews retroactively. A GIF's text or first frame does not establish motion timing.

For original work, design your own silhouette, composition, motifs, and palette. Do not trace, recolor, rearrange, or downscale source art and present it as a new design. Source artwork, paid downloads and private reference corpora stay outside the distributable skill.

No suitable local corpus is required: the bundled techniques are portable. If visual references were unavailable, state that limitation; do not claim reference inspection.

For a larger piece, choose the smallest grid that carries the requested forms, up to 512×512. Rectangular masters are supported. Keep the existing small-grid defaults; a larger canvas is not permission for more variants or review loops. Author native structure with editable parts or compact geometry, not a magnified small sprite. Use scene composition when independent masters need a larger world.

## 3. Plan the forms and choose a direction

For multipart assets, use [executable construction](references/executable-construction.md) when a pose, attachment, or overlap needs controlled revision. `construct.py` compiles named part masks and anchors, exposes ownership, and binds stage transitions to observed reviews. For a simple flat asset, [construction-plan.json](assets/construction-plan.json) remains a brief working note.

Map geometry before details: a posed body dummy, shared architectural corners, functional machine modules, species-specific crown groups, or scene depth bands. See [construction-workflow.md](references/construction-workflow.md) and [artistic-construction.md](references/artistic-construction.md). Give the design a visual thesis, then solve main masses, form clusters and edge pixels at their appropriate scales. Recognition alone does not establish finish. A recognizable but rigid design needs gesture or mass relationships, not necessarily more polish.

Choose one construction direction from the brief before drawing. State the main masses, gesture, overlap and palette roles; retain the selected direction through the pass. Resolve an uncertain artistic choice with a stated assumption, without generating alternatives.

Only for an explicit alternatives request, author the three same-grid drafts required by `study`. Change construction rather than palette alone, inspect `blind.html` before `index.html`, and record the chosen direction and its losses. A comparison or rejected draft alone does not authorize a study.

## 4. Construct in visible passes

**Block:** build dominant and secondary masses and negative space. Flat silhouette must carry subject, support and orientation. Rectangles, circles and runs are valid scaffolds; refine their junctions into the intended form. For characters, solve gesture before costume and recheck it after equipment. For a family, test one module before repeating its errors across variants.

**Planes:** map light onto surfaces and overlaps. Use the few value groups that explain volume; three is a useful trial, not a universal minimum. Inspect grayscale before texture. Frontal light is not automatically pillow shading. Mirror symmetric geometry only when appropriate; recheck side-specific equipment and relight the finished surfaces.

**Material:** choose a small cluster vocabulary with a surface, purpose, direction, scale and quiet region. Reuse `motifs` and `stamps` where they preserve structure, avoid overlap artifacts during placement. Do not fill space merely because it remains. Dithering, isolated eyes/glints and manual palette-bound antialiasing can carry deliberate information; they are not automatic defects.

Check whether value regions turn the surface. Horizontal bands can flatten a flask or canopy; roof marks can contradict its plane; a load above legs can read as a head. Inspect that relationship before adding detail. If it blocks the current stage, record the incomplete result instead of rebuilding it. An edge belongs to adjacent regions: joining a highlight also changes the shape of the neighboring shadow. Name both surfaces and their relation.

**Edges and subtraction:** inspect staircase rhythm, doubled elbows, tangencies, banding and competing highlights. Distinguish silhouette, contact, seam, fold and light transition. Remove details only when the native read improves without losing protected identity. Automatic smoothing must not change the exact grid or create fringes.

Inspect each pass before authoring the next. Checkpoints exported after finishing do not show decisions between passes. In the executable route, reviewed block permits planes, then reviewed planes permit material. A changed mask, anchor or placement returns to block; old reviews cannot authorize new structure. These records do not authenticate the reviewer or grant artistic acceptance. Use [craft-workflow.md](references/craft-workflow.md) and [artifact-schema.md](references/artifact-schema.md).

## 5. Repair only when explicitly requested

State **visible symptom -> responsible relationship and region -> pixel operation -> expected native change -> identity at risk**. Choose one bounded relationship to repair; report other defects without starting additional interventions. Inspect coordinates:

```bash
python <skill-dir>/scripts/pixel_lab.py inspect <output>/pixel-art.json --region 8 6 12 10
```

Use returned rows, palette legend, cluster locations and fingerprint. For constructed assets, edit named source parts with `construct.py edit`; rebuild a color-only revision from its reviewed predecessor, or return to block when structure changes. Flat repairs reject constructed artifacts because they discard editable parts. For a small flat repair, fill [pixel-patch.json](assets/pixel-patch.json) and run `pixel_lab.py patch`: original grid, expected colors, protected regions and palette budget are checked. For a flat structural rebuild, edit the source spec and use `build_pixel_art.py repair`.

For ambiguous relationships, `pixel_lab.py loupe` provides a labeled ROI with native context and optional before/after comparison. Its receipt binds coordinates and aliases to both grids. It supports diagnosis but does not replace final browser inspection.

Select one matching [original visual lesson](examples/part-construction/README.md). Transfer its decision, not its geometry. Record the counterexample and what must survive: a foliage repair must not accidentally change species; a portrait cleanup must not standardize its expression; a support repair must not make the structure look weaker.

Compare before/after at 1x and use `pixel_lab.py diff`. Keep an edit only if the visible hypothesis holds. Record clarified, unchanged, regressed or uncertain; relative preference alone cannot satisfy a lost requirement. After that intervention, deliver the comparison and remaining limitations. Do not try another construction or repair in the same request.

For image input, retain the automatic draft and provenance. See [source-recovery.md](references/source-recovery.md) for small-grid recovery requirements.

## 6. Prove the final pixels and presentation

Run `validate` and `critique`. Inspect generated HTML in a real browser at native 1x, 2x, 4x, silhouette and value. Use available browser tooling to open the artifact, exercise its controls and capture the relevant rendered states. No separate browser skill is required. Distinguish logical grid, canvas backing pixels, CSS scale, device pixel ratio and screen origin. A fractional DPR alone is not a failure; an integer product of CSS scale and DPR can still align. Do not attribute presentation blur to the drawing or silently resample the master.

Review without title, provenance, metrics or direction card first. Record actual subject, orientation/action, material, focus, signature and mismatch. A builder who knows the brief cannot claim an independent blind test.

Judge the current piece alone, then its requirements, and only then compare it with a baseline. Critique meaning, construction, material/light and finish; locate the most important failures on the grid. Admit ties, uncertainty and both-fail comparisons. A weaker baseline must not become the acceptance standard.

Inspect the actual background. For tiles, inspect the 3x repeat and required mixed transitions. For packs, compare distinct silhouettes plus shared baseline, padding, projection, light and palette roles within their intended domain.

Bounds, singletons, contrast and changed-cell totals locate risks; they never rank artistic quality. Read [quality-contract.md](references/quality-contract.md) and [visual-review.md](references/visual-review.md).

## 7. Deliver with the correct evidence tier

Keep `draft` without the required reviewer. `representative` requires a real non-builder review; `production-candidate` requires the owner. Copy [visual-review-input.json](assets/visual-review-input.json) only when that review occurs. `promote` binds it to the exact canonical grid; later drift invalidates it. Interpretation notes and successful retrieval tests do not replace this process.

When delivering two or more related pieces, use `pack` for a compact showcase unless the user requests only raw files. Use a short collection title, descriptive piece names, a coherent review background, and source links. The showcase controls let the viewer inspect scale, values, and silhouette without changing the art. Keep native cells at integer scale and preserve scroll access for larger masters. Do not generate extra pieces just to fill a gallery. See [commands and layouts](references/command-reference.md).

Return source spec, interpretation and relevant reference decisions, construction checkpoints (and a study only if requested), final HTML/JSON/PNG, material repair evidence, browser proof and remaining limits. Reuse the project's iteration record. Do not distribute a private reference corpus.

Stop a quality claim when native recognition needs its label, main construction remains unresolved, browser proof is missing, a defining requirement was lost, or self-review is being presented as independent acceptance. Return the useful draft and the specific remaining problem.
