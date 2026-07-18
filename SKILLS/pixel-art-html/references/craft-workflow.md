# Pixel-art craft workflow

Use this reference for text-authored art, manual cleanup after conversion, or critique of an existing master. It distills recurring craft rules from the 62-module SLYNYRD Pixelblog study; the workflow and wording here are original synthesis, not a substitute for the source tutorials.

## Evidence and direction first

Label the artifact `fixture`, `draft`, `representative`, or `production-candidate` before drawing. For recovery or direction-risk quality work, make three same-brief thumbnails before the direction card:

- change shape language, silhouette thesis, or material story, not only palette;
- keep the grid, subject list, use, and proof context comparable;
- choose one against native-size readability, useful signature, feasibility, and material potential;
- preserve one memorable functional move and remove one stock/default construction.

A fixture may be ugly and still useful, but it must never become visual-quality evidence. Read [visual-review.md](visual-review.md) for the full claim boundary.

## Direction card

Write this before painting cells:

```text
Use: icon | sprite | tile | prop | portrait | scene | background
Grid and display scale:
Subject, action, and one-sentence read:
Projection and scale convention:
Silhouette cue and focal cue:
Light direction, hardness, and mood:
Value groups: dark / mid / light / accent
Palette ramps and shared colors:
Material or texture cluster grammar:
Background, padding, and overlap rules:
Evidence tier and proof claim:
Selected direction, signature, and subtraction:
```

If a field is unknown, decide it before detail. Projection, light, scale, and palette are scene-wide contracts; changing them late usually creates a patchwork result.

## Build in passes

Keep a buildable spec throughout. Render after every material pass; do not wait until the end to discover that the native-size read failed.

### 1. Gesture and silhouette

- Start smaller than feels necessary. Allocate the canvas to the dominant mass, secondary mass, negative space, and one focal cue.
- For a character, place the line of action and weight before costume. For architecture, vehicle, or mech, block structural primitives before surface panels. For an organic subject, block the large blob before leaf, fur, or rock marks.
- Judge the shape as one flat color. The subject must remain identifiable without interior detail.
- Use asymmetry for action, personality, or a unique landmark. Use symmetry when an asset will repeat or mirror.

Done when the native 1x silhouette communicates subject, orientation, and pose.

### 2. Projection and volume

- Select one projection: frontal, side, 3/4 side, 3/4 top-down, top-down, cabinet-like side view, or isometric 2:1. Apply it to every compatible element.
- In 3/4 views, clean readable angles beat mathematically delicate perspective. In isometric work, count the 2:1 stair pattern; do not eyeball it.
- Map hidden edges mentally for buildings, vehicles, and isometric objects. Visible faces should agree on scale and shared corners.
- Use overlap and vertical placement to show depth. Do not ask detail to repair contradictory geometry.

Done when flat face colors already produce coherent depth.

### 3. Value plan and palette ramps

- Design in HSV/HSB terms: hue identity, saturation intensity, and value/lightness.
- Assign colors jobs: outline/deep shadow, shadow, base, light, highlight, accent, environment bridge. Reuse colors across nearby materials when the scene allows it.
- Build each ramp by increasing value. Shift hue along the ramp; a warm-light/cool-shadow drift is a strong default. Keep the brightest colors less saturated unless a hot accent is intentional.
- Prioritize value separation over extra hues. A large palette is a library; the artifact should use a small sub-palette.
- Reserve pure white or maximum chroma for the focal point, emissive effects, or critical gameplay information.

Suggested working budgets:

| Grid/asset | Starting colors | Texture clusters | Information target |
|---|---:|---:|---|
| 8x8 | 2-4 | 0-2 | orientation, identity cue, strong outline or separation |
| 16x16 | 3-8 | 2-3 | silhouette, pose, one material/focal break |
| 24-32px | 6-16 | 3-5 | secondary form, controlled light, material distinction |
| 40-64px | 8-24 | 5-6 per major surface | hierarchy plus selective surface detail |
| compact scene | 8-16 shared colors | by depth plane | focal subject remains above the environment |

These are starting budgets, not hard limits. Add a color only when it creates a new readable job.

Done when a grayscale read separates silhouette, major planes, and focal point.

### 4. Directional light and shadow

- Establish the source before shading: direction, elevation, hardness, and ambient color.
- Use at least three functional values on important volumes: shadow, local/base, light. Tiny assets may collapse this to two plus an accent.
- Place light as connected slabs or clusters on planes facing the source. Place cast shadows consistently across nearby assets.
- Shape corners with contrast: hard materials can drop a middle edge color; soft materials keep a gentler transition.
- Match shadow edges to atmosphere: hard in clear or airless scenes, softer and lower contrast in haze.
- Avoid pillow shading. A bright center with uniformly dark edges describes a sticker, not a lit volume.

Done when removing texture still leaves convincing volume and mood.

### 5. Material and texture grammar

For every material, define a small cluster vocabulary, then repeat it with controlled variation:

- simplify the real detail into clusters;
- repeat a few cluster shapes instead of inventing every mark;
- balance dense and quiet areas;
- vary spacing or hue enough to avoid wallpaper repetition;
- keep same-color pixels connected when possible;
- allow isolated pixels only as intentional sparkles, stars, particles, or micro-accents.

Scale texture with depth. Near surfaces can carry larger, higher-contrast clusters. Distant surfaces use fewer, smaller, lower-contrast marks or none. Never draw every leaf, brick, blade, scale, or muscle.

Useful material cues:

- foliage/clouds: overlapping rounded masses, then light/shadow zones, then a few repeated edge clusters;
- rock: angular fractures for hard igneous forms, horizontal strata for sedimentary forms, folded veins for metamorphic forms;
- brick/walls: grout and structural rhythm first, selective aging last; leave quiet gaps;
- metal/mech: large clean planes, edge highlights, accent stripes that wrap the volume;
- food: warm appetizing local colors, distinct ingredient signatures, readable outline or cluster separation;
- water: connected wave or blob rhythm, brighter surface crests, reflection colors pulled toward the water ramp;
- hair/fabric: one mass and flow lines first, separated locks/folds only where they reinforce motion.

Done when the material reads from its cluster rhythm, not from noisy single pixels.

### 6. Focus and subtraction

- Protect one dominant read and one focal cue. A secondary cue must support rather than compete.
- Put the strongest value/chroma contrast at the focus. Lower contrast and detail away from it.
- Remove details that only become visible while zoomed in. If a detail does not improve identity, material, depth, mood, or gameplay readability, delete it.
- Blend outlines toward adjacent ramps instead of surrounding every form with straight black. Keep stronger outlines where separation or gameplay demands them.
- Recheck transparent edges, repeated motifs, tangencies, accidental edge contact, and inconsistent shadow lengths.

Done when subtraction no longer improves the 1x read.

### 7. Proof, not decoration

Inspect the final HTML and PNG through all of these views:

1. Native 1x: identity, pose, focus, and scale.
2. 2x and 4x: cluster shapes, stair-step rhythm, edge cleanup.
3. Flat silhouette: structure without interior rendering.
4. Grayscale/value: plane and focus separation.
5. Repeated context for tiles/props: seams, obvious motifs, visual fatigue.
6. Neighbor context for game assets: collision silhouette, overlap, HUD/background competition.

The deterministic critique report is a risk detector only. A clean report does not certify good art; a warning must be inspected in context because a star, eye highlight, or particle may be an intentional singleton.

## Common failure repairs

| Symptom | Likely source | Repair |
|---|---|---|
| Valid but generic/blocky | rectangles survived past scaffold | reshape silhouette with a local grid or motif stamps before detail |
| Recognizable but forgettable | first feasible direction was accepted | compare three shape/material theses, preserve one useful signature, remove one stock cue |
| Muddy despite many colors | weak value jobs, excess near-duplicates | merge colors, widen dark/mid/light separation, reserve accent |
| Flat volume | light direction undefined or pillow shading | choose one source and rebuild plane-facing clusters |
| Noisy surface | unique marks and orphan pixels | reduce to 2-6 repeatable cluster motifs with quiet gaps |
| Scene feels inconsistent | mixed projection, scale, ramps, or shadow rules | restate the scene contract and normalize every asset |
| Character feels stiff | costume painted before gesture | return to line of action, weight, and large body masses |
| Tiny asset unreadable | realistic proportions/details exceed grid | enlarge identity cue, simplify anatomy, remove secondary detail |
| Converted image looks like a thumbnail | quantization preserved source noise | manually repixelize silhouette, value groups, and material clusters |
| Tile repetition obvious | landmark-like motif repeats or edges do not loop | neutralize the base, overlap edges, add restrained variants, test 3x3 |
| Background competes with subject | equal contrast/detail at every depth | lower distant contrast/saturation and remove fine clusters |
