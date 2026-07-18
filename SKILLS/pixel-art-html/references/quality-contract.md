# Pixel-art quality contract

This is the acceptance rubric. Use [craft-workflow.md](craft-workflow.md) for construction and [subject-recipes.md](subject-recipes.md) for subject-specific decisions.

## Required reads

The artifact must pass all applicable rows. Record `N/A` only with a concrete reason.

| Gate | Acceptance |
|---|---|
| Evidence tier | artifact declares `fixture`, `draft`, `representative`, or `production-candidate`; claims stay inside that tier |
| Resolution fit | fixed runtime grids are honored; otherwise the chosen grid has enough cells for the declared identity, materials, and signature without using resolution to hide a weak silhouette |
| Direction | recovery and direction-risk quality work compares three materially different candidates; selection, signature, and subtraction are recorded |
| Silhouette | subject, orientation, and pose read at native 1x without interior detail |
| Composition | one dominant mass/read, one focal cue, intentional padding or edge contact |
| Projection | every compatible element follows one view, scale, and overlap convention |
| Value | dark/mid/light groups separate major planes and focus in grayscale |
| Palette | each color has a job; ramps shift hue/value coherently; no unused or redundant colors |
| Light | one declared source controls plane light, cast shadows, edge hardness, and mood |
| Clusters | connected deliberate shapes dominate; single pixels are intentional accents, not noise |
| Materials | texture grammar matches material and scales down with distance/resolution |
| Specificity | at least one useful shape or construction decision makes the subject more specific than a stock pictogram without weakening recognition |
| Focus | highest contrast/chroma/detail supports the intended focal point or gameplay read |
| Edges | hard pixel edges, integer scaling, clean alpha, no automatic anti-aliasing or fringe |
| Context | tiles loop, repeated props avoid obvious landmarks, backgrounds do not compete, as applicable; tile/texture specs expose the automatic 3x repeat proof |
| Animation handoff | frame masters preserve identity and native cell scale; state workflow, order, durations, loop, runtime cell, safe margin, and ground/contact pivot are explicit before atlas extraction |
| Output | canonical JSON, PNG, and standalone HTML agree exactly and use no network requests; validation checks PNG dimensions and RGBA cell parity |
| Blind read | representative and production-candidate evidence is reviewed title-free; observed subject, material, focus, signature, family read, and mismatch are recorded |

## Evidence tiers and claim safety

- `fixture` proves a mechanic such as alpha, timing, extraction, atlas layout, or parity. It is invalid evidence for artistic quality even when every structural check passes.
- `draft` is incomplete or unreviewed. Use it for direction decisions, not as a finished showcase.
- `representative` demonstrates the skill's normal quality path and requires a completed `visual-review.md` beside the output.
- `production-candidate` targets a real project and requires the same record plus explicit owner/reviewer approval. The label itself is never approval.

The compiler defaults to `draft` and rejects the self-certifying label `production`. Read [visual-review.md](visual-review.md) for direction search, the title-free perceptual gate, and review-record requirements.

## Resolution ladder

- 8x8: orientation, silhouette, and one identity cue; omission is the aesthetic.
- 16x16: silhouette, pose, one material/focal break, two or three texture clusters maximum.
- 24x24: one secondary form or material region.
- 32x32: balanced default master with deliberate light and cluster hierarchy.
- 40x40: one added detail tier without changing the established silhouette.
- 48x48: controlled surface information; avoid scattered single pixels.
- 64x64: preserve low-resolution cluster rhythm; extra cells do not create a duty to fill them.

Text-authored sizes are independent masters. Image-derived sizes convert from the original source and then receive size-specific cleanup. A downscaled 64x64 grid is not a responsive 16x16 master.

## Image conversion acceptance

- Canonical source metadata records the classified source type, confidence, detector, requested target, inferred lattice when available, and applied reconstruction.
- Exact-grid sources are nearest-preserved only when their lattice matches the requested target; detected source dimensions never override a fixed runtime grid.
- Pseudo-pixel and painterly sources use target-aware structure/color packing before the final palette clamp; legacy resize-first output is comparison evidence only.
- `contain` preserves complete icons/characters; `cover` fills scenes; `stretch` is explicit distortion.
- Final crop preserves identity features and required negative space.
- Alpha edges have no source-background halo.
- Quantization noise has been replaced with authored clusters.
- Palette count is within the requested limit and still provides value separation.
- The exact grid, not the source image, carries recognition.
- At 8x8 and 16x16, automatic reconstruction remains `draft` until a human or agent explicitly repairs the silhouette and one identity cue and passes the title-free native-scale read.
- Reconstruction benchmark metrics may justify routing changes, but they do not measure composition, specificity, material read, or artistic quality.

Read [image-source-brief.md](image-source-brief.md) before generation or conversion when the source is not already pixel-clean.

## Deterministic critique signals

`critique` reports subject bounds, same-color cluster count, singleton clusters, palette value span, and low-contrast boundary ratio. These are review prompts, never a quality score:

- an eye glint, star, or spark may be a correct singleton;
- a soft fog scene may correctly use low boundary contrast;
- a scene background may intentionally touch every edge;
- a report without warnings can still describe weak composition or anatomy.

`subject_cells` excludes the declared opaque background but includes every painted cell when the background is transparent. Do not compare that count across different background modes as if it were a normalized density score.

Resolve every warning through visual inspection or state why it is intentional.

## Rejection conditions

- The native 1x read needs the title or source image to be understood.
- A clean deterministic report is presented as proof that the art is good.
- A fixture or draft is presented as representative or production evidence.
- Three candidate directions differ only by palette, ornament, or detail density.
- Rectangular scaffolds, default ellipses, or generic outlines remain visible as construction shortcuts.
- Pillow shading, contradictory projection, light, scale, or shadow rules flatten the form.
- Texture is homogeneous noise, a photographic downscale, or scattered orphan pixels.
- More colors/details were added without a new readable job.
- The declared material is inferred only from hue; silhouette, planes, edges, and highlights do not support it.
- Every item is recognizable but interchangeable with a stock pictogram because no useful signature or specific construction survives.
- The background has equal or greater contrast/detail than the focal subject.
- Any requested collection master is missing or mechanically resized from another master.
- Browser proof is absent, blurry, clipped, empty, or not the final generated artifact.
- HTML depends on a server, CDN, external font, framework, or network request.
