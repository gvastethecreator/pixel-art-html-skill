from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "SKILLS" / "pixel-art-html" / "scripts"
TEST_PATH = SCRIPTS / "test_build_pixel_art.py"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run pixel-art-html tests with an explicit dependency profile.")
    parser.add_argument("--profile", choices=("core", "full"), required=True)
    args = parser.parse_args()
    modules = [load_test_module(), load_test_module(SCRIPTS / "test_interpretation.py", "pixel_art_interpretation_tests")]
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromModule(module) for module in modules)
    cases = list(iter_cases(suite))
    image_cases = [case for case in cases if requires_pillow(case)]
    if args.profile == "full" and not pillow_available():
        print("Full image test profile unavailable: Pillow is not installed.", file=sys.stderr)
        print("Install the declared dependency with `python -m pip install pillow==12.3.0`, then rerun `pnpm run test:full`.", file=sys.stderr)
        print("`pnpm run test:core` remains a complete dependency-free gate.", file=sys.stderr)
        return 2
    # Validate real installed method IDs; unit-test routing fixtures are not substitutes.
    gate = subprocess.run([sys.executable, str(SCRIPTS / "tutorial_bridge.py"), "validate"], check=False)
    if gate.returncode:
        return 1
    selected = cases if args.profile == "full" else [case for case in cases if case not in image_cases]
    print(f"Pixel-art test profile: {args.profile} ({len(selected)} selected; {len(image_cases)} Pillow tests).")
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(unittest.TestSuite(selected))
    if args.profile == "full" and result.skipped:
        print(f"Full image profile must not skip tests; skipped: {len(result.skipped)}", file=sys.stderr)
        return 1
    if not result.wasSuccessful():
        return 1
    if args.profile == "core":
        print(f"Core profile passed: {len(selected)} dependency-free tests; {len(image_cases)} Pillow tests intentionally excluded.")
    else:
        print(f"Full profile passed: {len(selected)} tests; no Pillow tests omitted.")
    return 0


def load_test_module(test_path: Path = TEST_PATH, name: str = "pixel_art_test_suite"):
    spec = importlib.util.spec_from_file_location(name, test_path)
    if not spec or not spec.loader:
        raise RuntimeError(f"Could not load test suite: {test_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def iter_cases(suite: unittest.TestSuite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iter_cases(item)
        else:
            yield item


def requires_pillow(case: unittest.TestCase) -> bool:
    method = getattr(case, case._testMethodName)
    return bool(getattr(method, "requires_pillow", False))


def pillow_available() -> bool:
    return importlib.util.find_spec("PIL") is not None


if __name__ == "__main__":
    raise SystemExit(main())
