# Blind review and promotion

Structural validation proves exact files. Promotion: a real reviewer identified the final grid without the context that helped build it.

## Claim boundary

| Tier | Created by | Meaning |
|---|---|---|
| `fixture` | authoring command | mechanics-only. Never an art-quality sample |
| `draft` | authoring command | incomplete or not independently accepted |
| `representative` | `promote` | accepted on the normal quality path by a non-builder |
| `production-candidate` | `promote` | accepted by the project owner for project consideration. Still not deployed approval |

A spec or image command can author only `fixture` or `draft`. Self-review can improve a draft but cannot promote.

## Direction study

Use `study` if work was rejected, a quality claim matters, or the direction is uncertain.

1. Keep subject, use, grid, background context, and proof scale fixed.
2. Author exactly three draft grids with different silhouette or construction theses.
3. Open `blind.html` — no titles, source metadata, evidence tiers, direction text, or metrics.
4. Record the winning sample, why each other sample loses, one signature to preserve, and one generic element to remove.
5. Open the named overview only after selection.

If the grids are identical or dimensions differ, the runner rejects the study.

## Review order

Review final generated output, not a source sketch or older screenshot:

1. Native 1x: subject, orientation, action.
2. Silhouette: same read without interior detail.
3. Value: major planes and first focal point.
4. Material: from plane, edge, highlight, cluster behavior.
5. Signature: what is remembered after looking away.
6. Context: real background, neighboring assets, set order, or repeat.
7. Browser: crisp final pixels, complete crop, no hidden/clipped art.

Enable the proof page's blind control before step 1 — hides title, source, tier, palette, facts, metrics, and export context; leaves art and perceptual proofs visible.

## Review input

Copy [visual-review-input.json](../assets/visual-review-input.json). Fill every empty or failed field with what the reviewer actually observed. Do not infer a pass from the brief.

Required observations: `subject`, `orientation_action`, `material`, `focal_cue`, `signature`, `mismatch`.

Required passed gates: `blind_read`, `native_silhouette`, `value_hierarchy`, `material_read`, `focal_read`, `browser_proof`.

For a collection or pack, `observations.items` must contain one non-empty blind read keyed by every manifest item path, and `set_context` must pass.

Reviewer kinds: `self` (structured author review; cannot promote); `user` (can promote to `representative`); `independent-agent` (can promote to `representative` only if that fresh agent actually saw the unlabeled proof); `owner` (either tier; required for `production-candidate`).

## Promotion

```bash
python <skill-dir>/scripts/build_pixel_art.py promote <draft-output> <review-input.json> --tier representative
```

Revalidates JSON/PNG/HTML parity. Refuses fixtures, already-promoted output, and direction studies. Validates reviewer authority, observations, and gates. Fingerprints width, height, background, palette, and every exact grid cell. Writes canonical `visual-review.json`, updates the evidence tier and embedded proof, then validates the promoted output again.

For a set, every child receives the same bound review and the root record binds every child path. Later pixel drift, a stale proof page, a missing item observation, or a changed fingerprint fails `validate`.

If no suitable reviewer is available, hand back a verified `draft` and state that artistic acceptance remains unassessed.
