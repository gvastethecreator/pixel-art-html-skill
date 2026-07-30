# Blind review and promotion

Structural validation proves exact files. Promotion records that a real reviewer identified the final grid without the context that helped build it.

## Claim boundary

| Tier | Created by | Meaning |
|---|---|---|
| `fixture` | authoring command | mechanics-only evidence; never an art-quality sample |
| `draft` | authoring command | incomplete or not independently accepted |
| `representative` | `promote` | accepted through the normal quality path by a non-builder reviewer |
| `production-candidate` | `promote` | accepted by the project owner for project consideration; still not deployed approval |

A spec or image command can author only `fixture` or `draft`. A self-review can improve a draft but cannot promote it.

## Direction study

Use `study` when work was rejected, a quality claim matters, or the direction is uncertain.

1. Keep subject, use, grid, background context, and proof scale fixed.
2. Author exactly three draft grids with different silhouette or construction theses.
3. Open `blind.html`; it contains no titles, source metadata, evidence tiers, direction text, or metrics.
4. Record the winning sample, the reason each other sample loses, one signature to preserve, and one generic element to remove.
5. Open the named overview only after selection.

If the grids are identical or dimensions differ, the runner rejects the study.

## Review order

Review the final generated output, not a source sketch or older screenshot:

1. Native 1x: name subject, orientation, and action.
2. Silhouette: confirm the same read without interior detail.
3. Value: identify major planes and the first focal point.
4. Material: name it from plane, edge, highlight, and cluster behavior.
5. Signature: state what is remembered after looking away.
6. Context: inspect real background, neighboring assets, set order, or repeat.
7. Browser: confirm crisp final pixels, complete crop, and no hidden/clipped art.

Enable the proof page's blind control before step 1. It hides title, source, tier, palette, facts, metrics, and export context while leaving the art and perceptual proofs visible.

## Review input

Copy [visual-review-input.json](../assets/visual-review-input.json). Replace every empty or failed field with what the reviewer actually observed. Do not infer a pass from the brief.

Required observations:

- `subject`
- `orientation_action`
- `material`
- `focal_cue`
- `signature`
- `mismatch`

Required passed gates:

- `blind_read`
- `native_silhouette`
- `value_hierarchy`
- `material_read`
- `focal_read`
- `browser_proof`

For a collection or pack, `observations.items` must contain one non-empty blind read keyed by every manifest item path, and `set_context` must pass.

Reviewer kinds:

- `self`: structured author review; cannot promote;
- `user`: may promote to `representative`;
- `independent-agent`: may promote to `representative` only if that fresh agent actually saw the unlabeled proof;
- `owner`: may promote to either tier and is required for `production-candidate`.

## Promotion

```bash
python <skill-dir>/scripts/build_pixel_art.py promote <draft-output> <review-input.json> --tier representative
```

The command:

- revalidates JSON/PNG/HTML parity;
- refuses fixtures, already-promoted output, and direction studies;
- validates reviewer authority, observations, and gates;
- fingerprints width, height, background, palette, and every exact grid cell;
- writes canonical `visual-review.json`;
- updates the evidence tier and embedded proof;
- validates the promoted output again.

For a set, every child receives the same bound review and the root record binds every child path. Later pixel drift, a stale proof page, a missing item observation, or a changed fingerprint fails `validate`.

If a suitable reviewer is unavailable, hand back a verified `draft` and state that artistic acceptance remains unassessed.
