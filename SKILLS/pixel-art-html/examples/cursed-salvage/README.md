# Cursed salvage draft case study

This pack is a reproducible recovery draft, not representative evidence and not a style prescription. It preserves a useful lesson from an earlier rejected pickup pack: change construction and silhouette before polishing.

| Bound blood flask | Hooked ruin key | Bitten crimson shield | Fractured mana crystal |
|---|---|---|---|
| ![Bound blood flask](previews/potion.png) | ![Hooked ruin key](previews/key.png) | ![Bitten crimson shield](previews/shield.png) | ![Fractured mana crystal](previews/crystal.png) |

The four specs use different damaged silhouettes and share an amber repair motif, violet shadow family, light direction, and frame. The motif follows each volume instead of acting as a palette-only variant.

Known limits:

- the published materials were assessed only through structured author review;
- the key remains darker and less immediate than the other three items;
- the earlier direction search was not emitted through the anonymous `study` helper;
- no fingerprint-bound non-builder review exists.

The specs therefore declare `draft`. Use them to inspect compact full-grid authoring, family constraints, and subtraction—not as proof that the skill reliably produces accepted art.

## Rebuild

From this directory:

```powershell
python ..\..\scripts\build_pixel_art.py pack .\specs\potion.json .\specs\key.json .\specs\shield.json .\specs\crystal.json --output .\output --title "Cursed salvage pickups 48x48" --scale 5
python ..\..\scripts\build_pixel_art.py validate .\output
python ..\..\scripts\build_pixel_art.py critique .\output
```

Keep the result at `draft` until a non-builder completes the blind set review and `promote` succeeds.
