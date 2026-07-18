# Artifact schema

Author a JSON object. Dimensions must be integers from 8 through 128.

```json
{
  "title": "Tiny lighthouse",
  "width": 16,
  "height": 16,
  "evidence_tier": "draft",
  "art_direction": {
    "use": "scene",
    "projection": "side view",
    "light": "upper-left moonlight",
    "focus": "warm lantern"
  },
  "background": null,
  "palette": {
    "ink": "#172038",
    "light": "#FFD166",
    "foam": "#EAF6FF"
  },
  "rects": [
    {"x": 7, "y": 5, "width": 3, "height": 8, "color": "foam"}
  ],
  "runs": [
    {"x": 4, "y": 13, "length": 9, "color": "ink"}
  ],
  "motifs": {
    "foam": [". foam foam .", "foam foam foam foam"]
  },
  "stamps": [
    {"motif": "foam", "x": 1, "y": 14},
    {"motif": "foam", "x": 10, "y": 12, "flip_x": true}
  ],
  "pixels": [
    {"x": 8, "y": 6, "color": "light"}
  ]
}
```

## Fields

- `title`: optional label.
- `width`, `height`: required unless both default to 32.
- `evidence_tier`: `fixture`, `draft`, `representative`, or `production-candidate`. Defaults to `draft`. The compiler rejects `production` because a spec cannot approve itself.
- `art_direction`: optional string-to-string direction card preserved in canonical source metadata. Record use, projection, light, focus, or other proof-relevant decisions.
- `background`: `null`, `.`, `transparent`, a palette alias, or `#RGB`/`#RRGGBB`.
- `palette`: alias-to-color object. Aliases keep specs compact.
- `grid`: optional full grid. Each row may be a compact character string, a whitespace-separated string, or a JSON array. Compact rows require one-character palette aliases and are ideal for unique silhouettes; `"....iill...."` is twelve cells. Use `.`, `..`, `null`, or `transparent` for clear cells.
- `rects`: filled rectangles with `x`, `y`, `width`, `height`, `color`.
- `runs`: horizontal runs with `x`, `y`, `length`, `color`.
- `motifs`: reusable local cluster patterns. Each value is an equal-width row list; rows may be whitespace-separated strings, compact one-character strings, or JSON arrays. A row string that exactly matches a semantic palette alias is one cell, so a one-column motif may use `"grass"`; use arrays to remove ambiguity. Clear tokens are transparent/no-op inside a motif.
- `stamps`: motif placements with `motif`, `x`, and `y`; optional `flip_x`, `flip_y`, and `map` recolor aliases while preserving cluster topology.
- `pixels`: individual cells with `x`, `y`, `color`.

Apply order: background, `grid`, `rects`, `runs`, `stamps`, `pixels`. Later operations overwrite earlier cells. All coordinates are zero-based. A clear motif cell leaves the earlier layer unchanged.

Use rectangles and runs for scaffolding and broad planes. Use motifs for repeated foliage, clouds, brick chips, foam, lights, panel marks, or other coherent cluster grammar. Use a full grid when the silhouette needs one-off local control; do not force a complex subject into rectangles.

The compiler emits canonical JSON with a complete `grid` of `#RRGGBB` or `null` cells, the declared `evidence_tier`, source metadata, derived proof intent, and a deterministic `quality` risk report. `proofs.repeat_3x` is true only when `art_direction.use` identifies a tile, tileset, texture, or seamless master. Do not hand-author canonical output when a compact source spec is easier to review. The report is diagnostic and never a semantic quality score.

Image-derived canonical output also records:

```json
{
  "source": {
    "kind": "image",
    "requested_reconstruction": "auto",
    "reconstruction": "two-stage",
    "structure_colors": 16,
    "manual_repair_required": true,
    "analysis": {
      "class": "pseudo-pixel",
      "confidence": "medium",
      "detector": "local-target-analysis",
      "inferred_grid": {"width": 24, "height": 24, "step_x": 5.5, "step_y": 5.5},
      "target_grid": {"width": 16, "height": 16},
      "metrics": {},
      "reasons": []
    }
  }
}
```

`analysis` is diagnostic provenance. Its inferred source grid never changes the requested runtime dimensions, and neither detector confidence nor reconstruction fidelity promotes an artifact beyond its declared evidence tier. `manual_repair_required` is true for image-derived 8x8/16x16 output unless an exact matching source lattice was preserved; the proof page surfaces the requirement as a review warning. An optional external detector is recorded by stable detector/mode/result metadata; executable paths are never serialized.

## Authored repair specs

Use the normal spec fields plus three mandatory decisions:

```json
{
  "title": "Bound flask — 8x8 repair",
  "width": 8,
  "height": 8,
  "evidence_tier": "draft",
  "palette": {"i": "#1A1022", "r": "#9A1230", "a": "#D89238"},
  "grid": ["........", "...aa...", "...ii...", "..irri..", ".iarri..", ".irrri..", "..ii....", "........"],
  "repair_decisions": {
    "silhouette": "broad shoulder and round body",
    "identity_cue": "descending amber binding",
    "subtraction": "remove sampled microfacets and isolated glints"
  }
}
```

Compile it with `repair <canonical-baseline.json> <repair-spec.json>`. Dimensions default to the baseline but may never differ. The canonical repair source records `kind: manual-repair`, `manual_repair_status: authored-review-required`, full baseline grid/palette, the decisions, original analysis when present, and exact delta evidence. Validation recomputes the baseline palette, dimensions, subject cells, changed cells, repaired subject cells, proof intents, and status so edited metadata cannot fake the comparison.

Canonical palette arrays follow first raster appearance, not source declaration order. Compare palette sets or semantic source aliases when order is not itself part of the test.

## Resolution collections

Recommended square masters: `16`, `24`, `32`, `40`, `48`, and `64`. Single artifacts may use any width and height from 8 through 128.

- Image input: pass `--sizes all` or a comma-separated list. Convert each target directly from the original image. `--reconstruction auto` preserves a trustworthy exact lattice only when it matches the target and otherwise uses two-stage target packing; use `legacy` only for comparison.
- Text input: author one spec per target size, then pass the files to `collection`.
- Keep subject identity, pose, palette roles, and framing coherent across the set.
- Change detail density intentionally. Do not mechanically cascade from the largest grid.

The collection compiler writes `manifest.json`, a standalone comparison `index.html`, and one exact artifact directory per dimension.

## Asset packs

Use `pack` when related artifacts share a resolution or when item identity matters more than a resolution ladder. Each spec remains an independent master with its own title, direction card, canonical grid, PNG, and exact proof. The pack compiler derives Unicode-safe, accent-normalized stable item folders from titles and adds numeric suffixes only when titles collide.

```bash
python scripts/build_pixel_art.py pack potion.json key.json shield.json crystal.json --output pickup-pack --title "RPG pickups"
```

The pack writes a `kind: pack` manifest and a standalone overview. Same dimensions are expected; shared projection, lighting, palette roles, baseline, and padding must be reviewed as a set-level contract.
