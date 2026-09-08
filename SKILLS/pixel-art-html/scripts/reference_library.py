#!/usr/bin/env python3
"""Index local references, retrieve evidence, and make explicitly sampled study boards."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unicodedata
from urllib.parse import unquote

TECHNIQUES = Path(__file__).resolve().parents[1] / "references" / "techniques.json"
IMAGE_TYPES = {".png", ".gif", ".jpg", ".jpeg", ".webp", ".bmp"}
TEXT_TYPES = {".md", ".txt", ".html", ".json", ".csv", ".ps1", ".log"}
VIDEO_TYPES = {".mp4", ".webm", ".mov", ".mkv"}


def terms(value: str) -> set[str]:
    normalized = unicodedata.normalize("NFKD", value.lower())
    return set(re.findall(r"[a-z0-9]+", "".join(c for c in normalized if not unicodedata.combining(c))))


class GalleryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images: dict[str, str] = {}
        self.image = ""
        self.caption = False
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "img":
            self.image = attrs.get("src", "")
        if tag == "figcaption":
            self.caption = True

    def handle_endtag(self, tag):
        if tag == "figcaption":
            self.caption = False

    def handle_data(self, data):
        self.parts.append(data)
        if self.caption and self.image:
            self.images[self.image] = self.images.get(self.image, "") + data


def probe_video(path: Path) -> dict:
    if not shutil.which("ffprobe"):
        return {"video_probe": "unavailable: ffprobe is not installed"}
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,nb_frames:format=duration", "-of", "json", str(path)],
        check=True, capture_output=True, timeout=30,
    )
    value = json.loads(result.stdout)
    stream = value.get("streams", [{}])[0]
    return {"width": stream.get("width"), "height": stream.get("height"),
            "frames": stream.get("nb_frames"), "duration_seconds": float(value["format"]["duration"]),
            "video_probe": "metadata-only"}


def source_roots(values: list[str]) -> dict[str, Path]:
    roots = {}
    for value in values:
        alias, separator, raw_path = value.partition("=")
        if not separator or not re.fullmatch(r"[a-z][a-z0-9_-]*", alias) or alias in roots:
            raise ValueError("Each root must be a unique alias=directory, with a lowercase alias")
        path = Path(raw_path).resolve(strict=True)
        if not path.is_dir():
            raise ValueError(f"Source is not a directory: {path}")
        roots[alias] = path
    return roots


def index_library(roots: dict[str, Path], probe: bool = False, workers: int = 4) -> dict:
    from PIL import Image

    tasks = []
    captions = {}
    for alias, root in roots.items():
        for path in sorted(root.rglob("*")):
            if path.is_symlink() or not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if any(part in {".git", "node_modules", "__pycache__"} for part in Path(relative).parts):
                continue
            tasks.append((alias, path, relative))
            if path.name == "article.html":
                parser = GalleryParser()
                parser.feed(path.read_text(encoding="utf-8-sig"))
                for source, caption in parser.images.items():
                    captions[(alias, (path.parent / source).resolve())] = unquote(caption)

    def inspect(task):
        alias, path, relative = task
        ext = path.suffix.lower()
        kind = "image" if ext in IMAGE_TYPES else "video" if ext in VIDEO_TYPES else "text" if ext in TEXT_TYPES else "other"
        entry = {"id": hashlib.sha256(f"{alias}/{relative}".encode()).hexdigest()[:16],
                 "root": alias, "path": relative, "kind": kind, "extension": ext,
                 "caption": captions.get((alias, path.resolve()), ""), "inspection": "not-viewed"}
        match = re.match(r"(\d{2})-[^/]+/", relative)
        if match:
            entry["chapter"] = int(match[1])
        try:
            entry["bytes"] = path.stat().st_size
            with path.open("rb") as stream:
                entry["sha256"] = hashlib.file_digest(stream, "sha256").hexdigest()
            if kind == "text":
                entry["text"] = path.read_text(encoding="utf-8-sig", errors="replace")
                entry["inspection"] = "text-indexed"
            elif kind == "image":
                with Image.open(path) as im:
                    entry.update(width=im.width, height=im.height, frames=getattr(im, "n_frames", 1))
                    im.seek(0)
                    im.load()
                entry["inspection"] = "header-and-first-frame-decoded"
            elif kind == "video":
                entry.update(probe_video(path) if probe else {"video_probe": "not-requested"})
        except (OSError, ValueError, subprocess.SubprocessError, KeyError, IndexError) as exc:
            entry["error"] = str(exc)
        return entry

    with ThreadPoolExecutor(max_workers=workers) as pool:
        entries = list(pool.map(inspect, tasks))
    hashes = {}
    for entry in entries:
        digest = entry.get("sha256")
        if digest in hashes:
            entry["duplicate_of"] = hashes[digest]
        elif digest:
            hashes[digest] = entry["id"]
    return {"schema_version": 1, "roots": {alias: str(path) for alias, path in roots.items()},
            "coverage": {"files": len(entries), "by_root": dict(Counter(e["root"] for e in entries)),
                         "by_kind": dict(Counter(e["kind"] for e in entries)),
                         "exact_duplicates": sum("duplicate_of" in e for e in entries),
                         "errors": sum("error" in e for e in entries),
                         "visual_review": "none; indexing is not a visual review",
                         "excluded": ["symlinks", ".git", "node_modules", "__pycache__"]},
            "entries": entries}


def search_entries(index: dict, query: str, limit: int = 12, root: str | None = None,
                   kind: str | None = None, duplicates: bool = False) -> list[dict]:
    wanted = terms(query)
    matches = []
    for entry in index["entries"]:
        if root and entry["root"] != root or kind and entry["kind"] != kind:
            continue
        title_terms = terms(entry["path"] + " " + entry.get("caption", ""))
        text_terms = terms(entry.get("text", ""))
        score = len(wanted & title_terms) * 8 + len(wanted & text_terms)
        if wanted and not score:
            continue
        if "thumb" in title_terms:
            score -= 1
        matches.append((score, entry))
    matches.sort(key=lambda item: (-item[0], item[1]["root"], item[1]["path"]))
    results = []
    seen = set()
    for score, entry in matches:
        digest = entry.get("sha256", entry["id"])
        if not duplicates and digest in seen:
            continue
        seen.add(digest)
        results.append({**entry, "retrieval_score": score})
        if len(results) == limit:
            break
    return results


def local_path(index: dict, entry: dict) -> Path:
    root = Path(index["roots"][entry["root"]]).resolve(strict=True)
    path = (root / entry["path"]).resolve(strict=True)
    if not path.is_relative_to(root):
        raise ValueError("Reference path leaves its source root")
    return path


def sample_image(path: Path, kind: str, fraction: float = 0.0):
    from PIL import Image
    if kind == "video":
        if not shutil.which("ffmpeg"):
            raise ValueError("Video sampling needs local ffmpeg and ffprobe")
        info = probe_video(path)
        if "duration_seconds" not in info:
            raise ValueError(info["video_probe"])
        timestamp = max(0.0, info["duration_seconds"] * fraction)
        result = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", str(timestamp), "-i", str(path),
             "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
            check=True, capture_output=True, timeout=30,
        )
        with Image.open(io.BytesIO(result.stdout)) as im:
            return im.convert("RGBA"), {"seconds": round(timestamp, 4), "sampling": "single-frame"}
    with Image.open(path) as im:
        count = getattr(im, "n_frames", 1)
        frame = min(count - 1, int(count * fraction))
        im.seek(frame)
        return im.convert("RGBA"), {"frame": frame, "total_frames": count, "sampling": "single-frame"}


def make_board(index: dict, entries: list[dict], output: Path, fractions=(0.0,), columns=6) -> dict:
    from PIL import Image, ImageDraw
    if any(output.resolve().is_relative_to(Path(root).resolve()) for root in index["roots"].values()):
        raise ValueError("Store study boards outside every source root")
    if not entries:
        raise ValueError("No media matched the board request")
    if not 1 <= columns <= 12:
        raise ValueError("columns must be between 1 and 12")
    records = []
    cells = []
    for entry in entries:
        source_error = None
        try:
            path = local_path(index, entry)
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            if digest != entry["sha256"]:
                raise ValueError("Source changed after indexing; rebuild the index")
        except (OSError, ValueError) as exc:
            source_error = str(exc)
        for fraction in fractions:
            tile = Image.new("RGB", (240, 200), "#20252d")
            draw = ImageDraw.Draw(tile)
            record = {"id": entry["id"], "path": entry["path"], "root": entry["root"],
                      "source_sha256": entry["sha256"], "fraction": fraction}
            try:
                if source_error:
                    raise ValueError(source_error)
                picture, sample = sample_image(path, entry["kind"], fraction)
                record.update(sample)
                # Overview only. Explicit nearest resizing; inspect the original to judge clusters.
                ratio = min(224 / picture.width, 152 / picture.height)
                size = (max(1, int(picture.width * ratio)), max(1, int(picture.height * ratio)))
                picture = picture.resize(size, Image.Resampling.NEAREST)
                tile.paste(picture, ((240 - size[0]) // 2, (156 - size[1]) // 2), picture)
            except (OSError, ValueError, subprocess.SubprocessError) as exc:
                record["error"] = str(exc)
                draw.text((8, 50), "SAMPLE UNAVAILABLE", fill="#ffbb88")
            draw.text((8, 157), f"{len(cells):03} {entry['id']} {fraction:g}", fill="#e8edf4")
            label = entry.get("caption") or entry["path"]
            label = label.rsplit("/", 1)[-1]
            draw.text((8, 173), label[:35], fill="#bfc9d6")
            draw.text((8, 186), label[35:70], fill="#bfc9d6")
            records.append(record)
            cells.append(tile)
    rows = (len(cells) + columns - 1) // columns
    board = Image.new("RGB", (240 * columns, rows * 200), "#12161d")
    for number, tile in enumerate(cells):
        board.paste(tile, (number % columns * 240, number // columns * 200))
    output.parent.mkdir(parents=True, exist_ok=True)
    board.save(output)
    record = {"purpose": "Reference overview; resized samples cannot prove native pixel quality or full motion",
              "samples": records, "errors": sum("error" in r for r in records)}
    output.with_suffix(".json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    index_cmd = commands.add_parser("index", help="Read all local files; write a private, reusable search index")
    index_cmd.add_argument("--root", action="append", required=True, help="alias=directory; repeat for each collection")
    index_cmd.add_argument("--output", type=Path, required=True)
    index_cmd.add_argument("--probe-video", action="store_true")
    index_cmd.add_argument("--workers", type=int, choices=range(1, 9), default=4)
    search_cmd = commands.add_parser("search", help="Search paths, gallery captions, and complete local text")
    board_cmd = commands.add_parser("board", help="Create a sampled reference sheet with source IDs")
    for cmd in (search_cmd, board_cmd):
        cmd.add_argument("index", type=Path)
        cmd.add_argument("query", nargs="?", default="")
        cmd.add_argument("--root")
        cmd.add_argument("--kind", choices=("image", "video", "text", "other"))
        cmd.add_argument("--limit", type=int, default=12)
        cmd.add_argument("--duplicates", action="store_true")
    search_cmd.add_argument("--text", action="store_true", help="Include complete indexed text for the selected documents")
    board_cmd.add_argument("--ids", nargs="+", help="Exact IDs from search; bypass query ranking")
    board_cmd.add_argument("--output", type=Path, required=True)
    board_cmd.add_argument("--fractions", default="0", help="Comma-separated samples in [0,1), e.g. 0,0.33,0.66")
    board_cmd.add_argument("--columns", type=int, default=6)
    lesson_cmd = commands.add_parser("techniques", help="Retrieve bundled construction decisions without local datasets")
    lesson_cmd.add_argument("query")
    lesson_cmd.add_argument("--limit", type=int, default=4)
    args = parser.parse_args()
    try:
        if args.command == "index":
            roots = source_roots(args.root)
            if any(args.output.resolve().is_relative_to(root) for root in roots.values()):
                raise ValueError("Store the index outside every source root")
            result = index_library(roots, args.probe_video, args.workers)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(result["coverage"], indent=2))
            return 1 if result["coverage"]["errors"] else 0
        if args.limit < 1:
            raise ValueError("limit must be positive")
        if args.command == "techniques":
            catalog = json.loads(TECHNIQUES.read_text(encoding="utf-8"))
            wanted = terms(args.query)
            ranked = [(len(wanted & terms(" ".join([item["id"], item["title"], *item["tags"], item["when"]]))), item)
                      for item in catalog["techniques"]]
            ranked.sort(key=lambda value: (-value[0], value[1]["id"]))
            chosen = [item for score, item in ranked if score > 0][:args.limit]
            source_ids = {number for item in chosen for number in item["chapters"]}
            print(json.dumps({"techniques": chosen, "sources": [s for s in catalog["sources"] if s["chapter"] in source_ids]}, ensure_ascii=False, indent=2))
            return 0
        index = json.loads(args.index.read_text(encoding="utf-8"))
        entries = search_entries(index, args.query, args.limit, args.root, args.kind, args.duplicates)
        if args.command == "search":
            print(json.dumps([{k: v for k, v in e.items() if args.text or k != "text"} for e in entries], ensure_ascii=False, indent=2))
        else:
            if args.ids:
                by_id = {e["id"]: e for e in index["entries"]}
                entries = [by_id[key] for key in args.ids]
            entries = [e for e in entries if e["kind"] in {"image", "video"}]
            fractions = tuple(float(value) for value in args.fractions.split(","))
            if not fractions or any(not 0 <= value < 1 for value in fractions):
                raise ValueError("fractions must be in [0,1)")
            result = make_board(index, entries, args.output, fractions, args.columns)
            print(json.dumps({"output": str(args.output), "samples": len(result["samples"]), "errors": result["errors"]}))
            return 1 if result["errors"] else 0
    except (OSError, ValueError, KeyError, ImportError) as exc:
        print(f"Reference library: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
