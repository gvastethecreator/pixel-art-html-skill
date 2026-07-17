# Pixel-art quality contract

This is the acceptance rubric. Use [craft-workflow.md](craft-workflow.md) for construction and [subject-recipes.md](subject-recipes.md) for subject-specific decisions.

## Required reads

The artifact must pass all applicable rows. Record `N/A` only with a concrete reason.

| Gate | Acceptance |
|---|---|
| Silhouette | subject, orientation, and pose read at native 1x without interior detail |
| Composition | one dominant mass/read, one focal cue, intentional padding or edge contact |
| Projection | every compatible element follows one view, scale, and overlap convention |
| Value | dark/mid/light groups separate major planes and focus in grayscale |
| Palette | each color has a job; ramps shift hue/value coherently; no unused or redundant colors |
| Light | one declared source controls plane light, cast shadows, edge hardness, and mood |
| Clusters | connected deliberate shapes dominate; single pixels are intentional accents, not noise |
| Materials | texture grammar matches material and scales down with distance/resolution |
| Focus | highest contrast/chroma/detail supports the intended focal point or gameplay read |
| Edges | hard pixel edges, integer scaling, clean alpha, no automatic anti-aliasing or fringe |
| Context | tiles loop, repeated props avoid obvious landmarks, backgrounds do not compete, as applicable; tile/texture specs expose the automatic 3x repeat proof |
| Animation handoff | frame masters preserve identity and native cell scale; state workflow, order, durations, loop, runtime cell, safe margin, and ground/contact pivot are explicit before atlas extraction |
| Output | canonical JSON, PNG, and standalone HTML agree exactly and use no network requests; validation checks PNG dimensions and RGBA cell parity |

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

- `contain` preserves complete icons/characters; `cover` fills scenes; `stretch` is explicit distortion.
- Final crop preserves identity features and required negative space.
- Alpha edges have no source-background halo.
- Quantization noise has been replaced with authored clusters.
- Palette count is within the requested limit and still provides value separation.
- The exact grid, not the source image, carries recognition.

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
- Rectangular scaffolds, default ellipses, or generic outlines remain visible as construction shortcuts.
- Pillow shading, contradictory projection, light, scale, or shadow rules flatten the form.
- Texture is homogeneous noise, a photographic downscale, or scattered orphan pixels.
- More colors/details were added without a new readable job.
- The background has equal or greater contrast/detail than the focal subject.
- Any requested collection master is missing or mechanically resized from another master.
- Browser proof is absent, blurry, clipped, empty, or not the final generated artifact.
- HTML depends on a server, CDN, external font, framework, or network request.
