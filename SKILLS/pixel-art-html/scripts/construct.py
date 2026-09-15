#!/usr/bin/env python3
"""Compose named pixel parts and advance only from a reviewed construction stage."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

import build_pixel_art as core

STAGES = ('block', 'planes', 'material')
TEMPLATE = core.SKILL_DIR / 'assets' / 'pixel-art-construction-template.html'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def integer(value, name, low=None, high=None):
    if type(value) is not int or (low is not None and value < low) or (high is not None and value > high):
        raise ValueError(f'{name}: expected an integer in range {low}..{high}')
    return value


def pair(value, name):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f'{name}: expected [x, y]')
    return [integer(v, name) for v in value]


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{name}: expected nonempty text')
    return value


def compile_parts(source):
    if source.get('kind') != 'construction' or source.get('schema_version') != 1 or source.get('stage') not in STAGES:
        raise ValueError('Expected construction schema 1 and block, planes, or material stage')
    width, height = [integer(source.get(k), k, 8, core.MAX_DIMENSION) for k in ('width', 'height')]
    text(source.get('title'), 'title')
    text(source.get('intent'), 'intent')
    text(source.get('light'), 'light')
    budget = integer(source.get('palette_budget'), 'palette_budget', 1, 256)
    background = core.normalize_color(source.get('background'))
    palette = source.get('palette')
    if not isinstance(palette, dict) or not palette:
        raise ValueError('palette needs single-character aliases')
    colors = {}
    for alias, color in palette.items():
        if len(alias) != 1 or alias == '.' or core.normalize_color(color) is None:
            raise ValueError('Palette aliases must be one character, excluding .; colors must be opaque')
        colors[alias] = core.normalize_color(color)
    parts = source.get('parts')
    if not isinstance(parts, list) or not parts:
        raise ValueError('At least one part is required')
    by_id, origins, masks, anchors = {}, {}, {}, {}
    for part in parts:
        name = text(part.get('id'), 'part id')
        if name in by_id:
            raise ValueError(f'Duplicate part {name}')
        by_id[name] = part
        if part.get('role', 'subject') not in ('subject', 'environment'):
            raise ValueError(f'{name}: role must be subject or environment')
        pair(part.get('origin'), f'{name} origin')
        rows = part.get('grid')
        if not isinstance(rows, list) or not rows or not all(isinstance(r, str) for r in rows):
            raise ValueError(f'{name}: grid needs string rows')
        pw = len(rows[0])
        if not 1 <= pw <= core.MAX_DIMENSION or len(rows) > core.MAX_DIMENSION or any(len(r) != pw for r in rows):
            raise ValueError(f'{name}: grid must be rectangular, at most {core.MAX_DIMENSION}x{core.MAX_DIMENSION}')
        if any(c not in colors and c != '.' for r in rows for c in r):
            raise ValueError(f'{name}: unknown palette alias')
        if not any(c != '.' for r in rows for c in r):
            raise ValueError(f'{name}: empty part')
        for aid, point in part.get('anchors', {}).items():
            text(aid, 'anchor id')
            ax, ay = pair(point, 'anchor')
            if not (0 <= ax < pw and 0 <= ay < len(rows)):
                raise ValueError(f'{name}.{aid}: anchor outside part bounds')

    def locate(name, visiting=()):
        if name in origins:
            return origins[name]
        if name not in by_id or name in visiting:
            raise ValueError('Unknown parent or parent cycle')
        part = by_id[name]
        x, y = part['origin']
        parent = part.get('parent')
        if parent is not None:
            px, py = locate(parent, (*visiting, name))
            x, y = x + px, y + py
        if x < 0 or y < 0 or x + len(part['grid'][0]) > width or y + len(part['grid']) > height:
            raise ValueError(f'{name}: part bounds leave the world')
        origins[name] = [x, y]
        return x, y

    grid = [[background] * width for _ in range(height)]
    owner = [[None] * width for _ in range(height)]
    for part in parts:
        name = part['id']
        ox, oy = locate(name)
        masks[name] = set()
        anchors[name] = {aid: [ox + p[0], oy + p[1]] for aid, p in part.get('anchors', {}).items()}
        for y, row in enumerate(part['grid']):
            for x, alias in enumerate(row):
                if alias != '.':
                    masks[name].add((ox + x, oy + y))
                    grid[oy + y][ox + x], owner[oy + y][ox + x] = colors[alias], name
    used = {c for row in grid for c in row if c is not None}
    # Hidden paint still counts: toggling a part must not reveal undeclared extra colors.
    used.update(colors[c] for p in parts for row in p['grid'] for c in row if c != '.')
    if len(used) > budget:
        raise ValueError('Construction exceeds palette_budget, including hidden paint and background')

    def anchor(ref):
        if not isinstance(ref, list) or len(ref) != 2 or ref[0] not in anchors or ref[1] not in anchors[ref[0]]:
            raise ValueError('Anchor reference must be [part_id, anchor_id]')
        return anchors[ref[0]][ref[1]]

    constraints = source.get('constraints', [])
    if not isinstance(constraints, list):
        raise ValueError('constraints must be an array')
    checks, check_ids = [], set()
    for c in constraints:
        cid = text(c.get('id'), 'constraint id')
        if cid in check_ids:
            raise ValueError('Constraint ids must be unique')
        check_ids.add(cid)
        kind = c.get('kind')
        if kind == 'anchor':
            a, b = anchor(c.get('a')), anchor(c.get('b'))
            limit = integer(c.get('max_distance', 0), 'max_distance', 0, core.MAX_DIMENSION)
            actual = max(abs(a[0] - b[0]), abs(a[1] - b[1]))
            passed = actual <= limit
            detail = {'a': a, 'b': b, 'distance': actual, 'maximum': limit}
        elif kind == 'visible':
            name = c.get('part')
            if name not in masks:
                raise ValueError('visible constraint refers to an unknown part')
            minimum = integer(c.get('min_cells'), 'min_cells', 1, width * height)
            actual = sum(v == name for row in owner for v in row)
            passed, detail = actual >= minimum, {'part': name, 'visible_cells': actual, 'minimum': minimum}
        elif kind == 'inside':
            point = anchor(c.get('at'))
            container, excluded = c.get('container'), c.get('exclude', [])
            if container not in masks or not isinstance(excluded, list) or any(n not in masks for n in excluded):
                raise ValueError('inside constraint needs known container and exclusion parts')
            hits = [name for name in excluded if tuple(point) in masks[name]]
            passed = tuple(point) in masks[container] and not hits
            detail = {'point': point, 'container': container, 'excluded_by': hits}
        elif kind == 'clear':
            region = c.get('region')
            if not isinstance(region, list) or len(region) != 4:
                raise ValueError('clear region must be [x,y,width,height]')
            x, y, w, h = [integer(v, 'clear coordinate', 0) for v in region]
            names = c.get('parts')
            if w < 1 or h < 1 or x + w > width or y + h > height or not isinstance(names, list) or not names or any(n not in masks for n in names):
                raise ValueError('Invalid clear region or parts')
            hits = sorted(set().union(*(masks[n] for n in names)) & {(px, py) for py in range(y, y+h) for px in range(x, x+w)})
            passed, detail = not hits, {'region': region, 'occupied_cells': [list(p) for p in hits]}
        else:
            raise ValueError(f'Unknown constraint kind {kind}')
        checks.append({'id': cid, 'kind': kind, 'passed': passed, **detail})
    artifact = core.canonical_artifact(title=source['title'], grid=grid, background=background,
        source={'kind': 'construction', 'source_fingerprint': digest(source), 'stage': source['stage']}, evidence_tier='draft')
    core.validate_artifact(artifact)
    report = {'source_fingerprint': digest(source), 'artifact_fingerprint': core.artifact_fingerprint(artifact),
              'stage': source['stage'], 'palette': colors, 'background': background,
              'origins': origins, 'anchors': anchors, 'owner': owner, 'checks': checks,
              'constraints_passed': all(c['passed'] for c in checks),
              'limit': 'Declared geometry only. Anchor proximity and visible cell counts do not prove recognition or good art.'}
    return artifact, report


def structure(source):
    return {k: source.get(k) for k in ('width', 'height', 'background', 'intent', 'light', 'palette_budget', 'constraints')} | {
        'parts': [{k: p.get(k) for k in ('id', 'parent', 'origin', 'anchors', 'role')} |
                  {'mask': [''.join('.' if c == '.' else '#' for c in row) for row in p['grid']]} for p in source['parts']]}


def check_review(source, review):
    _, report = compile_parts(source)
    if review.get('source_fingerprint') != digest(source) or review.get('artifact_fingerprint') != report['artifact_fingerprint']:
        raise ValueError('Review does not bind this source and rendered grid')
    if review.get('stage') != source['stage'] or review.get('decision') not in ('advance', 'rework'):
        raise ValueError('Review needs matching stage and advance or rework decision')
    if review.get('reviewer_kind') not in ('self', 'independent-agent', 'user'):
        raise ValueError('Declare reviewer_kind: self, independent-agent, or user')
    for key in ('reviewer', 'observed_read', 'remaining_limit', 'evidence'):
        text(review.get(key), key)
    views = review.get('views', {})
    required = ('native', 'silhouette') if source['stage'] == 'block' else ('native', 'silhouette', 'value')
    if any(views.get(k) is not True for k in required):
        raise ValueError('Required views must be inspected before a stage review')
    issues = review.get('issues')
    if not isinstance(issues, list) or len(issues) > 3:
        raise ValueError('Review needs an issues array with at most three major issues')
    for issue in issues:
        for k in ('region_or_part', 'observed', 'cause', 'intervention', 'preserve'):
            text(issue.get(k), f'issue {k}')
    if review['decision'] == 'advance' and (issues or not report['constraints_passed']):
        raise ValueError('Resolve blocking issues and failed constraints before advancing')
    if review['decision'] == 'rework' and not issues:
        raise ValueError('Rework needs a concrete observed issue')
    return review


def check_lineage(source, lineage):
    index = STAGES.index(source['stage'])
    if not isinstance(lineage, list) or len(lineage) != index:
        raise ValueError('Stage cannot skip its reviewed predecessors')
    for i, step in enumerate(lineage):
        prior, review = step['source'], step['review']
        if prior['stage'] != STAGES[i]:
            raise ValueError('Stage lineage is out of order')
        check_review(prior, review)
        if review['decision'] != 'advance':
            raise ValueError('A rework review cannot authorize the next stage')
        if structure(prior) != structure(source):
            raise ValueError('Structure changed after review; return to block with the revised construction')


def payload(source, report):
    return {'source': source, 'report': report}


def validate_output(output):
    output = Path(output)
    state = read(output / 'construction.json')
    source, lineage = state['source'], state['lineage']
    artifact, report = compile_parts(source)
    check_lineage(source, lineage)
    actual = core.validate_output(output)
    if actual != artifact or read(output / 'construction-report.json') != report:
        raise ValueError('Construction, report, and native artifact disagree')
    if core.read_embedded_json(output / 'parts.html', 'construction-data') != payload(source, report):
        raise ValueError('Part viewer payload drift')
    core.validate_standalone_html(output / 'parts.html', ('__CONSTRUCTION__',))
    return state


def build(source, output, previous=None, review=None):
    output = Path(output)
    if output.exists():
        raise ValueError('Output must be a new directory; keep the previous stage')
    artifact, report = compile_parts(source)
    lineage = []
    if previous is not None:
        prior = validate_output(previous)
        if review is None:
            raise ValueError('The previous stage needs an observed review')
        lineage = [*prior['lineage'], {'source': prior['source'], 'review': review}]
    elif review is not None:
        raise ValueError('Review requires a previous stage')
    check_lineage(source, lineage)
    page = TEMPLATE.read_text(encoding='utf-8').replace('__CONSTRUCTION__', json.dumps(payload(source, report), ensure_ascii=False).replace('<', '\\u003c'))
    core.write_artifact(artifact, output, 1)
    save(output / 'construction.json', {'source': source, 'lineage': lineage})
    save(output / 'construction-report.json', report)
    (output / 'parts.html').write_text(page, encoding='utf-8', newline='\n')
    validate_output(output)
    return report


def edit(source, patch):
    if patch.get('source_fingerprint') != digest(source):
        raise ValueError('Edit fingerprint is stale')
    compile_parts(source)
    result = copy.deepcopy(source)
    by_id = {p['id']: p for p in result['parts']}
    ops = patch.get('operations')
    if not isinstance(ops, list) or not ops:
        raise ValueError('Edit needs operations')
    text(patch.get('hypothesis'), 'hypothesis')
    for op in ops:
        name = op.get('part')
        if name not in by_id:
            raise ValueError('Edit refers to an unknown part')
        p = by_id[name]
        kind = op.get('kind')
        if kind == 'translate':
            delta = pair(op.get('delta'), 'delta')
            p['origin'] = [a + b for a, b in zip(p['origin'], delta)]
        elif kind == 'replace-grid':
            p['grid'] = copy.deepcopy(op.get('grid'))
        elif kind == 'mirror':
            if any(v.get('parent') == name for v in result['parts']):
                raise ValueError('Mirror a leaf part only; reauthor a multipart pose and its light explicitly')
            width = len(p['grid'][0])
            p['grid'] = [r[::-1] for r in p['grid']]
            p['anchors'] = {k: [width - 1 - v[0], v[1]] for k, v in p.get('anchors', {}).items()}
            result['stage'] = 'block'
        else:
            raise ValueError(f'Unknown edit operation {kind}')
    if structure(result) != structure(source):
        result['stage'] = 'block'
    compile_parts(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    cmds = parser.add_subparsers(dest='command', required=True)
    b = cmds.add_parser('build')
    b.add_argument('source', type=Path)
    b.add_argument('--output', type=Path, required=True)
    b.add_argument('--previous', type=Path)
    b.add_argument('--review', type=Path)
    v = cmds.add_parser('validate')
    v.add_argument('output', type=Path)
    r = cmds.add_parser('review')
    r.add_argument('stage', type=Path)
    r.add_argument('input', type=Path)
    r.add_argument('--output', type=Path, required=True)
    e = cmds.add_parser('edit')
    e.add_argument('source', type=Path)
    e.add_argument('patch', type=Path)
    e.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'build':
            result = build(read(args.source), args.output, args.previous, read(args.review) if args.review else None)
        elif args.command == 'validate':
            state = validate_output(args.output)
            result = {'valid': True, 'stage': state['source']['stage'], 'source_fingerprint': digest(state['source'])}
        elif args.command == 'review':
            state = validate_output(args.stage)
            result = check_review(state['source'], read(args.input))
            save(args.output, result)
        else:
            result = edit(read(args.source), read(args.patch))
            save(args.output, result)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, KeyError, TypeError, RecursionError) as exc:
        print(f'Construction: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
