#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
from collections import defaultdict
from io import BytesIO
import json
import math
from pathlib import Path
import random
from statistics import mean
from types import SimpleNamespace
from typing import Any

import build_pixel_art as builder

DISTORTIONS = ("nearest", "fractional", "soft", "drift", "noise", "jpeg")
METHODS = ("legacy", "two-stage")


def authored_master(size: int) -> Any:
    from PIL import Image

    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    pixels = image.load()
    mask: set[tuple[int, int]] = set()
    for y in range(size):
        ny = (y + 0.5) / size
        for x in range(size):
            nx = (x + 0.5) / size
            if 0.18 <= ny < 0.34 and abs(nx - 0.5) <= 0.12:
                mask.add((x, y))
            elif 0.31 <= ny <= 0.86:
                half_width = 0.16 + 0.16 * math.sin(min(1.0, (ny - 0.31) / 0.55) * math.pi * 0.82)
                if abs(nx - 0.5) <= half_width:
                    mask.add((x, y))
    for x, y in mask:
        edge = any((x + dx, y + dy) not in mask for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)))
        if y < round(size * 0.31):
            color = (210, 132, 58, 255)
        elif edge:
            color = (24, 28, 38, 255)
        else:
            color = (190, 36, 54, 255)
        pixels[x, y] = color
    accent_x = max(0, min(size - 1, round(size * 0.43)))
    accent_y = max(0, min(size - 1, round(size * 0.47)))
    if (accent_x, accent_y) in mask:
        pixels[accent_x, accent_y] = (255, 218, 120, 255)
    return image


def distort(image: Any, kind: str, seed: int) -> Any:
    from PIL import Image, ImageFilter

    if kind == "nearest":
        return image.resize((image.width * 6, image.height * 6), Image.Resampling.NEAREST)
    if kind == "fractional":
        side = max(16, round(image.width * 5.5))
        return image.resize((side, side), Image.Resampling.BICUBIC)
    if kind == "soft":
        enlarged = image.resize((image.width * 6, image.height * 6), Image.Resampling.NEAREST)
        return enlarged.filter(ImageFilter.GaussianBlur(radius=0.9))
    if kind == "drift":
        enlarged = image.resize((image.width * 6, image.height * 6), Image.Resampling.NEAREST)
        shear = 0.055
        return enlarged.transform(
            enlarged.size,
            Image.Transform.AFFINE,
            (1, shear, -shear * enlarged.height / 2, 0, 1, 0),
            resample=Image.Resampling.BICUBIC,
        )
    if kind == "jpeg":
        enlarged = image.resize((image.width * 6, image.height * 6), Image.Resampling.NEAREST)
        background = Image.new("RGB", enlarged.size, (8, 10, 14))
        background.paste(enlarged, mask=enlarged.getchannel("A"))
        buffer = BytesIO()
        background.save(buffer, "JPEG", quality=58, subsampling=2)
        buffer.seek(0)
        return Image.open(buffer).convert("RGBA")
    if kind == "noise":
        rng = random.Random(seed)
        enlarged = image.resize((image.width * 6, image.height * 6), Image.Resampling.NEAREST)
        values = builder.image_pixels(enlarged)
        noisy = []
        for r, g, b, a in values:
            delta = rng.randint(-8, 8)
            noisy.append((max(0, min(255, r + delta)), max(0, min(255, g + delta)), max(0, min(255, b + delta)), a))
        enlarged.putdata(noisy)
        return enlarged
    raise ValueError(f"unsupported distortion: {kind}")


def artifact_image(artifact: dict[str, Any]) -> Any:
    from PIL import Image

    image = Image.new("RGBA", (artifact["width"], artifact["height"]), (0, 0, 0, 0))
    pixels = image.load()
    for y, row in enumerate(artifact["grid"]):
        for x, color in enumerate(row):
            if color:
                pixels[x, y] = tuple(int(color[index:index + 2], 16) for index in (1, 3, 5)) + (255,)
    return image


def reconstruction_metrics(expected: Any, actual: Any) -> dict[str, Any]:
    expected_pixels = builder.image_pixels(expected.convert("RGBA"))
    actual_pixels = builder.image_pixels(actual.convert("RGBA"))
    exact = sum(left == right for left, right in zip(expected_pixels, actual_pixels)) / len(expected_pixels)
    expected_mask = {index for index, color in enumerate(expected_pixels) if color[3] > 127}
    actual_mask = {index for index, color in enumerate(actual_pixels) if color[3] > 127}
    union = expected_mask | actual_mask
    intersection = expected_mask & actual_mask
    silhouette_iou = len(intersection) / len(union) if union else 1.0
    rgb_error = mean(
        sum(abs(expected_pixels[index][channel] - actual_pixels[index][channel]) for channel in range(3)) / 3
        for index in intersection
    ) if intersection else 255.0
    return {
        "exact_cell_ratio": round(exact, 4),
        "silhouette_iou": round(silhouette_iou, 4),
        "mean_rgb_error": round(rgb_error, 3),
        "recovery_fidelity": round(0.7 * silhouette_iou + 0.3 * max(0.0, 1.0 - rgb_error / 255), 4),
    }


def data_uri(path: Path, scale_to: int = 160) -> str:
    from PIL import Image

    with Image.open(path) as opened:
        image = opened.convert("RGBA")
    scale = max(1, scale_to // max(image.size))
    image = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
    buffer = BytesIO()
    image.save(buffer, "PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def render_report(report: dict[str, Any], output: Path) -> None:
    rows = []
    for sample in report["samples"]:
        rows.append(
            "<tr>"
            f"<td>{sample['target_size']}x{sample['target_size']}</td>"
            f"<td>{sample['distortion']}</td><td>{sample['method']}</td>"
            f"<td>{sample['metrics']['silhouette_iou']:.4f}</td>"
            f"<td>{sample['metrics']['exact_cell_ratio']:.4f}</td>"
            f"<td>{sample['metrics']['mean_rgb_error']:.3f}</td>"
            f"<td><img alt=\"master {sample['target_size']}px\" src=\"{data_uri(output / sample['master'])}\"></td>"
            f"<td><img alt=\"source {sample['target_size']}px {sample['distortion']}\" src=\"{data_uri(output / sample['source'])}\"></td>"
            f"<td><img alt=\"{sample['method']} {sample['target_size']}px {sample['distortion']}\" src=\"{data_uri(output / sample['recovered'])}\"></td>"
            "</tr>"
        )
    aggregate = "".join(
        f"<article><strong>{method}</strong><span>fidelity {values['recovery_fidelity']:.4f}</span><span>silhouette {values['silhouette_iou']:.4f}</span><span>RGB error {values['mean_rgb_error']:.3f}</span></article>"
        for method, values in report["aggregate"].items()
    )
    html = f"""<!doctype html>
<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><link rel=\"icon\" href=\"data:,\"><title>Small-grid reconstruction benchmark</title>
<style>:root{{color-scheme:dark;font-family:ui-monospace,Cascadia Mono,monospace}}*{{box-sizing:border-box}}body{{margin:0;background:#080b0a;color:#f2efe6}}main{{width:min(1180px,calc(100% - 24px));margin:auto;padding:28px 0 48px}}h1{{font:800 clamp(34px,7vw,72px)/.95 Bahnschrift,sans-serif;max-width:15ch;margin:.2em 0}}p{{color:#aaa69b;max-width:72ch}}.aggregate{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:24px 0}}article{{display:grid;gap:7px;padding:16px;border:1px solid #4d534b;background:#121510}}article strong{{font-size:20px}}table{{width:100%;border-collapse:collapse;background:#10130f}}th,td{{padding:10px;border:1px solid #343a34;text-align:left}}th{{color:#c8a75d}}img{{display:block;width:96px;height:96px;object-fit:contain;image-rendering:pixelated;background:#050605}}.scroll{{overflow:auto}}@media(max-width:600px){{th,td{{padding:7px;font-size:12px}}img{{width:72px;height:72px}}}}</style></head>
<body><main><p>PIXEL PROOF / TECHNICAL FIXTURE</p><h1>Small-grid reconstruction benchmark</h1><p>Known native masters, deterministic degradations, target-aware reconstruction. Fidelity metrics do not score artistic quality.</p><section class=\"aggregate\">{aggregate}</section><div class=\"scroll\"><table><thead><tr><th>Target</th><th>Distortion</th><th>Method</th><th>Silhouette IoU</th><th>Exact cells</th><th>RGB error</th><th>Master</th><th>Source</th><th>Recovered</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></main></body></html>"""
    (output / "index.html").write_text(html, encoding="utf-8", newline="\n")


def run_benchmark(output: Path, sizes: list[int], distortions: list[str]) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=True)
    (output / "masters").mkdir(exist_ok=True)
    (output / "sources").mkdir(exist_ok=True)
    (output / "recovered").mkdir(exist_ok=True)
    samples: list[dict[str, Any]] = []
    aggregate_values: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for size in sizes:
        master = authored_master(size)
        master_path = output / "masters" / f"{size}.png"
        master.save(master_path)
        for distortion_index, distortion_name in enumerate(distortions):
            source = distort(master, distortion_name, seed=size * 100 + distortion_index)
            suffix = ".jpg" if distortion_name == "jpeg" else ".png"
            source_path = output / "sources" / f"{size}-{distortion_name}{suffix}"
            if distortion_name == "jpeg":
                source.convert("RGB").save(source_path, "JPEG", quality=95)
            else:
                source.save(source_path)
            for method in METHODS:
                args = SimpleNamespace(
                    image=source_path, width=None, height=None, size=size, colors=4,
                    alpha_threshold=10, background="transparent", fit="contain",
                    resample="lanczos", source_class="auto", reconstruction=method,
                    structure_colors=8, min_cluster=1, dither="none",
                    title=f"{size}px {distortion_name} {method}", evidence_tier="fixture",
                )
                artifact = builder.artifact_from_image(args)
                recovered = artifact_image(artifact)
                recovered_path = output / "recovered" / f"{size}-{distortion_name}-{method}.png"
                recovered.save(recovered_path)
                metrics = reconstruction_metrics(master, recovered)
                for key, value in metrics.items():
                    aggregate_values[method][key].append(float(value))
                samples.append({
                    "target_size": size,
                    "distortion": distortion_name,
                    "method": method,
                    "source_class": artifact["source"]["analysis"]["class"],
                    "source_confidence": artifact["source"]["analysis"]["confidence"],
                    "palette_count": len(artifact["palette"]),
                    "master": master_path.relative_to(output).as_posix(),
                    "source": source_path.relative_to(output).as_posix(),
                    "recovered": recovered_path.relative_to(output).as_posix(),
                    "metrics": metrics,
                })
    aggregate = {
        method: {metric: round(mean(values), 4) for metric, values in metrics.items()}
        for method, metrics in aggregate_values.items()
    }
    report = {
        "schema_version": 1,
        "kind": "small-grid-reconstruction-benchmark",
        "sizes": sizes,
        "distortions": distortions,
        "methods": list(METHODS),
        "aggregate": aggregate,
        "samples": samples,
    }
    (output / "benchmark.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    render_report(report, output)
    return report


def parse_csv_ints(value: str) -> list[int]:
    sizes = [int(token.strip()) for token in value.split(",") if token.strip()]
    if not sizes or any(size not in {8, 16, 24, 32} for size in sizes) or len(sizes) != len(set(sizes)):
        raise argparse.ArgumentTypeError("sizes must be unique values from 8,16,24,32")
    return sizes


def parse_distortions(value: str) -> list[str]:
    names = [token.strip() for token in value.split(",") if token.strip()]
    unknown = [name for name in names if name not in DISTORTIONS]
    if not names or unknown or len(names) != len(set(names)):
        raise argparse.ArgumentTypeError(f"distortions must be unique values from {','.join(DISTORTIONS)}")
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark target-aware recovery against known 8/16/24/32 masters.")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sizes", type=parse_csv_ints, default=parse_csv_ints("8,16,24,32"))
    parser.add_argument("--distortions", type=parse_distortions, default=parse_distortions(",".join(DISTORTIONS)))
    args = parser.parse_args()
    report = run_benchmark(args.output, args.sizes, args.distortions)
    print(json.dumps({"status": "ok", "output": str(args.output.resolve()), "sizes": report["sizes"], "distortions": report["distortions"], "methods": report["methods"], "aggregate": report["aggregate"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
