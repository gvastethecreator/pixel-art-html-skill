# Image-source brief and repixelization

Use this reference for Codex ImageGen, an attached image, a local render, or a photo/reference that will become exact-grid pixel art. A source image supplies composition and shape evidence; it does not satisfy the final pixel-art contract.

For a representative, production-candidate, or recovery task with direction risk, generate or sketch three materially different concepts from the same source brief before selecting one. The concepts prove a direction decision only; the manually repixelized exact grid remains the artifact.

## Build the source brief

Specify the target before generating or choosing a source:

```text
Final use and exact grid:
Subject, pose, orientation, and crop:
Projection and camera height:
Dominant silhouette and one identity cue:
Three or four broad value groups:
Palette mood and accent placement:
Single light direction and shadow hardness:
Large material regions:
Background and negative-space requirement:
Details that must survive / details to omit:
```

For generation, describe the image using craft properties instead of an artist name:

```text
[subject and action], [projection and crop], centered readable silhouette with [identity cue],
large connected shape groups, [light direction] with three broad value bands,
controlled [palette mood] palette, [material regions] separated clearly,
quiet [transparent/removable/flat] background, no text, no watermark,
no tiny decorative clutter, composition designed to survive a [W]x[H] exact pixel grid
```

Hard pixel edges in the source can help, but never trust a model-generated image to contain a correct grid, palette, or cluster topology.

## Conversion is a draft

1. Preserve the accepted source inside the project.
2. Classify the source as `exact-grid`, `pseudo-pixel`, or `painterly`. Review confidence, reasons, and any inferred lattice; override only with visual evidence.
3. Crop and choose `contain` or `cover` based on use; use `stretch` only for intentional distortion.
4. Convert every target size directly from the original source. Leave `--reconstruction auto`: it preserves an exact matching lattice and uses target-aware two-stage packing otherwise.
5. Inspect silhouette, crop, alpha fringe, value groups, palette, focal cue, and the recovered source-lattice overlay.
6. Open the canonical grid or reconstruct it as a spec. Merge noisy colors, repair stair steps, replace source texture with cluster motifs, and remove accidental singletons.
7. At 8x8 or 16x16, redraw the silhouette and one identity cue rather than accepting the automatic cell choices. Omission is part of the deliverable.
8. Rebuild and compare at native 1x, 2x, and 4x.

Image quantization preserves photographic/model noise surprisingly well. Manual repixelization must reassert the same pass order as text authoring: silhouette -> projection -> value/palette -> directional light -> material clusters -> focus/cleanup.

For an already pixel-clean source whose lattice matches the target, automatic reconstruction selects nearest-neighbor preservation. For visible quantization speckle, `--min-cluster 2` may merge one-cell color islands into adjacent opaque colors without eroding alpha; it is an opt-in cleanup draft, not a replacement for deciding which glints and accents are intentional. Read [source-recovery.md](source-recovery.md) for classifier evidence, two-stage behavior, benchmark usage, and the optional detector boundary.

## Source-specific checks

### Character or creature

- Pose and line of action survive the crop.
- Head, hands, weapon, hair, horns, or other identity cue have enough cell budget.
- Limbs do not merge into the torso or background.
- Costume detail can collapse into large equipment/color regions.

### Object, vehicle, or building

- Functional components remain distinguishable.
- Projection and visible faces are unambiguous.
- Highlights and stripes follow volume rather than image-space decoration.
- Repeated modules can become motifs instead of unique noisy detail.

### Landscape or background

- Depth planes are already separated by value and scale.
- The source leaves a quiet action/focal area.
- Distant details can be removed cleanly.
- Haze and sky-color shifts survive palette reduction.

### Transparent icon

- There is real breathing room on every required side.
- The background is flat/removable with no glow or color spill.
- Semi-transparent edge halos are absent or easy to replace.
- The silhouette works before interior texture.

## Reject or regenerate the source when

- the identity depends on detail smaller than the target grid;
- limbs, props, or focal features are clipped;
- the source mixes projections or multiple incompatible lights;
- the background contaminates subject edges;
- every surface has photographic texture or micro-contrast;
- palette reduction merges the subject into the background;
- a cleaner source would cost less than manually rescuing the conversion.
