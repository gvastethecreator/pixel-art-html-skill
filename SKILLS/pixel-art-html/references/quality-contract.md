# Pixel-art quality contract

Acceptance rubric. Construction: [craft-workflow.md](craft-workflow.md). Subject decisions: [subject-recipes.md](subject-recipes.md).

## Required reads

The artifact must pass all applicable rows. Record `N/A` only with a concrete reason.

| Gate | Acceptance |
|---|---|
| Evidence tier | authoring: `fixture` or `draft` only. Promoted tiers need a valid fingerprint-bound `visual-review.json` |
| Resolution fit | honor fixed runtime grids. Else enough cells for identity, materials, signature. Do not hide a weak silhouette |
| Direction | recovery / direction-risk work uses a validated three-item same-grid study. Record blind selection, signature, subtraction |
| Silhouette | subject, orientation, pose read at native 1x without interior detail |
| Composition | one dominant mass/read, one focal cue, intentional padding or edge contact |
| Projection | every compatible element follows one view, scale, and overlap convention |
| Value | dark/mid/light groups separate major planes and focus in grayscale |
| Palette | each color has a job. Ramps shift hue/value coherently. No unused or redundant colors |
| Light | one declared source controls plane light, cast shadows, edge hardness, mood |
| Clusters | connected deliberate shapes dominate. Single pixels are intentional accents, not noise |
| Materials | texture grammar matches material and scales down with distance/resolution |
| Specificity | at least one useful shape or construction decision more specific than a stock pictogram, without weakening recognition |
| Focus | highest contrast/chroma/detail supports the intended focal point or gameplay read |
| Edges | hard pixel edges, integer scaling, clean alpha, no automatic anti-aliasing or fringe |
| Context | tiles loop; repeated props avoid obvious landmarks; backgrounds do not compete, as applicable. Tile/texture specs expose the automatic 3x repeat proof |
| Animation handoff | frame masters preserve identity and native cell scale. State workflow, order, durations, loop, runtime cell, safe margin, and ground/contact pivot before atlas extraction |
| Output | canonical JSON, PNG, and standalone HTML agree exactly; no network requests. Validation checks PNG dimensions and RGBA cell parity |
| Blind read | promoted evidence records title-free subject, orientation/action, material, focus, signature, mismatch, browser proof, and per-item set reads if applicable |

## Evidence tiers and claim safety

- `fixture` proves a mechanic (alpha, timing, extraction, atlas layout, parity). Invalid for artistic quality even if every structural check passes.
- `draft` is incomplete or unreviewed. Direction decisions only — not a finished showcase.
- `representative` is the skill's normal quality path. Created only by `promote` with a non-builder review bound to the exact grid.
- `production-candidate` targets a real project. Created only by `promote` with an owner review. Still not deployment approval.

Authoring defaults to `draft` and rejects `representative`, `production-candidate`, and the unsupported label `production`. Direction search, title-free perceptual gate, and promotion: [visual-review.md](visual-review.md).

## Resolution ladder

- 8x8: orientation, silhouette, one identity cue. Omission is the aesthetic.
- 16x16: silhouette, pose, one material/focal break, two or three texture clusters max.
- 24x24: one secondary form or material region.
- 32x32: balanced default master with deliberate light and cluster hierarchy.
- 40x40: one added detail tier without changing the established silhouette.
- 48x48: controlled surface information. Avoid scattered single pixels.
- 64x64: preserve low-resolution cluster rhythm. Extra cells are not a duty to fill.

Text-authored sizes are independent masters. Image-derived sizes convert from the original source, then get size-specific cleanup. A downscaled 64x64 is not a responsive 16x16 master.

## Image conversion acceptance

Canonical source metadata records classified source type, confidence, detector, requested target, inferred lattice if available, and applied reconstruction. Exact-grid sources are nearest-preserved only if their lattice matches the requested target. Detected source dimensions never override a fixed runtime grid. Pseudo-pixel and painterly sources use target-aware structure/color packing before the final palette clamp. Legacy resize-first output is comparison evidence only.

`contain` preserves complete icons/characters. `cover` fills scenes. `stretch` is explicit distortion. Final crop preserves identity features and required negative space. Alpha edges have no source-background halo. Replace quantization noise with authored clusters. Palette count within the requested limit and still provides value separation. The exact grid, not the source image, carries recognition.

At 8x8 and 16x16, automatic reconstruction stays `draft` until a human or agent explicitly repairs the silhouette and one identity cue and passes the title-free native-scale read. Representative 8x8/16x16 image recovery preserves the losing canonical baseline, records silhouette/identity/subtraction decisions, and exposes a same-grid blind before/after proof. A non-empty changed-cell delta proves intervention, not improvement. Reconstruction benchmark metrics can justify routing changes — they do not measure composition, specificity, material read, or artistic quality.

If the source is not already pixel-clean, read [image-source-brief.md](image-source-brief.md) before generation or conversion.

## Deterministic critique signals

`critique` reports subject bounds, same-color cluster count, singleton clusters, palette value span, and low-contrast boundary ratio. Review prompts, never a quality score: an eye glint, star, or spark can be a correct singleton; a soft fog scene can correctly use low boundary contrast; a scene background can intentionally touch every edge; a report without warnings can still describe weak composition or anatomy.

If the background is transparent, `subject_cells` includes every painted cell. If opaque, it excludes that background. Do not compare that count across background modes as if it were a normalized density score.

Resolve every warning through visual inspection or state why it is intentional.

## Rejection conditions

- Native 1x read needs the title or source image to be understood.
- A clean deterministic report presented as proof the art is good.
- A fixture or draft presented as representative or production evidence, or a source spec self-assigns a promoted tier.
- Three candidate directions differ only by palette, ornament, or detail density.
- Rectangular scaffolds, default ellipses, or generic outlines remain visible as construction shortcuts.
- Pillow shading, contradictory projection, light, scale, or shadow rules flatten the form.
- Texture is homogeneous noise, a photographic downscale, or scattered orphan pixels.
- More colors/details added without a new readable job.
- Declared material inferred only from hue — silhouette, planes, edges, and highlights do not support it.
- Every item recognizable but interchangeable with a stock pictogram — no useful signature or specific construction survives.
- Background has equal or greater contrast/detail than the focal subject.
- Any requested collection master is missing or mechanically resized from another master.
- An image-derived 8x8/16x16 artifact promoted without an authored same-grid repair record, title-hidden baseline comparison, and fingerprint-bound reviewer record.
- Browser proof absent, blurry, clipped, empty, or not the final generated artifact.
- HTML depends on a server, CDN, external font, framework, or network request.
