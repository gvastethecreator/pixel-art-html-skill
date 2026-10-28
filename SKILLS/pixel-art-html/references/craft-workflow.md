# Craft passes

Passes for text-authored grids, same-grid repair, and manual cleanup after conversion. Keep checkpoints buildable. Advance only if the native 1x read supports it. Before these passes, use [construction-workflow.md](construction-workflow.md) to translate references into bounds, anchors, overlaps, and pixel decisions.

## Direction card

```text
Use and exact grid:
Subject / orientation / action:
Projection and scale cue:
Silhouette thesis and negative gap:
Light direction and hardness:
Value jobs: dark / mid / light / accent:
Material plane and edge grammar:
Focal cue:
Useful signature:
Element to remove:
Background, padding, and context:
```

If fields cannot fit in short card, direction is not decided.

## BLOCK - silhouette

- Dominant mass, secondary mass, negative space, one cue.
- Start smaller than canvas. Edge contact only if composition needs it.
- Full grid for unique contour. Rectangles and runs as broad scaffolds.
- Connected clusters and controlled stair steps.
- Judge one flat foreground color against background.

Pass: title-free viewer identifies subject, orientation, pose/action. If the shape is confused with a generic box, bottle, person, or ship, change the defining contour before continuing. A simple shape can be intentional.

## LIGHT - projection and value

- One frontal, side, top-down, three-quarter, isometric convention.
- Overlap and vertical placement for depth. Detail cannot repair contradictory faces.
- Give each color a job. Try dark, base, light, and one accent, then use only the groups the grid needs.
- Increase value through each ramp. Shift hue only if it supports light or material.
- Strongest contrast on focal cue.
- Light as connected plane-shaped clusters. Avoid bright center with dark edges.

Pass: grayscale separates main planes and focus. If silhouette or value blocks advancement, stop with an incomplete draft. Restarting or changing direction requires an explicit request.

## FINISH - material and signature

Start with a few cluster shapes per important material and add another only for a visible job:

- metal or glass: clean planes, narrow hard highlights, selective dark seams
- cloth, hair, foliage: one main mass, flow direction, few subordinate breaks
- stone or wood: structural fractures, grain, strata, chips with quiet gaps
- water or clouds: connected rhythm and overlapping light/shadow masses
- brick or panels: structural cadence first, sparse wear last

Repeat vocabulary with controlled variation. Scale detail down with depth. Add selected signature through construction — cutout, asymmetry, wraparound band, unusual mass. No floating decal.

Pass: material named from shape, planes, edges, highlights without hue.

## CUT - native subtraction

At 1x:

- remove cells visible only while zoomed
- merge near-duplicate colors with no separate job
- delete orphan pixels unless deliberate eye, glint, star, spark, particle
- clear tangencies that merge forms
- lower detail and contrast away from focus
- compare against an existing baseline only for an explicit repair; alternatives require an explicit request

Pass: another removal weakens recognition, material, focus, useful signature.

## PROVE - clean surface

Inspect:

1. native 1x
2. flat silhouette
3. grayscale/value
4. 2x and 4x cluster rhythm
5. real background, neighboring assets, 3x repeat
6. blind title-free read
7. named/provenance view only after observations recorded

Deterministic critique reports bounds, cluster count, singleton count, value span, and low-contrast boundaries. They are questions, not grades. A clean report can describe bad anatomy, generic design, or the wrong material. `pixel_lab.py inspect` locates small clusters on the grid; `patch` and `diff` support a controlled repair in a new draft.

## Repair map for an explicit bounded intervention

During new single-pass construction, use this map to name a blocking limitation, not to return to an earlier stage. Variants remain explicit-only.

| Symptom | Return to | Change |
|---|---|---|
| valid but generic | BLOCK | strengthen the silhouette thesis within the requested repair |
| recognizable only by title | BLOCK | enlarge identity cue and negative gap |
| muddy despite many colors | LIGHT | merge colors; widen value jobs |
| flat volume | LIGHT | one source; rebuild plane clusters |
| wrong material | FINISH | change plane, edge, highlight grammar |
| noisy | FINISH / CUT | reusable clusters and quiet gaps |
| tiny conversion looks like thumbnail | BLOCK | same-grid repair. Remove sampled micro-detail |
| tile repeats visibly | FINISH / PROVE | neutralize base, fix edges, move landmarks to variants |
| set looks coherent but interchangeable | BLOCK | strengthen item-specific silhouette cues |
