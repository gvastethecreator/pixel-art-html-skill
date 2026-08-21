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
- `evidence_tier`: authoring accepts only `fixture` or `draft`; defaults to `draft`. `representative` and `production-candidate` are written only by the reviewed `promote` command.
- `art_direction`: optional string-to-string direction card in canonical source metadata. Record use, projection, light, focus, or other proof-relevant decisions.
- `background`: `null`, `.`, `transparent`, a palette alias, or `#RGB`/`#RRGGBB`.
- `palette`: alias-to-color object. Aliases keep specs compact.
- `grid`: optional full grid. Rows: compact character string, whitespace-separated string, or JSON array. Compact rows need one-character aliases; suit unique silhouettes. `"....iill...."` is twelve cells. Clear cells: `.`, `..`, `null`, or `transparent`.
- `rects`: filled rectangles with `x`, `y`, `width`, `height`, `color`.
- `runs`: horizontal runs with `x`, `y`, `length`, `color`.
- `motifs`: reusable local cluster patterns. Each value is an equal-width row list: whitespace-separated strings, compact one-character strings, or JSON arrays. A row string that exactly matches a semantic palette alias is one cell, so a one-column motif can use `"grass"`. Use arrays to remove ambiguity. Clear tokens are transparent/no-op inside a motif.
- `stamps`: motif placements with `motif`, `x`, and `y`. Optional `flip_x`, `flip_y`, and `map` recolor aliases while preserving cluster topology.
- `pixels`: individual cells with `x`, `y`, `color`.

Apply order: background, `grid`, `rects`, `runs`, `stamps`, `pixels`. Later ops overwrite earlier cells. Coordinates are zero-based. A clear motif cell leaves the earlier layer unchanged.

Rectangles and runs for scaffolding and broad planes. Motifs for repeated foliage, clouds, brick chips, foam, lights, panel marks, or other coherent cluster grammar. Silhouette needing one-off local control: use a full grid. Do not force a complex subject into rectangles.

Compiler emits canonical JSON with a complete `grid` of `#RRGGBB` or `null` cells, plus authored evidence tier, source metadata, derived proof intent, and a deterministic `quality` risk report. `proofs.repeat_3x` is true only if `art_direction.use` identifies a tile, tileset, texture, or seamless master. If a compact source spec is easier to review, do not hand-author canonical output. The report is diagnostic, never a semantic quality score.

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

`analysis` is diagnostic provenance. Its inferred source grid never changes requested runtime dimensions. Detector confidence and reconstruction fidelity do not promote an artifact beyond its declared evidence tier. `manual_repair_required` is true for image-derived 8x8/16x16 unless an exact matching source lattice was preserved. Proof page surfaces that as a review warning. Optional external detector: stable detector/mode/result metadata. Never serialize executable paths.

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

Compile with `repair <canonical-baseline.json> <repair-spec.json>`. Dimensions default to the baseline but must never differ. Canonical repair source records `kind: manual-repair`, `manual_repair_status: authored-review-required`, full baseline grid/palette, the decisions, original analysis if present, and exact delta evidence. Validation recomputes baseline palette, dimensions, subject cells, changed cells, repaired subject cells, proof intents, and status. Edited metadata cannot fake the comparison.

Canonical palette arrays follow first raster appearance, not source declaration order. If order is not part of the test, compare palette sets or semantic source aliases.

## Resolution collections

Recommended square masters: `16`, `24`, `32`, `40`, `48`, and `64`. Single artifacts: any width and height from 8 through 128.

- Image input: pass `--sizes all` or a comma-separated list. Convert each target directly from the original image. `--reconstruction auto` preserves a trustworthy exact lattice only if it matches the target. Otherwise it uses two-stage target packing. Use `legacy` only for comparison.
- Text input: author one spec per target size, then pass the files to `collection`.
- Keep subject identity, pose, palette roles, and framing coherent across the set.
- Change detail density intentionally. Do not mechanically cascade from the largest grid.

Collection compiler writes `manifest.json`, a standalone comparison `index.html`, and one exact artifact directory per dimension.

## Direction studies

`study` accepts exactly three draft specs. All must have the same width and height and materially different grid topology. Validation canonicalizes color roles before comparison, so a palette swap over the same masses is rejected. It writes:

```text
index.html
blind.html
manifest.json
sample-a/{index.html,pixel-art.json,pixel-art.png}
sample-b/{index.html,pixel-art.json,pixel-art.png}
sample-c/{index.html,pixel-art.json,pixel-art.png}
```

Named overview preserves full direction metadata. Blind payload: anonymous labels, dimensions, background, palette, and exact grids. Validation proves blind grids still match the three children.

## Asset packs

Use `pack` if related artifacts share a resolution, or if item identity matters more than a resolution ladder. Each spec remains an independent master with its own title, direction card, canonical grid, PNG, and exact proof. Pack compiler derives Unicode-safe, accent-normalized stable item folders from titles; numeric suffixes only if titles collide.

```bash
python scripts/build_pixel_art.py pack potion.json key.json shield.json crystal.json --output pickup-pack --title "RPG pickups"
```

Pack writes a `kind: pack` manifest and a standalone overview. Same dimensions expected. Shared projection, lighting, palette roles, baseline, and padding must be reviewed as a set-level contract.

## Promoted review record

`promote` changes a validated draft to `representative` or `production-candidate` only after a valid blind review. Generated `visual-review.json` stores reviewer authority, observations, passed gates, the promoted tier, and SHA-256 fingerprints over width, height, background, palette, and exact grid.

Single artifact fingerprint key: `pixel-art.json`. Pack or collection root keys: `<item-path>/pixel-art.json`. Every item has a bound child record. Review input must include one observation per item path. The record is generated, not hand-authored. Later grid drift fails validation.
