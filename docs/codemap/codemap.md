# Code map: pixel-art-html-skill

Generated: 2026-09-13T05:38:38Z | Commit: `72f22179d2a1` | Schema: 2
Generation: `7625411af2b00092a26685215cbaca0585a9864dc774d3729420ffaf47601e7b`
Scope: . | Inventory: working-tree
Nodes: 58 | Edges: 249 | Flows: 5

## Coverage

- Analysis: **partial**; 17 analyzed of 17 included files.
- Configuration files: 0; omitted untracked files: 0.
- Unresolved references and analysis limits: 48.
- Static references and call paths do not prove runtime execution or test coverage.

## Modules

- `SKILLS/pixel-art-html/SKILL.md` | module | Repository | callers: none | callees: none | tests: 0 | entry: none
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` | interface | Repository | callers: none | callees: external:python:PIL, external:python:__future__, external:python:argparse, external:python:argparse | tests: 0 | entry: SKILLS/pixel-art-html/examples/city-clash/build_city.py:main
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` | interface | Repository | callers: none | callees: external:python:PIL, external:python:argparse, external:python:argparse, external:python:build_pixel_art | tests: 0 | entry: SKILLS/pixel-art-html/examples/part-construction/build_demo.py:main
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` | interface | Repository | callers: none | callees: external:python:PIL, external:python:__future__, external:python:argparse, external:python:argparse | tests: 0 | entry: SKILLS/pixel-art-html/examples/part-construction/create_sources.py:main
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` | module | Repository | callers: none | callees: external:python:PIL, external:python:__future__, external:python:argparse, external:python:argparse | tests: 0 | entry: none
- `SKILLS/pixel-art-html/scripts/build_pixel_art.py` | module | Repository | callers: none | callees: external:python:PIL, external:python:__future__, external:python:argparse, external:python:argparse | tests: 0 | entry: none
- `SKILLS/pixel-art-html/scripts/compose_scene.py` | interface | Repository | callers: none | callees: external:python:__future__, external:python:argparse, external:python:argparse, external:python:build_pixel_art | tests: 0 | entry: SKILLS/pixel-art-html/scripts/compose_scene.py:main
- `SKILLS/pixel-art-html/scripts/construct.py` | module | Repository | callers: none | callees: external:python:__future__, external:python:argparse, external:python:argparse, external:python:build_pixel_art | tests: 0 | entry: none
- `SKILLS/pixel-art-html/scripts/interpretation.py` | module | Repository | callers: none | callees: external:python:__future__, external:python:re, external:python:re, external:python:typing | tests: 0 | entry: none
- `SKILLS/pixel-art-html/scripts/pixel_lab.py` | module | Repository | callers: none | callees: external:python:PIL, external:python:__future__, external:python:argparse, external:python:argparse | tests: 0 | entry: none
- `SKILLS/pixel-art-html/scripts/reference_library.py` | module | Repository | callers: none | callees: external:python:PIL, external:python:__future__, external:python:argparse, external:python:argparse | tests: 0 | entry: none
- `SKILLS/pixel-art-html/scripts/test_build_pixel_art.py` | module | Repository | callers: none | callees: external:python:PIL, external:python:__future__, external:python:compose_scene, external:python:compose_scene | tests: 0 | entry: none
- `SKILLS/pixel-art-html/scripts/test_interpretation.py` | module | Repository | callers: none | callees: external:python:__future__, external:python:contextlib, external:python:copy, external:python:copy | tests: 0 | entry: none
- `SKILLS/pixel-art-html/scripts/tutorial_bridge.py` | module | Repository | callers: none | callees: external:python:__future__, external:python:argparse, external:python:argparse, external:python:collections | tests: 0 | entry: none
- `external:javascript:node:fs` | external | External | callers: scripts/validate-skill-pack.mjs | callees: none | tests: 0 | entry: none
- `external:javascript:node:path` | external | External | callers: scripts/validate-skill-pack.mjs | callees: none | tests: 0 | entry: none
- `external:javascript:node:url` | external | External | callers: scripts/validate-skill-pack.mjs, scripts/validate-skill-pack.mjs | callees: none | tests: 0 | entry: none
- `external:python:PIL` | external | External | callers: SKILLS/pixel-art-html/examples/city-clash/build_city.py, SKILLS/pixel-art-html/examples/part-construction/build_demo.py, SKILLS/pixel-art-html/examples/part-construction/create_sources.py, SKILLS/pixel-art-html/scripts/benchmark_small_grids.py | callees: none | tests: 1 | entry: none
- `external:python:__future__` | external | External | callers: SKILLS/pixel-art-html/examples/city-clash/build_city.py, SKILLS/pixel-art-html/examples/part-construction/create_sources.py, SKILLS/pixel-art-html/scripts/benchmark_small_grids.py, SKILLS/pixel-art-html/scripts/build_pixel_art.py | callees: none | tests: 2 | entry: none
- `external:python:argparse` | external | External | callers: SKILLS/pixel-art-html/examples/city-clash/build_city.py, SKILLS/pixel-art-html/examples/city-clash/build_city.py, SKILLS/pixel-art-html/examples/part-construction/build_demo.py, SKILLS/pixel-art-html/examples/part-construction/build_demo.py | callees: none | tests: 0 | entry: none
- Showing 20 of 58 nodes. Query `impact --module <path>` or open the HTML hierarchy for the rest.

## Edges

- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:PIL` | imports
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:__future__` | imports
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:argparse` | calls
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:argparse` | imports
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:build_pixel_art` | calls
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:build_pixel_art` | imports
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:compose_scene` | calls
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:compose_scene` | imports
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:json` | calls
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:json` | imports
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:pathlib` | calls
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:pathlib` | imports
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:sys` | imports
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:PIL` | imports
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:argparse` | calls
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:argparse` | imports
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:build_pixel_art` | calls
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:build_pixel_art` | imports
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:compose_scene` | calls
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:compose_scene` | imports
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:construct` | calls
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:construct` | imports
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:html` | calls
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:html` | imports
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:json` | calls
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:json` | imports
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:pathlib` | calls
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:pathlib` | imports
- `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:sys` | imports
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:PIL` | imports
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:__future__` | imports
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:argparse` | calls
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:argparse` | imports
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:construct` | calls
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:construct` | imports
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:json` | calls
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:json` | imports
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:pathlib` | calls
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:pathlib` | imports
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py` -> `external:python:sys` | imports
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` -> `external:python:PIL` | imports
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` -> `external:python:__future__` | imports
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` -> `external:python:argparse` | calls
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` -> `external:python:argparse` | imports
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` -> `external:python:base64` | calls
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` -> `external:python:base64` | imports
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` -> `external:python:build_pixel_art` | calls
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` -> `external:python:build_pixel_art` | imports
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` -> `external:python:collections` | calls
- `SKILLS/pixel-art-html/scripts/benchmark_small_grids.py` -> `external:python:collections` | imports
- Showing 50 of 249 edges; JSON contains every edge and its evidence.

## Unknown

- `SKILLS/pixel-art-html/examples/city-clash/build_city.py:37`: object-member-call-not-resolved (Image)
- `SKILLS/pixel-art-html/examples/city-clash/build_city.py:38`: object-member-call-not-resolved (ImageDraw)
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py:28`: object-member-call-not-resolved (Image)
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py:28`: object-member-call-not-resolved (ImageDraw)
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py:115`: object-member-call-not-resolved (Image)
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py:115`: object-member-call-not-resolved (ImageDraw)
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py:178`: object-member-call-not-resolved (Image)
- `SKILLS/pixel-art-html/examples/part-construction/create_sources.py:178`: object-member-call-not-resolved (ImageDraw)
- `SKILLS/pixel-art-html/scripts/build_pixel_art.py:1621`: object-member-call-not-resolved (datetime)
- `SKILLS/pixel-art-html/scripts/build_pixel_art.py:1622`: object-member-call-not-resolved (Path)
- `SKILLS/pixel-art-html/scripts/build_pixel_art.py:1635`: object-member-call-not-resolved (datetime)
- `SKILLS/pixel-art-html/scripts/build_pixel_art.py:1772`: object-member-call-not-resolved (Path)

## Flows

- Python __main__: `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:argparse` | Static call path reaches external:python:argparse:ArgumentParser
- Python __main__: `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:construct` | Static call path reaches external:python:construct:read
- Python __main__: `SKILLS/pixel-art-html/scripts/compose_scene.py` -> `external:python:pathlib` | Static call path reaches external:python:pathlib:Path
- Python __main__: `SKILLS/pixel-art-html/examples/part-construction/build_demo.py` -> `external:python:json` | Static call path reaches external:python:json:dumps
- Python __main__: `SKILLS/pixel-art-html/examples/city-clash/build_city.py` -> `external:python:json` | Static call path reaches external:python:json:dumps

## Architecture changes

- Nodes: +0 / -0; edges: +0 / -0.
- Boundary changes: 0; new cycles: 0.

## Read next

- Use `status` before relying on this generation.
- Use `impact --changed` for possible impact and related test evidence.
- Use `diff --before <model> --after <model>` for architecture changes.
