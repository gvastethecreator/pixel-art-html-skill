#!/usr/bin/env python3
from __future__ import annotations

import argparse
import binascii
from collections.abc import Iterator
from datetime import datetime, timezone
import html
import json
import re
import struct
import sys
import unicodedata
import zlib
from collections import Counter
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "assets" / "pixel-art-template.html"
COLLECTION_TEMPLATE_PATH = SKILL_DIR / "assets" / "pixel-art-collection-template.html"
PROJECT_HUB_TEMPLATE_PATH = SKILL_DIR / "assets" / "pixel-art-project-hub-template.html"
CLEAR_TOKENS = {None, "", ".", "..", "none", "null", "transparent", "clear"}
RECOMMENDED_SIZES = (16, 24, 32, 40, 48, 64)
WINDOWS_RESERVED_NAMES = {"CON", "PRN", "AUX", "NUL", *(f"COM{index}" for index in range(1, 10)), *(f"LPT{index}" for index in range(1, 10))}


class ArtifactError(ValueError):
    pass


def normalize_color(value: Any, palette: dict[str, str] | None = None) -> str | None:
    if value is None:
        return None
    if isinstance(value, str) and palette and value in palette:
        value = palette[value]
    text = str(value).strip()
    if text.lower() in CLEAR_TOKENS:
        return None
    if text.startswith("#"):
        text = text[1:]
    if len(text) == 3 and all(char in "0123456789abcdefABCDEF" for char in text):
        text = "".join(char * 2 for char in text)
    if len(text) != 6 or not all(char in "0123456789abcdefABCDEF" for char in text):
        raise ArtifactError(f"Invalid color: {value!r}")
    return f"#{text.upper()}"


def checked_dimension(value: Any, name: str) -> int:
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ArtifactError(f"{name} must be an integer") from exc
    if not 8 <= result <= 128:
        raise ArtifactError(f"{name} must be between 8 and 128")
    return result


def checked_int(value: Any, name: str) -> int:
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ArtifactError(f"{name} must be an integer") from exc


def pattern_rows(value: Any, name: str, palette: dict[str, str | None] | None = None) -> list[list[Any]]:
    if not isinstance(value, list) or not value:
        raise ArtifactError(f"{name} must be a non-empty row list")
    rows: list[list[Any]] = []
    width: int | None = None
    for index, row in enumerate(value):
        if isinstance(row, str):
            text = row.strip()
            if (palette and text in palette) or text.lower() in CLEAR_TOKENS:
                cells = [text]
            else:
                cells = text.split() if any(char.isspace() for char in text) else list(text)
        else:
            cells = row
        if not isinstance(cells, list) or not cells:
            raise ArtifactError(f"{name} row {index} must contain cells")
        if any(cell is not None and not isinstance(cell, str) for cell in cells):
            raise ArtifactError(f"{name} row {index} cells must be strings or null")
        if width is None:
            width = len(cells)
        elif len(cells) != width:
            raise ArtifactError(f"{name} rows must have equal width")
        rows.append(cells)
    return rows


def compile_spec(spec: dict[str, Any]) -> dict[str, Any]:
    width = checked_dimension(spec.get("width", 32), "width")
    height = checked_dimension(spec.get("height", 32), "height")
    raw_palette = spec.get("palette", {})
    if not isinstance(raw_palette, dict):
        raise ArtifactError("palette must be an object")
    palette = {str(key): normalize_color(value) for key, value in raw_palette.items()}
    if any(value is None for value in palette.values()):
        raise ArtifactError("palette entries must be opaque colors")
    background = normalize_color(spec.get("background"), palette)
    grid: list[list[str | None]] = [[background for _ in range(width)] for _ in range(height)]

    if "grid" in spec:
        rows = spec["grid"]
        if not isinstance(rows, list) or len(rows) != height:
            raise ArtifactError(f"grid must contain {height} rows")
        compiled_rows: list[list[str | None]] = []
        for y, row in enumerate(rows):
            cells = row.split() if isinstance(row, str) else row
            if not isinstance(cells, list) or len(cells) != width:
                raise ArtifactError(f"grid row {y} must contain {width} cells")
            compiled_rows.append([normalize_color(cell, palette) for cell in cells])
        grid = compiled_rows

    def paint(x: int, y: int, color: Any) -> None:
        if not (0 <= x < width and 0 <= y < height):
            raise ArtifactError(f"coordinate out of bounds: ({x}, {y})")
        grid[y][x] = normalize_color(color, palette)

    for index, rect in enumerate(spec.get("rects", [])):
        if not isinstance(rect, dict):
            raise ArtifactError(f"rects[{index}] must be an object")
        x = checked_int(rect.get("x"), "rect.x")
        y = checked_int(rect.get("y"), "rect.y")
        rect_width = checked_int(rect.get("width"), "rect.width")
        rect_height = checked_int(rect.get("height"), "rect.height")
        if rect_width <= 0 or rect_height <= 0:
            raise ArtifactError("rectangle dimensions must be positive")
        for yy in range(y, y + rect_height):
            for xx in range(x, x + rect_width):
                paint(xx, yy, rect.get("color"))

    for index, run in enumerate(spec.get("runs", [])):
        if not isinstance(run, dict):
            raise ArtifactError(f"runs[{index}] must be an object")
        x = checked_int(run.get("x"), "run.x")
        y = checked_int(run.get("y"), "run.y")
        length = checked_int(run.get("length"), "run.length")
        if length <= 0:
            raise ArtifactError("run length must be positive")
        for xx in range(x, x + length):
            paint(xx, y, run.get("color"))

    raw_motifs = spec.get("motifs", {})
    if not isinstance(raw_motifs, dict):
        raise ArtifactError("motifs must be an object")
    motifs = {str(name): pattern_rows(rows, f"motifs.{name}", palette) for name, rows in raw_motifs.items()}
    for index, stamp in enumerate(spec.get("stamps", [])):
        if not isinstance(stamp, dict):
            raise ArtifactError(f"stamps[{index}] must be an object")
        motif_name = str(stamp.get("motif", ""))
        if motif_name not in motifs:
            raise ArtifactError(f"unknown motif: {motif_name!r}")
        x = checked_int(stamp.get("x"), "stamp.x")
        y = checked_int(stamp.get("y"), "stamp.y")
        color_map = stamp.get("map", {})
        if not isinstance(color_map, dict):
            raise ArtifactError(f"stamps[{index}].map must be an object")
        rows = motifs[motif_name]
        if stamp.get("flip_y", False):
            rows = list(reversed(rows))
        for offset_y, source_row in enumerate(rows):
            row = list(reversed(source_row)) if stamp.get("flip_x", False) else source_row
            for offset_x, source_color in enumerate(row):
                mapped_color = color_map.get(source_color, source_color)
                if normalize_color(mapped_color, palette) is not None:
                    paint(x + offset_x, y + offset_y, mapped_color)

    for index, pixel in enumerate(spec.get("pixels", [])):
        if not isinstance(pixel, dict):
            raise ArtifactError(f"pixels[{index}] must be an object")
        paint(checked_int(pixel.get("x"), "pixel.x"), checked_int(pixel.get("y"), "pixel.y"), pixel.get("color"))

    art_direction = spec.get("art_direction", {})
    if not isinstance(art_direction, dict) or any(not isinstance(key, str) or not isinstance(value, str) for key, value in art_direction.items()):
        raise ArtifactError("art_direction must be a string-to-string object")
    return canonical_artifact(
        title=str(spec.get("title") or "Untitled pixel art"),
        grid=grid,
        background=background,
        source={"kind": "spec", "art_direction": art_direction},
    )


def source_requires_repeat_proof(source: dict[str, Any]) -> bool:
    art_direction = source.get("art_direction", {})
    if not isinstance(art_direction, dict):
        return False
    use = str(art_direction.get("use", "")).lower()
    return bool(re.search(r"\b(tile|tileset|texture|seamless)\b", use))


def canonical_artifact(*, title: str, grid: list[list[str | None]], background: str | None, source: dict[str, Any]) -> dict[str, Any]:
    if not grid or not grid[0]:
        raise ArtifactError("grid cannot be empty")
    width = len(grid[0])
    height = len(grid)
    colors: list[str] = []
    seen: set[str] = set()
    normalized_grid: list[list[str | None]] = []
    for y, row in enumerate(grid):
        if len(row) != width:
            raise ArtifactError(f"grid row {y} width mismatch")
        normalized_row = []
        for cell in row:
            color = normalize_color(cell)
            normalized_row.append(color)
            if color and color not in seen:
                colors.append(color)
                seen.add(color)
        normalized_grid.append(normalized_row)
    artifact = {
        "schema_version": 1,
        "title": title,
        "width": width,
        "height": height,
        "background": normalize_color(background),
        "palette": colors,
        "grid": normalized_grid,
        "source": source,
        "proofs": {"repeat_3x": source_requires_repeat_proof(source)},
    }
    artifact["quality"] = artifact_quality_report(artifact)
    return artifact


def color_luminance(color: str) -> float:
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def artifact_quality_report(artifact: dict[str, Any]) -> dict[str, Any]:
    grid = artifact["grid"]
    width = artifact["width"]
    height = artifact["height"]
    background = normalize_color(artifact.get("background"))
    subject = {(x, y) for y, row in enumerate(grid) for x, color in enumerate(row) if color is not None and color != background}
    colors = sorted({color for row in grid for color in row if color})
    luminances = [color_luminance(color) for color in colors]
    visited: set[tuple[int, int]] = set()
    clusters: list[int] = []
    for start in subject:
        if start in visited:
            continue
        target = grid[start[1]][start[0]]
        pending = [start]
        visited.add(start)
        size = 0
        while pending:
            x, y = pending.pop()
            size += 1
            for neighbor in (
                (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                (x - 1, y),                     (x + 1, y),
                (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
            ):
                nx, ny = neighbor
                if 0 <= nx < width and 0 <= ny < height and neighbor not in visited and grid[ny][nx] == target:
                    visited.add(neighbor)
                    pending.append(neighbor)
        clusters.append(size)

    boundary_contrasts: list[float] = []
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            if not color:
                continue
            for nx, ny in ((x + 1, y), (x, y + 1)):
                if nx >= width or ny >= height:
                    continue
                adjacent = grid[ny][nx]
                if adjacent and adjacent != color:
                    boundary_contrasts.append(abs(color_luminance(color) - color_luminance(adjacent)))

    if subject:
        xs = [point[0] for point in subject]
        ys = [point[1] for point in subject]
        bbox: list[int] | None = [min(xs), min(ys), max(xs), max(ys)]
        padding: list[int] | None = [min(xs), min(ys), width - 1 - max(xs), height - 1 - max(ys)]
    else:
        bbox = None
        padding = None

    singleton_count = sum(size == 1 for size in clusters)
    warnings: list[str] = []
    if background and not subject:
        warnings.append("No cells differ from the declared background.")
    if len(colors) > 16 and max(width, height) <= 32:
        warnings.append("More than 16 colors on a small grid may weaken palette economy.")
    if len(clusters) >= 4 and singleton_count / len(clusters) > 0.35:
        warnings.append("Many same-color clusters are single pixels; inspect for orphan-pixel noise.")
    value_span = round(max(luminances) - min(luminances), 4) if luminances else 0.0
    if len(colors) > 1 and value_span < 0.18:
        warnings.append("Palette value span is narrow; inspect silhouette and volume readability.")
    low_contrast_ratio = round(sum(value < 0.08 for value in boundary_contrasts) / len(boundary_contrasts), 4) if boundary_contrasts else 0.0
    if len(boundary_contrasts) >= 6 and low_contrast_ratio > 0.6:
        warnings.append("Most color boundaries have low luminance contrast; inspect focal hierarchy.")

    return {
        "subject_cells": len(subject),
        "bbox": bbox,
        "padding": padding,
        "clusters": len(clusters),
        "single_pixel_clusters": singleton_count,
        "value_span": value_span,
        "low_contrast_boundary_ratio": low_contrast_ratio,
        "warnings": warnings,
    }


def critique_output(output: Path) -> dict[str, Any]:
    result = validate_output(output)
    if result.get("kind") in {"collection", "pack"}:
        return {
            "status": "ok",
            "kind": result["kind"],
            "output": str(output.resolve()),
            "items": [
                {"path": item["path"], "quality": artifact_quality_report(json.loads((output / item["path"] / "pixel-art.json").read_text(encoding="utf-8")))}
                for item in result["items"]
            ],
        }
    return {"status": "ok", "kind": "single", "output": str(output.resolve()), "quality": artifact_quality_report(result)}


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", binascii.crc32(kind + payload) & 0xFFFFFFFF)


def write_png(artifact: dict[str, Any], path: Path, scale: int) -> None:
    if not 1 <= scale <= 32:
        raise ArtifactError("scale must be between 1 and 32")
    width = artifact["width"] * scale
    height = artifact["height"] * scale
    rows: list[bytes] = []
    for source_row in artifact["grid"]:
        row = bytearray()
        for color in source_row:
            if color:
                rgba = bytes((int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16), 255))
            else:
                rgba = bytes((0, 0, 0, 0))
            row.extend(rgba * scale)
        encoded = b"\x00" + bytes(row)
        rows.extend([encoded] * scale)
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    path.write_bytes(signature + png_chunk(b"IHDR", ihdr) + png_chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + png_chunk(b"IEND", b""))


def paeth_predictor(left: int, above: int, upper_left: int) -> int:
    estimate = left + above - upper_left
    left_distance = abs(estimate - left)
    above_distance = abs(estimate - above)
    upper_left_distance = abs(estimate - upper_left)
    if left_distance <= above_distance and left_distance <= upper_left_distance:
        return left
    if above_distance <= upper_left_distance:
        return above
    return upper_left


def read_png_rgba(path: Path) -> tuple[int, int, Iterator[bytes]]:
    payload = path.read_bytes()
    if payload[:8] != b"\x89PNG\r\n\x1a\n":
        raise ArtifactError(f"{path.name} is not a PNG")
    position = 8
    header: tuple[int, int, int, int, int, int, int] | None = None
    compressed_chunks: list[bytes] = []
    saw_end = False
    while position + 12 <= len(payload):
        length = struct.unpack(">I", payload[position:position + 4])[0]
        kind = payload[position + 4:position + 8]
        start = position + 8
        end = start + length
        if end + 4 > len(payload):
            raise ArtifactError(f"{path.name} contains a truncated PNG chunk")
        chunk = payload[start:end]
        expected_crc = struct.unpack(">I", payload[end:end + 4])[0]
        if binascii.crc32(kind + chunk) & 0xFFFFFFFF != expected_crc:
            raise ArtifactError(f"{path.name} contains a corrupt PNG chunk")
        if kind == b"IHDR":
            if length != 13:
                raise ArtifactError(f"{path.name} has an invalid PNG header")
            header = struct.unpack(">IIBBBBB", chunk)
        elif kind == b"IDAT":
            compressed_chunks.append(chunk)
        elif kind == b"IEND":
            saw_end = True
            break
        position = end + 4
    if header is None or not compressed_chunks or not saw_end:
        raise ArtifactError(f"{path.name} is missing required PNG chunks")
    width, height, bit_depth, color_type, compression, filter_method, interlace = header
    if (bit_depth, color_type, compression, filter_method, interlace) != (8, 6, 0, 0, 0):
        raise ArtifactError(f"{path.name} must be a non-interlaced 8-bit RGBA PNG")
    stride = width * 4

    def decoded_rows() -> Iterator[bytes]:
        previous = bytearray(stride)
        buffer = bytearray()
        row_count = 0
        decompressor = zlib.decompressobj()
        stream_ended = False
        row_size = stride + 1

        def decode(row_payload: bytes) -> bytes:
            nonlocal previous
            filter_type = row_payload[0]
            encoded = row_payload[1:]
            if filter_type > 4:
                raise ArtifactError(f"{path.name} uses an unsupported PNG row filter")
            decoded = bytearray(stride)
            if filter_type == 0:
                decoded[:] = encoded
            else:
                for index, value in enumerate(encoded):
                    left = decoded[index - 4] if index >= 4 else 0
                    above = previous[index]
                    upper_left = previous[index - 4] if index >= 4 else 0
                    if filter_type == 1:
                        predictor = left
                    elif filter_type == 2:
                        predictor = above
                    elif filter_type == 3:
                        predictor = (left + above) // 2
                    else:
                        predictor = paeth_predictor(left, above, upper_left)
                    decoded[index] = (value + predictor) & 0xFF
            previous = decoded
            return bytes(decoded)

        try:
            for compressed in compressed_chunks:
                if stream_ended:
                    if compressed:
                        raise ArtifactError(f"{path.name} contains compressed data after the PNG pixel stream")
                    continue
                pending = compressed
                while pending:
                    pending_size = len(pending)
                    emitted = decompressor.decompress(pending, row_size - len(buffer))
                    buffer.extend(emitted)
                    pending = decompressor.unconsumed_tail
                    if decompressor.unused_data:
                        raise ArtifactError(f"{path.name} contains an extra compressed stream")
                    if len(buffer) == row_size:
                        if row_count >= height:
                            raise ArtifactError(f"{path.name} pixel payload exceeds its header")
                        row_count += 1
                        yield decode(bytes(buffer))
                        buffer.clear()
                    if decompressor.eof:
                        if pending:
                            raise ArtifactError(f"{path.name} contains compressed data after the PNG pixel stream")
                        stream_ended = True
                        break
                    if not pending:
                        break
                    if len(pending) == pending_size and not emitted:
                        raise ArtifactError(f"{path.name} compressed pixel stream made no progress")
        except zlib.error as exc:
            raise ArtifactError(f"{path.name} contains invalid compressed pixels") from exc
        if row_count != height or buffer or not stream_ended or not decompressor.eof or decompressor.unused_data:
            raise ArtifactError(f"{path.name} pixel payload size does not match its header")

    return width, height, decoded_rows()


def validate_png_parity(artifact: dict[str, Any], path: Path) -> int:
    png_width, png_height, png_rows = read_png_rgba(path)
    width = artifact["width"]
    height = artifact["height"]
    if png_width % width or png_height % height:
        raise ArtifactError("pixel-art.png dimensions are not an integer scale of the canonical grid")
    scale_x = png_width // width
    scale_y = png_height // height
    if scale_x != scale_y or not 1 <= scale_x <= 32:
        raise ArtifactError("pixel-art.png must use one integer scale from 1 through 32")
    scale = scale_x
    row_iterator = iter(png_rows)
    for source_row in artifact["grid"]:
        expected = bytearray()
        for color in source_row:
            rgba = bytes((int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16), 255)) if color else b"\x00\x00\x00\x00"
            expected.extend(rgba * scale)
        expected_row = bytes(expected)
        for _ in range(scale):
            try:
                png_row = next(row_iterator)
            except StopIteration as exc:
                raise ArtifactError("pixel-art.png ended before the canonical grid") from exc
            if png_row != expected_row:
                raise ArtifactError("pixel-art.png pixels do not match the canonical grid")
    try:
        next(row_iterator)
    except StopIteration:
        pass
    else:
        raise ArtifactError("pixel-art.png contains rows beyond the canonical grid")
    return scale


def render_html(artifact: dict[str, Any], path: Path) -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    payload = json.dumps(artifact, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("&", "\\u0026")
    title_text = html.escape(str(artifact["title"]))
    result = template.replace("__TITLE_TEXT__", title_text).replace("__ARTIFACT_JSON__", payload)
    if "__ARTIFACT_JSON__" in result or "__TITLE_TEXT__" in result:
        raise ArtifactError("template placeholder replacement failed")
    path.write_text(result, encoding="utf-8", newline="\n")


def render_collection_html(title: str, items: list[dict[str, Any]], path: Path, kind: str = "collection") -> None:
    template = COLLECTION_TEMPLATE_PATH.read_text(encoding="utf-8")
    payload = json.dumps({"kind": kind, "title": title, "items": items}, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("&", "\\u0026")
    result = template.replace("__TITLE_TEXT__", html.escape(title)).replace("__COLLECTION_JSON__", payload)
    if "__COLLECTION_JSON__" in result or "__TITLE_TEXT__" in result:
        raise ArtifactError("collection template placeholder replacement failed")
    path.write_text(result, encoding="utf-8", newline="\n")


def write_artifact(artifact: dict[str, Any], output: Path, scale: int) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "pixel-art.json").write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    render_html(artifact, output / "index.html")
    write_png(artifact, output / "pixel-art.png", scale)


def write_collection(artifacts: list[dict[str, Any]], output: Path, scale: int, title: str, kind: str = "collection") -> dict[str, Any]:
    if len(artifacts) < 2:
        raise ArtifactError("a collection or pack needs at least two artifacts")
    if kind not in {"collection", "pack"}:
        raise ArtifactError(f"unsupported collection kind: {kind}")
    output.mkdir(parents=True, exist_ok=True)
    manifest_items: list[dict[str, Any]] = []
    html_items: list[dict[str, Any]] = []
    used_paths: set[str] = set()
    for artifact in artifacts:
        validate_artifact(artifact)
        relative_path = f"{artifact['width']}x{artifact['height']}" if kind == "collection" else slugify(artifact["title"])
        if relative_path in used_paths:
            if kind == "collection":
                raise ArtifactError(f"duplicate collection dimensions: {relative_path}")
            suffix = 2
            base_path = relative_path
            while relative_path in used_paths:
                relative_path = f"{base_path}-{suffix}"
                suffix += 1
        used_paths.add(relative_path)
        write_artifact(artifact, output / relative_path, scale)
        manifest_items.append({
            "path": relative_path,
            "title": artifact["title"],
            "width": artifact["width"],
            "height": artifact["height"],
            "colors": len(artifact["palette"]),
        })
        html_items.append({"path": relative_path, "artifact": artifact})
    manifest = {"schema_version": 1, "kind": kind, "title": title, "items": manifest_items}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    render_collection_html(title, html_items, output / "index.html", kind)
    return manifest


def parse_sizes(value: str) -> list[int]:
    tokens = [str(size) for size in RECOMMENDED_SIZES] if value.strip().lower() == "all" else [token.strip() for token in value.split(",") if token.strip()]
    if not tokens:
        raise ArtifactError("sizes cannot be empty")
    sizes = [checked_dimension(token, "size") for token in tokens]
    if len(sizes) != len(set(sizes)):
        raise ArtifactError("sizes cannot contain duplicates")
    return sizes


def fit_image(image: Any, width: int, height: int, fit: str) -> Any:
    from PIL import Image

    source = image.convert("RGBA")
    if fit == "stretch":
        return source.resize((width, height), Image.Resampling.LANCZOS)
    source_ratio = source.width / source.height
    target_ratio = width / height
    if fit == "contain":
        scale = min(width / source.width, height / source.height)
    else:
        scale = max(width / source.width, height / source.height)
    resized = source.resize((max(1, round(source.width * scale)), max(1, round(source.height * scale))), Image.Resampling.LANCZOS)
    if fit == "contain":
        result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        result.alpha_composite(resized, ((width - resized.width) // 2, (height - resized.height) // 2))
        return result
    left = max(0, (resized.width - width) // 2)
    top = max(0, (resized.height - height) // 2)
    return resized.crop((left, top, left + width, top + height))


def image_pixels(image: Any) -> list[Any]:
    flattened = getattr(image, "get_flattened_data", None)
    return list(flattened()) if flattened else list(image.getdata())


def artifact_from_image(args: argparse.Namespace) -> dict[str, Any]:
    try:
        from PIL import Image
    except ImportError as exc:
        raise ArtifactError("Pillow is required for from-image. Run with: uv run --with pillow==11.0.0 python ...") from exc

    width = checked_dimension(args.width or args.size, "width")
    height = checked_dimension(args.height or args.size, "height")
    if not 2 <= args.colors <= 256:
        raise ArtifactError("colors must be between 2 and 256")
    if not 0 <= args.alpha_threshold <= 255:
        raise ArtifactError("alpha-threshold must be between 0 and 255")
    background = normalize_color(args.background)
    with Image.open(args.image) as opened:
        fitted = fit_image(opened, width, height, args.fit)
    if background:
        base = Image.new("RGBA", fitted.size, (*tuple(int(background[i:i + 2], 16) for i in (1, 3, 5)), 255))
        base.alpha_composite(fitted)
        fitted = base

    rgba_pixels = image_pixels(fitted)
    visible = [(r, g, b) for r, g, b, a in rgba_pixels if a > args.alpha_threshold]
    dominant = Counter(visible).most_common(1)[0][0] if visible else (255, 255, 255)
    rgb_pixels = [(r, g, b) if a > args.alpha_threshold else dominant for r, g, b, a in rgba_pixels]
    rgb = Image.new("RGB", fitted.size)
    rgb.putdata(rgb_pixels)
    dither = Image.Dither.NONE if args.dither == "none" else Image.Dither.FLOYDSTEINBERG
    quantized = rgb.quantize(colors=args.colors, method=Image.Quantize.MEDIANCUT, dither=dither).convert("RGB")
    quantized_pixels = image_pixels(quantized)
    grid: list[list[str | None]] = []
    for y in range(height):
        row: list[str | None] = []
        for x in range(width):
            index = y * width + x
            alpha = rgba_pixels[index][3]
            if not background and alpha <= args.alpha_threshold:
                row.append(None)
            else:
                r, g, b = quantized_pixels[index]
                row.append(f"#{r:02X}{g:02X}{b:02X}")
        grid.append(row)
    return canonical_artifact(
        title=args.title or Path(args.image).stem.replace("-", " ").replace("_", " ").title(),
        grid=grid,
        background=background,
        source={"kind": "image", "name": Path(args.image).name, "fit": args.fit, "dither": args.dither, "requested_colors": args.colors},
    )


def validate_artifact(artifact: dict[str, Any]) -> None:
    required = {"schema_version", "title", "width", "height", "palette", "grid", "source"}
    missing = required - set(artifact)
    if missing:
        raise ArtifactError(f"missing canonical fields: {', '.join(sorted(missing))}")
    if artifact["schema_version"] != 1:
        raise ArtifactError("unsupported schema_version")
    width = checked_dimension(artifact["width"], "width")
    height = checked_dimension(artifact["height"], "height")
    if not isinstance(artifact["grid"], list) or len(artifact["grid"]) != height:
        raise ArtifactError("canonical grid height mismatch")
    emitted = set()
    for y, row in enumerate(artifact["grid"]):
        if not isinstance(row, list) or len(row) != width:
            raise ArtifactError(f"canonical grid row {y} width mismatch")
        for cell in row:
            color = normalize_color(cell)
            if color:
                emitted.add(color)
    palette = artifact["palette"]
    if not isinstance(palette, list) or any(normalize_color(color) != color for color in palette):
        raise ArtifactError("canonical palette must contain uppercase #RRGGBB colors")
    if emitted != set(palette):
        raise ArtifactError("canonical palette does not match grid colors")
    if len(palette) != len(set(palette)):
        raise ArtifactError("canonical palette contains duplicate colors")
    if not emitted:
        raise ArtifactError("canonical grid contains no painted pixels")
    if "quality" in artifact and artifact["quality"] != artifact_quality_report(artifact):
        raise ArtifactError("canonical quality report does not match grid")
    if "proofs" in artifact:
        expected_proofs = {"repeat_3x": source_requires_repeat_proof(artifact.get("source", {}))}
        if artifact["proofs"] != expected_proofs:
            raise ArtifactError("canonical proof intents do not match source direction")


def validate_standalone_html(path: Path, placeholders: tuple[str, ...]) -> None:
    html_text = path.read_text(encoding="utf-8")
    if any(placeholder in html_text for placeholder in placeholders):
        raise ArtifactError("HTML contains unresolved placeholders")
    lowered = html_text.lower()
    if "http://" in lowered or "https://" in lowered:
        raise ArtifactError("HTML contains a remote URL")


def read_embedded_json(path: Path, element_id: str) -> Any:
    html_text = path.read_text(encoding="utf-8")
    match = re.search(rf'<script\s+id="{re.escape(element_id)}"[^>]*>(.*?)</script>', html_text, flags=re.DOTALL)
    if not match:
        raise ArtifactError(f"HTML is missing embedded payload: {element_id}")
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ArtifactError(f"HTML contains invalid embedded JSON: {element_id}") from exc


def validate_output(output: Path) -> dict[str, Any]:
    manifest_path = output / "manifest.json"
    if manifest_path.is_file():
        index_path = output / "index.html"
        if not index_path.is_file():
            raise ArtifactError("collection is missing index.html")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("schema_version") != 1 or manifest.get("kind") not in {"collection", "pack"}:
            raise ArtifactError("invalid collection or pack manifest")
        items = manifest.get("items")
        if not isinstance(items, list) or len(items) < 2:
            raise ArtifactError("collection manifest needs at least two items")
        validate_standalone_html(index_path, ("__COLLECTION_JSON__", "__TITLE_TEXT__"))
        embedded = read_embedded_json(index_path, "collection-data")
        if not isinstance(embedded, dict) or embedded.get("kind") != manifest["kind"] or embedded.get("title") != manifest.get("title"):
            raise ArtifactError("collection overview metadata does not match manifest.json")
        embedded_items = embedded.get("items")
        if not isinstance(embedded_items, list) or len(embedded_items) != len(items):
            raise ArtifactError("collection overview item count does not match manifest.json")
        seen: set[str] = set()
        for item, embedded_item in zip(items, embedded_items):
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                raise ArtifactError("invalid collection manifest item")
            relative = Path(item["path"])
            if relative.is_absolute() or len(relative.parts) != 1 or relative.name != item["path"] or item["path"] in {".", ".."}:
                raise ArtifactError(f"invalid collection path: {item['path']}")
            if item["path"] in seen:
                raise ArtifactError(f"duplicate collection path: {item['path']}")
            seen.add(item["path"])
            artifact = validate_output(output / item["path"])
            expected_metadata = {
                "path": item["path"],
                "title": artifact["title"],
                "width": artifact["width"],
                "height": artifact["height"],
                "colors": len(artifact["palette"]),
            }
            if item != expected_metadata:
                raise ArtifactError(f"collection manifest item does not match child: {item['path']}")
            if not isinstance(embedded_item, dict) or embedded_item.get("path") != item["path"] or embedded_item.get("artifact") != artifact:
                raise ArtifactError(f"collection overview item does not match child: {item['path']}")
        return manifest

    expected = [output / "index.html", output / "pixel-art.json", output / "pixel-art.png"]
    missing = [path.name for path in expected if not path.is_file()]
    if missing:
        raise ArtifactError(f"missing output files: {', '.join(missing)}")
    artifact = json.loads((output / "pixel-art.json").read_text(encoding="utf-8"))
    validate_artifact(artifact)
    validate_standalone_html(output / "index.html", ("__ARTIFACT_JSON__", "__TITLE_TEXT__"))
    if read_embedded_json(output / "index.html", "pixel-art-data") != artifact:
        raise ArtifactError("HTML embedded artifact does not match pixel-art.json")
    validate_png_parity(artifact, output / "pixel-art.png")
    return artifact


def result_summary(result: dict[str, Any], output: Path) -> dict[str, Any]:
    summary: dict[str, Any] = {"status": "ok", "output": str(output.resolve())}
    if result.get("kind") in {"collection", "pack"}:
        summary["count"] = len(result["items"])
        summary["sizes"] = [f"{item['width']}x{item['height']}" for item in result["items"]]
        summary["kind"] = result["kind"]
    else:
        summary.update(width=result["width"], height=result["height"], colors=len(result["palette"]))
    return summary


def slugify(value: str) -> str:
    normalized = "".join(character for character in unicodedata.normalize("NFKD", value.casefold()) if not unicodedata.combining(character))
    slug = re.sub(r"[_\W]+", "-", normalized, flags=re.UNICODE).strip("-")[:64].rstrip("-") or "pixel-art"
    return f"pixel-{slug}" if slug.upper() in WINDOWS_RESERVED_NAMES else slug


def resolve_output(args: argparse.Namespace, title: str, now: datetime | None = None) -> tuple[Path, Path | None]:
    if args.output:
        return args.output, None
    moment = now or datetime.now(timezone.utc)
    library = (args.project_root or Path.cwd()) / "pixel-art"
    month = library / f"{moment.year:04d}" / f"{moment.month:02d}"
    month.mkdir(parents=True, exist_ok=True)
    used = []
    for child in month.iterdir():
        match = re.match(r"^(\d{3})-", child.name) if child.is_dir() else None
        if match:
            used.append(int(match.group(1)))
    sequence = max(used, default=0) + 1
    return month / f"{sequence:03d}-{slugify(args.slug or title)}", library


def iteration_metadata(result: dict[str, Any], output: Path, library: Path, created_at: datetime | None = None) -> dict[str, Any]:
    moment = created_at or datetime.now(timezone.utc)
    relative = output.relative_to(library).as_posix()
    if result.get("kind") in {"collection", "pack"}:
        sizes = [f"{item['width']}x{item['height']}" for item in result["items"]]
        preferred = next((item for item in result["items"] if item["width"] == 32 and item["height"] == 32), result["items"][0])
        thumbnail = f"{relative}/{preferred['path']}/pixel-art.png"
        source_kind = result["kind"]
    else:
        sizes = [f"{result['width']}x{result['height']}"]
        thumbnail = f"{relative}/pixel-art.png"
        source_kind = result.get("source", {}).get("kind", "unknown")
    return {
        "schema_version": 1,
        "id": relative,
        "title": result["title"],
        "kind": result.get("kind", "single"),
        "created_at": moment.isoformat().replace("+00:00", "Z"),
        "path": relative,
        "entry": f"{relative}/index.html",
        "thumbnail": thumbnail,
        "sizes": sizes,
        "source_kind": source_kind,
    }


def discover_iterations(library: Path) -> list[dict[str, Any]]:
    items = []
    for metadata_path in library.glob("[0-9][0-9][0-9][0-9]/[0-9][0-9]/*/iteration.json"):
        try:
            item = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(item, dict) and item.get("schema_version") == 1 and item.get("entry"):
            items.append(item)
    return sorted(items, key=lambda item: (str(item.get("created_at", "")), str(item.get("id", ""))), reverse=True)


def rebuild_project_hub(library: Path) -> dict[str, Any]:
    library.mkdir(parents=True, exist_ok=True)
    items = discover_iterations(library)
    catalog = {"schema_version": 1, "kind": "pixel-art-library", "count": len(items), "items": items}
    (library / "catalog.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    template = PROJECT_HUB_TEMPLATE_PATH.read_text(encoding="utf-8")
    payload = json.dumps(catalog, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("&", "\\u0026")
    rendered = template.replace("__HUB_JSON__", payload)
    if "__HUB_JSON__" in rendered:
        raise ArtifactError("hub template placeholder replacement failed")
    (library / "index.html").write_text(rendered, encoding="utf-8", newline="\n")
    validate_standalone_html(library / "index.html", ("__HUB_JSON__",))
    return catalog


def finish_managed(result: dict[str, Any], output: Path, library: Path | None) -> dict[str, Any]:
    summary = result_summary(result, output)
    if library is None:
        return summary
    metadata = iteration_metadata(result, output, library)
    (output / "iteration.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    catalog = rebuild_project_hub(library)
    summary.update(managed=True, iteration=metadata["id"], hub=str((library / "index.html").resolve()), library_count=catalog["count"])
    return summary


def add_output_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--output", type=Path, help="Write directly here and skip project-library indexing.")
    parser.add_argument("--project-root", type=Path, help="Project that owns the pixel-art library; defaults to the current directory.")
    parser.add_argument("--slug", help="Folder slug for a managed iteration.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build exact-grid pixel-art HTML artifacts without model API calls.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    spec_parser = subparsers.add_parser("from-spec", help="Compile a compact JSON scene spec.")
    spec_parser.add_argument("spec", type=Path)
    add_output_options(spec_parser)
    spec_parser.add_argument("--scale", type=int, default=16)

    collection_parser = subparsers.add_parser("collection", help="Compile several exact specs into one resolution set.")
    collection_parser.add_argument("specs", nargs="+", type=Path)
    add_output_options(collection_parser)
    collection_parser.add_argument("--title", default="Pixel art resolution set")
    collection_parser.add_argument("--scale", type=int, default=16)

    pack_parser = subparsers.add_parser("pack", help="Compile several same-size or mixed-size specs into one named asset set.")
    pack_parser.add_argument("specs", nargs="+", type=Path)
    add_output_options(pack_parser)
    pack_parser.add_argument("--title", default="Pixel art asset pack")
    pack_parser.add_argument("--scale", type=int, default=16)

    image_parser = subparsers.add_parser("from-image", help="Convert a local image with Pillow.")
    image_parser.add_argument("image", type=Path)
    add_output_options(image_parser)
    image_parser.add_argument("--size", type=int, default=32)
    image_parser.add_argument("--sizes", help="Comma-separated square sizes or 'all' for 16,24,32,40,48,64.")
    image_parser.add_argument("--width", type=int)
    image_parser.add_argument("--height", type=int)
    image_parser.add_argument("--colors", type=int, default=16)
    image_parser.add_argument("--fit", choices=("contain", "cover", "stretch"), default="contain")
    image_parser.add_argument("--dither", choices=("none", "floyd"), default="none")
    image_parser.add_argument("--background", default="transparent")
    image_parser.add_argument("--alpha-threshold", type=int, default=10)
    image_parser.add_argument("--title")
    image_parser.add_argument("--scale", type=int, default=16)

    validate_parser = subparsers.add_parser("validate", help="Validate a generated output directory.")
    validate_parser.add_argument("output", type=Path)

    critique_parser = subparsers.add_parser("critique", help="Validate an output and report craft-risk signals without assigning a quality score.")
    critique_parser.add_argument("output", type=Path)

    hub_parser = subparsers.add_parser("hub", help="Rebuild a project's pixel-art library hub from iteration metadata.")
    hub_parser.add_argument("--project-root", type=Path, default=Path.cwd())
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "from-spec":
            spec = json.loads(args.spec.read_text(encoding="utf-8"))
            if not isinstance(spec, dict):
                raise ArtifactError("spec root must be an object")
            artifact = compile_spec(spec)
            output, library = resolve_output(args, artifact["title"])
            write_artifact(artifact, output, args.scale)
            result = validate_output(output)
            print(json.dumps(finish_managed(result, output, library), ensure_ascii=False))
        elif args.command == "collection":
            artifacts: list[dict[str, Any]] = []
            for spec_path in args.specs:
                spec = json.loads(spec_path.read_text(encoding="utf-8"))
                if not isinstance(spec, dict):
                    raise ArtifactError(f"spec root must be an object: {spec_path}")
                artifacts.append(compile_spec(spec))
            output, library = resolve_output(args, args.title)
            write_collection(artifacts, output, args.scale, args.title)
            result = validate_output(output)
            print(json.dumps(finish_managed(result, output, library), ensure_ascii=False))
        elif args.command == "pack":
            artifacts = []
            for spec_path in args.specs:
                spec = json.loads(spec_path.read_text(encoding="utf-8"))
                if not isinstance(spec, dict):
                    raise ArtifactError(f"spec root must be an object: {spec_path}")
                artifacts.append(compile_spec(spec))
            output, library = resolve_output(args, args.title)
            write_collection(artifacts, output, args.scale, args.title, kind="pack")
            result = validate_output(output)
            print(json.dumps(finish_managed(result, output, library), ensure_ascii=False))
        elif args.command == "from-image":
            if not args.image.is_file():
                raise ArtifactError(f"image not found: {args.image}")
            if args.sizes:
                if args.width or args.height:
                    raise ArtifactError("--sizes cannot be combined with --width or --height")
                artifacts = []
                base_title = args.title or args.image.stem.replace("-", " ").replace("_", " ").title()
                for size in parse_sizes(args.sizes):
                    variant_args = argparse.Namespace(**vars(args))
                    variant_args.size = size
                    variant_args.title = f"{base_title} — {size}x{size}"
                    artifacts.append(artifact_from_image(variant_args))
                title = args.title or f"{base_title} — resolution set"
                output, library = resolve_output(args, title)
                write_collection(artifacts, output, args.scale, title)
            else:
                artifact = artifact_from_image(args)
                output, library = resolve_output(args, artifact["title"])
                write_artifact(artifact, output, args.scale)
            result = validate_output(output)
            print(json.dumps(finish_managed(result, output, library), ensure_ascii=False))
        elif args.command == "hub":
            library = args.project_root / "pixel-art"
            catalog = rebuild_project_hub(library)
            print(json.dumps({"status": "ok", "hub": str((library / "index.html").resolve()), "count": catalog["count"]}, ensure_ascii=False))
        elif args.command == "critique":
            print(json.dumps(critique_output(args.output), ensure_ascii=False))
        else:
            result = validate_output(args.output)
            print(json.dumps(result_summary(result, args.output), ensure_ascii=False))
        return 0
    except (ArtifactError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
