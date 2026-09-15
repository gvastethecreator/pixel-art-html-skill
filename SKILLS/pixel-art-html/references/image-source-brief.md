# Image-source brief and repixelization

Use for Codex ImageGen, an attached image, a local render, or a photo/reference that will become exact-grid pixel art. Source supplies composition and shape evidence; it does not satisfy the final pixel-art contract.

Choose one source direction before construction. Follow the [single-pass contract](../SKILL.md#single-pass-delivery); generate alternatives only when explicitly requested. A source concept does not satisfy the exact-grid artifact or its review requirements.

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

For generation, describe craft properties, not an artist name:

```text
[subject and action], [projection and crop], centered readable silhouette with [identity cue],
large connected shape groups, [light direction] with three broad value bands,
controlled [palette mood] palette, [material regions] separated clearly,
quiet [transparent/removable/flat] background, no text, no watermark,
no tiny decorative clutter, composition designed to survive a [W]x[H] exact pixel grid
```

Hard pixel edges in the source can help. Never trust a model-generated image for a correct grid, palette, or cluster topology.

## Conversion is a draft

1. Preserve the accepted source inside the project.
2. Classify the source as `exact-grid`, `pseudo-pixel`, or `painterly`. Review confidence, reasons, and any inferred lattice. Override only with visual evidence.
3. Crop and choose `contain` or `cover` based on use. Use `stretch` only for intentional distortion.
4. Convert every target size directly from the original source. Leave `--reconstruction auto`. It preserves an exact matching lattice and uses target-aware two-stage packing otherwise.
5. Inspect silhouette, crop, alpha fringe, value groups, palette, focal cue, and the recovered source-lattice overlay.
6. When manual repixelization is part of the brief, use the conversion as a scaffold for one progressive construction pass. At 8x8 or 16x16, reserve the silhouette and one identity cue before detail. A conversion-only request ends with the inspected draft and its limits.
7. Export and inspect the result at native 1x, 2x, and 4x. Record failures without starting another artistic repair cycle. Technical export corrections remain allowed.

Image quantization preserves photographic or model noise well. Manual repixelization uses the same pass order as text authoring: silhouette -> projection -> value/palette -> directional light -> material clusters -> focus/cleanup.

If the source is already pixel-clean and its lattice matches the target, automatic reconstruction selects nearest-neighbor preservation. If quantization speckle is visible, `--min-cluster 2` can merge one-cell color islands into adjacent opaque colors without eroding alpha. Opt-in cleanup draft — it does not replace a decision about which glints and accents are intentional. Read [source-recovery.md](source-recovery.md) for classifier evidence, two-stage behavior, benchmark usage, and the optional detector boundary.

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

- Depth planes already separated by value and scale.
- Source leaves a quiet action/focal area.
- Distant details can be removed cleanly.
- Haze and sky-color shifts survive palette reduction.

### Transparent icon

- Real breathing room on every required side.
- Background is flat/removable with no glow or color spill.
- Semi-transparent edge halos absent or easy to replace.
- Silhouette works before interior texture.

## Record an unsuitable source when

- identity depends on detail smaller than the target grid
- limbs, props, or focal features are clipped
- source mixes projections or multiple incompatible lights
- background contaminates subject edges
- every surface has photographic texture or micro-contrast
- palette reduction merges the subject into the background
- a cleaner source costs less than a manual rescue of the conversion

State the limiting source property. Regeneration requires an explicit request; an unsuitable source does not authorize alternatives or retries.
