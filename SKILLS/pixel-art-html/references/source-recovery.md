# Small-grid source recovery

Use this reference when converting an uncertain image source to an exact 8x8-32x32 runtime grid. The recovery path improves cell placement; it does not replace low-resolution art direction or manual pixel editing.

## 1. Classify before packing

The local target-aware classifier emits one of three source classes:

- `exact-grid`: hard, internally uniform cells align to a plausible lattice. Nearest-neighbor preservation is safe only when that lattice exactly matches the requested target.
- `pseudo-pixel`: blocks are visible but fractional scaling, filtering, drift, or soft edges make the stored pixels unreliable as canonical cells. The local classifier does not invent an inferred lattice from the requested target.
- `painterly`: gradients, anti-aliasing, texture, or high local complexity dominate; no trustworthy source lattice is assumed.

Canonical `source.analysis` records confidence, detector, target grid, inferred grid when available, metrics, and human-readable reasons. A reviewer may use `--source-class` to override the class, but the override is recorded as `forced` / `user-override`. Detection never changes `--size`, `--sizes`, `--width`, or `--height`.

## 2. Choose the reconstruction route

`--reconstruction auto` is the normal path:

1. Preserve an exact-grid source with nearest sampling when its inferred lattice matches the target.
2. Otherwise align crop/padding at source resolution.
3. Quantize a temporary structure image with more labels than the final palette.
4. Select the winning structure label inside each target cell with center weighting.
5. Recover representative source color and majority alpha from that label.
6. Clamp to the requested final palette while preserving rare focal accents.

This separation prevents anti-aliased boundary colors from voting as if they were subject structure. `--structure-colors 0` derives a temporary budget from the requested final palette; explicit values from 2 through 64 are available for controlled experiments.

`--reconstruction legacy` retains resize-first conversion for regression comparison. `--reconstruction two-stage` forces target-aware packing even when the source appears exact.

## 3. Inspect the evidence

Generated proof HTML shows:

- source class and confidence;
- detector provenance;
- inferred lattice dimensions and step;
- applied reconstruction;
- a toggleable projection of the recovered source lattice over the target canvas.

The overlay is diagnostic and adaptively skips source lines when they would be closer than four display pixels; browser metrics record the displayed stride. A high-confidence lattice can still yield a poor 8x8 icon because recognition, pose, material, and focal hierarchy are not detector outputs.

## 4. Repair small grids

Automatic conversion always remains a draft at 8x8 and 16x16:

- redraw the outer silhouette before interior pixels;
- keep one orientation cue and one identity/focal cue;
- remove secondary forms that compete for the same cells;
- prefer connected dark, mid, and light clusters over local source fidelity;
- use at most one or two single-cell accents, only when they survive native 1x review;
- compare without the title or source image visible.

Image-derived canonical metadata sets `manual_repair_required` for these sizes unless an exact matching lattice was preserved. The proof page repeats that requirement as a review warning so a clean validator result cannot hide the missing authoring pass.

Compile the authored master against the losing canonical draft:

```bash
python <skill-dir>/scripts/build_pixel_art.py repair <draft>/pixel-art.json <repair-spec.json> --output <repair-output>
```

The repair spec uses the normal exact-grid schema and must add:

```json
{
  "repair_decisions": {
    "silhouette": "structural read changed",
    "identity_cue": "cue that receives the remaining cells",
    "subtraction": "source detail deliberately removed"
  }
}
```

The compiler rejects missing decisions, dimension drift, and zero-cell no-ops. Canonical output preserves the full baseline grid/palette, repair decisions, original image analysis when present, and recomputed changed/painted-cell evidence. Its proof page shows baseline and repair at equal scale; blind mode hides the artifact title and changes the captions to neutral `Sample A` / `Sample B` labels. These fields prove a reviewable authored intervention, never automatic artistic acceptance.

If the subject cannot read after subtraction, change the crop, pose, or source direction. More structure labels or colors will not repair an information-budget failure.

## 5. Run the deterministic reconstruction benchmark

```bash
uv run --with pillow==12.3.0 python <skill-dir>/scripts/benchmark_small_grids.py --output <benchmark-output>
```

The benchmark authors known masters at 8, 16, 24, and 32 cells, applies deterministic nearest, fractional, soft, affine-drift, noise, and JPEG degradations, and compares `legacy` with `two-stage`. It writes:

```text
benchmark.json
index.html
masters/*.png
sources/*
recovered/*.png
```

Use silhouette IoU, exact-cell ratio, RGB error, and composite reconstruction fidelity to catch packing regressions. The standalone report shows master, degraded source, and recovered output. These technical fixtures do not score composition, cluster craft, specificity, or subjective quality.

## 6. Optional Pixel Art Fixer boundary

When a local compatible Pixel Art Fixer binary is already installed, pass:

```bash
python <skill-dir>/scripts/build_pixel_art.py from-image <image> --sizes 8,16,24,32 --pixel-fixer-bin <binary> --pixel-fixer-mode full
```

The adapter:

- invokes a local process without a shell or hosted service;
- expects JSON containing `cols`, `rows`, `step_x`, and `step_y`;
- validates dimensions and positive finite step values;
- records stable result metadata without serializing the executable path;
- executes once and reuses the result across a resolution set;
- treats detection as advisory while the skill remains responsible for target packing, palette, alpha, proof, and manual repair.

No Pixel Art Fixer code or binary is vendored here. The integration design was informed by [Retro-Diffusion/pixel-art-fixer](https://github.com/Retro-Diffusion/pixel-art-fixer), commit `ef376e57e1c272633ca2dbf5f29ec3fcf6596465`, licensed MIT. Keep upstream evaluation and local artistic acceptance separate.
