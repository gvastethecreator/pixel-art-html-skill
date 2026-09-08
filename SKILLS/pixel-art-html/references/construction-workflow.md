# From visual evidence to exact pixels

## Make references change decisions

A useful reference note has three parts:

| Observed | Inferred method | Application |
|---|---|---|
| A foliage process repeats rounded bundles with darker rear masses. | Bundle placement carries volume; leaf marks carry texture. | Use three overlapping original crown masses; texture only their exposed light-facing regions. |
| A car tutorial separates cabin, chassis, and wheels before assembly. | Shared anchors make projection easier to control. | Locate axle centers and cabin corners before filling planes. |
| A character revision removes costume detail and changes value allocation. | Extra information can hide the pose. | Protect the hand/weapon gap; remove a belt stripe that merges the arm into the torso. |

These are operational inferences from Pixelblogs 44, 54, and 55. The chapter links and local directory names are in [techniques.json](techniques.json). They are construction methods, not templates to trace.

For an original asset, add a difference statement: your own mass arrangement, identifying feature, palette allocation, and composition. A new label or palette does not make a traced reference into an original design. The source should answer a construction question; the brief should drive the design.

## Choose a representation the model can edit

| Problem | Representation | Why |
|---|---|---|
| Unique small silhouette | Full grid with single-character aliases | Every contour cell is visible in one place. |
| A large plane or foundation | Rectangles and runs | Compact scaffolding with predictable coverage. |
| Repeated material marks | Named motifs, ordered stamps, palette maps | Reuse topology while varying placement and lighting. |
| Anatomy or an assembled object | Part bounds, anchors, overlap order in the plan | Gives edits a spatial purpose before color. |
| A localized visual defect | Fingerprinted cell patch | Preserves the rest of the grid and records the intervention. |

Use semantic names for palette roles and motifs. Compact grids may use short aliases with an explicit legend. Do not generate hundreds of unrelated `pixels` to imitate a picture; reserve them for controlled finishing or repair.

The compiler paints `grid`, then `rects`, `runs`, `stamps`, and `pixels`. A transparent motif cell is a no-op. To remove an earlier cell, use an explicit transparent `pixel` or a patch with `after: null`. Geometric shape helpers must resolve to the final native grid; CSS transforms, shadows, and smoothing are presentation, not authored cells.

## Plan only the relationships that matter

For a 32x32 machine, a useful plan can fit in a few lines:

```text
Projection: top-down, nose up. Light: upper left.
Body: x10..21, y7..23; tapered nose; broad rear.
Cockpit: x14..17, y10..13; protected focal cluster.
Engines: x6..10 and x21..25, y17..26; attach under the rear body.
Gap: keep x11..12 and x19..20 clear beside the engine tips.
Order: engines -> hull -> cockpit -> accents.
Palette: ink, shadow, hull, lit hull, cockpit, exhaust.
```

Do not confuse an inclusive bound such as `x10..21` with a width. Tool regions use `[x, y, width, height]`; all coordinates start at zero. A plan proposes geometry. The rendered grid decides whether it works.

## Spend information by pass

1. **Block:** solve outer contour, overlap, gesture, and identifying gaps. Compare the silhouette against the most likely wrong interpretation.
2. **Planes:** allocate values to surfaces. A temporary body-part palette can help with anatomy, but replace it with intentional value roles before judging finish.
3. **Material:** mark a few characteristic surface changes. For foliage use crown bundles; for rock use unequal facets; for brick use joint cadence; for metal use selective hard reflections.
4. **Edges:** inspect how boundaries meet. Break accidental highlight bands, doubled diagonal elbows, one-cell tangencies, and isolated motif remnants.
5. **Cut:** remove a candidate detail and compare at 1x. Restore it only when it contributes to recognition, volume, material, or focus.

Named parts are not permission to finalize them independently. A good head can still be wrong for its body; a good crown can obscure the trunk. Judge the assembled asset between passes.

Inspect the support and attachment regions on the intended background. Dark legs, handles, straps, or support struts may exist in the grid yet disappear in use. Repair the local value allocation before increasing detail or adding a global bright outline. For a heavy machine, compare the load with its feet, joints, and support width. For a small face, reserve a connected face plane before placing eyes.

## Make studies explore a decision

Different grid hashes are a mechanical requirement, not proof of useful alternatives. Ask what the viewer would perceive differently in each candidate. For a backpack, compare a roll top, a framed load carrier, and a hinged flap; changing the same bag's width alone may teach little. For a character, change the line of action and supporting contacts, not only the head position. For water, compare surface behavior, not only the phase of the same wave pattern.

Keep an inadequate study as evidence when it exposes weak exploration. Do not turn a selected draft into an artistic success because its other two candidates were weaker.

## Use controlled experiments

An experiment changes one causal feature, not necessarily one cell. Repairing a face angle may move several connected clusters. Recoloring every surface while changing the silhouette prevents a useful before/after explanation.

Write: `The right arm merges with the torso at x18..20/y12..16. Remove the dark bridge and move the hand outward. The arm/weapon gap should become readable at 1x.` Then inspect, patch, and compare. If the expected read does not appear, keep the losing evidence and revise the hypothesis.

For a local patch:

```bash
python <skill-dir>/scripts/pixel_lab.py inspect <baseline>/pixel-art.json --region 18 12 3 5
python <skill-dir>/scripts/pixel_lab.py patch <baseline>/pixel-art.json <patch.json> --output <new-repair>
python <skill-dir>/scripts/pixel_lab.py diff <baseline>/pixel-art.json <new-repair>/pixel-art.json
```

`before` and `after` accept a hex color or `null`. Read the original colors from the inspector. `base_fingerprint` binds the entire grid; `before` catches a wrong coordinate; `protected_regions` and `max_colors` enforce the constraints you declare. The patch writes standard repair provenance plus `patch.json` and `delta.json`. It does not grant artistic acceptance.

`protected_regions` is an array of `[x, y, width, height]` arrays. For example, `[[14, 10, 4, 4]]` protects native cells x14..17 and y10..13. Replace this example with the actual focal region; an empty array protects nothing. Use `patch --scale 1` for a native PNG or another integer from 1 through 32 for an enlarged export. The default is 12. Export scale never changes the canonical grid.

## Know what not to universalize

- A three-value study is useful; monochrome or two-value art can be intentional.
- A 2:1 screen diagonal is a chosen projection convention. It is not a law for every organic edge.
- Single pixels can be valid eyes, glints, particles, or texture accents. Connectivity alone cannot decide.
- Palette-bound manual antialiasing can soften an internal edge without changing the grid. It should not create a halo against a variable background.
- Dithering can describe a transition or material. Apply a chosen pattern to a chosen region, never as a default repair for weak volume.
- A simple rectangular form can be the correct subject. Reject accidental generic construction, not geometry itself.
- A source GIF may mix diagrams, holds, finished loops, and construction. Sample indices do not establish semantic stages or real-time timing.

## Evaluate the pipeline itself

Use the controlled requests in [evals.json](../evals/evals.json). Compare the previous and updated workflow with the same model, brief, dimensions, palette budget, reference access, and allowed effort. Record model and settings in the run, not in shared skill instructions.

Shuffle outputs for a reviewer who did not build them. Ask for the visible subject, gesture, material, and specific errors before asking for preference. Count `win`, `tie`, `loss`, or `not-assessed` per case. Record reference retrieval cost, repair attempts, mechanical failures, and elapsed time separately. A successful demonstration or passing test suite cannot establish a general improvement across LLMs.
