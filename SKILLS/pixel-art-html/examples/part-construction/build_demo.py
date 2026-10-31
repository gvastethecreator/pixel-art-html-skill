#!/usr/bin/env python3
"""Replay recorded examples and original failure lessons; this is not a fresh review."""
from pathlib import Path
import argparse
import html
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / 'scripts'))
import construct
import build_pixel_art as core
import compose_scene


def camera(source, output):
    """Export the recorded encounter as native parts in the existing scene viewer."""
    _, report = construct.compile_parts(source)
    output.mkdir(parents=True)
    spec = {k: source[k] for k in ('title', 'width', 'height', 'background', 'palette_budget')}
    spec.update(subtitle='Original study: supports, grips, and occlusion', caption='CONSTRUCTION BY PARTS',
                assets={}, placements=[], groups=[{'id': k, 'label': v} for k, v in
                [('ninja', 'Ninja'), ('knight', 'Knight'), ('skeleton', 'Skeleton')]])
    for depth, part in enumerate(source['parts']):
        name = part['id']
        ox, oy = report['origins'][name]
        w, h = max(8, len(part['grid'][0])), max(8, len(part['grid']))
        # Pad tiny masters without moving their visible world cells outside the scene.
        x, y = min(ox, source['width'] - w), min(oy, source['height'] - h)
        grid = [[None] * w for _ in range(h)]
        for py, row in enumerate(part['grid']):
            for px, alias in enumerate(row):
                if alias != '.':
                    grid[oy - y + py][ox - x + px] = report['palette'][alias]
        artifact = core.canonical_artifact(title=name, grid=grid, background=None,
                    source={'kind': 'construction-part', 'part': name, 'source_fingerprint': construct.digest(source)})
        core.write_artifact(artifact, output / 'masters' / name, 1)
        spec['assets'][name] = f'masters/{name}/pixel-art.json'
        placement = {'asset': name, 'x': x, 'y': y, 'depth': depth, 'subject': part.get('role') != 'environment'}
        if placement['subject']:
            placement['group'] = name.split('-')[0]
        spec['placements'].append(placement)
    construct.save(output / 'scene-source.json', spec)
    scene = compose_scene.compile_scene(spec, output)
    compose_scene.write_scene(scene, output / 'view')
    compose_scene.validate_output(output / 'view')
    expected, _ = construct.compile_parts(source)
    if compose_scene.scene_grid(scene) != expected['grid']:
        raise ValueError('Scene export changed the constructed pixels')


def lesson_gallery(output):
    lessons = construct.read(ROOT / 'lessons.json')
    output.mkdir(parents=True)
    payload = json.dumps(lessons, ensure_ascii=False).replace('<', '\\u003c')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Original repair lessons</title>
<style>body{background:#111111;color:#eeeeee;font:16px/1.5 system-ui;margin:28px;max-width:1150px}select{font:inherit;background:#1a1a1a;color:inherit;padding:8px;max-width:100%}main{display:flex;gap:50px}figure{margin:16px 0}canvas{image-rendering:pixelated;background:#222222;margin-right:20px}p{max-width:90ch}dt{font-weight:700;color:#e6c784}dd{margin:0 0 10px}small{color:#a8a8a8}</style>
<h1>Seven original failure / repair lessons</h1><p>Recorded local revisions from three studies. Includes a failed repair and a partial improvement. These are conditional lessons, not independent quality tests.</p><label for="lesson">Failure to inspect</label> <select id="lesson"></select><main></main><dl></dl><script id="lessons-data" type="application/json">PAYLOAD</script><script>
const data=JSON.parse(document.getElementById('lessons-data').textContent),pick=document.getElementById('lesson');data.lessons.forEach(l=>{let o=document.createElement('option');o.value=l.id;o.textContent=l.title;pick.append(o)});
function draw(){let l=data.lessons.find(l=>l.id===pick.value);document.querySelector('main').replaceChildren();['before','after'].forEach(k=>{let f=document.createElement('figure');let title=document.createElement('h2');title.textContent=k==='before'?'Observed problem':'Revision';f.append(title);const a=l[k];[1,4].forEach(z=>{const c=document.createElement('canvas');c.width=a.width;c.height=a.height;c.style.width=a.width*z+'px';c.style.height=a.height*z+'px';c.dataset.side=k;c.dataset.zoom=z;c.setAttribute('role','img');c.setAttribute('aria-label',`${k==='before'?'Recorded baseline':'Recorded revision'} at ${z}×`);const ctx=c.getContext('2d');ctx.imageSmoothingEnabled=false;a.grid.forEach((r,y)=>r.forEach((v,x)=>{if(v){ctx.fillStyle=v;ctx.fillRect(x,y,1,1)}}));f.append(c)});document.querySelector('main').append(f)});const dl=document.querySelector('dl');dl.replaceChildren();for(const k of ['observed','cause','intervention','preserve','limit','probe']){const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=k;dd.textContent=l[k];dl.append(dt,dd)}}pick.onchange=draw;draw();</script></html>'''
    (output / 'index.html').write_text(page.replace('PAYLOAD', payload), encoding='utf-8')
    from PIL import Image, ImageDraw, ImageColor
    for lesson in lessons['lessons']:
        a, b = lesson['before'], lesson['after']
        board = Image.new('RGB', (max(520, (a['width'] + b['width']) * 4 + 70), max(a['height'], b['height']) * 4 + 72), '#111111')
        d = ImageDraw.Draw(board)
        d.text((12, 8), lesson['id'], fill='#eeeeee')
        for x, item, label in [(12, a, 'Observed'), (max(270, a['width']*4+40), b, 'Revision')]:
            d.text((x, 28), label, fill='#e6c784')
            image = Image.new('RGBA', (item['width'], item['height']))
            image.putdata([((*ImageColor.getrgb(c), 255) if c else (0, 0, 0, 0)) for row in item['grid'] for c in row])
            board.paste(image.resize((image.width * 4, image.height * 4), Image.Resampling.NEAREST), (x, 50))
        board.save(output / (lesson['id'] + '.png'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output must be a new directory; preserve previous evidence')
    args.output.mkdir(parents=True)
    links = []
    for name in ('lighthouse', 'tree', 'encounter'):
        record = construct.read(ROOT / 'recordings' / (name + '.json'))
        previous = None
        for i, step in enumerate([*record['lineage'], {'source': record['source']}]):
            source = step['source']
            destination = args.output / name / source['stage']
            review = record['lineage'][i-1]['review'] if i else None
            construct.build(source, destination, previous, review)
            previous = destination
        links.append(f'<article><h2>{html.escape(record["source"]["title"])}</h2><img src="{name}/material/pixel-art.png" alt="{html.escape(record["source"]["title"])}"><p><a href="{name}/material/parts.html">Inspect parts</a> · <a href="{name}/block/parts.html">Block</a> · <a href="{name}/planes/parts.html">Planes</a></p></article>')
        if name == 'encounter':
            camera(record['source'], args.output / 'encounter-scene')
    lesson_gallery(args.output / 'lessons')
    (args.output / 'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><title>Recorded construction studies</title><style>body{background:#111111;color:#eeeeee;font:17px system-ui;margin:32px}a{color:#e6c784}main{display:flex;gap:32px;align-items:start}article{max-width:35%}img{image-rendering:pixelated;min-width:128px;max-width:100%;width:288px}p{max-width:85ch}</style><h1>Original construction studies</h1><p>Historical replay of actual authoring stages and self-reviews. Rebuilding these records does not create new visual evidence. All three remain drafts with documented limits.</p><p><a href="encounter-scene/view/index.html">Open encounter · pan and zoom</a> · <a href="lessons/index.html">Seven failure / repair lessons</a></p><main>''' + ''.join(links) + '</main></html>', encoding='utf-8')
    print(json.dumps({'output': str(args.output), 'replayed_studies': 3, 'lessons': 7, 'scene_parity': 'passed', 'claim': 'Historical replay, not fresh review'}))


if __name__ == '__main__':
    main()
