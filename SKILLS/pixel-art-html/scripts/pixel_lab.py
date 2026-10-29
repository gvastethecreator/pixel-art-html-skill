#!/usr/bin/env python3
"""Locate pixel problems and apply small, preconditioned repairs to a new draft."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

import build_pixel_art as builder


def read_artifact(path: Path) -> dict:
    if path.is_dir():
        artifact = builder.validate_output(path)
    else:
        artifact = json.loads(path.read_text(encoding="utf-8-sig"))
        builder.validate_artifact(artifact)
    if "grid" not in artifact:
        raise ValueError("Select one canonical pixel-art.json, not a collection")
    return artifact


def integer(value, name: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer")
    return value


def region_bounds(region, artifact: dict) -> tuple[int, int, int, int]:
    if not isinstance(region, (list, tuple)) or len(region) != 4:
        raise ValueError("region must be [x, y, width, height]")
    x, y, width, height = (integer(v, "region coordinate") for v in region)
    if x < 0 or y < 0 or width < 1 or height < 1 or x + width > artifact["width"] or y + height > artifact["height"]:
        raise ValueError("region leaves the native grid")
    return x, y, width, height


def cluster_locations(artifact: dict) -> list[dict]:
    """Use the compiler's eight-neighbor convention, with explicit coordinates."""
    grid = artifact["grid"]
    seen = set()
    result = []
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            if color in (None, artifact["background"]) or (x, y) in seen:
                continue
            pending = [(x, y)]
            seen.add((x, y))
            cells = []
            while pending:
                px, py = pending.pop()
                cells.append([px, py])
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx, ny = px + dx, py + dy
                        if 0 <= nx < artifact["width"] and 0 <= ny < artifact["height"] and (nx, ny) not in seen and grid[ny][nx] == color:
                            seen.add((nx, ny))
                            pending.append((nx, ny))
            xs, ys = [c[0] for c in cells], [c[1] for c in cells]
            result.append({"color": color, "size": len(cells), "bbox": [min(xs), min(ys), max(xs), max(ys)],
                           "cells": sorted(cells, key=lambda point: (point[1], point[0]))})
    return sorted(result, key=lambda item: (item["size"], item["bbox"][1], item["bbox"][0]))


def inspect_artifact(artifact: dict, region=None, limit: int = 12) -> dict:
    x, y, width, height = region_bounds(region or [0, 0, artifact["width"], artifact["height"]], artifact)
    aliases = {color: f"p{i}" for i, color in enumerate(artifact["palette"])}
    aliases[None] = "."
    clusters = cluster_locations(artifact)
    visible = [c for c in clusters if any(x <= px < x + width and y <= py < y + height for px, py in c["cells"])]
    return {"fingerprint": builder.artifact_fingerprint(artifact), "region": [x, y, width, height],
            "coordinates": "zero-based; region is x,y,width,height; bbox is inclusive x0,y0,x1,y1",
            "legend": {alias: color for color, alias in aliases.items()},
            "rows": [{"y": py, "x_start": x, "cells": [aliases[c] for c in artifact["grid"][py][x:x + width]]} for py in range(y, y + height)],
            "palette_usage": dict(Counter(c for row in artifact["grid"] for c in row if c)),
            "small_clusters": [{k: v for k, v in c.items() if k != "cells" or c["size"] <= 4} for c in visible[:limit]],
            "cluster_connectivity": 8, "total_clusters_in_region": len(visible),
            "risk_note": "Small clusters may be eyes, glints, contour steps, or deliberate texture. Inspect before editing."}


def grid_delta(before: dict, after: dict) -> dict:
    if (before["width"], before["height"], before["background"]) != (after["width"], after["height"], after["background"]):
        raise ValueError("A pixel comparison needs the same dimensions and declared background")
    changes = [{"x": x, "y": y, "before": color, "after": after["grid"][y][x]}
               for y, row in enumerate(before["grid"]) for x, color in enumerate(row) if color != after["grid"][y][x]]
    background = before["background"]
    def occupied(color):
        return color is not None and color != background
    return {"before_fingerprint": builder.artifact_fingerprint(before), "after_fingerprint": builder.artifact_fingerprint(after),
            "changed_cells": len(changes),
            "silhouette_changes": sum(occupied(c["before"]) != occupied(c["after"]) for c in changes),
            "changes": changes, "verdict": "not-assessed; a delta does not prove improvement"}


def write_loupe(artifact: dict, output: Path, region=None, compare=None, background="#222222") -> dict:
    """Render a bounded coordinate diagnostic without altering either grid."""
    try:
        from PIL import Image, ImageColor, ImageDraw
    except ImportError as exc:
        raise ValueError("loupe requires Pillow; inspect, diff, and patch do not") from exc
    x, y, width, height = region_bounds(region or [0, 0, artifact["width"], artifact["height"]], artifact)
    if width > 32 or height > 32:
        raise ValueError("Choose a --region no larger than 32 by 32 cells")
    background = builder.normalize_color(background)
    if background is None:
        raise ValueError("loupe needs an opaque display background")
    receipt_path = output.with_suffix(".json")
    if output.suffix.lower() != ".png" or output.stem.lower() == "pixel-art" or output.exists() or receipt_path.exists():
        raise ValueError("Choose a new diagnostic PNG and JSON path, never pixel-art.png")
    delta = grid_delta(artifact, compare) if compare is not None else None
    artifacts = [artifact] + ([compare] if compare is not None else [])
    colors = list(dict.fromkeys(c for a in artifacts for c in a["palette"]))
    aliases = {c: f"p{i}" for i, c in enumerate(colors)}
    aliases[None] = "."
    scale = max(1, min(128 // artifact["width"], 128 // artifact["height"]))
    cell, left = 18, 42
    top = max(128, artifact["height"] * scale) + 60
    zoom_left = 36 + artifact["width"]
    panel_width = max(400, left + width * cell + 20, zoom_left + artifact["width"] * scale + 12)
    legend_top = top + height * cell + 24
    image = Image.new("RGB", (panel_width * len(artifacts), legend_top + 20 * (len(colors) + 2)), "#111111")
    draw = ImageDraw.Draw(image)
    panels = []
    for index, current in enumerate(artifacts):
        offset = index * panel_width
        native = Image.new("RGB", (current["width"], current["height"]), background)
        native.putdata([ImageColor.getrgb(c or background) for row in current["grid"] for c in row])
        draw.text((offset + 12, 10), "BASELINE" if compare is not None and index == 0 else "CURRENT", fill="#EEEEEE")
        image.paste(native, (offset + 12, 34))
        image.paste(native.resize((native.width * scale, native.height * scale), Image.Resampling.NEAREST), (offset + zoom_left, 34))
        draw.text((offset + 12, top - 22), f"ROI x={x}, y={y}, w={width}, h={height}", fill="#EEEEEE")
        for px in range(width):
            draw.text((offset + left + px * cell + 2, top - 12), str(x + px), fill="#AAAAAA")
        rows = []
        for py in range(height):
            draw.text((offset + 14, top + py * cell + 3), str(y + py), fill="#AAAAAA")
            row = current["grid"][y + py][x:x + width]
            rows.append({"y": y + py, "x_start": x, "cells": [aliases[c] for c in row]})
            for px, color in enumerate(row):
                sx, sy = offset + left + px * cell, top + py * cell
                draw.rectangle((sx, sy, sx + cell - 2, sy + cell - 2), fill=color or background)
        panels.append({"fingerprint": builder.artifact_fingerprint(current), "rows": rows,
                       "roi_image_origin_xy": [offset + left, top]})
    for index, color in enumerate(colors):
        draw.rectangle((12, legend_top + index * 20, 25, legend_top + index * 20 + 13), fill=color)
        draw.text((34, legend_top + index * 20), f"{aliases[color]}  {color}", fill="#EEEEEE")
    draw.text((12, legend_top + len(colors) * 20), ". = transparent; labels and gaps are diagnostic", fill="#AAAAAA")
    report = {"kind": "coordinate-loupe", "region": [x, y, width, height], "display_background": background,
              "coordinates": "zero-based native cells; image origins and cell pitch are diagnostic pixels",
              "legend": {alias: color for color, alias in aliases.items()}, "panels": panels,
              "cell_pitch": cell, "delta": delta,
              "verdict": "not-assessed; inspect native and browser views before accepting a repair"}
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    receipt_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def apply_patch(artifact: dict, patch: dict) -> tuple[dict, dict]:
    if patch.get("base_fingerprint") != builder.artifact_fingerprint(artifact):
        raise ValueError("base_fingerprint does not match; inspect the current grid before applying this repair")
    if not isinstance(patch.get("hypothesis"), str) or not patch["hypothesis"].strip():
        raise ValueError("hypothesis must state the visible problem and expected improvement")
    edits = patch.get("edits")
    if not isinstance(edits, list) or not edits:
        raise ValueError("edits must be a non-empty list")
    protected = [region_bounds(r, artifact) for r in patch.get("protected_regions", [])]
    grid = [row[:] for row in artifact["grid"]]
    seen = set()
    for edit in edits:
        if not isinstance(edit, dict) or not {"x", "y", "before", "after"} <= edit.keys():
            raise ValueError("Each edit needs x, y, before, and after")
        x, y = integer(edit["x"], "x"), integer(edit["y"], "y")
        region_bounds([x, y, 1, 1], artifact)
        if (x, y) in seen:
            raise ValueError(f"Repeated edit at ({x}, {y})")
        if any(px <= x < px + width and py <= y < py + height for px, py, width, height in protected):
            raise ValueError(f"Edit touches protected region at ({x}, {y})")
        before, after = builder.normalize_color(edit["before"]), builder.normalize_color(edit["after"])
        if grid[y][x] != before:
            raise ValueError(f"before color does not match at ({x}, {y})")
        if before == after:
            raise ValueError(f"Edit does not change ({x}, {y})")
        grid[y][x] = after
        seen.add((x, y))
    if "max_colors" in patch:
        maximum = integer(patch["max_colors"], "max_colors")
        if maximum < 1 or len({c for row in grid for c in row if c}) > maximum:
            raise ValueError("Repair exceeds max_colors")
    spec = {"title": artifact["title"], "width": artifact["width"], "height": artifact["height"],
            "background": artifact["background"], "grid": grid, "evidence_tier": "draft",
            "art_direction": artifact.get("source", {}).get("art_direction", {}),
            "repair_decisions": patch.get("repair_decisions")}
    repaired = builder.compile_repair(artifact, spec)
    return repaired, grid_delta(artifact, repaired)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inspect_cmd = commands.add_parser("inspect")
    inspect_cmd.add_argument("artifact", type=Path)
    inspect_cmd.add_argument("--region", type=int, nargs=4, metavar=("X", "Y", "W", "H"))
    inspect_cmd.add_argument("--limit", type=int, default=12)
    diff_cmd = commands.add_parser("diff")
    diff_cmd.add_argument("before", type=Path)
    diff_cmd.add_argument("after", type=Path)
    loupe_cmd = commands.add_parser("loupe")
    loupe_cmd.add_argument("artifact", type=Path)
    loupe_cmd.add_argument("--region", type=int, nargs=4, metavar=("X", "Y", "W", "H"))
    loupe_cmd.add_argument("--compare", type=Path)
    loupe_cmd.add_argument("--background", default="#222222")
    loupe_cmd.add_argument("--output", type=Path, required=True)
    patch_cmd = commands.add_parser("patch")
    patch_cmd.add_argument("artifact", type=Path)
    patch_cmd.add_argument("patch", type=Path)
    patch_cmd.add_argument("--output", type=Path, required=True)
    patch_cmd.add_argument("--scale", type=int, choices=range(1, 33), default=12,
                           help="PNG integer scale; 1 exports native pixels (default: 12)")
    args = parser.parse_args()
    try:
        if args.command == "inspect":
            if args.limit < 1:
                raise ValueError("limit must be positive")
            result = inspect_artifact(read_artifact(args.artifact), args.region, args.limit)
        elif args.command == "diff":
            result = grid_delta(read_artifact(args.before), read_artifact(args.after))
        elif args.command == "loupe":
            result = write_loupe(read_artifact(args.artifact), args.output, args.region,
                                 read_artifact(args.compare) if args.compare else None, args.background)
        else:
            if args.output.exists():
                raise ValueError("Repair output must be a new directory; keep the baseline")
            artifact = read_artifact(args.artifact)
            patch = json.loads(args.patch.read_text(encoding="utf-8-sig"))
            repaired, result = apply_patch(artifact, patch)
            builder.write_artifact(repaired, args.output, args.scale)
            (args.output / "patch.json").write_text(json.dumps(patch, indent=2) + "\n", encoding="utf-8")
            (args.output / "delta.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"Pixel lab: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
