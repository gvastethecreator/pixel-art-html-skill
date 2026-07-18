from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
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
        self.assertEqual(artifact["evidence_tier"], "draft")
        self.assertEqual(artifact["grid"][2][3], "#FFD166")
        self.assertEqual(set(artifact["palette"]), {"#112233", "#FFD166"})
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            module.write_artifact(artifact, output, 4)
            verified = module.validate_output(output)
            self.assertEqual(verified["title"], "Test beacon")
            self.assertNotIn("https://", (output / "index.html").read_text(encoding="utf-8"))
            self.assertEqual((output / "pixel-art.png").read_bytes()[:8], b"\x89PNG\r\n\x1a\n")
            self.assertIn("native-scale-proof", (output / "index.html").read_text(encoding="utf-8"))

    def test_evidence_tier_is_explicit_and_rejects_false_labels(self) -> None:
        fixture = module.compile_spec({
            "title": "Timing fixture",
            "width": 8,
            "height": 8,
            "evidence_tier": "fixture",
            "background": "#123",
        })
        self.assertEqual(fixture["evidence_tier"], "fixture")
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            module.write_artifact(fixture, output, 4)
            proof = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn("Fixture / mechanics only", proof)
            self.assertIn("evidence_tier", proof)
        with self.assertRaisesRegex(module.ArtifactError, "evidence_tier must be one of"):
            module.compile_spec({"width": 8, "height": 8, "evidence_tier": "production", "background": "#123"})

    def test_motifs_support_reuse_flips_and_palette_maps(self) -> None:
        artifact = module.compile_spec({
            "width": 8,
            "height": 8,
            "palette": {"a": "#123", "b": "#456", "c": "#abc"},
            "motifs": {"leaf": [". a .", "a a a", ". b ."]},
            "stamps": [
                {"motif": "leaf", "x": 0, "y": 1},
                {"motif": "leaf", "x": 4, "y": 1, "flip_x": True, "map": {"a": "c"}},
            ],
        })
        self.assertEqual(artifact["grid"][1][1], "#112233")
        self.assertEqual(artifact["grid"][3][1], "#445566")
        self.assertEqual(artifact["grid"][1][5], "#AABBCC")
        self.assertEqual(artifact["quality"]["clusters"], 4)

    def test_one_column_motif_accepts_a_semantic_palette_alias(self) -> None:
        artifact = module.compile_spec({
            "width": 8,
            "height": 8,
            "palette": {"grass": "#385A3A"},
            "motifs": {"stem": ["grass", "grass", "."]},
            "stamps": [{"motif": "stem", "x": 2, "y": 1}],
        })
        self.assertEqual(artifact["grid"][1][2], "#385A3A")
        self.assertEqual(artifact["grid"][2][2], "#385A3A")
        self.assertIsNone(artifact["grid"][3][2])

    def test_full_grid_accepts_compact_one_character_alias_rows(self) -> None:
        artifact = module.compile_spec({
            "width": 8,
            "height": 8,
            "palette": {"i": "#112233", "l": "#FFD166"},
            "grid": [
                "........",
                "...ii...",
                "..ill...",
                "..iiii..",
                "..iiii..",
                "...ii...",
                "...ii...",
                "........",
            ],
        })
        self.assertEqual(artifact["grid"][2][2:5], ["#112233", "#FFD166", "#FFD166"])
        self.assertIsNone(artifact["grid"][0][0])

    def test_quality_report_surfaces_orphan_pixel_risk_without_scoring_art(self) -> None:
        artifact = module.compile_spec({
            "width": 8,
            "height": 8,
            "palette": {"ink": "#202020", "near": "#242424"},
            "pixels": [
                {"x": 0, "y": 0, "color": "ink"},
                {"x": 2, "y": 2, "color": "ink"},
                {"x": 4, "y": 4, "color": "near"},
                {"x": 6, "y": 6, "color": "near"},
            ],
        })
        report = artifact["quality"]
        self.assertEqual(report["single_pixel_clusters"], 4)
        self.assertTrue(any("orphan-pixel" in warning for warning in report["warnings"]))
        self.assertTrue(any("value span" in warning for warning in report["warnings"]))
        self.assertNotIn("score", report)

    def test_image_cluster_cleanup_merges_opt_in_singletons_without_eroding_alpha(self) -> None:
        grid = [
            [None, "#111111", "#111111"],
            [None, "#FF0000", "#111111"],
            [None, "#111111", "#111111"],
        ]
        cleaned = module.merge_small_color_clusters(grid, 2)
        self.assertIsNone(cleaned[1][0])
        self.assertEqual(cleaned[1][1], "#111111")
        self.assertEqual(module.merge_small_color_clusters(grid, 1), grid)

    def test_rejects_out_of_bounds_operations(self) -> None:
        with self.assertRaisesRegex(module.ArtifactError, "out of bounds"):
            module.compile_spec({"width": 8, "height": 8, "pixels": [{"x": 8, "y": 0, "color": "#fff"}]})

    def test_rejects_malformed_motifs(self) -> None:
        with self.assertRaisesRegex(module.ArtifactError, "equal width"):
            module.compile_spec({"width": 8, "height": 8, "motifs": {"bad": ["x x", "x"]}})
        with self.assertRaisesRegex(module.ArtifactError, "strings or null"):
            module.compile_spec({"width": 8, "height": 8, "motifs": {"bad": [[{"color": "#fff"}]]}})

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
            critique = module.critique_output(output)
            self.assertEqual([item["path"] for item in critique["items"]], ["8x8", "12x12"])

    def test_write_and_validate_same_size_asset_pack(self) -> None:
        first = module.compile_spec({"title": "Copper key", "width": 8, "height": 8, "background": "#123"})
        second = module.compile_spec({"title": "Moon key", "width": 8, "height": 8, "background": "#456"})
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            module.write_collection([first, second], output, 4, "Key set", kind="pack")
            manifest = module.validate_output(output)
            self.assertEqual(manifest["kind"], "pack")
            self.assertEqual([item["path"] for item in manifest["items"]], ["copper-key", "moon-key"])
            self.assertTrue((output / "copper-key" / "pixel-art.png").is_file())
            self.assertEqual(module.critique_output(output)["kind"], "pack")
            self.assertEqual(module.result_summary(manifest, output)["evidence_tiers"], ["draft", "draft"])

    def test_validation_rejects_png_pixels_that_drift_from_grid(self) -> None:
        artifact = module.compile_spec({"width": 8, "height": 8, "background": "#123"})
        drifted = module.compile_spec({"width": 8, "height": 8, "background": "#456"})
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            module.write_artifact(artifact, output, 4)
            module.write_png(drifted, output / "pixel-art.png", 4)
            with self.assertRaisesRegex(module.ArtifactError, "pixels do not match"):
                module.validate_output(output)

    def test_validation_rejects_a_second_compressed_png_stream(self) -> None:
        artifact = module.compile_spec({"width": 8, "height": 8, "background": "#123"})
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            module.write_artifact(artifact, output, 1)
            png_path = output / "pixel-art.png"
            payload = png_path.read_bytes()
            position = 8
            rebuilt = bytearray(payload[:8])
            while position < len(payload):
                length = module.struct.unpack(">I", payload[position:position + 4])[0]
                kind = payload[position + 4:position + 8]
                chunk = payload[position + 8:position + 8 + length]
                if kind == b"IDAT":
                    chunk += module.zlib.compress(b"unexpected second stream")
                rebuilt.extend(module.png_chunk(kind, chunk))
                position += 12 + length
            png_path.write_bytes(bytes(rebuilt))
            with self.assertRaisesRegex(module.ArtifactError, "extra compressed stream"):
                module.validate_output(output)

    def test_tile_artifacts_include_automatic_repeat_proof(self) -> None:
        artifact = module.compile_spec({
            "title": "Grass tile",
            "width": 8,
            "height": 8,
            "art_direction": {"use": "top-down tile"},
            "background": "#385A3A",
        })
        non_tile = module.compile_spec({"width": 8, "height": 8, "art_direction": {"use": "item"}, "background": "#385A3A"})
        self.assertTrue(artifact["proofs"]["repeat_3x"])
        self.assertFalse(non_tile["proofs"]["repeat_3x"])
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            module.write_artifact(artifact, output, 4)
            embedded = module.read_embedded_json(output / "index.html", "pixel-art-data")
            self.assertTrue(embedded["proofs"]["repeat_3x"])

    def test_validation_rejects_stale_single_and_pack_html(self) -> None:
        first = module.compile_spec({"title": "First", "width": 8, "height": 8, "background": "#123"})
        second = module.compile_spec({"title": "Second", "width": 8, "height": 8, "background": "#456"})
        replacement = module.compile_spec({"title": "Replacement", "width": 8, "height": 8, "background": "#789"})
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            module.write_collection([first, second], output, 4, "Pair", kind="pack")
            module.write_artifact(replacement, output / "first", 4)
            with self.assertRaisesRegex(module.ArtifactError, "manifest item does not match child"):
                module.validate_output(output)
            module.write_artifact(first, output / "first", 4)
            (output / "first" / "pixel-art.json").write_text(json.dumps(replacement), encoding="utf-8")
            with self.assertRaisesRegex(module.ArtifactError, "HTML embedded artifact does not match"):
                module.validate_output(output / "first")

    def test_slugify_preserves_international_title_identity(self) -> None:
        self.assertEqual(module.slugify("Poción mágica"), "pocion-magica")
        self.assertEqual(module.slugify("生命水晶"), "生命水晶")
        self.assertEqual(module.slugify("CON"), "pixel-con")

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
            args = type("Args", (), {"image": source, "width": None, "height": None, "size": 8, "colors": 4, "alpha_threshold": 10, "background": "transparent", "fit": "contain", "resample": "nearest", "min_cluster": 1, "dither": "none", "title": "Image fixture"})()
            artifact = module.artifact_from_image(args)
            self.assertEqual((artifact["width"], artifact["height"]), (8, 8))
            self.assertTrue(any(cell for row in artifact["grid"] for cell in row))
            self.assertTrue(any(cell is None for row in artifact["grid"] for cell in row))
            self.assertEqual(artifact["source"]["resample"], "nearest")

    def test_source_classification_distinguishes_exact_pseudo_and_painterly_inputs(self) -> None:
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")

        native = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
        for y in range(2, 6):
            for x in range(2, 6):
                native.putpixel((x, y), (220, 50, 60, 255))
        exact_scaled = native.resize((40, 40), Image.Resampling.NEAREST)
        exact = module.classify_image_source(exact_scaled, 8, 8)
        self.assertEqual(exact["class"], "exact-grid")
        self.assertEqual(exact["confidence"], "high")
        self.assertEqual(exact["inferred_grid"], {"width": 8, "height": 8, "step_x": 5.0, "step_y": 5.0})

        pseudo = native.resize((61, 61), Image.Resampling.BICUBIC)
        pseudo_result = module.classify_image_source(pseudo, 8, 8)
        self.assertEqual(pseudo_result["class"], "pseudo-pixel")
        self.assertIn(pseudo_result["confidence"], {"medium", "high"})
        self.assertIsNone(pseudo_result["inferred_grid"])

        painterly = Image.new("RGBA", (64, 64), (0, 0, 0, 255))
        for y in range(64):
            for x in range(64):
                painterly.putpixel((x, y), ((x * 3 + y) % 256, (y * 5 + x) % 256, (x * 7 + y * 11) % 256, 255))
        painted_result = module.classify_image_source(painterly, 8, 8)
        self.assertEqual(painted_result["class"], "painterly")
        self.assertIsNone(painted_result["inferred_grid"])

    def test_image_route_records_source_analysis_and_allows_an_explicit_class_override(self) -> None:
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.png"
            image = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
            image.putpixel((3, 3), (255, 80, 40, 255))
            image.save(source)
            values = {
                "image": source, "width": None, "height": None, "size": 8,
                "colors": 4, "alpha_threshold": 10, "background": "transparent",
                "fit": "contain", "resample": "nearest", "min_cluster": 1,
                "dither": "none", "title": "Analysis fixture", "source_class": "auto",
                "reconstruction": "legacy", "evidence_tier": "draft",
            }
            artifact = module.artifact_from_image(type("Args", (), values)())
            self.assertEqual(artifact["source"]["analysis"]["class"], "exact-grid")
            self.assertEqual(artifact["source"]["analysis"]["confidence"], "high")
            self.assertEqual(artifact["source"]["reconstruction"], "legacy")

            values["source_class"] = "painterly"
            overridden = module.artifact_from_image(type("Args", (), values)())
            self.assertEqual(overridden["source"]["analysis"]["class"], "painterly")
            self.assertEqual(overridden["source"]["analysis"]["confidence"], "forced")
            self.assertEqual(overridden["source"]["analysis"]["detector"], "user-override")

    def test_two_stage_reconstruction_preserves_small_grid_structure_alpha_and_palette_budget(self) -> None:
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "degraded.png"
            native = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
            for y in range(2, 6):
                for x in range(2, 6):
                    native.putpixel((x, y), (24, 28, 38, 255) if x in {2, 5} or y in {2, 5} else (205, 45, 55, 255))
            native.putpixel((3, 3), (255, 225, 130, 255))
            native.resize((61, 61), Image.Resampling.BICUBIC).save(source)
            args = type("Args", (), {
                "image": source, "width": None, "height": None, "size": 8,
                "colors": 4, "alpha_threshold": 10, "background": "transparent",
                "fit": "contain", "resample": "lanczos", "min_cluster": 1,
                "dither": "none", "title": "Two stage fixture", "source_class": "auto",
                "reconstruction": "two-stage", "structure_colors": 8,
                "evidence_tier": "draft",
            })()
            artifact = module.artifact_from_image(args)
            self.assertLessEqual(len(artifact["palette"]), 4)
            self.assertIsNone(artifact["grid"][0][0])
            self.assertIsNotNone(artifact["grid"][2][2])
            self.assertIsNotNone(artifact["grid"][3][3])
            self.assertNotEqual(artifact["grid"][3][3], artifact["grid"][4][4])
            self.assertEqual(artifact["source"]["reconstruction"], "two-stage")
            self.assertEqual(artifact["source"]["structure_colors"], 8)
            self.assertTrue(artifact["source"]["manual_repair_required"])

    def test_image_proof_exposes_source_detection_metadata_and_overlay_control(self) -> None:
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.png"
            Image.new("RGBA", (8, 8), (30, 40, 50, 255)).resize((40, 40), Image.Resampling.NEAREST).save(source)
            args = type("Args", (), {
                "image": source, "width": None, "height": None, "size": 8,
                "colors": 4, "alpha_threshold": 10, "background": "transparent",
                "fit": "contain", "resample": "nearest", "min_cluster": 1,
                "dither": "none", "title": "Overlay fixture", "source_class": "auto",
                "reconstruction": "auto", "structure_colors": 0,
                "evidence_tier": "draft",
            })()
            output = root / "proof"
            module.write_artifact(module.artifact_from_image(args), output, 4)
            proof = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn('id="source-grid"', proof)
            self.assertIn("Show recovered source lattice", proof)
            self.assertIn("Source class", proof)
            self.assertIn("Manual repair", proof)
            self.assertIn("Manual silhouette and identity-cue repair required", proof)
            self.assertIn("sourceGridOverlay", proof)
            self.assertIn("sourceGridStride", proof)

    def test_repair_cli_preserves_losing_baseline_and_exposes_blind_before_after_proof(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            baseline_path = root / "baseline.json"
            repair_path = root / "repair.json"
            output = root / "output"
            baseline = module.canonical_artifact(
                title="Automatic draft",
                grid=[["#111111" if (x, y) == (3, 3) else None for x in range(8)] for y in range(8)],
                background=None,
                source={"kind": "image", "manual_repair_required": True},
                evidence_tier="draft",
            )
            baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
            repair_path.write_text(json.dumps({
                "title": "Authored repair",
                "width": 8,
                "height": 8,
                "evidence_tier": "draft",
                "palette": {"l": "#F2E5C4"},
                "grid": [
                    "........", "........", "........", "...ll...",
                    "........", "........", "........", "........",
                ],
                "art_direction": {"use": "pickup icon", "focus": "two-cell light cluster"},
                "repair_decisions": {
                    "silhouette": "replace isolated source fragment with one connected cue",
                    "identity_cue": "two-cell light cluster",
                    "subtraction": "remove all source noise",
                },
            }), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(MODULE_PATH), "repair", str(baseline_path), str(repair_path), "--output", str(output), "--scale", "4"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            artifact = json.loads((output / "pixel-art.json").read_text(encoding="utf-8"))
            self.assertEqual(artifact["source"]["kind"], "manual-repair")
            self.assertEqual(artifact["source"]["baseline"]["title"], "Automatic draft")
            self.assertEqual(artifact["source"]["baseline_grid"], baseline["grid"])
            self.assertEqual(artifact["source"]["repair_decisions"]["identity_cue"], "two-cell light cluster")
            self.assertEqual(artifact["source"]["repair_evidence"], {
                "changed_cells": 2,
                "baseline_subject_cells": 1,
                "repaired_subject_cells": 2,
            })
            proof = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn('id="repair-comparison"', proof)
            self.assertIn('id="blind-review"', proof)
            self.assertIn('id="repair-baseline-label"', proof)
            self.assertIn('id="repair-current-label"', proof)
            self.assertIn("blind ? 'Sample A' : 'Baseline'", proof)
            self.assertIn("blind ? 'Sample B' : 'Authored repair'", proof)
            self.assertIn("Authored repair", proof)
            self.assertIn("repairChangedCells", proof)
            self.assertNotIn("https://", proof)

    def test_repair_rejects_a_noop_that_cannot_prove_authored_change(self) -> None:
        baseline = module.canonical_artifact(
            title="Unchanged draft",
            grid=[["#111111" if (x, y) == (3, 3) else None for x in range(8)] for y in range(8)],
            background=None,
            source={"kind": "image", "manual_repair_required": True},
            evidence_tier="draft",
        )
        repair_spec = {
            "title": "False repair",
            "width": 8,
            "height": 8,
            "palette": {"i": "#111111"},
            "grid": [
                "........", "........", "........", "...i....",
                "........", "........", "........", "........",
            ],
            "repair_decisions": {
                "silhouette": "claim a silhouette repair",
                "identity_cue": "claim an identity cue",
                "subtraction": "claim removed noise",
            },
        }
        with self.assertRaisesRegex(module.ArtifactError, "repair must change at least one cell"):
            module.compile_repair(baseline, repair_spec)

    def test_repair_canonical_validation_rejects_a_malformed_comparison_grid(self) -> None:
        baseline = module.canonical_artifact(
            title="Baseline",
            grid=[["#111111" if (x, y) == (3, 3) else None for x in range(8)] for y in range(8)],
            background=None,
            source={"kind": "image", "manual_repair_required": True},
            evidence_tier="draft",
        )
        repaired = module.compile_repair(baseline, {
            "title": "Repair",
            "palette": {"l": "#EEEEEE"},
            "grid": [
                "........", "........", "........", "...ll...",
                "........", "........", "........", "........",
            ],
            "repair_decisions": {
                "silhouette": "connect the cue",
                "identity_cue": "two light cells",
                "subtraction": "remove the orphan",
            },
        })
        repaired["source"]["baseline_grid"] = [[None]]
        with self.assertRaisesRegex(module.ArtifactError, "repair baseline grid must match artifact dimensions"):
            module.validate_artifact(repaired)

    def test_small_grid_benchmark_cli_writes_machine_and_browser_reports(self) -> None:
        try:
            import PIL  # noqa: F401
        except ImportError:
            self.skipTest("Pillow not installed")
        benchmark_script = MODULE_PATH.with_name("benchmark_small_grids.py")
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "benchmark"
            completed = subprocess.run(
                [sys.executable, str(benchmark_script), "--output", str(output), "--sizes", "8", "--distortions", "nearest,fractional"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout.strip())
            self.assertEqual(summary["sizes"], [8])
            self.assertEqual(summary["distortions"], ["nearest", "fractional"])
            self.assertEqual(summary["methods"], ["legacy", "two-stage"])
            report = json.loads((output / "benchmark.json").read_text(encoding="utf-8"))
            self.assertEqual(len(report["samples"]), 4)
            self.assertEqual({sample["target_size"] for sample in report["samples"]}, {8})
            html = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn("Small-grid reconstruction benchmark", html)
            self.assertIn("data:image/png;base64,", html)
            self.assertNotIn("https://", html)

    def test_optional_pixel_fixer_adapter_records_external_detection_without_path_leak(self) -> None:
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.png"
            Image.new("RGBA", (8, 8), (40, 50, 60, 255)).resize((40, 40), Image.Resampling.NEAREST).save(source)
            fake = root / "fake_fixer.py"
            fake.write_text(
                "import json\nprint(json.dumps({'cols': 8, 'rows': 8, 'step_x': 5.0, 'step_y': 5.0, 'consensus': 'fast:ac+rl(S)'}))\n",
                encoding="utf-8",
            )
            args = type("Args", (), {
                "image": source, "width": None, "height": None, "size": 8,
                "colors": 4, "alpha_threshold": 10, "background": "transparent",
                "fit": "contain", "resample": "nearest", "min_cluster": 1,
                "dither": "none", "title": "External detector fixture", "source_class": "auto",
                "reconstruction": "auto", "structure_colors": 0, "pixel_fixer_bin": fake,
                "pixel_fixer_mode": "full", "evidence_tier": "draft",
            })()
            artifact = module.artifact_from_image(args)
            analysis = artifact["source"]["analysis"]
            self.assertEqual(analysis["detector"], "pixel-art-fixer")
            self.assertEqual(analysis["confidence"], "high")
            self.assertEqual(analysis["external"]["consensus"], "fast:ac+rl(S)")
            self.assertEqual(analysis["inferred_grid"]["width"], 8)
            self.assertNotIn(str(fake), json.dumps(artifact))

    def test_optional_pixel_fixer_adapter_rejects_incomplete_detector_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fake = root / "bad_fixer.py"
            fake.write_text("print('{}')\n", encoding="utf-8")
            source = root / "source.png"
            source.write_bytes(b"not-used-by-fake")
            with self.assertRaisesRegex(module.ArtifactError, "needs cols, rows, step_x, and step_y"):
                module.run_pixel_fixer_detector(fake, source)

            fake.write_text("print('{\"cols\": 8, \"rows\": 8, \"step_x\": NaN, \"step_y\": 5}')\n", encoding="utf-8")
            with self.assertRaisesRegex(module.ArtifactError, "invalid grid dimensions"):
                module.run_pixel_fixer_detector(fake, source)

    def test_image_artifact_reuses_precomputed_pixel_fixer_result_for_resolution_sets(self) -> None:
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.png"
            Image.new("RGBA", (8, 8), (40, 50, 60, 255)).resize((40, 40), Image.Resampling.NEAREST).save(source)
            args = type("Args", (), {
                "image": source, "width": None, "height": None, "size": 8,
                "colors": 4, "alpha_threshold": 10, "background": "transparent",
                "fit": "contain", "resample": "nearest", "min_cluster": 1,
                "dither": "none", "title": "Cached detector fixture", "source_class": "auto",
                "reconstruction": "auto", "structure_colors": 0,
                "pixel_fixer_bin": root / "missing-binary.exe", "pixel_fixer_mode": "full",
                "pixel_fixer_result": {
                    "detector": "pixel-art-fixer", "mode": "full", "cols": 8, "rows": 8,
                    "step_x": 5.0, "step_y": 5.0, "consensus": "cached", "confidence": "high",
                },
                "evidence_tier": "draft",
            })()
            artifact = module.artifact_from_image(args)
            self.assertEqual(artifact["source"]["analysis"]["external"]["consensus"], "cached")

    def test_resolution_set_cli_invokes_optional_pixel_fixer_once(self) -> None:
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "source.png"
            output = root / "output"
            Image.new("RGBA", (8, 8), (40, 50, 60, 255)).resize((40, 40), Image.Resampling.NEAREST).save(source)
            fake = root / "fake_fixer.py"
            fake.write_text(
                "import json\nfrom pathlib import Path\n"
                "counter = Path(__file__).with_suffix('.count')\n"
                "counter.write_text(str(int(counter.read_text()) + 1) if counter.exists() else '1')\n"
                "print(json.dumps({'cols': 8, 'rows': 8, 'step_x': 5.0, 'step_y': 5.0, 'consensus': 'cached-once'}))\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable, str(MODULE_PATH), "from-image", str(source),
                    "--sizes", "8,16", "--colors", "4", "--pixel-fixer-bin", str(fake),
                    "--output", str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(fake.with_suffix(".count").read_text(encoding="utf-8"), "1")
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual([item["path"] for item in manifest["items"]], ["8x8", "16x16"])

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
