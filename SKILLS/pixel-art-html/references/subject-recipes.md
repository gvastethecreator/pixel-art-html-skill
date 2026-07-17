# Subject recipes and corpus routing

Read only the sections matching the requested artifact. These recipes adapt the 62-module SLYNYRD Pixelblog study to exact-grid static masters. Animation guidance here shapes poses, modular layers, and frame readiness; actual atlases still route to `$spritesheet-expert`.

## Tiny icons, items, and props

- Lead with the iconic silhouette, then one color signature and one highlight/material cue.
- Keep the object inside a consistent frame and baseline so a set feels related.
- Use symmetry for frequently repeated generic props; reserve asymmetry for landmarks or unique pickups.
- Keep cast shadows short and consistent. Separate the shadow when the prop must work over multiple surfaces.
- For collectables, preserve affordance in the still: a lifted pose, shine cluster, strong outline, or unmistakable color role. Do not let feedback effects replace object readability.
- Food needs warm, fresh local colors and recognizable ingredient blocks. A photo-like downscale with many colors is a failed sprite.

Strong source modules: 21, 24, 30, 34, 36, 45, 47, 51, 59.

## Characters, portraits, and action poses

- Anatomy first, stylization second. Choose a head-count model appropriate to the grid; small sprites normally need enlarged heads, hands, weapons, or hair masses.
- Build `line of action -> dummy/wireframe -> volume masses -> costume/equipment -> light -> detail`.
- Preserve anatomical placement even when exaggerating feature size. Hair starts as one blob with flow lines, not individual strands.
- A combat still should imply its phase: stance, anticipation, hit, follow-through, or recovery. Extend limbs and weapon paths enough to read at 1x.
- Use an anchor near the center of gravity. Keep mirrored poses truly mirrorable; asymmetrical gear requires unique left/right treatment.
- Design equipment as separate visual layers when future animation or customization is likely. Reduce small costume detail that would flicker between frames.
- For monsters, combine a recognizable real anatomy base with one deliberate fantasy deformation. A coherent blob can be reverse-engineered into structure; random feature mixtures cannot.

Strong source modules: 8, 9, 17, 22, 25, 29, 36-39, 49, 50, 52, 53, 55-60.

## Vehicles, aircraft, ships, and mecha

- Decide the machine's design trade-off before drawing: mobility, power, defense, cargo, or role. Express it through silhouette.
- Construct from functional primitives: hull/body, cockpit or operator space, propulsion, control surfaces, joints, weapon mounts, and support/feet.
- Add a human, door, cockpit, wheel, or tile reference when scale matters.
- Wrap paint stripes and highlights around the volume. A flat decal that ignores planes destroys depth.
- Build swappable weapons/attachments as motifs or layers. Reuse a coherent base rather than inventing each faction unit from zero.
- Aircraft need a readable wing/propulsion silhouette; submarines need hull, tower, horizontal and vertical control surfaces, and propulsion; mecha need a strong torso/shoulder/foot relationship rather than human anatomy with panels pasted on.
- For small tactical mecha, omit parts aggressively: one or two bright optics can carry the face; shoulders and feet carry power and stability.

Strong source modules: 12, 18, 19, 31, 32, 39, 46, 48, 59-61.

## Architecture, interiors, and cities

- Use a constructive sequence: footprint or foundation -> roof/top mass -> visible faces -> openings -> light/shadow -> selective wear.
- Establish one projection and light source with a style-guide building before assembling a settlement.
- Duplicate modules with small variations; use unique silhouettes only for landmarks.
- Make form follow use: defensive castle parts, farm machinery components, civic building cues, industrial clutter, or social hierarchy should be readable in the structure.
- Keep straight architectural masses against a softer sky, foliage, haze, or terrain countershape.
- For interiors, design furniture and stairs inside the tile/grid contract. Use separate foreground rails or overlap pieces for depth sorting.
- Blend outlines into local ramps; unbroken black contours usually make compact buildings harsh.

Strong source modules: 3, 4, 14, 16, 28, 34, 35, 39, 41, 42, 45, 51, 54, 57, 61.

## Landscapes and backgrounds

- Organize at least three depth planes. Closest planes carry strongest contrast, saturation, scale, and texture; distant planes shift toward the sky color and lose detail.
- Use the horizon and vertical placement as depth cues. Add a haze bridge where ground and distant forms otherwise collide.
- Choose sky, cloud family, time, and atmosphere together; terrain lighting must agree with them.
- Let backgrounds serve foreground action. Reserve highest contrast and sharpest clusters for the subject or intended focal plane.
- Reuse palette colors across sky, mountains, shadows, and haze. Fifteen well-assigned colors can carry a full compact scene.
- Scale cluster grammar with distance: thick near grass becomes short clusters, then no individual blades; near rocks become simplified silhouettes far away.
- Build city skylines with a few landmark rhythms, not homogeneous noise. Build parallax layers only after the static depth read works.

Strong source modules: 11, 13-15, 18, 23, 27, 32, 40, 42, 46, 48, 62.

## Foliage, rocks, water, weather, and materials

- Foliage: rounded mass -> light/shadow zones -> repeated leaf-cluster motifs. Match species, season, and biomes; vary hue inside a shared ramp.
- Trees: repeat a small leaf bundle with overlap and cleanup. Shade the crown as a large volume before individual clusters.
- Rocks: choose geology. Igneous suggests angular fracture, sedimentary horizontal layering, metamorphic veins/folds. Match rock hue to surrounding soil.
- Water: use connected curves/blobs and bright crests; reflections inherit source shapes but shift toward the water ramp. A still should imply flow direction.
- Wind: establish flow points. Fabric, hair, plants, dust, and leaves should agree on direction; ambient motion must not displace the main composition.
- Brick/walls: grout and divisibility establish structure; aging is a sparse final pass. Do not outline every brick.
- Food and organic matter: simplify characteristic shape and local color, then add only the texture needed for freshness/material identity.

Strong source modules: 2, 10, 13, 15, 18, 27, 30, 33, 34, 43-45, 62.

## Top-down tiles and objects

- Start with a neutral seamless base texture. Test it repeated 3x3 before adding transitions or landmarks.
- Keep key clusters from touching except controlled edge/corner loops. Busy next to busy creates noise; preserve negative space.
- Use layered overlays for walls, terraces, water edges, shadows, and decorative variants instead of baking every combination.
- Match props to tile units, projection, palette, geology, and shadow convention. Large repeated objects should be symmetric or have variants.
- In top-down depth, vertical overlap is readable; horizontal overlap often creates ambiguity.
- Keep drop shadows conservative and standardized even when realism would vary their length.

Strong source modules: 20-22, 35, 43-45, 48, 51, 55, 56, 58, 61.

## Side-view tiles and action scenes

- Build tiles in three passes: large color fields and cabinet-like depth -> rough cluster texture -> selective fine detail.
- Separate visual edging from collision shape. Add support structures under static platforms.
- Prefer several simple background layers over one detailed layer that competes with the player.
- Design character scale against gameplay pace: smaller supports fast movement; larger supports deliberate positioning.
- A responsive jump/shot pose avoids decorative anticipation. Reuse compatible crouch/landing frames and separate legs/torso when combinatorial movement is expected.

Strong source modules: 7, 9, 23, 28, 31, 32, 36-38, 46, 50, 53, 60.

## Isometric assets

- Use the 2:1 stair-step line as a measured invariant. Work on a grid or keep a ruler motif; do not trust the eye alone.
- Construct cuboids and map hidden lines before detail. Pick one cube/edge style and keep it across the scene.
- Shade the three visible face families consistently. Textures must loop across every surface they occupy.
- Derive organic objects from geometric foundations, then soften them without losing scale or projection.
- Keep components layered for reuse and editing. Half-height water, stacked cubes, and reusable top-surface textures create depth economically.
- Isometric presentation is strong for deliberate tactics/building, weak for twitch platforming or precision action.

Strong source modules: 4, 41, 54, 61.

## Retro and severe-resolution work

- Treat missing information as the aesthetic. At 8x8, each pixel must carry orientation, identity, separation, or motion.
- Use two to four colors, a strong outline/separation strategy, and one exaggerated cue.
- Break larger enemies or machines into readable modules rather than enlarging a noisy blob.
- Preserve hardware-inspired palette/cluster economy without copying old display artifacts blindly; clean clusters for sharp modern displays.
- Reuse poses, palette swaps, and motifs. More frames/colors/details are not automatic improvements.

Strong source modules: 5, 7, 36-40, 47, 59, 60.

## UI and gameplay-readable art

- Define a visual grammar for health, currency, pickups, hazards, projectiles, and interaction states.
- Critical objects must remain distinct from backgrounds and each other by silhouette, outline, value, motion cue, or color role.
- Keep HUD emphasis peripheral until state changes demand attention. Gameplay feedback belongs near the affected sprite, not only in a gauge.
- Make appearance match behavior: homing, spread, laser, weight, speed, danger, and collectability should be inferable from shape and treatment.
- Measure poses and attacks against tile/hitbox expectations. Avoid phantom range and invisible unfair reach.

Strong source modules: 9, 24, 26, 31, 32, 36-38, 53, 56.

## 62-module transfer map

This map proves corpus coverage and gives a fast route back to the relevant lesson. Each row records the most transferable rule for static exact-grid work.

| # | Topic | Transferable rule |
|---:|---|---|
| 01 | Color palettes | value-ordered hue-shifted ramps; small scene sub-palettes |
| 02 | Texture | simplify, repeat, balance, contrast, remove accidental orphans |
| 03 | 3/4 projection | uniform projection and corner light beat strict realism |
| 04 | Isometric projection | measured 2:1 grid, reusable clusters, consistent face light |
| 05 | Basics | clusters are the unit; small canvas, hard edges, integer scale |
| 06 | Light and shadow | declare one source; directional planes, no pillow shading |
| 07 | Style | style comes from repeated constraints in color, clusters, view, scale, subject |
| 08 | Animation intro | strong key pose and anchor survive; excess detail/frames dilute energy |
| 09 | Melee | stance, readable arc, overshoot, and gameplay reach define the still |
| 10 | Water | connected wave rhythm, flow components, reflection color integration |
| 11 | Landscapes | atmospheric perspective through value, saturation, scale, and vertical position |
| 12 | Space | modular craft, neutral base plus accents, coherent light terminators |
| 13 | Rocks | geology determines silhouette, strata, fracture, erosion, and color |
| 14 | Cityscapes | constructive modules, shared light, landmark rhythm, organic countershape |
| 15 | Plants | botanical reference filtered through large masses and repeated clusters |
| 16 | Medieval fantasy | functional castles and iconic weapon/creature silhouettes preserve recognition |
| 17 | Human anatomy | line of action and proportion model before stylized volume |
| 18 | Flight | aircraft/cloud taxonomy, silhouette, and altitude-consistent depth |
| 19 | Mecha | human scale, cockpit logic, role trade-off, wraparound paint cues |
| 20 | Top-down tiles | seamless neutral base, negative space, key-cluster consistency |
| 21 | Top-down objects | reusable symmetry, geology/palette fit, short adaptable shadows |
| 22 | Top-down sprites | tile-unit scale, large identity cues, Y-overlap depth rules |
| 23 | Parallax | static depth first; divisible loops and quiet repeated layers |
| 24 | Items | iconic silhouette and consistent affordance/feedback language |
| 25 | Motion cycles | articulated extremes, anchor, and section-by-section construction |
| 26 | UX/UI | visual grammar, peripheral hierarchy, state-based feedback |
| 27 | Underwater | biology/material behavior and depth-dependent color create credibility |
| 28 | Side-view tiles | color block, rough cluster, fine detail; separate edging/collision |
| 29 | Anime faces/hair | anatomical placement plus hierarchical exaggeration; hair mass first |
| 30 | Food | appetizing local color, modular composition, deliberate outline treatment |
| 31 | Shmup design I | screen ratio controls pace; factions and hazards need instant separation |
| 32 | Shmup design II | behavior-shaped weapons/pickups; landmarks create visual pacing |
| 33 | Wind | coherent flow points and layered propagation, never random ambient noise |
| 34 | Farm | references, roof/body structure first, restrained weathering, asset meshing |
| 35 | Top-down interiors | cozy intent, tile-fit furniture, depth layers, live repetition proof |
| 36 | 8-bit adventure | two-pose economy, color swaps, biome-linked creature simplicity |
| 37 | Castlevania study | rework from multiple references; preserve limits and clean CRT-era clusters |
| 38 | Metroid study | stable center-of-gravity anchor and player-mobility-aware enemies |
| 39 | Sci-fi RPG | reusable body/head bases, essential shading, modular mixed-size tiles |
| 40 | Faux 3D | color/value progression sells depth and rotation more than shape churn |
| 41 | Isometric | count 2:1 pixels, map hidden structure, keep surface textures seamless |
| 42 | Cyberpunk | night-light hierarchy, warm-to-cool vertical depth, physical neon clutter |
| 43 | Top-down tiles II | layered overlays, recycled transitions, standardized short shadows |
| 44 | Top-down trees | reusable leaf bundles, spherical crown light, back-to-front assembly |
| 45 | Bricks/walls | divisible structure and grout first; variants and universal corners/shadows |
| 46 | Anti-gravity racers | manufacturer/role in silhouette; depth through omission and atmospheric layers |
| 47 | Tiny pixels | beauty from omitted information; one-pixel decisions and modular enemies |
| 48 | Military shmup | distinct silhouettes, skew-aware unique views, cheap coherent shadow/rig layers |
| 49 | Realistic anatomy | color-coded dummy, reference, proportion lines, detail only after volume |
| 50 | Walk cycle | contact/down/pass/swing clarity, cross-lateral limbs, asymmetric organic rhythm |
| 51 | City builder | recognizable idealization, foundation/roof sequence, subtle local outlines |
| 52 | Idle stance | personality, torso anchor, gravity-weighted asymmetry, restrained secondary motion |
| 53 | Punches/kicks | attack phase vocabulary, smear direction, hit emphasis, snap-back overshoot |
| 54 | More isometric | outlines/hidden lines first; luminous material ramps and measured bevel rhythm |
| 55 | Top-down animation | direction budget, reusable dummy, variable bounce, layer equipment |
| 56 | Top-down attacks | anticipation/smear/follow-through/recover encode weapon weight and reach |
| 57 | Knights/monsters/castles | anatomy or governing blob first; simple clusters before refined clusters |
| 58 | Top-down animation III | templates and layers preserve clarity; reduce flicker rather than worship pixels |
| 59 | Tiny sci-fi | 8x8 identity economy, outlines, baked light, diegetic scale compression |
| 60 | Run-and-gun | responsive poses, reusable walk/run structure, separate torso/legs, 8x8 tiles |
| 61 | Isometric mecha tactics | 32px abstraction, role-shaped units, reusable cube tops, half-height water |
| 62 | Landscape backgrounds | foreground service, atmospheric bands, color reuse, depth-scaled cluster grammar |

## Source note

The routing above was synthesized from the local educational `slynyrd-wiki` corpus, which in turn credits Raymond Schlitter's [Pixelblog catalogue](https://www.slynyrd.com/pixelblog-catalogue). Use the rules as craft prompts and evaluation lenses; do not request imitation of a living artist's signature style.

