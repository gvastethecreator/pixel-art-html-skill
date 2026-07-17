# Artifact schema

Author a JSON object. Dimensions must be integers from 8 through 128.

```json
{
  "title": "Tiny lighthouse",
  "width": 16,
  "height": 16,
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
- `art_direction`: optional string-to-string direction card preserved in canonical source metadata. Record use, projection, light, focus, or other proof-relevant decisions.
- `background`: `null`, `.`, `transparent`, a palette alias, or `#RGB`/`#RRGGBB`.
- `palette`: alias-to-color object. Aliases keep specs compact.
- `grid`: optional full grid. Each row may be a whitespace-separated string or a JSON array. Use `.`, `..`, `null`, or `transparent` for clear cells.
- `rects`: filled rectangles with `x`, `y`, `width`, `height`, `color`.
- `runs`: horizontal runs with `x`, `y`, `length`, `color`.
- `motifs`: reusable local cluster patterns. Each value is an equal-width row list; rows may be whitespace-separated strings, compact one-character strings, or JSON arrays. Clear tokens are transparent/no-op inside a motif.
- `stamps`: motif placements with `motif`, `x`, and `y`; optional `flip_x`, `flip_y`, and `map` recolor aliases while preserving cluster topology.
- `pixels`: individual cells with `x`, `y`, `color`.

Apply order: background, `grid`, `rects`, `runs`, `stamps`, `pixels`. Later operations overwrite earlier cells. All coordinates are zero-based. A clear motif cell leaves the earlier layer unchanged.

Use rectangles and runs for scaffolding and broad planes. Use motifs for repeated foliage, clouds, brick chips, foam, lights, panel marks, or other coherent cluster grammar. Use a full grid when the silhouette needs one-off local control; do not force a complex subject into rectangles.

The compiler emits canonical JSON with a complete `grid` of `#RRGGBB` or `null` cells, source metadata, and a deterministic `quality` risk report. Do not hand-author canonical output when a compact source spec is easier to review. The report is diagnostic and never a semantic quality score.

## Resolution collections

Recommended square masters: `16`, `24`, `32`, `40`, `48`, and `64`. Single artifacts may use any width and height from 8 through 128.

- Image input: pass `--sizes all` or a comma-separated list. Convert each target directly from the original image.
- Text input: author one spec per target size, then pass the files to `collection`.
- Keep subject identity, pose, palette roles, and framing coherent across the set.
- Change detail density intentionally. Do not mechanically cascade from the largest grid.

The collection compiler writes `manifest.json`, a standalone comparison `index.html`, and one exact artifact directory per dimension.
