# Characters and creatures

Treat a face as a feature group: eye axis, center line, jaw, and skull tilt must agree. Move the group when changing the pose. A single raised eye without a matching head tilt often reads as an error. Preserve local eye-to-skin contrast when the far temple falls into shadow.

Retrieve `anatomy-before-costume`, `face-hair-masses`, `tiny-information-budget`, or `frame-master-handoff` with `reference_library.py techniques`. For difficult poses, map the pelvis, rib cage, head, support foot, grip, and limb gaps before clothing. A temporary part-color dummy exposes wrong overlaps more clearly than finished shading.

## Direction choices

- Name the action phase: stance, anticipation, contact, follow-through, recovery, or idle.
- Choose line of action, center of gravity, facing, and ground/contact point before costume.
- Pick one identity mass that survives the grid: hair, scarf, weapon, ears, shell, horns, or limb proportion.
- Base a creature on coherent anatomy or one governing blob, then one deliberate deformation. Random feature lists do not create a readable body.

## Build

1. Place head, torso, pelvis, and contact points as large masses.
2. Test the flat silhouette at 1x. Enlarge hands, head, weapon, or hair only if it improves action or identity.
3. Add front/back overlap and two or three value planes. Keep the face or gameplay cue at strongest contrast.
4. Treat hair, fur, cloth, and armor as masses with a flow or plane direction. Add only a few subordinate locks, folds, tufts, or plates.
5. Cut costume detail that flickers, merges limbs, or changes the pose read.

Adapt the scaffold to the animal. For an insect, map head, thorax, abdomen or wing case, three leg-pair attachments, visible endpoints, and near/far overlaps. Do not force a humanoid pelvis onto it. If a leg count matters to the brief, trace each attachment-to-foot path and inspect the visible count at native size. Six paths in the source do not prove six readable legs. Separate antennae, mandibles, equipment, and leg tips before material detail.

## Reject

- costume painted before gesture
- symmetric limbs in an asymmetric action
- feet or contact point drifting between related frame masters
- face readable only from the title or zoom
- hair rendered as disconnected strands
- monster features with no shared anatomy, weight, or light

For later animation, hand off exact grid, contact pivot, frame action phase, order, durations, and stable identity palette to `$spritesheet-expert`.
