from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("build_pixel_art.py")
SPEC = importlib.util.spec_from_file_location("build_pixel_art", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class PixelArtBuilderTests(unittest.TestCase):
    def test_compile_spec_and_write_standalone_artifact(self) -> None:
        spec = {
            "title": "Test beacon",
            "width": 8,
            "height": 8,
            "palette": {"ink": "#123", "light": "#ffd166"},
            "rects": [{"x": 3, "y": 1, "width": 2, "height": 6, "color": "ink"}],
            "runs": [{"x": 2, "y": 7, "length": 4, "color": "ink"}],
            "pixels": [{"x": 3, "y": 2, "color": "light"}],
        }
        artifact = module.compile_spec(spec)
        self.assertEqual((artifact["width"], artifact["height"]), (8, 8))
        self.assertEqual(artifact["grid"][2][3], "#FFD166")
        self.assertEqual(set(artifact["palette"]), {"#112233", "#FFD166"})
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            module.write_artifact(artifact, output, 4)
            verified = module.validate_output(output)
            self.assertEqual(verified["title"], "Test beacon")
            self.assertNotIn("https://", (output / "index.html").read_text(encoding="utf-8"))
            self.assertEqual((output / "pixel-art.png").read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_rejects_out_of_bounds_operations(self) -> None:
        with self.assertRaisesRegex(module.ArtifactError, "out of bounds"):
            module.compile_spec({"width": 8, "height": 8, "pixels": [{"x": 8, "y": 0, "color": "#fff"}]})

    def test_rejects_palette_drift(self) -> None:
        artifact = module.compile_spec({"width": 8, "height": 8, "pixels": [{"x": 0, "y": 0, "color": "#fff"}]})
        artifact["palette"] = []
        with self.assertRaisesRegex(module.ArtifactError, "palette does not match"):
            module.validate_artifact(artifact)

    def test_rejects_empty_art(self) -> None:
        artifact = module.compile_spec({"width": 8, "height": 8})
        with self.assertRaisesRegex(module.ArtifactError, "no painted pixels"):
            module.validate_artifact(artifact)

    def test_parse_recommended_size_set(self) -> None:
        self.assertEqual(module.parse_sizes("all"), [16, 24, 32, 40, 48, 64])
        self.assertEqual(module.parse_sizes("16, 32,64"), [16, 32, 64])
        with self.assertRaisesRegex(module.ArtifactError, "duplicates"):
            module.parse_sizes("16,16")

    def test_write_and_validate_collection(self) -> None:
        first = module.compile_spec({"title": "Small", "width": 8, "height": 8, "background": "#123"})
        second = module.compile_spec({"title": "Large", "width": 12, "height": 12, "background": "#456"})
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            module.write_collection([first, second], output, 4, "Resolution set")
            manifest = module.validate_output(output)
            self.assertEqual(manifest["kind"], "collection")
            self.assertEqual([item["path"] for item in manifest["items"]], ["8x8", "12x12"])
            self.assertTrue((output / "8x8" / "pixel-art.png").is_file())
            self.assertNotIn("https://", (output / "index.html").read_text(encoding="utf-8"))

    def test_image_route_when_pillow_is_available(self) -> None:
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.png"
            image = Image.new("RGBA", (16, 8), (0, 0, 0, 0))
            for y in range(2, 6):
                for x in range(4, 12):
                    image.putpixel((x, y), (240, 70, 50, 255))
            image.save(source)
            args = type("Args", (), {"image": source, "width": None, "height": None, "size": 8, "colors": 4, "alpha_threshold": 10, "background": "transparent", "fit": "contain", "dither": "none", "title": "Image fixture"})()
            artifact = module.artifact_from_image(args)
            self.assertEqual((artifact["width"], artifact["height"]), (8, 8))
            self.assertTrue(any(cell for row in artifact["grid"] for cell in row))
            self.assertTrue(any(cell is None for row in artifact["grid"] for cell in row))

    def test_managed_iterations_are_numbered_and_hubbed(self) -> None:
        artifact = module.compile_spec({"title": "Night Beacon", "width": 8, "height": 8, "background": "#123"})
        moment = datetime(2026, 7, 11, 12, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            args = type("Args", (), {"output": None, "project_root": root, "slug": None})()
            first, library = module.resolve_output(args, artifact["title"], moment)
            self.assertEqual(first.relative_to(root).as_posix(), "pixel-art/2026/07/001-night-beacon")
            module.write_artifact(artifact, first, 4)
            result = module.validate_output(first)
            metadata = module.iteration_metadata(result, first, library, moment)
            (first / "iteration.json").write_text(json.dumps(metadata), encoding="utf-8")
            second, _ = module.resolve_output(args, artifact["title"], moment)
            self.assertEqual(second.name, "002-night-beacon")
            catalog = module.rebuild_project_hub(library)
            self.assertEqual(catalog["count"], 1)
            self.assertEqual(catalog["items"][0]["entry"], "2026/07/001-night-beacon/index.html")
            hub = (library / "index.html").read_text(encoding="utf-8")
            self.assertNotIn("__HUB_JSON__", hub)
            self.assertNotIn("https://", hub)

    def test_collection_metadata_prefers_32_thumbnail(self) -> None:
        artifacts = [module.compile_spec({"title": str(size), "width": size, "height": size, "background": "#123"}) for size in (16, 32, 64)]
        with tempfile.TemporaryDirectory() as temp:
            library = Path(temp) / "pixel-art"
            output = library / "2026" / "07" / "001-set"
            result = module.write_collection(artifacts, output, 2, "Scale set")
            metadata = module.iteration_metadata(result, output, library)
            self.assertEqual(metadata["thumbnail"], "2026/07/001-set/32x32/pixel-art.png")
            self.assertEqual(metadata["sizes"], ["16x16", "32x32", "64x64"])


if __name__ == "__main__":
    unittest.main()
