# Pixel Art HTML

> Codex skill for creating exact-grid pixel art and self-contained HTML artifact libraries without calling a model API.

Pixel Art HTML turns text-authored grids, local images, or accepted Codex ImageGen outputs into deterministic JSON, PNG, and standalone HTML. Managed builds are stored as chronological project iterations and automatically indexed in a dark, local-first gallery.

- Build single images or deliberate multi-resolution sets from 8x8 through 128x128.
- Convert locally with Pillow while enforcing exact dimensions and palette limits.
- Keep ImageGen optional and separate from deterministic pixel processing.
- Produce standalone proof pages with no external runtime or network requests.
- Maintain `pixel-art/YYYY/MM/NNN-slug/` iterations and a generated project hub.

## Install

Install with the Skills CLI:

```powershell
npx skills add gvastethecreator/pixel-art-html-skill --skill pixel-art-html
```

Or clone the repository and install `SKILLS/pixel-art-html` through your Codex skill workflow.

## Quick Start

Create a managed artifact from a compact scene spec:

```powershell
python .\SKILLS\pixel-art-html\scripts\build_pixel_art.py from-spec .\scene.json --project-root . --slug night-beacon
```

Convert an image into the recommended resolution ladder:

```powershell
uv run --with pillow==11.0.0 python .\SKILLS\pixel-art-html\scripts\build_pixel_art.py from-image .\source.png --project-root . --slug character-set --sizes all
```

Both commands regenerate `pixel-art/index.html`, which navigates every managed iteration in the project. Use `--output <directory>` when an unindexed standalone destination is preferable.

## Develop And Verify

Node 20 or newer and Python 3.11 or newer are recommended:

```powershell
npm run check
```

The image-conversion test runs when Pillow is installed; all other tests use the Python standard library.

## Documentation

- [Skill workflow](./SKILLS/pixel-art-html/SKILL.md)
- [Artifact schema](./SKILLS/pixel-art-html/references/artifact-schema.md)
- [Project library contract](./SKILLS/pixel-art-html/references/project-library.md)
- [Visual quality contract](./SKILLS/pixel-art-html/references/quality-contract.md)

## Background

The project was inspired by the idea of agent-directed pixel-art conversion explored by [robustonian/ai-pixel-art-converter](https://github.com/robustonian/ai-pixel-art-converter). This repository is an independent implementation focused on Codex skills, local deterministic processing, standalone HTML, and project-level artifact navigation; it does not use that project's API/server implementation.

## Status

Preview skill pack. The deterministic spec and HTML paths are dependency-free; image conversion requires Pillow. Visual quality still depends on the supplied source or authored grid.

## License

[MIT](./LICENSE)

