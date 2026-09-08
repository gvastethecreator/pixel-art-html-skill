# Compose a scene from native masters

Use this route when several sprites and structures must share a world, or when the user needs a canvas with pan and zoom. Keep individual masters within the existing 8–128 pixel contract. Compose them at integer world coordinates; do not enlarge a small scene and call it a more detailed master.

## Design relationships before decoration

Define a shared projection, character height, doorway unit, light, ground plane, and palette roles. Allocate the palette across the whole scene. A collection of good isolated sprites can still fail as a scene.

For an interaction, write actor -> action -> target. Place head, grip, weapon tip, support foot, and target/contact coordinates in world space. Check facing against the target. In the city example, a shield bearer initially faced away from the skeleton attacking it; the individual sprite was valid, but the interaction failed.

Distinguish ground height from draw order. A rooftop actor needs a roof contact point. Increasing its depth only puts it in front of the building; it does not place its feet on the roof. A crypt entrance needs a readable threshold rather than a skeleton painted over its roof.

Plan front/back occlusion for each interaction. Stable depth order is useful for ground actors, but roofs, bridges, and upper floors need deliberate placements. Split an occluder into layers when one flat sprite cannot express both the hidden and visible parts. Do not use one global Y sort to explain different elevations.

Keep contact shadows separate from subject silhouettes. If an opaque shadow is part of the actor sprite, a one-color proof can hide the leg gaps. Mark the actor placement as `subject: true`; keep its shadow in the same visibility group with `subject: false`.

Use silhouette, equipment, and action to distinguish factions. Color is another cue, not the whole distinction. Preserve quiet background space around weapons, faces, and feet. A focal lamp can be the brightest mark without becoming the largest mass; brightness and identity compete differently for the grid.

Mirroring geometry also mirrors painted light and handed equipment. Inspect that result in the scene. Reauthor the material planes when a mirrored sprite contradicts the lighting contract.

## Scene manifest

Build the masters with the existing compiler. Paths in `assets` resolve from the scene manifest. The compositor embeds each canonical artifact once; the resulting HTML needs no external images or server-side code.

```json
{
  "title": "Courtyard encounter",
  "subtitle": "Two travelers meet at the gate.",
  "caption": "The courtyard",
  "width": 320,
  "height": 240,
  "background": "#192532",
  "palette_budget": 24,
  "assets": {
    "gate": "masters/gate/pixel-art.json",
    "guard": "masters/guard/pixel-art.json"
  },
  "groups": [{"id": "people", "label": "People", "color": "#75BAB1"}],
  "placements": [
    {"asset": "gate", "x": 70, "y": 20, "depth": 100},
    {"asset": "guard", "x": 108, "y": 82, "depth": 114, "group": "people", "subject": true}
  ],
  "focus_points": [{"label": "The gate", "x": 120, "y": 90, "zoom": 4}]
}
```

`width` and `height` are integers from 8 to 2048. Each placement needs an asset, integer X/Y, and integer depth. Lower depth paints first; ties preserve manifest order. Transparent cells leave the previous layer unchanged. Optional `flip_x` mirrors the native master. Placements must fit entirely in the world; author a deliberate crop when needed. Groups control visibility. `subject` controls the actor silhouette proof independently of visibility groups.

```bash
python <skill-dir>/scripts/compose_scene.py build scene-source.json --output <new-scene-directory>
python <skill-dir>/scripts/compose_scene.py validate <new-scene-directory>
```

The new output contains standalone `index.html`, editable `scene.json` with embedded exact masters, and native `scene.png`. Validation recomposes placements and compares PNG and HTML against the same scene. A scene fingerprint binds assets, placement, groups, and camera destinations. Output remains draft; this route does not promote a composition from its child tiers.

## Camera and visual proof

The viewer provides drag pan, wheel zoom at the pointer, zoom buttons, native scale, fit, keyboard arrows and Home, optional group visibility, and authored focus points. Color, values, and actor silhouettes are separate views. Actor silhouettes leave a subdued environment for occlusion context.

The camera uses integer physical pixels, including fractional device pixel ratios. `1×` means one native cell per physical display pixel. The backing canvas uses its content box; including the CSS border in its backing dimensions stretches the art. Pointer positions must use the same device-pixel conversion as the camera. Record the viewport and device pixel ratio when judging native readability.

At closeout, inspect the composed image, a crowded interaction, and a foreground/background crossing. Exercise actual drag, wheel anchoring, zoom limits, fit, native scale, keyboard pan, and group toggles. Check cancellation or loss of pointer capture so the camera does not remain in dragging state. Source/PNG equality alone does not prove these controls.

The [city clash example](../examples/city-clash/README.md) includes the original authoring script and the placement corrections found in a real scene. Reuse the construction method; create new actors and architecture for a new brief.
