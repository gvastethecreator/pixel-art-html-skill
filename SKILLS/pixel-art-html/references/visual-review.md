# Visual review and evidence tiers

Use this contract whenever an artifact is presented as evidence of artistic quality. Deterministic validation proves exact files; it does not prove design.

## Evidence tier

Declare one tier before authoring:

| Tier | Meaning | Claim boundary |
|---|---|---|
| `fixture` | Tests dimensions, timing, alpha, manifests, extraction, or another mechanic. | Never cite it as an art-quality sample. |
| `draft` | Direction or construction is incomplete. | Useful for decisions; not an accepted portfolio or production result. |
| `representative` | Built to demonstrate the skill's normal visual-quality path. | Requires the full visual review record and real context proof. |
| `production-candidate` | Intended for a real consuming project. | Requires the full record plus approval by the project owner or a named reviewer; the label is not approval. |

The compiler defaults to `draft`. It intentionally rejects `production`: a source spec cannot certify its own acceptance.

## Recovery and direction search

If the user rejects the result, or if the artifact is `representative` / `production-candidate` and visual identity is direction-sensitive:

1. Mark the current artifact `loss`; do not defend it with technical checks.
2. Record the strongest visual failure, user harm, source cause, and proof that would change the verdict.
3. Produce exactly three cheap, materially different directions against the same brief and grid. Use flat silhouettes plus value blocks; ImageGen concepts may guide shape and material, but never count as the final grid.
4. Compare user value, native-size read, signature, feasibility, and proof path. Choose one; do not default to a hybrid.
5. Name one useful signature to preserve and one generic element to remove.

Palette swaps, added detail, or three versions of the same silhouette are one direction, not three.

## Perceptual gate

Review the final PNG or browser proof with the title and direction card hidden. For a set, shuffle the order and hide every item label.

Before final detail, compare the information budget to the grid. If subject identity, two or more material boundaries, and the useful signature collide at 32x32, either simplify the thesis or move to 48x48 when the runtime contract allows it. Record the decision; do not silently enlarge the canvas.

Record observed words, not numeric self-scores:

```text
Understood subject / orientation / action:
Material read:
Focal cue:
Useful signature remembered:
Set-family read, if applicable:
Mismatch or ambiguity:
Repair or acceptance decision:
```

The artifact passes only when:

- subject and orientation are identified without the title;
- the declared material is named from shape, planes, edge treatment, and highlights rather than color alone;
- the focal cue and gameplay role agree;
- the signature is noticed without overpowering item identity;
- a set reads as one family while each silhouette remains distinct;
- no material mismatch remains unresolved.

A review performed by the author is structured self-review, not independent judgment. Name an independent reviewer only when another person or fresh agent actually inspected raw, unlabeled evidence.

## Pass sequence

Keep each pass separately judgeable:

1. Three direction thumbnails.
2. Selected flat silhouette.
3. Dark / mid / light / accent value master.
4. Material planes with directional light.
5. Signature and selective cluster detail.
6. Subtraction pass at native 1x.
7. Context and blind read.

If the silhouette or value master fails, do not add texture. If two consecutive revisions are flat or worse, reset the direction.

## Review record

Copy [visual-review-template.md](../assets/visual-review-template.md) beside the representative or production-candidate output as `visual-review.md`. Link screenshots, concept sources, source specs, and the final exact proof. A missing gate is `failed` or `limited`, never silently passed.
