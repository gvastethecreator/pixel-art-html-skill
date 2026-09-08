# Edit named forms, then review the stage

Use `construct.py` for a multipart sprite whose supports, pose, or occlusion need deliberate repair. Small standalone marks can still use the regular compiler. This route preserves editable part masks and turns declared relationships into diagnostics. It does not recognize anatomy or judge art.

## Source

The example below is a mechanical fixture for the format, not an artistic model. The world uses the existing 8–128 grid contract. Parts may be smaller. Palette keys are single characters; `.` is transparent. Parts paint in array order. Parent relationships control translation, not paint order. An origin is relative to its parent, or to the world when `parent` is absent. Anchors are local cell coordinates inside the part's rectangular grid. They may deliberately sit in a transparent cell; an anchor check alone does not prove contact with visible paint.

```json
{
  "kind": "construction", "schema_version": 1, "stage": "block",
  "title": "Attachment experiment", "width": 16, "height": 16,
  "intent": "A narrow pole carries an offset flag",
  "light": "Upper left", "background": null, "palette_budget": 3,
  "palette": {"p": "#586466", "f": "#9E4051", "l": "#E4B568"},
  "parts": [
    {"id": "pole", "origin": [6, 3], "grid": ["p", "p", "p", "p", "p", "p", "p", "p"], "anchors": {"hook": [0, 0]}},
    {"id": "flag", "parent": "pole", "origin": [0, 0], "grid": ["fffff", "ffff.", "fff.."], "anchors": {"hook": [0, 0]}}
  ],
  "constraints": [
    {"id": "flag attachment", "kind": "anchor", "a": ["pole", "hook"], "b": ["flag", "hook"], "max_distance": 0},
    {"id": "exposed shaft", "kind": "visible", "part": "pole", "min_cells": 5},
    {"id": "space below flag", "kind": "clear", "region": [7, 7, 4, 3], "parts": ["flag"]}
  ]
}
```

`anchor` measures Chebyshev distance between two declared points. `visible` counts cells that still belong to a part after every overlap. `clear` requires no paint from the listed parts in a world-space rectangle, including hidden paint. `inside` tests an anchor against a container mask and optional excluded masks: `{"id":"sole on deck","kind":"inside","at":["foot","sole"],"container":"deck","exclude":["front-rim"]}`. This can locate a foot outside its support surface; it does not infer balance or perspective. Each constraint needs a unique ID. Failed checks remain visible in the block output and prevent stage advancement; they do not prevent inspecting a candidate. Palette budgets include hidden part paint and the background.

Use `role: "environment"` on ground and scenery parts in a composed study; other parts default to `subject`. The silhouette view subdues environment parts so a filled floor cannot hide actor gaps. Roles belong to the reviewed structure.

Set constraints from the actual design question. There is no universal head ratio, foliage connectivity count, or acceptable blade distance. A passing constraint report says only that the declared relationships hold.

## Build, inspect, decide

```bash
python <skill-dir>/scripts/construct.py build block-source.json --output work/block-a
```

Open `index.html` for the standard native pixel proof and `parts.html` for color, value, silhouette, and part ownership. Select a part to read its world origin, anchors, and visible cell count. The view dims other parts while preserving their occlusion. Every output contains the exact source and a recomputed report.

Author the next pass only after viewing the current pass. Saving all stage images after completing the art is not evidence of decisions between passes. A record must describe what was actually seen; tool success cannot supply this observation.

Create a review input using the exact fingerprints from `construction-report.json`:

```json
{
  "source_fingerprint": "COPY_FROM_THE_OBSERVED_REPORT",
  "artifact_fingerprint": "COPY_FROM_THE_OBSERVED_REPORT",
  "stage": "block", "decision": "advance",
  "reviewer_kind": "self", "reviewer": "The active author",
  "views": {"native": true, "silhouette": true},
  "observed_read": "Describe the actual subject and action after viewing it",
  "remaining_limit": "Name a nonblocking limit, or state that none was observed",
  "evidence": "Identify the inspected view or capture; do not invent a saved screenshot",
  "issues": []
}
```

For `rework`, record one to three blocking issues. Each needs `region_or_part`, `observed`, `cause`, `intervention`, and `preserve`. Keep the rejected review. An `advance` decision must have no unresolved blocking issues and all declared constraints must pass. Planes and material reviews also require the value view.

```bash
python <skill-dir>/scripts/construct.py review work/block-a block-review-input.json --output work/block-review.json
python <skill-dir>/scripts/construct.py build planes-source.json --previous work/block-a --review work/block-review.json --output work/planes-a
python <skill-dir>/scripts/construct.py review work/planes-a planes-review-input.json --output work/planes-review.json
python <skill-dir>/scripts/construct.py build material-source.json --previous work/planes-a --review work/planes-review.json --output work/material-a
python <skill-dir>/scripts/construct.py validate work/material-a
```

The next stage keeps the same part IDs, masks, origins, parents, anchors, paint order, constraints, intent, light, background, dimensions, and palette budget. Color allocation can change within those masks. A structural improvement returns to `block` with a new source and review. This preserves the freedom to redraw while preventing an old review from authorizing a changed pose. Material may be the final pass; it still needs actual final visual inspection and remains a draft.

The output embeds reviewed ancestor sources and reviews so validation remains portable. It recomputes each ancestor and rejects missing stages, rework decisions, and stale source or pixel fingerprints. The records are declarations by the reviewer, not authenticated identities or proof of human perception. A self-review is valid authoring feedback, never independent acceptance. Use the existing promotion path only when its actual review requirements are met.

## Repair a part

```json
{
  "source_fingerprint": "COPY_FROM_THE_CURRENT_SOURCE_REPORT",
  "hypothesis": "Moving the arm outward should separate the grip from the chest",
  "operations": [{"kind": "translate", "part": "arm", "delta": [1, 0]}]
}
```

```bash
python <skill-dir>/scripts/construct.py edit source.json edit.json --output revised-source.json
```

Available operations are `translate` with `[dx,dy]`, `replace-grid` with new string rows, and `mirror` for a leaf part. Translation moves descendants through the parent relationship. Replacement preserves local anchors and rejects those that no longer fit. A mask or placement change resets the source to block. A mirror also resets it to block, because painted light and handed equipment need reinspection. Mirroring a parent is rejected; reauthor the multipart pose explicitly. Edits never overwrite the baseline.

For a new original brief, create new forms. Reuse attachment and inspection methods, not the example's silhouette. Reference processes and mistake lessons can guide a decision; test the decision again in its new context.

## Preserve parts during a color repair

A constructed `pixel-art.json` is an export of its named masks. Do not repair that export with the flat patch tool: it would discard the editable source. Flat repair commands reject constructed artifacts.

Extract `source` from the current `construction.json`. Use `replace-grid` on the responsible part, preserving its opaque mask for a color-only change. Rebuild the revised stage with its existing reviewed predecessor: for a material revision, pass the observed planes directory and its bound review. Inspect the new final result. The previous final review does not apply to changed pixels.

The [original examples and seven visual lessons](../examples/part-construction/README.md) show actual losing revisions, a partial repair, and historical stage replay. Select a lesson by its observed failure; do not load every example or reuse its silhouette for a new brief.
