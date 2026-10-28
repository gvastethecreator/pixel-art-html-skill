# Environments, materials, and tiles

Use unequal crown groups with selective overlap and visible branch continuity. Uniform light bands flatten foliage; completely isolated bright balls can look like a topiary. For rivers, change bend length and width with depth and terrain. Keep enough value separation between overlapping ridges even when the distant scene is quiet.

Retrieve `foliage-bundles`, `stone-facets`, `water-flow`, `masonry-rhythm`, `tiles-and-transitions`, or `landscape-depth` with `reference_library.py techniques`. For a tree, separate crown placement from leaf texture. For a tileset, build a small mixed neighborhood before multiplying variants. For a scene, solve depth bands before local material detail.

## Direction choices

- Establish depth bands through value, saturation, scale, overlap, and vertical position.
- Define a small cluster vocabulary for each material and one quiet-area rule.
- A tile base must be neutral enough to repeat. Landmarks belong in sparse variants or overlays.
- Backgrounds serve the focal subject. Lower distant contrast and cluster density.

## Build

1. Block foreground, middle, and distance as large value masses.
2. Shape the governing material structure: strata for rock, crown masses for foliage, connected flow for water, grout rhythm for walls, plane breaks for metal.
3. Repeat a small cluster vocabulary with controlled spacing, hue, and orientation. Inspect overlap junctions for holes and isolated remnants.
4. For seamless work, make opposite edges agree and inspect the generated 3x repeat proof.
5. If variants were requested, preserve projection, light, palette roles, and edge contract.

## Reject

- homogeneous noise or unique marks everywhere
- isolated pixels used as general texture
- one high-contrast landmark repeated in every tile
- seams, dominant crosses, or accidental diagonals in 3x context
- equal detail and contrast across all depth planes
- water, foliage, rock, or brick distinguished only by hue
- mechanically downscaled backgrounds whose clusters no longer match depth
