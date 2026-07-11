# Pixel-art quality contract

## Composition

- Preserve one dominant silhouette and one focal detail.
- Reserve padding around isolated subjects; avoid accidental edge contact.
- Use asymmetry intentionally. Do not add noise merely to appear handmade.
- Remove details that collapse below the target resolution.

## Palette

- Use value separation before hue variety.
- Give outline, shadow, base, light, and accent distinct jobs.
- Default to 8-16 colors for icons and 16-32 for compact scenes.
- Avoid dithering on tiny icons unless it clarifies a gradient or material.

## Image conversion

- Use `contain` for complete icons and characters.
- Use `cover` for scenes where filling the frame matters.
- Use `stretch` only when distortion is explicitly acceptable.
- Prefer a transparent or simple flat source background.
- Inspect alpha edges after conversion; regenerate or preprocess sources with halos.
- For multi-resolution output, convert every size directly from the original source. Never chain resizes.

## Resolution ladder

- 16x16: silhouette, pose, and one identity cue.
- 24x24: add one secondary shape or material break.
- 32x32: balanced default master.
- 40x40: add one detail tier while preserving compact clusters.
- 48x48: add controlled surface detail without noisy single pixels.
- 64x64: preserve clusters and hierarchy; do not fill space merely because cells are available.
- Compare all masters at native size before accepting the set.

## ImageGen source prompts

Include: centered subject, clean silhouette, broad value groups, limited visual clutter, target use and target grid, flat/removable background, no text, no watermark.

Do not depend on ImageGen to produce an exact pixel grid. Generate a readable source, then convert it deterministically.

## Rejection conditions

- Empty or nearly empty canvas.
- Blurred display or non-integer scaling.
- Clipped identity features.
- Palette count above the requested limit.
- Subject recognizable only in the source image, not in the final grid.
- HTML requiring a server, CDN, font, framework, or network request.
