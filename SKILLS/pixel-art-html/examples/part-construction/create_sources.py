"""Reproduce original construction studies. Reference pixels are not inputs."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from PIL import Image, ImageDraw

SKILL = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL / 'scripts'))
import construct

PALETTE = dict(i='#101923', s='#263946', d='#3E5260', m='#65776E', l='#9BAB9E',
               h='#E6EDCC', g='#E4B568', b='#DDD5AA', t='#327573', c='#719FA9',
               r='#9E4051', R='#5E3346', w='#805A48', f='#C8846E', q='#34454C')


class Drawing:
    def __init__(self, title, size, intent, budget=16):
        self.source = dict(kind='construction', schema_version=1, stage='block', title=title,
                           width=size[0], height=size[1], intent=intent, light='Upper left; warm beacon only in the lighthouse',
                           background='#17232C', palette_budget=budget, palette=PALETTE.copy(), parts=[], constraints=[])
        self.world_origins = {}

    def shape(self, name, points, color, *, anchors=None, parent=None, holes=()):
        x0,y0 = min(p[0] for p in points),min(p[1] for p in points)
        x1,y1 = max(p[0] for p in points),max(p[1] for p in points)
        im=Image.new('L',(x1-x0+1,y1-y0+1)); d=ImageDraw.Draw(im)
        d.polygon([(x-x0,y-y0) for x,y in points], fill=1)
        for box in holes: d.rectangle((box[0]-x0,box[1]-y0,box[2]-x0,box[3]-y0),fill=0)
        rows=[''.join(color if im.getpixel((x,y)) else '.' for x in range(im.width)) for y in range(im.height)]
        origin=[x0,y0]
        if parent:
            px,py=self.world_origins[parent];origin=[x0-px,y0-py]
        p={'id':name,'origin':origin,'grid':rows,'anchors':{k:[p[0]-x0,p[1]-y0] for k,p in (anchors or {}).items()}}
        if parent:p['parent']=parent
        self.source['parts'].append(p);self.world_origins[name]=[x0,y0]
        return p

    def visible(self, name, minimum):
        self.source['constraints'].append(dict(id=name+' remains visible',kind='visible',part=name,min_cells=minimum))

    def attach(self, aid, a, b):
        self.source['constraints'].append(dict(id=aid,kind='anchor',a=a,b=b,max_distance=0))


def lighthouse():
    c=Drawing('El faro del espolón',(16,16),'A slender sea lighthouse rises from a broken rock shelf; the small lantern is its brightest cue',8)
    c.shape('sea',[(0,12),(15,12),(15,15),(0,15)],'s')
    c.shape('rock',[(2,15),(3,13),(6,12),(11,12),(14,15)],'d')
    for p in c.source['parts']:p['role']='environment'
    c.shape('tower',[(7,4),(9,4),(10,13),(6,13)],'m',anchors={'lantern-seat':[8,4]})
    c.shape('lantern',[(7,3),(9,3),(9,4),(7,4)],'g',anchors={'base':[8,4]},parent='tower')
    c.shape('cap',[(7,2),(8,1),(9,2)],'d',parent='tower')
    c.shape('gallery',[(6,5),(10,5)],'d',parent='tower')
    c.attach('lantern seats on tower',['tower','lantern-seat'],['lantern','base'])
    c.visible('tower',16);c.visible('lantern',5)
    return c


def tree():
    c=Drawing('El árbol del viento',(32,32),'One wind-shaped crown leans right over a bent trunk; unequal overlapping lobes remain one canopy',9)
    c.shape('trunk',[(11,29),(15,25),(16,17),(12,13),(15,13),(18,17),(20,12),(22,11),(21,17),(18,23),(19,28),(24,30),(18,30),(16,28),(14,30)],'w')
    c.shape('rear-crown',[(2,16),(4,12),(7,10),(12,10),(16,13),(16,18),(13,22),(7,23),(3,20)],'s')
    c.shape('main-crown',[(7,13),(9,9),(11,8),(12,5),(17,2),(24,3),(28,7),(30,12),(28,17),(24,20),(17,21),(12,19),(9,18)],'t',holes=[(16,19,18,21)])
    c.shape('front-crown',[(2,19),(4,16),(9,15),(13,17),(14,20),(12,23),(8,24),(3,22)],'t')
    c.visible('trunk',35);c.visible('rear-crown',20)
    c.source['constraints'].append(dict(id='trunk opening',kind='clear',region=[16,21,2,3],parts=['main-crown','front-crown']))
    return c


def encounter():
    c=Drawing('La emboscada del puente',(96,80),'A low ninja attacks a braced knight while a skeleton thrusts from the other side; three opposing gestures share a narrow street',16)
    c.shape('street',[(0,20),(95,4),(95,74),(67,79),(0,79)],'q')
    c.shape('back-ledge',[(0,17),(95,0),(95,7),(0,25)],'s')
    c.shape('front-ledge',[(29,79),(95,67),(95,74),(68,79)],'s')
    for p in c.source['parts']:p['role']='environment'
    c.shape('ninja-rear-leg',[(20,43),(20,47),(13,53),(7,53),(6,51),(12,49),(15,43)],'R')
    c.shape('ninja-front-leg',[(24,42),(28,45),(30,52),(35,54),(34,56),(27,55),(23,47),(20,45)],'R')
    c.shape('ninja-body',[(16,43),(19,35),(25,31),(29,34),(26,41),(24,46)],'R')
    c.shape('ninja-scarf',[(23,33),(18,34),(12,31),(7,32),(4,29),(13,28),(20,31)],'r',parent='ninja-body')
    c.shape('ninja-head',[(23,27),(26,25),(31,27),(32,30),(29,34),(24,33)],'R',parent='ninja-body')
    c.shape('ninja-arm',[(26,35),(30,34),(33,31),(36,32),(33,37),(28,39)],'R',anchors={'grip':[35,32]},parent='ninja-body')
    c.shape('ninja-blade',[(35,32),(39,29),(46,26),(42,30),(36,33)],'c',anchors={'grip':[35,32]},parent='ninja-arm')
    c.shape('knight-far-leg',[(55,42),(61,46),(61,54),(66,57),(64,59),(57,57),(55,49),(52,46)],'d')
    c.shape('knight-near-leg',[(50,43),(55,45),(52,51),(47,57),(41,58),(40,56),(45,54),(47,47)],'d')
    c.shape('knight-body',[(49,33),(54,31),(59,35),(59,45),(55,48),(47,43),(46,36)],'t')
    c.shape('knight-head',[(50,24),(55,22),(59,25),(59,29),(55,34),(50,32),(48,27)],'d',parent='knight-body')
    c.shape('knight-shield-arm',[(49,35),(45,33),(41,34),(42,39),(48,40)],'d',parent='knight-body')
    c.shape('knight-shield',[(44,28),(49,32),(47,40),(42,44),(37,40),(39,32)],'t',parent='knight-shield-arm',anchors={'impact':[46,28]})
    c.shape('knight-sword-arm',[(58,37),(63,37),(66,41),(65,44),(61,41),(57,40)],'d',anchors={'grip':[65,42]},parent='knight-body')
    c.shape('knight-sword',[(65,42),(75,43),(79,45),(73,45),(65,43)],'c',anchors={'grip':[65,42]},parent='knight-sword-arm')
    c.shape('skeleton-far-leg',[(80,54),(86,57),(88,63),(92,64),(92,66),(86,66),(83,59),(78,58)],'m',anchors={'sole':[91,66]})
    c.shape('skeleton-near-leg',[(78,54),(79,57),(75,63),(76,68),(73,69),(71,66),(72,61),(75,56)],'b',anchors={'sole':[73,69]})
    c.shape('skeleton-spine',[(78,44),(80,45),(81,53),(79,57),(76,56),(78,52)],'b')
    c.shape('skeleton-ribs',[(77,43),(83,46),(84,51),(80,54),(75,51),(75,47)],'b',holes=[(77,47,80,48),(78,51,79,51)],parent='skeleton-spine')
    c.shape('skeleton-head',[(74,37),(78,35),(82,38),(81,43),(78,45),(74,42)],'b',parent='skeleton-spine')
    c.shape('skeleton-arm',[(77,45),(74,47),(70,44),(70,40),(72,39),(73,43)],'b',anchors={'grip':[71,40]},parent='skeleton-spine')
    c.shape('skeleton-spear',[(71,40),(61,30),(62,29),(72,40),(84,52),(83,53)],'w',anchors={'grip':[71,40]},parent='skeleton-arm')
    for a,b in [('ninja-arm','ninja-blade'),('knight-sword-arm','knight-sword'),('skeleton-arm','skeleton-spear')]:
        c.attach(b+' stays in grip',[a,'grip'],[b,'grip'])
    for name in ['ninja-head','knight-head','knight-shield','skeleton-head','skeleton-ribs']:c.visible(name,12)
    for name in ['skeleton-far-leg','skeleton-near-leg']:
        c.source['constraints'].append(dict(id=name+' stands on bridge',kind='inside',at=[name,'sole'],container='street',exclude=['front-ledge']))
    return c


def planes(source):
    """Paint authored surface regions inside the reviewed masks."""
    source=json.loads(json.dumps(source));source['stage']='planes'
    _,report=construct.compile_parts(source)
    parts={p['id']:p for p in source['parts']}
    def paint(name,points,color):
        p=parts[name];ox,oy=report['origins'][name]
        mask=Image.new('L',(len(p['grid'][0]),len(p['grid'])));d=ImageDraw.Draw(mask)
        if len(points)==1:d.point((points[0][0]-ox,points[0][1]-oy),fill=1)
        else:d.polygon([(x-ox,y-oy) for x,y in points],fill=1)
        p['grid']=[''.join(color if c!='.' and mask.getpixel((x,y)) else c for x,c in enumerate(row)) for y,row in enumerate(p['grid'])]
    def fill(name,color):
        p=parts[name];p['grid']=[''.join('.' if c=='.' else color for c in row) for row in p['grid']]
    if 'tower' in parts:
        paint('tower',[(7,5),(8,5),(8,12),(6,13)],'l')
        paint('tower',[(9,6),(10,13),(9,13)],'d')
        paint('tower',[(8,10),(8,11)],'i')
        paint('rock',[(3,13),(9,12),(11,12),(7,14)],'m')
        paint('cap',[(7,2),(8,1)],'m')
    elif 'main-crown' in parts:
        source['palette'].update(s='#234837',t='#3C7154',m='#73935A',l='#A9B875')
        paint('main-crown',[(27,8),(30,12),(28,17),(24,20),(17,21),(18,18),(23,17),(25,14)],'s')
        paint('main-crown',[(10,11),(14,6),(19,4),(24,5),(27,9),(24,10),(21,8),(17,9),(16,13),(12,14)],'m')
        paint('main-crown',[(15,7),(18,5),(23,6),(23,8),(20,8),(18,7),(17,9),(14,10)],'l')
        paint('front-crown',[(3,18),(6,16),(10,17),(12,19),(8,20),(4,20)],'m')
        paint('trunk',[(18,17),(22,12),(19,25),(19,28),(24,30),(18,30),(16,27)],'R')
        paint('trunk',[(16,20),(17,20),(16,27),(12,29),(11,29),(15,25)],'f')
    else:
        source['palette']['q']='#24343B'
        for name in ('ninja-rear-leg','ninja-front-leg','ninja-body','ninja-arm'):fill(name,'R')
        paint('ninja-rear-leg',[(15,44),(19,44),(15,49),(8,52),(6,51),(12,49)],'r')
        paint('ninja-front-leg',[(23,43),(26,45),(29,52),(28,53),(24,48)],'r')
        paint('ninja-body',[(20,35),(25,32),(27,35),(24,40),(17,43)],'r')
        paint('ninja-arm',[(27,35),(30,35),(34,32),(35,33),(31,37),(28,37)],'r')
        fill('ninja-head','i');paint('ninja-head',[(24,27),(27,26),(30,28),(26,30),(24,30)],'R')
        paint('ninja-head',[(28,29),(31,29)],'f')
        paint('ninja-head',[(24,31),(31,31)],'r')
        paint('ninja-blade',[(36,32),(46,26),(42,28)],'h')
        paint('ninja-scarf',[(5,29),(13,29),(18,32),(16,33),(11,30)],'f')
        paint('knight-body',[(49,34),(54,33),(56,36),(54,41),(49,40)],'c')
        paint('knight-body',[(54,42),(58,40),(58,46),(54,47),(48,43)],'s')
        paint('knight-head',[(50,25),(55,23),(57,25),(55,29),(50,30),(49,27)],'c')
        paint('knight-head',[(50,28),(57,27),(57,29),(51,30)],'i')
        paint('knight-head',[(51,24),(55,23),(56,24),(51,25)],'h')
        paint('knight-shield',[(40,32),(44,29),(46,31),(44,39),(41,42),(38,39)],'c')
        paint('knight-shield',[(41,33),(44,31),(46,33),(44,39),(41,41),(39,38)],'t')
        paint('knight-near-leg',[(49,46),(52,47),(49,53),(44,56),(41,56),(47,53)],'c')
        paint('knight-far-leg',[(58,46),(60,47),(60,53),(58,54)],'m')
        paint('knight-sword-arm',[(59,38),(62,38),(65,42),(63,42),(61,40)],'c')
        paint('knight-sword',[(66,42),(75,43),(78,44),(72,43)],'h')
        for name in ('skeleton-far-leg','skeleton-spine'):paint(name,[(79,43),(93,60),(93,70),(80,65)],'m')
        paint('skeleton-head',[(74,37),(78,36),(80,38),(78,40),(75,40)],'h')
        paint('skeleton-head',[(80,39),(81,40),(78,44),(78,42)],'m')
        paint('skeleton-head',[(75,39),(76,39),(76,40),(75,40)],'i')
        paint('skeleton-head',[(78,40)],'i')
        paint('skeleton-head',[(76,43),(78,43)],'i')
        paint('skeleton-ribs',[(81,47),(83,47),(83,50),(79,53),(79,52),(82,49)],'m')
        paint('skeleton-arm',[(71,42),(74,46)],'h')
        paint('skeleton-spear',[(61,30),(62,29),(66,34),(65,34)],'c')
        paint('back-ledge',[(0,17),(95,0),(95,2),(0,19)],'d')
        paint('front-ledge',[(29,79),(95,67),(95,69),(40,79)],'d')
    construct.compile_parts(source)
    return source


def material(source):
    source=json.loads(json.dumps(source));source['stage']='material'
    _,report=construct.compile_parts(source);parts={p['id']:p for p in source['parts']}
    def paint(name,points,color):
        p=parts[name];ox,oy=report['origins'][name]
        mask=Image.new('L',(len(p['grid'][0]),len(p['grid'])));d=ImageDraw.Draw(mask)
        if len(points)==1:d.point((points[0][0]-ox,points[0][1]-oy),fill=1)
        else:d.polygon([(x-ox,y-oy) for x,y in points],fill=1)
        p['grid']=[''.join(color if c!='.' and mask.getpixel((x,y)) else c for x,c in enumerate(row)) for y,row in enumerate(p['grid'])]
    if 'tower' in parts:
        paint('lantern',[(7,4)],'d');paint('lantern',[(9,4)],'d')
        paint('tower',[(9,12),(10,12)],'s')
        paint('sea',[(0,13),(2,13)],'d');paint('sea',[(12,13),(14,13)],'d')
        paint('sea',[(1,15),(3,15)],'m');paint('sea',[(13,15),(15,15)],'m')
        paint('rock',[(5,14),(6,13),(8,13)],'d')
    elif 'main-crown' in parts:
        # Short leaf clusters follow the large turning planes and leave quiet shadow.
        for points in [[(16,7),(18,6),(18,7)],[(20,7),(21,6),(22,7)],[(13,11),(15,9),(15,11)],[(23,8),(25,8),(24,9)]]:paint('main-crown',points,'l')
        for points in [[(18,8),(19,7),(20,8)],[(22,6),(23,6),(23,7)],[(15,12),(17,11),(17,12)],[(19,13),(21,12),(22,13)],[(24,14),(25,13),(26,14)],[(17,16),(19,15),(19,16)]]:paint('main-crown',points,'m')
        for points in [[(27,11),(28,12),(27,13)],[(23,18),(24,17),(25,17)],[(12,17),(14,18),(14,19)]]:paint('main-crown',points,'s')
        paint('front-crown',[(4,18),(6,17),(7,18)],'l')
        paint('front-crown',[(9,18),(10,19)],'t')
        paint('front-crown',[(5,21),(7,21),(8,22)],'s')
        paint('trunk',[(16,23),(17,24),(16,26)],'w')
        paint('trunk',[(17,28),(20,29)],'w')
    else:
        paint('ninja-body',[(20,39),(24,38),(24,39),(18,42)],'i')
        paint('ninja-body',[(24,34),(26,34),(24,36)],'f')
        paint('ninja-head',[(30,29)],'h')
        paint('ninja-arm',[(33,33),(35,32),(35,33)],'f')
        paint('ninja-front-leg',[(29,53),(34,55)],'i')
        paint('ninja-rear-leg',[(7,52),(10,52)],'i')
        paint('knight-head',[(54,28),(54,30)],'c')
        paint('knight-body',[(49,35),(51,34)],'h')
        paint('knight-body',[(50,43),(54,45)],'t')
        paint('knight-shield',[(43,33),(43,38)],'g')
        paint('knight-shield',[(41,35),(45,35)],'g')
        paint('knight-shield',[(40,31),(42,30)],'h')
        paint('knight-near-leg',[(48,49),(50,48)],'h')
        paint('knight-near-leg',[(42,56),(45,56)],'l')
        paint('knight-far-leg',[(61,56),(64,57)],'l')
        paint('skeleton-ribs',[(77,45),(80,46)],'h')
        paint('skeleton-ribs',[(76,49),(77,50)],'m')
        paint('skeleton-head',[(75,42)],'m')
        paint('skeleton-head',[(77,43)],'b')
        paint('skeleton-near-leg',[(74,62),(75,63)],'m')
        paint('skeleton-spear',[(69,37),(70,39)],'g')
        for x,y in [(10,17),(29,13),(48,10),(74,5)]:paint('back-ledge',[(x,y),(x+1,y+4)],'i')
        for x,y in [(49,76),(66,73),(83,70)]:paint('front-ledge',[(x,y),(x+1,y+4)],'i')
        paint('street',[(13,60),(18,58),(23,59),(19,61),(14,62)],'s')
        paint('street',[(46,20),(51,18),(57,18),(54,20)],'s')
    construct.compile_parts(source)
    return source


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--stage',choices=['block','planes','material'],default='block')
    parser.add_argument('--base',type=Path,help='Directory containing the observed preceding sources')
    args=parser.parse_args()
    if args.output.exists():raise SystemExit('Use a new source directory')
    args.output.mkdir(parents=True)
    for name,fn in [('lighthouse',lighthouse),('tree',tree),('encounter',encounter)]:
        if args.stage!='block':
            if args.base is None:raise SystemExit('A later pass requires the observed preceding source directory via --base')
            base=construct.read(args.base/(name+'.json'))
            expected='block' if args.stage=='planes' else 'planes'
            if base['stage']!=expected:raise SystemExit('The source stage does not precede the requested pass')
            s=(planes if args.stage=='planes' else material)(base)
        else:s=fn().source
        construct.compile_parts(s)
        construct.save(args.output/(name+'.json'),s)
    print(args.output)


if __name__=='__main__':main()
