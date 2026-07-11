# Artifact schema

Author a JSON object. Dimensions must be integers from 8 through 128.

```json
{
  "title": "Tiny lighthouse",
  "width": 16,
  "height": 16,
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
  "pixels": [
    {"x": 8, "y": 6, "color": "light"}
  ]
}
```

## Fields

- `title`: optional label.
- `width`, `height`: required unless both default to 32.
- `background`: `null`, `.`, `transparent`, a palette alias, or `#RGB`/`#RRGGBB`.
- `palette`: alias-to-color object. Aliases keep specs compact.
- `grid`: optional full grid. Each row may be a whitespace-separated string or a JSON array. Use `.`, `..`, `null`, or `transparent` for clear cells.
- `rects`: filled rectangles with `x`, `y`, `width`, `height`, `color`.
- `runs`: horizontal runs with `x`, `y`, `length`, `color`.
- `pixels`: individual cells with `x`, `y`, `color`.

Apply order: background, `grid`, `rects`, `runs`, `pixels`. Later operations overwrite earlier cells. All coordinates are zero-based.

The compiler emits canonical JSON with a complete `grid` of `#RRGGBB` or `null` cells. Do not hand-author canonical output when a compact source spec is easier to review.

## Resolution collections

Recommended square masters: `16`, `24`, `32`, `40`, `48`, and `64`. Single artifacts may use any width and height from 8 through 128.

- Image input: pass `--sizes all` or a comma-separated list. Convert each target directly from the original image.
- Text input: author one spec per target size, then pass the files to `collection`.
- Keep subject identity, pose, palette roles, and framing coherent across the set.
- Change detail density intentionally. Do not mechanically cascade from the largest grid.

The collection compiler writes `manifest.json`, a standalone comparison `index.html`, and one exact artifact directory per dimension.
