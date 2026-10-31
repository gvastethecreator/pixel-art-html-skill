"""Compose exact native masters into a portable scene with an interactive camera."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path

import build_pixel_art as core


def integer(value, name, low=None, high=None):
    value = core.checked_int(value, name)
    if (low is not None and value < low) or (high is not None and value > high):
        raise core.ArtifactError(f'{name} is outside its supported range')
    return value


def validate_scene(scene):
    if scene.get('kind') != 'scene' or scene.get('schema_version') != 1:
        raise core.ArtifactError('expected scene schema version 1')
    width = integer(scene.get('width'), 'width', 8, 2048)
    height = integer(scene.get('height'), 'height', 8, 2048)
    if scene.get('evidence_tier') != 'draft':
        raise core.ArtifactError('composed scenes remain draft')
    if core.normalize_color(scene.get('background')) != scene.get('background'):
        raise core.ArtifactError('scene background must use canonical color syntax')
    if not isinstance(scene.get('assets'), dict) or not scene['assets']:
        raise core.ArtifactError('scene needs embedded assets')
    for artifact in scene['assets'].values():
        core.validate_artifact(artifact)
    groups = scene.get('groups', [])
    ids = [g['id'] for g in groups]
    if len(ids) != len(set(ids)) or any(not isinstance(g, str) or not g for g in ids):
        raise core.ArtifactError('group ids must be unique nonempty strings')
    for group in groups:
        if not isinstance(group.get('label'), str):
            raise core.ArtifactError('group needs a label')
    if not isinstance(scene.get('placements'), list) or not scene['placements']:
        raise core.ArtifactError('scene needs placements')
    for i, placement in enumerate(scene['placements']):
        if placement.get('asset') not in scene['assets']:
            raise core.ArtifactError(f'unknown asset in placement {i}')
        artifact = scene['assets'][placement['asset']]
        x, y = (integer(placement.get(k), k) for k in ('x', 'y'))
        integer(placement.get('depth'), 'depth')
        if not isinstance(placement.get('flip_x', False), bool):
            raise core.ArtifactError('flip_x must be boolean')
        if not isinstance(placement.get('subject', False), bool):
            raise core.ArtifactError('subject must be boolean')
        if placement.get('group') is not None and placement['group'] not in ids:
            raise core.ArtifactError('placement uses an unknown group')
        if x < 0 or y < 0 or x + artifact['width'] > width or y + artifact['height'] > height:
            raise core.ArtifactError(f'placement {i} exceeds scene bounds; crop its source deliberately')
    for point in scene.get('focus_points', []):
        integer(point.get('x'), 'focus x', 0, width)
        integer(point.get('y'), 'focus y', 0, height)
        integer(point.get('zoom', 4), 'focus zoom', 1, 8)
        if not isinstance(point.get('label'), str):
            raise core.ArtifactError('focus point needs a label')
    integer(scene.get('palette_budget'), 'palette_budget', 1, 256)


def scene_grid(scene, hidden=()):
    """Stable depth order, transparent no-op, optional per-placement horizontal flip."""
    grid = [[scene['background']] * scene['width'] for _ in range(scene['height'])]
    for placement in sorted(scene['placements'], key=lambda p: p['depth']):
        if placement.get('group') in hidden:
            continue
        artifact = scene['assets'][placement['asset']]
        for sy, row in enumerate(artifact['grid']):
            source = reversed(row) if placement.get('flip_x') else row
            for sx, color in enumerate(source):
                if color is not None:
                    grid[placement['y'] + sy][placement['x'] + sx] = color
    return grid


def compile_scene(manifest, base):
    scene = {
        'kind': 'scene', 'schema_version': 1, 'evidence_tier': 'draft',
        'title': manifest.get('title', 'Pixel scene'),
        'subtitle': manifest.get('subtitle', ''),
        'caption': manifest.get('caption', 'Original scene'),
        'width': manifest.get('width'), 'height': manifest.get('height'),
        'background': core.normalize_color(manifest.get('background')),
        'palette_budget': manifest.get('palette_budget', 32),
        'assets': {}, 'placements': manifest.get('placements', []),
        'groups': manifest.get('groups', []),
        'focus_points': manifest.get('focus_points', []),
    }
    for key, relative in manifest.get('assets', {}).items():
        scene['assets'][key] = json.loads((base / relative).read_text(encoding='utf-8'))
    validate_scene(scene)
    grid = scene_grid(scene)
    colors = sorted({color for row in grid for color in row if color})
    if len(colors) > scene['palette_budget']:
        raise core.ArtifactError(f"composed palette has {len(colors)} colors; budget is {scene['palette_budget']}")
    scene['colors'] = colors
    scene['fingerprint'] = fingerprint(scene)
    return scene


def fingerprint(scene):
    payload = {key: value for key, value in scene.items() if key != 'fingerprint'}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def write_scene(scene, output):
    validate_scene(scene)
    if output.exists():
        raise core.ArtifactError('scene output must be a new directory')
    template = (Path(__file__).resolve().parents[1] / 'assets/pixel-art-scene-template.html').read_text(encoding='utf-8')
    payload = json.dumps(scene, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    page = template.replace('__TITLE_TEXT__', html.escape(scene['title'])).replace('__SCENE_JSON__', payload)
    output.mkdir(parents=True)
    (output / 'scene.json').write_text(json.dumps(scene, ensure_ascii=False, indent=2), encoding='utf-8')
    (output / 'index.html').write_text(page, encoding='utf-8')
    core.write_png({'grid': scene_grid(scene), 'width': scene['width'], 'height': scene['height']}, output / 'scene.png', 1)


def validate_output(output):
    scene = json.loads((output / 'scene.json').read_text(encoding='utf-8'))
    validate_scene(scene)
    if fingerprint(scene) != scene.get('fingerprint'):
        raise core.ArtifactError('scene fingerprint mismatch')
    core.validate_standalone_html(output / 'index.html', ('__SCENE_JSON__', '__TITLE_TEXT__'))
    if core.read_embedded_json(output / 'index.html', 'scene-data') != scene:
        raise core.ArtifactError('HTML scene payload differs from scene.json')
    grid = scene_grid(scene)
    colors = sorted({c for row in grid for c in row if c})
    if colors != scene.get('colors') or len(colors) > scene['palette_budget']:
        raise core.ArtifactError('scene palette drift')
    scale = core.validate_png_parity({'grid': grid, 'width': scene['width'], 'height': scene['height']}, output / 'scene.png')
    if scale != 1:
        raise core.ArtifactError('scene PNG must remain native')
    return {'kind': 'scene', 'width': scene['width'], 'height': scene['height'], 'assets': len(scene['assets']), 'placements': len(scene['placements']), 'colors': len(colors), 'fingerprint': scene['fingerprint'], 'parity': 'passed', 'tier': 'draft'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    build = commands.add_parser('build')
    build.add_argument('manifest', type=Path)
    build.add_argument('--output', type=Path, required=True)
    check = commands.add_parser('validate')
    check.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'build':
            spec = json.loads(args.manifest.read_text(encoding='utf-8'))
            write_scene(compile_scene(spec, args.manifest.parent), args.output)
        print(json.dumps(validate_output(args.output), indent=2))
    except (core.ArtifactError, OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f'error: {error}\n')


if __name__ == '__main__':
    main()
