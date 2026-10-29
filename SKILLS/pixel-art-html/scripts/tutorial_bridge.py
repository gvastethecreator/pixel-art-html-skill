#!/usr/bin/env python3
"""Retrieve contextual tutorial lessons without downloading or executing source content.

Pure standard library. Scores describe lexical matches, never artistic quality.
This module is additive: the existing reference_library.py remains unchanged.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import re
import sys
import unicodedata
from typing import Any

from interpretation import (STAGES, PROJECTIONS, SUBJECTS, PATTERNS, BASE_ROUTES,
                            BASE_CONTEXT, interpret, normalize)

ROOT = Path(__file__).resolve().parents[1]
STOP_WORDS = set('el la los las un una unos unas de del en con que por para al es se mi mis me y the a an of in with is my to and looks parece tiene como'.split())
ACCESS = {'metadata-only', 'public-index-reviewed', 'public-text-reviewed', 'user-file-reviewed'}


def terms(value: str) -> set[str]:
    if not isinstance(value, str):
        raise ValueError('Search text must be a string')
    normalized = unicodedata.normalize('NFKD', value.casefold())
    clean = ''.join(c for c in normalized if not unicodedata.combining(c))
    return set(re.findall(r'[a-z0-9]+', clean)) - STOP_WORDS


def load_json(path: Path) -> dict[str, Any]:
    # Local data, never instructions to execute. Reject duplicate keys and oversized input.
    if path.stat().st_size > 2_000_000:
        raise ValueError('JSON input exceeds the 2 MB limit')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate JSON key: {key}')
            result[key] = value
        return result
    data = json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=unique)
    if not isinstance(data, dict):
        raise ValueError(f'Expected JSON object: {path}')
    return data


def load_catalog(root: Path = ROOT) -> tuple[dict, dict]:
    lessons = load_json(root / 'references/tutorial-lessons.json')
    sources = load_json(root / 'references/tutorial-sources.json')
    validate_catalog(lessons, sources)
    return lessons, sources


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_catalog(lessons: dict, registry: dict, base: dict | None = None) -> dict:
    _require(type(lessons.get('schema_version')) is int and type(registry.get('schema_version')) is int and
             lessons.get('schema_version') == 2 and registry.get('schema_version') == 1,
             'Unsupported catalog schema')
    source_list = registry.get('sources')
    lesson_list = lessons.get('lessons')
    _require(isinstance(source_list, list) and bool(source_list) and
             isinstance(lesson_list, list) and bool(lesson_list), 'Missing or empty lists')
    sources: dict[str, dict] = {}
    for s in source_list:
        _require(isinstance(s, dict) and isinstance(s.get('id'), str), 'Invalid source')
        sid = s['id']
        _require(sid not in sources, f'Duplicate source: {sid}')
        _require(s.get('access') in ACCESS, f'Unknown access state: {sid}')
        _require(isinstance(s.get('url'), str) and s['url'].startswith('https://'), f'Invalid URL: {sid}')
        _require(s.get('redistribute_media') is False, f'Media redistribution not allowed: {sid}')
        date.fromisoformat(s.get('checked_at', ''))
        _require(isinstance(s.get('review_scope'), list) and s['review_scope'], f'Missing scope: {sid}')
        _require(isinstance(s.get('body_reviewed'), bool) and isinstance(s.get('media_reviewed'), bool), f'Missing evidence flags: {sid}')
        if s['access'] in ('metadata-only', 'public-index-reviewed'):
            _require(s['body_reviewed'] is False and s['media_reviewed'] is False, f'Metadata cannot prove content review: {sid}')
        sources[sid] = s
    base_ids = {t['id'] for t in base['techniques']} if base is not None else None
    if base_ids is not None:
        _require(set(BASE_CONTEXT) <= base_ids, 'Missing base routing IDs: ' + ', '.join(sorted(set(BASE_CONTEXT) - base_ids)))
    seen: set[str] = set()
    required = ('id','extends','title','source_observation','transfer_decision','visual_check','counterexample','acceptance','authority')
    for lesson in lesson_list:
        _require(isinstance(lesson, dict), 'Invalid lesson')
        _require(all(isinstance(lesson.get(k), str) and lesson[k].strip() for k in required), 'Incomplete lesson text')
        lid = lesson['id']
        _require(lid not in seen, f'Duplicate lesson: {lid}')
        seen.add(lid)
        for key in ('symptoms','tags','stages','projections','source_ids','pixel_operations','issues','subjects'):
            _require(isinstance(lesson.get(key), list) and bool(lesson[key]) and
                     all(isinstance(v, str) and v for v in lesson[key]), f'Invalid {key}: {lid}')
        _require(set(lesson['stages']) <= set(STAGES), f'Unknown stage: {lid}')
        _require(set(lesson['issues']) <= set(PATTERNS), f'Unknown issue: {lid}')
        _require(set(lesson['subjects']) <= set(SUBJECTS) | {'any'}, f'Unknown subject: {lid}')
        _require(isinstance(lesson.get('when_terms_any', []), list) and
                 all(isinstance(v, str) and v.strip() for v in lesson.get('when_terms_any', [])),
                 f'Invalid conditional terms: {lid}')
        _require(set(lesson['projections']) <= set(PROJECTIONS) | {'any'}, f'Unknown projection: {lid}')
        for sid in lesson['source_ids']:
            _require(sid in sources, f'Unknown source {sid}: {lid}')
            _require(sources[sid]['body_reviewed'] is True, f'Metadata cannot support lesson content: {lid}')
        if base_ids is not None:
            _require(lesson['extends'] in base_ids, f'Unknown baseline technique: {lesson["extends"]}')
        e = lesson.get('exercise', {})
        _require(isinstance(e, dict), f'Invalid exercise: {lid}')
        grid = e.get('grid')
        _require(isinstance(grid, list) and len(grid) == 2 and all(type(v) is int and 1 <= v <= 1024 for v in grid), f'Invalid exercise grid: {lid}')
        _require(type(e.get('budget')) is int and 1 <= e['budget'] <= 256, f'Invalid palette budget: {lid}')
        for key in ('brief','protected','comparison','question'):
            _require(isinstance(e.get(key), str) and e[key].strip(), f'Incomplete exercise: {lid}')
    return {'lessons':len(seen),'sources':len(sources),'baseline_ids_checked':base is not None,
            'artistic_acceptance':'not evaluated'}


def diagnose(query: str | None, catalog: dict, registry: dict, *, stage: str | None = None,
             projection: str | None = None, subject: str | None = None,
             context: dict | None = None, base: dict | None = None, limit: int = 3) -> dict:
    """Retrieve conditional methods AFTER bounded interpretation; never diagnose an image."""
    _require(type(limit) is int and 1 <= limit <= 12, 'limit must be between 1 and 12')
    observed = interpret(query, context, stage=stage, projection=projection, subject=subject)
    stage, projection, subject = (observed['filters'][k] for k in ('stage','projection','subject'))
    active = set(observed['active_issues'])
    positive = ' '.join(s['text'] for s in observed['statements']
                        if s['polarity'] == 'observed' and set(s['issues']) & active)
    wanted = terms(positive)
    candidates, mismatches = [], []
    for lesson in catalog['lessons']:
        matched_issues = active & set(lesson['issues'])
        if not matched_issues:
            continue
        if subject and 'any' not in lesson['subjects'] and subject not in lesson['subjects']:
            continue
        if projection and 'any' not in lesson['projections'] and projection not in lesson['projections']:
            continue
        if stage and stage not in lesson['stages']:
            mismatches.append({'id':lesson['id'], 'allowed_stages':lesson['stages']})
            continue
        conditional = lesson.get('when_terms_any', [])
        if conditional and not any(terms(term) <= wanted for term in conditional):
            continue
        vocabulary = terms(' '.join([*lesson['symptoms'], *lesson['tags']]))
        matched = sorted(wanted & vocabulary)
        score = len(matched_issues) * 10 + len(matched)
        candidates.append({'kind':'conditional-lesson','lexical_score':score,
                           'matched_terms':matched,'matched_issues':sorted(matched_issues), **lesson})
    candidates.sort(key=lambda item:(-item['lexical_score'],item['id']))
    lessons = candidates[:limit]
    covered = {issue for item in lessons for issue in item['matched_issues']}
    techniques = []
    base_by_id = {item['id']:item for item in (base or {}).get('techniques', [])}
    fallback_matches: dict[str, set[str]] = {}
    for issue in sorted(active - covered):
        routes = BASE_ROUTES.get(issue, ())
        if issue == 'silhouette-read' and subject:
            routes = ({'character':'anatomy-before-costume', 'foliage':'foliage-bundles',
                       'machine':'functional-machines', 'architecture':'constructive-architecture',
                       'prop':'icon-affordance', 'interface':'icon-affordance',
                       'scene':'landscape-depth', 'tile':'tiles-and-transitions'}[subject],)
        if issue == 'pose-rigidity' and subject == 'machine':
            routes = ('functional-machines',)
        if issue == 'material-read' and wanted & {'metal','glass','vidrio','plastico','armor','armadura'}:
            routes = ('metal-glass',)
        for tid in routes:
            stages, subjects = BASE_CONTEXT[tid]
            if subject and subject not in subjects:
                continue
            if stage and stage not in stages:
                mismatches.append({'id':tid, 'allowed_stages':list(stages)})
                continue
            if tid in base_by_id:
                fallback_matches.setdefault(tid, set()).add(issue)
    for tid, issues in sorted(fallback_matches.items(), key=lambda pair:(-len(pair[1]),pair[0])):
        techniques.append({'kind':'base-technique','matched_issues':sorted(issues), **base_by_id[tid]})
    techniques = techniques[:max(0, limit-len(lessons))]
    used = {sid for item in lessons for sid in item['source_ids']}
    chapters = {ch for item in techniques for ch in item.get('chapters', [])}
    notice = ('Inspect the actual asset, confirm the relationship, and test the intervention. '
              'This text retrieval does not establish a visual defect or artistic acceptance.')
    if not active:
        notice = 'No uncontradicted current observation. Nothing was inferred from exclusions or protected intent.'
    elif not lessons and not techniques:
        notice = ('No compatible method found. Recheck subject, stage and the visible relationship; '
                  'no generic texture repair was substituted.')
    return {'query':query, 'interpretation':observed, 'filters':observed['filters'],
            'retrieval':'bounded ES/EN polarity plus explicit issue/subject/stage routing; no image analysis',
            'lessons':lessons, 'techniques':techniques, 'preserve':observed['preserve'],
            'sources':[s for s in registry['sources'] if s['id'] in used],
            'base_sources':[s for s in (base or {}).get('sources', []) if s.get('chapter') in chapters],
            'base_catalog_available':base is not None,
            'stage_mismatches':list({m['id']:m for m in mismatches}.values()),
            'status':('methods-to-test' if lessons or techniques else
                      'no-compatible-method' if active else 'needs-observation'), 'notice':notice}


def exercise_plan(lesson: dict, registry: dict) -> dict:
    e = lesson['exercise']
    return {'schema':'pixel-art-tutorial-exercise/v1','lesson_id':lesson['id'],'status':'draft',
            'scope':'Working brief only. Not a build_pixel_art artifact, stage receipt, or independent review.',
            'brief':e['brief'],'native_grid':e['grid'],'palette_budget':e['budget'],
            'protected':e['protected'],'comparison':e['comparison'],'question':e['question'],
            'source_ids':lesson['source_ids'],'source_access':{s['id']:s['access'] for s in registry['sources'] if s['id'] in lesson['source_ids']},
            'hypothesis':{'observed_symptom':None,'region_xywh':None,'responsible_relationship':None,
                          'operation':None,'expected_native_change':None},
            'reference_transfer':{'observed_in_reference':None,'inference':None,'deliberate_differences':None},
            'review':{'baseline_path':None,'revised_path':None,'browser_observed':False,
                      'result':'not-reviewed','remaining_problem':None,'reviewer_role':None},
            'next_step':'Fill from actual observation, then use the existing construct/pixel_lab workflow within the authorized pass or repair. Use study only when alternatives were explicitly requested.'}


def scale_contract(width: int, height: int, scale: int, target_width: int | None = None,
                   target_height: int | None = None) -> dict:
    _require(all(type(v) is int and 1 <= v <= 16384 for v in (width,height,scale)), 'Dimensions and scale must be positive integers <=16384')
    _require((target_width is None) == (target_height is None), 'Provide both target dimensions')
    native = [width,height]
    rendered = [width*scale,height*scale]
    result: dict = {'native':native,'integer_scale':scale,'rendered':rendered,
                    'scope':'Pixel arithmetic only; browser DPR, zoom and CSS layout require separate observation.'}
    if target_width is not None:
        _require(all(type(v) is int and 1 <= v <= 1048576 for v in (target_width,target_height)), 'Invalid target dimensions')
        delta = [target_width-rendered[0],target_height-rendered[1]]
        result.update(target=[target_width,target_height],exact=delta==[0,0],remaining_space=delta,
                      fits_without_crop=all(v>=0 for v in delta),
                      note='Exact fit.' if delta==[0,0] else 'Choose explicit margins, cropping, a different scale, or a separately authored native size; do not silently stretch.')
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill-dir', type=Path, default=ROOT)
    commands = parser.add_subparsers(dest='command', required=True)
    d = commands.add_parser('diagnose', help='Retrieve a few contextual lessons by visible symptom')
    d.add_argument('query', nargs='?'); d.add_argument('--context', type=Path)
    d.add_argument('--subject', choices=SUBJECTS)
    d.add_argument('--stage',choices=STAGES); d.add_argument('--projection',choices=PROJECTIONS)
    d.add_argument('--limit',type=int,default=3)
    commands.add_parser('coverage',help='Report exactly what was and was not reviewed')
    v = commands.add_parser('validate',help='Validate extension schema and optionally baseline IDs')
    v.add_argument('--base-techniques',type=Path)
    e = commands.add_parser('exercise',help='Write an unreviewed working brief, never fabricated evidence')
    e.add_argument('lesson_id'); e.add_argument('--output',type=Path); e.add_argument('--force',action='store_true')
    s = commands.add_parser('scale',help='Verify integer render dimensions')
    for name in ('width','height','factor'): s.add_argument(name,type=int)
    s.add_argument('--target',type=int,nargs=2,metavar=('WIDTH','HEIGHT'))
    args = parser.parse_args(argv)
    try:
        if args.command == 'scale':
            result = scale_contract(args.width,args.height,args.factor,*(args.target or (None,None)))
        else:
            catalog, registry = load_catalog(args.skill_dir)
            if args.command == 'diagnose':
                base_path = args.skill_dir / 'references/techniques.json'
                base = load_json(base_path) if base_path.exists() else None
                if base is not None:
                    validate_catalog(catalog, registry, base)
                result = diagnose(args.query,catalog,registry,stage=args.stage,projection=args.projection,
                                  subject=args.subject,context=load_json(args.context) if args.context else None,
                                  base=base,limit=args.limit)
            elif args.command == 'coverage':
                result = {'scope':registry['scope'],'review_date':registry['review_date'],
                          'counts_by_access':dict(Counter(s['access'] for s in registry['sources'])),
                          'sources':registry['sources'],'lessons':len(catalog['lessons']),
                          'media_sequences_reviewed':sum(s.get('sequences_reviewed', 0) for s in registry['sources']),'collection_completeness':'not established'}
            elif args.command == 'validate':
                base_path = args.base_techniques or args.skill_dir / 'references/techniques.json'
                result = validate_catalog(catalog,registry,load_json(base_path))
            else:
                selected = next((l for l in catalog['lessons'] if l['id']==args.lesson_id),None)
                _require(selected is not None, f'Unknown lesson: {args.lesson_id}')
                result = exercise_plan(selected,registry)
                if args.output:
                    args.output.parent.mkdir(parents=True,exist_ok=True)
                    # Exclusive creation by default; do not accidentally overwrite an observed review.
                    with args.output.open('w' if args.force else 'x',encoding='utf-8') as stream:
                        stream.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
                    result = {'output':str(args.output),'status':'draft','review':'not-reviewed'}
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(f'Tutorial bridge: {exc}',file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
