# Make the construction carry the art

Recognition is the first gate. A recognizable sprite can still have flat volume, arbitrary anatomy, generic design, or decorative noise. The construction passes must solve those problems before the result is called polished.

## Give the object a visual thesis

Write one sentence connecting function or character to a visible construction decision. For example: `A low cargo walker carries an offset crate on a continuous platform; its optical unit belongs to the platform, so the crate cannot be mistaken for a head.`

The sentence must predict geometry. “Detailed,” “professional,” “beautiful,” and an attractive subject name do not. Protect that geometry while changing less useful details. An original design needs its own arrangement and identifying feature; reference artwork supplies methods, not a silhouette to reuse.

## Work at three scales of shape

| Scale | What it does | Typical failure |
|---|---|---|
| Main masses | Establish subject, pose, support, depth, and composition. | A decorated box, floating equipment, or a river with mechanical zigzags. |
| Form clusters | Turn surfaces, show overlaps, and distinguish material. | Horizontal bands, equal highlight islands, or unrelated triangular facets. |
| Edge pixels | Control a contour step, glint, expression, notch, or transition. | Small marks conceal unresolved form or make every boundary equally loud. |

Move between these scales as needed. A material problem may require rebuilding a main mass. A face problem may require moving several connected features. Finishing is not a promise to keep every earlier shape.

Author broad geometry with compact helpers when useful, then take ownership of its native contour and internal clusters. A polygon rasterizer chooses a staircase from coordinates; it does not decide whether that staircase describes a cheek, roof, leaf group, or metal bevel.

## Construct a surface, not a stack of stripes

First identify its front, turn, overlap, and light-facing region. Shape the base and shadow as connected regions around those relationships. Place the highlight where that surface turns toward light. Do not assign a horizontal stripe to each value merely because the sprite has several rows available.

For a curved flask, the liquid needs a top surface, a side turn, and a lower pool. Let the glass reflection interrupt the rim selectively. A bright rectangular patch beside a dark rectangular patch can satisfy a palette budget while making both glass and liquid look opaque.

For a tree, offset the crown groups in both depth and height. Let a few dark gaps enter from the contour to separate groups. Give their light-facing regions unequal shapes and keep subordinate groups quieter. A continuous bright band across the whole crown flattens it, even if individual marks resemble leaves.

For architecture, solve the actual faces first. A gable roof has a ridge, eaves, and planes sharing those edges. Tile marks must follow the chosen plane. Marks that ignore it can make a solid roof look dented. Use an exact native scaffold when corners disagree, then replace the visible scaffold with intentional edges.

## Give clusters ownership

Before adding a cluster, name its surface and job: `front crown turning into light`, `underside of the collar`, `near cheek`, or `receding bank`. Make its shape follow that job.

Useful cluster operations include:

- Join two highlight flecks when they describe one continuous lit plane.
- Split a light patch where a real overlap or change of surface interrupts it.
- Taper a cluster toward the turning edge instead of surrounding it with a uniform dark rim.
- Shift an entire eye, hand, or glint relationship instead of adding isolated compensating pixels.
- Remove a mark that only repeats information already carried by a larger shape.

A shared material vocabulary does not require identical stamps. Vary a motif's contour, extent, overlap, and value assignment to fit its surface. Reusing the same bright speck in every instance advertises the stamp.

## Resolve shared axes before small features

On a face, establish the skull angle, eye line, center line, and jaw. Eyes may differ in size or height when perspective and tilt explain the difference. A single shifted eye cannot establish a tilt that the skull, nose, and mouth contradict. Check the feature group together at native size.

On a machine, distinguish load, body, sensors, attachments, and supports. A box above two legs may read as a head rather than cargo. Thickening the legs alone cannot fix that semantic error. Change the relationship between the crate and carrying platform, then simplify the chest or chassis so the important gap remains visible.

On a landscape, construct the route through space. A river should turn with unequal arcs, change width with depth and terrain, and disappear behind intentional banks. Regular equal-length elbows are a property of the drawing method, not a convincing landscape. Change the course before adding foam or grass.

## Control edge emphasis

Choose which edges must remain visible on the actual background and which can merge into shadow. Handles, feet, grips, and support joints often need local contrast because they carry function. Give those regions sufficient value separation without adding a bright outline around the whole sprite.

Distinguish an outer contour, a contact shadow, a material seam, and a light transition. Repeating the same dark line on all four flattens the object. Hard materials may need compact sharp reflections; matte or rounded forms often need broader turning clusters. Deliberate palette-bound antialiasing remains available when it serves the intended display context.

## Inspect, form a hypothesis, and intervene

Open the native view first. Identify the wrong read or the weakest construction. Then inspect its coordinates with `pixel_lab.py inspect`; use `pixel_lab.py loupe` when a labeled enlarged region makes the local relationship easier to inspect. The loupe is diagnostic evidence, not a replacement for the final browser view.

Record four concrete statements:

1. **Observed:** what the viewer actually sees, including a plausible wrong interpretation.
2. **Cause:** the responsible relationship between masses, clusters, or features.
3. **Intervention:** the region and operation to change; what must stay intact.
4. **Expected change:** what should become clearer at native size.

Keep the same grid and palette budget during the comparison unless the brief explicitly changes. Preserve the earlier draft. Use a local patch for a local error; use a same-grid authored repair when the cause is structural. If two local attempts leave the wrong read intact, change the construction hypothesis rather than making the same detail pass again.

## Judge improvement on the visible problem

First judge the current piece alone, without the weaker baseline beside it. State what prevents it from looking finished in its intended use. Then compare versions to evaluate the intervention. A weak baseline makes small improvements easy to prefer and can lower the reviewer's standard.

Use this order for a serious critique:

1. **Meaning:** name what the image actually depicts. Can a key requirement be mistaken for something else, or only found after reading the brief?
2. **Construction:** trace the load path, joint, shared edge, feature axis, or depth overlap responsible for the read. Locate a conflict on the native grid.
3. **Material and light:** identify what distinguishes surfaces beyond their hue. Expose a highlight that does not belong to a surface, an opaque glass wall, or texture that ignores a plane.
4. **Design and finish:** identify accidental repetition, uniform edge emphasis, ambiguous focal hierarchy, or decorative pixels doing no useful work.

For each major defect, record the region, visible evidence, cause, intended intervention, and a constraint the intervention could damage. Distinguish an observable conflict from a style preference. Prioritize at most three major defects in an iteration so their causes remain testable. Do not replace an unsuccessful diagnosis with a long list of minor polish requests.

Compare anonymous before/after views with the same background and integer scale. Ask what each depicts before disclosing the intended design. A difference in the file, additional texture, or a larger color count is not a win.

Record whether the intervention clarified the intended relationship, introduced a new defect, or had no visible benefit. Keep uncertainty explicit. A fresh reviewer can expose errors the builder has learned to overlook; an independent agent review is still model evidence, not a human study or proof of general improvement across models.

Separate preference from task success. A reviewer may prefer a wider mechanical body while still reading its payload as a head. The relative preference is real evidence, but the functional requirement still fails. Keep the wrong interpretation in the review record and change the relationship that produces it.

Originality must retain identity. A distinctive roll-top bag can accidentally resemble a face or handled container when two fastenings become eyes and a fold becomes a mouth. A novel arrangement is not a successful backpack if the viewer cannot read straps, closure, and fabric body. Replace the misleading relationship; do not explain the intended object through a caption.

Check supports as paths, not inventories. Follow load -> mount -> body -> joint -> foot on the rendered grid. Several parallel bars can contain all the right named parts while obscuring which one carries the load. A continuous body, fewer bands, and separate attachment points may explain more than additional mechanical detail. For small limbs, inspect the endpoints against the actual background and separate neighboring tips before increasing their brightness.

Do not overcorrect a real defect into a new convention. Breaking a canopy into three disconnected balls removes banding but can produce a topiary. Connect some foliage and branches across the gaps. Removing a flask's stripes must preserve a clear liquid level. Quiet distant planes still need enough overlap to separate the ridges. Recheck the constraint that the repair might have weakened.

The [original construction-repair examples](../examples/construction-repair/README.md) include editable before/after grids, an anonymous comparison, concrete criticisms, and the tradeoffs still visible after a preferred repair. Use them to calibrate diagnosis, not as silhouettes to reproduce.
