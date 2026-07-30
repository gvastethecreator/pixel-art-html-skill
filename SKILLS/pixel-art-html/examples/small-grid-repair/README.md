# Small-grid repair draft case study

This case keeps the real automatic 8x8/16x16 potion baselines, three same-grid directions, and two authored repairs. It demonstrates the repair seam and information-budget choices. It does not claim independent artistic acceptance.

## Before and after

| Grid | Automatic draft | Authored repair |
|---|---|---|
| 8x8 | ![Automatic 8x8 draft](previews/automatic-8.png) | ![Authored 8x8 repair](previews/authored-8.png) |
| 16x16 | ![Automatic 16x16 draft](previews/automatic-16.png) | ![Authored 16x16 repair](previews/authored-16.png) |

The 8x8 repair replaces sampled fragments with a bottle mass and spends its remaining cells on one diagonal amber cue. The 16x16 repair adds only the glass/liquid planes that survive native size. Lower singleton counts support inspection but do not prove a better read.

## Anonymous direction study

```powershell
python ..\..\scripts\build_pixel_art.py study .\directions\a-bound-flask.json .\directions\b-signal-vial.json .\directions\c-heart-reliquary.json --output .\output\study --title "8x8 potion direction study" --scale 24
```

Open `output/study/blind.html` first. The intended selection is Sample A because it preserves bottle identity and a diagonal binding; Sample B tends toward a beacon and Sample C toward a heart emblem. Re-check that observation rather than inheriting it.

## Repair contract

Every repair spec supplies:

```json
{
  "repair_decisions": {
    "silhouette": "what structural read changed",
    "identity_cue": "which cue receives the cell budget",
    "subtraction": "which source detail was removed"
  }
}
```

The runner rejects a no-op or dimension change, preserves the exact losing grid, records the delta, and generates a neutral Sample A/Sample B proof.

## Rebuild

```powershell
python ..\..\scripts\build_pixel_art.py repair .\baselines\8x8.json .\repairs\potion-8.json --output .\output\8x8 --scale 24
python ..\..\scripts\build_pixel_art.py repair .\baselines\16x16.json .\repairs\potion-16.json --output .\output\16x16 --scale 12
python ..\..\scripts\build_pixel_art.py validate .\output\8x8
python ..\..\scripts\build_pixel_art.py validate .\output\16x16
```

Both authored repairs remain `draft` until an authorized blind review is recorded and promoted.

## Transfer fixtures

The character and ship fixtures prove that baseline preservation and repair metadata work on other subjects. Their authored 8x8 previews are still near-abstract blocks and do not substantiate the old prose claims of a running scout or arrowhead ship. Treat them as negative semantic fixtures: mechanics pass, recognition is unassessed or failing.
