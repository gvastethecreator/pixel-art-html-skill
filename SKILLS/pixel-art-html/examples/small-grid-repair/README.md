# Small-grid repair draft case study

Automatic 8x8/16x16 potion baselines, three same-grid directions, two authored repairs. Repair seam and information-budget choices — not artistic acceptance.

## Before and after

| Grid | Automatic draft | Authored repair |
|---|---|---|
| 8x8 | ![Automatic 8x8 draft](previews/automatic-8.png) | ![Authored 8x8 repair](previews/authored-8.png) |
| 16x16 | ![Automatic 16x16 draft](previews/automatic-16.png) | ![Authored 16x16 repair](previews/authored-16.png) |

8x8: sampled fragments → bottle mass; remaining cells on one diagonal amber cue. 16x16: only glass/liquid planes that survive native size. Lower singleton counts support inspection; don't prove a better read.

## Anonymous direction study

```powershell
python ..\..\scripts\build_pixel_art.py study .\directions\a-bound-flask.json .\directions\b-signal-vial.json .\directions\c-heart-reliquary.json --output .\output\study --title "8x8 potion direction study" --scale 24
```

Open `output/study/blind.html` first. Intended selection: Sample A — bottle identity + diagonal binding. Sample B tends toward a beacon; Sample C toward a heart emblem. Confirm the observation; don't inherit it.

## Repair contract

Every repair spec:

```json
{
  "repair_decisions": {
    "silhouette": "what structural read changed",
    "identity_cue": "which cue receives the cell budget",
    "subtraction": "which source detail was removed"
  }
}
```

Runner rejects a no-op or dimension change. Preserves the exact losing grid, records the delta, generates a neutral Sample A/B proof.

## Rebuild

```powershell
python ..\..\scripts\build_pixel_art.py repair .\baselines\8x8.json .\repairs\potion-8.json --output .\output\8x8 --scale 24
python ..\..\scripts\build_pixel_art.py repair .\baselines\16x16.json .\repairs\potion-16.json --output .\output\16x16 --scale 12
python ..\..\scripts\build_pixel_art.py validate .\output\8x8
python ..\..\scripts\build_pixel_art.py validate .\output\16x16
```

Both authored repairs stay `draft` until an authorized blind review is recorded and promoted.

## Transfer fixtures

Character and ship fixtures prove baseline preservation and repair metadata on other subjects. Authored 8x8 previews are near-abstract blocks — they don't support old prose of a running scout or arrowhead ship. Negative semantic fixtures: mechanics pass; recognition unassessed or failing.
