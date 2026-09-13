# Observe the relationship before choosing a repair

This is a decision record, not a new asset schema, renderer, stage receipt or acceptance system. It complements the existing [construction workflow](construction-workflow.md) and [artistic construction](artistic-construction.md). The bridge runs with Python's standard library and does not call a model API.

## Separate observation, inference, constraint and preference

Open the current asset at its native grid and intended background. Record what it actually depicts before seeing its explanation. Keep four fields separate:

| Field | Meaning | Must not be used as |
|---|---|---|
| `observed` | A current, concrete visible symptom. | An inferred cause or a desired style. |
| `ruled_out` | A defect the observation explicitly excludes. | Evidence that the defect is present. |
| `uncertain` | A question, conflicting interpretation, uninspected source or unresolved symptom. | A confirmed diagnosis. |
| `preserve` | Up to two defining visual relationships to protect. | More search terms or automatically frozen coordinates. |

Classify the problem as `technical`, `construction`, `style-preference` or `unspecified`. A preference such as liking rough textures is not a technical defect. The bridge suppresses automatic defect routes for `style-preference`; the builder must first relate the preference to the brief. Other kinds guide review but are not pixel-level validators.

The operative sequence is **observation -> relationship -> bounded intervention -> protected identity -> native/context check**. Avoid “remove detail” as a universal response. A stiff figure can require moving the pelvis and support; changing the hue or deleting noise will not necessarily change the gesture.

## Supported structured input

Copy [the empty input](../assets/interpretation-input.json), then fill only what has actually been observed. Empty `observed` is valid and yields no methods. Example below is a text-routing example, not a claim that an image was inspected:

```json
{
  "schema_version": 1,
  "original_text": "No tiene ruido, pero la pose es rígida y no se entiende a quién pertenece el arma.",
  "subject": "character",
  "stage": "block",
  "projection": "top-down-oblique",
  "problem_kind": "construction",
  "observed": ["pose reads rigid", "weapon ownership unclear"],
  "ruled_out": ["texture noise", "wrong palette"],
  "uncertain": [],
  "preserve": ["asymmetric shoulder", "left-facing stance"]
}
```

```bash
python <skill-dir>/scripts/tutorial_bridge.py diagnose --context <work>/interpretation.json
python <skill-dir>/scripts/tutorial_bridge.py diagnose "no tiene ruido pero la pose es rígida" --subject character --stage block
python <skill-dir>/scripts/tutorial_bridge.py validate
python <skill-dir>/scripts/tutorial_bridge.py coverage
```

Provide exactly one positional query or `--context`. Optional filters must agree with the JSON; conflicting filters fail rather than silently override it. Supported subjects are `character`, `foliage`, `prop`, `architecture`, `machine`, `tile`, `scene`, `interface`. Stages are `block`, `planes`, `material`, `edges`, `runtime`. Projections are `top-down-orthographic`, `top-down-oblique`, `side`, `isometric`.

The JSON permits only documented fields, string lists, version 1 and bounded lengths. Unknown keys, duplicate keys, invalid enum values and oversized input fail with exit code 2. Queries without a current compatible observation return a normal result containing `needs-observation`, not an invented repair. Original text, classified clauses, exclusions, conflicts, active issue IDs and preservation notes remain in the response.

## Retrieval authority and limitations

The language pass is a bounded ES/EN rule set, not general natural-language understanding. It handles tested forms of simple absence, contrast, negative capability (“no se entiende”), resolved/history reports, questions, quoted examples and preservation requests. It does not resolve arbitrary nested negation, coreference, irony or every language. Unsupported or ambiguous phrases remain visible as uncertainty. Separate observations for different assets; do not let a sentence about several subjects silently choose one.

Broad nouns such as light, silhouette or color are not defects. Asymmetry and mirroring alone are not defects. Desired texture is not noise to remove. A retrieved lesson is a **method to test**, not proof that its associated defect exists.

Subject, stage, projection and explicit issue IDs gate conditional lessons before lexical matches rank them. The existing [technique library](techniques.json) supplies fallback methods when no specialized lesson fits. Character silhouette failures use anatomy; machine silhouette failures use functional-machine construction; architecture uses linked volumes. Missing core data are reported explicitly, never replaced with fabricated technique contents.

A stage mismatch is a reason to reconsider the stage. A pose failure found during material work may require returning to block under the normal `construct.py` review rules. It is not a reason to retrieve an unrelated texture lesson. The unchanged `reference_library.py techniques` command remains a lexical topic search; do not send it a negated defect report and treat the hit as a diagnosis.

## Protect identity without protecting mistakes

State one or two relationships that make the design its own: the weight of a shoulder relative to the spear, a swept hair mass relative to the brow, or a bent trunk below an unequal canopy. Preserve their *visual function*. Move their coordinates when necessary, but check the same function again after the edit. Use the compiler's protected-region/pixel mechanisms only for actual coordinate constraints.

Name the relationship on both sides of a boundary: cheek/nose, roof/wall, pallet/chassis, crown/branch. Identify whether the boundary is a contour, contact, seam, fold or light transition. Joining one cluster changes its neighbor; removing a shadow can destroy an overlap. A repair must name the most likely regression as well as the desired gain.

Try a deliberate subtraction, not an automatic texture diet. Isolated eyes, glints, manual palette-bound antialiasing and a defining garment pattern can be essential. A canopy may need connected masses rather than fewer leaves; a support may need a continuous load path rather than brighter bars. These are conditional hypotheses, not universal pixel-count thresholds.

## Prevent contract contamination

Each asset owns its use, camera, subject, light and emissive-surface assumptions. A family can share a primary light direction and palette roles, but do not copy a lantern emitter into a portrait or tree. Do not invent a hidden lamp merely to justify inherited text. Static checks can flag inconsistent declarations; they cannot infer an unseen light from arbitrary JSON.

Specify true overhead separately from an oblique RPG view. Keep per-domain contracts for world, portrait, UI and map rather than forcing all into one grid convention. Distinguish a source palette from the colors created by alpha compositing against the runtime background. Preserve original source data when inspecting presentation effects.

## Transfer references honestly

For each source, keep observed content, the author's claim and the builder's inference separate. A teaching sequence reconstructed after completion is useful instruction but not a historical record. An image index or first GIF frame does not establish that a whole animation was observed. Do not fill old stage receipts with reconstructed observations.

Keep paid or private media outside the distribution. Source links are attribution, not permission to redistribute images or entire articles. New examples must have original silhouettes, compositions and identifying cues. Textual study without visual access must be stated as such.

## Calibrate and judge in the right order

Calibrate one small prop, a posed character and a structural module before multiplying families. Use the appropriate grid, including rectangular character masters. Do not automatically call a completed calibration draft representative: the existing non-builder review and owner acceptance tiers still apply.

Judge the current piece alone, then mandatory requirements, then the relative preference. Record whether an intervention clarified, changed nothing, regressed or remains uncertain. Keep wrong readings and failed attempts. A preferred crate can still have unclear support; a cleaner face can lose the required expression.

The eight transfer briefs and three calibration briefs in [interpretation evaluations](../evals/interpretation-evals.json) are unexecuted visual tasks. Mechanical routing tests and metadata hashes do not fill their results. The historical repaired assets remain drafts and are not new successful transfer experiments.

## Basis and attribution

This is an original operational synthesis. Useful primary discussions include [Saint11 on low resolution](https://saint11.art/blog/thoughts_on_low_resolution/), [Saint11 on consistency](https://saint11.art/blog/consistency/), [cure's pixel-art tutorial](https://pixeljoint.com/forum/forum_posts.asp?TID=11299), [Derek Yu's common mistakes](https://www.derekyu.com/makegames/pixelart2.html), and [SLYNYRD's character and architecture study](https://www.slynyrd.com/blog/2025/7/28/pixelblog-57-knights-monsters-amp-castles). Their different preferences are not a shared universal rulebook. The local source registry records the narrower access used for the bundled conditional lessons.

For presentation, [MDN's crisp pixel-art guide](https://developer.mozilla.org/en-US/docs/Games/Techniques/Crisp_pixel_art_look) distinguishes canvas/source sampling from CSS scaling. Logical cells, backing pixels, CSS scale, device pixel ratio and content origin must not be conflated. A CSS scale of 4 at DPR 1.25 gives a calculated 5-device-pixel cell; alignment still depends on the origin and browser presentation. This calculation is not certification of every monitor or zoom mode.
