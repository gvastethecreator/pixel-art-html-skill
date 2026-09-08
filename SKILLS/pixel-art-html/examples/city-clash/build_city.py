"""Draw an original city skirmish from native masters; no source art is sampled."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'scripts'))
import build_pixel_art as core
import compose_scene

P = dict(i='#101923', n='#192532', s='#243444', d='#374651', m='#586466', l='#818774',
         p='#3B4D54', q='#4D5F63', h='#657575', r='#293646', t='#344C5C', u='#4D6B78',
         v='#668993', w='#654A42', x='#44333A', o='#9C6C4E', g='#E4B568', a='#FFE0A1',
         c='#327573', C='#75BAB1', R='#9E4051', H='#DF6A59', b='#B2C2BB', e='#779EA8',
         B='#E5D6AD', D='#AF987E', f='#654665')


class Art:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.ops = []

    def add(self, kind, points, color, stage=1, width=1):
        self.ops.append((kind, points, color, stage, width))

    def r(self, box, color, stage=1): self.add('rectangle', box, color, stage)
    def p(self, points, color, stage=1): self.add('polygon', points, color, stage)
    def e(self, box, color, stage=1): self.add('ellipse', box, color, stage)
    def l(self, points, color, width=1, stage=2): self.add('line', points, color, stage, width)

    def image(self, stage=2):
        image = Image.new('RGBA', (self.width, self.height))
        d = ImageDraw.Draw(image)
        for kind, points, color, level, width in self.ops:
            if level <= stage:
                fill = P[color] if color else (0, 0, 0, 0)
                if kind == 'line': d.line(points, fill=fill, width=width)
                else: getattr(d, kind)(points, fill=fill)
        return image

    def spec(self, title, stage=2):
        im = self.image(stage)
        reverse = {tuple(bytes.fromhex(color[1:])): name for name, color in P.items()}
        rows = [''.join(reverse[im.getpixel((x, y))[:3]] if im.getpixel((x, y))[3] else '.' for x in range(self.width)) for y in range(self.height)]
        used = set(''.join(rows)) - {'.'}
        return {'title': title, 'width': self.width, 'height': self.height, 'evidence_tier': 'draft', 'background': None,
                'palette': {key: value for key, value in P.items() if key in used}, 'grid': rows,
                'art_direction': {'use': 'scene master', 'projection': 'oblique town, shared verticals and shallow ground depth', 'light': 'cool upper left; warm local lanterns', 'originality': 'independent geometry and palette; no source pixels'}}


def window(c, x, y, width=10, height=14, warm=True):
    c.r((x-2,y-2,x+width+2,y+height+3),'s')
    c.r((x,y,x+width,y+height),'o' if warm else 't')
    c.r((x+1,y+1,x+width-1,y+height-1),'g' if warm else 'v',2)
    c.l([(x+width//2,y),(x+width//2,y+height)],'w',2)
    c.l([(x,y+height//2),(x+width,y+height//2)],'w')
    c.r((x-3,y+height+2,x+width+3,y+height+4),'l')


def house(kind):
    c=Art(128,112)
    c.p([(13,100),(98,100),(123,88),(121,101),(98,110),(8,110)],'n',0)
    c.p([(15,44),(91,44),(91,102),(15,102)],'m',0)
    c.p([(91,44),(115,32),(115,90),(91,102)],'d',0)
    c.r((18,48,87,98),'l')
    c.r((18,48,87,53),'d')
    for y in (67,86):
        c.r((16,y,90,y+3),'w')
    for x in (18,51,86): c.r((x,49,x+3,100),'w')
    # A long ridge, front slope, right hip, and eave share their corners.
    c.p([(7,45),(29,15),(95,15),(119,32),(95,50),(10,50)],'i',0)
    c.p([(10,44),(31,18),(95,18),(90,44)],'t')
    c.p([(95,18),(116,32),(92,44)],'r')
    c.l([(31,17),(95,17),(117,32)],'v',2)
    c.r((10,44,92,47),'u')
    for row,y in enumerate((25,32,39)):
        start=28-row*5
        c.l([(start,y),(90,y)],'u')
        for x in range(start+7+(row%2)*7,89,16): c.l([(x,y-5),(x-3,y)],'r')
    c.l([(94,44),(115,33)],'s',2)
    # Chimney grows through the roof with a recessed top.
    c.r((67,4,78,24),'d',0);c.r((67,4,70,23),'m');c.r((65,3,80,7),'l');c.r((68,3,77,4),'i')
    window(c,28,56,11,13,kind!='crypt')
    window(c,63,56,11,13,kind!='crypt')
    c.r((34,80,49,101),'w');c.r((37,82,47,101),'x');c.l([(40,84),(40,100)],'o');c.r((46,91,47,92),'g',2)
    c.p([(31,102),(50,102),(56,107),(31,107)],'h');c.l([(31,103),(49,103)],'l')
    if kind=='inn':
        c.l([(92,55),(111,55)],'w',3);c.r((101,56,112,68),'x');c.r((103,58,110,65),'o');c.r((105,59,109,62),'g',2)
        c.r((62,86,79,99),'s');c.r((65,89,76,98),'t')
        c.p([(61,78),(84,78),(91,86),(59,86)],'c');c.l([(60,86),(88,86)],'C',2)
    else:
        c.r((62,82,79,100),'t');c.l([(69,85),(69,98)],'v')
        c.p([(88,55),(88,77),(96,82),(101,75),(101,53)],'c');c.p([(90,57),(90,75),(95,78),(98,73),(98,57)],'u');c.l([(94,60),(94,72)],'g',2)
    # Quiet plaster is interrupted by a few connected chips, not uniform noise.
    for x,y in ((23,76),(72,74),(83,95),(24,93)): c.l([(x,y),(x+3,y),(x+3,y-1)],'m')
    return c


def gate():
    c=Art(128,128)
    c.p([(8,118),(110,118),(127,110),(124,127),(6,127)],'n',0)
    c.r((19,40,108,119),'d',0);c.r((24,41,100,117),'m')
    for x in (9,92):
        c.r((x,22,x+24,115),'d',0);c.r((x+2,23,x+17,112),'m');c.r((x+3,27,x+14,110),'l')
        c.r((x-3,21,x+26,27),'h')
        for xx in range(x-3,x+25,10): c.r((xx,13,xx+6,24),'m',0);c.l([(xx,13),(xx+5,13)],'l')
        for yy in (43,67,92): c.l([(x+2,yy),(x+17,yy)],'m')
        c.r((x+7,48,x+11,63),'s');c.r((x+8,49,x+9,61),'i')
    c.p([(43,118),(43,78),(48,64),(62,56),(74,61),(83,74),(83,119)],'s',0)
    c.p([(48,119),(48,79),(54,68),(63,64),(73,68),(78,80),(78,119)],'i')
    c.p([(39,78),(44,62),(61,51),(77,57),(88,76),(81,78),(72,64),(62,59),(50,67),(45,80)],'h')
    for x,y in ((42,73),(48,61),(59,54),(72,58),(81,68)): c.l([(x,y),(x+4,y+3)],'l')
    for x in (51,57,64,71,77): c.r((x,75,x+1,98),'w');c.p([(x,99),(x+2,99),(x+1,104)],'w')
    c.r((48,87,79,89),'o')
    c.r((37,42,88,47),'h');c.r((44,34,84,39),'m')
    c.p([(56,23),(72,23),(72,43),(64,50),(56,44)],'c');c.l([(63,26),(63,43)],'C',2);c.l([(59,33),(69,33)],'g',2)
    for x in (32,86):
        c.r((x,85,x+2,97),'w');c.p([(x-2,87),(x-3,81),(x,74),(x+1,81),(x+4,83),(x+3,87)],'H');c.p([(x-1,85),(x,78),(x+2,85)],'a',2)
    return c


def crypt():
    c=Art(128,104)
    c.p([(7,94),(91,94),(121,78),(121,92),(91,102),(4,102)],'n',0)
    c.p([(15,40),(87,40),(87,92),(15,92)],'d',0);c.p([(87,40),(112,26),(112,79),(87,92)],'s',0)
    c.p([(8,41),(32,10),(90,10),(117,26),(89,48),(10,48)],'s',0)
    c.p([(12,40),(34,14),(89,14),(85,41)],'m');c.p([(89,14),(113,26),(87,41)],'d')
    c.l([(34,13),(89,13),(114,26)],'h',2);c.l([(14,41),(85,41)],'h',2)
    c.p([(28,91),(28,65),(34,54),(43,49),(54,53),(61,65),(61,92)],'i')
    c.p([(23,69),(26,58),(34,48),(43,44),(55,49),(64,59),(67,71),(59,69),(53,57),(43,53),(34,59),(31,70)],'h')
    for xx in (19,68): c.r((xx,48,xx+7,92),'m');c.r((xx,48,xx+2,90),'h');c.r((xx-2,87,xx+9,92),'h')
    c.p([(28,90),(64,90),(75,102),(16,102)],'d');c.l([(24,94),(68,94)],'h');c.l([(20,98),(72,98)],'m')
    # Broken pediment and a small skull relief identify the crypt.
    c.r((54,24,63,31),'l');c.r((56,22,61,24),'l');c.r((56,31,61,34),'m');c.r((55,27,57,28),'s');c.r((60,27,62,28),'s')
    c.p([(83,14),(89,14),(87,24),(84,24),(82,33),(78,37),(79,26)],'s',2)
    c.l([(97,41),(97,55),(92,60),(94,69)],'i',2)
    c.r((33,78,34,85),'f');c.r((56,76,57,84),'f')
    return c


def market():
    c=Art(120,88)
    c.p([(5,76),(94,76),(116,65),(116,82),(96,87),(2,87)],'n',0)
    c.r((12,31,89,75),'w',0);c.r((17,36,87,69),'x')
    c.r((12,21,16,77),'o');c.r((88,15,91,78),'o')
    c.p([(6,27),(20,9),(96,9),(113,21),(91,39),(9,39)],'x',0)
    c.p([(10,26),(23,12),(95,12),(90,33),(9,33)],'R')
    for x in (25,50,75): c.p([(x,12),(x+9,12),(x+3,33),(x-7,33)],'o')
    c.l([(23,11),(95,11)],'H',2)
    for x in range(11,87,12): c.p([(x,33),(x+9,33),(x+9,39),(x+4,42),(x,39)],'R')
    c.p([(16,60),(88,60),(107,50),(34,50)],'o');c.r((16,62,89,74),'w');c.l([(17,61),(87,61)],'g',2)
    for x,y in ((29,53),(37,52),(47,53),(71,54),(77,52)): c.e((x,y,x+5,y+4),'l');c.r((x+1,y,x+3,y+1),'g',2)
    for x in (21,82): c.r((x,71,x+4,81),'x')
    c.r((94,60,108,75),'w');c.l([(94,60),(108,75)],'o');c.l([(108,60),(94,75)],'o')
    return c


def monument():
    c=Art(72,72)
    c.e((2,40,69,70),'n',0)
    c.p([(5,49),(26,37),(48,37),(66,49),(66,58),(45,69),(25,69),(5,57)],'d',0)
    c.p([(6,48),(27,37),(48,37),(65,48),(45,60),(24,60)],'h')
    c.p([(15,48),(29,40),(45,40),(55,48),(44,55),(28,55)],'s')
    c.p([(18,48),(30,43),(44,43),(51,48),(42,52),(29,52)],'c')
    c.l([(22,48),(29,50),(40,50)],'C',2)
    c.r((31,22,40,47),'d',0);c.r((31,22,34,45),'l');c.p([(27,24),(33,19),(44,19),(44,24),(36,29),(27,28)],'h')
    c.p([(34,9),(41,3),(45,8),(41,13),(43,19),(38,24),(34,20)],'m',0)
    c.l([(41,5),(37,10),(37,19)],'l',2)
    c.l([(10,53),(24,60),(45,60),(61,51)],'l',2)
    return c


def lantern():
    c=Art(16,48)
    c.e((0,42,15,47),'n',0);c.r((6,17,8,44),'x',0);c.r((6,40,10,44),'d');c.l([(6,19),(6,38)],'o')
    c.p([(4,15),(1,7),(4,3),(11,3),(14,7),(11,15)],'i',0)
    c.r((4,6,11,13),'g');c.r((5,7,9,11),'a',2);c.l([(8,5),(8,14)],'o');c.r((4,1,10,3),'d');c.r((3,14,12,16),'o')
    return c


def crate():
    c=Art(24,24);c.p([(2,10),(12,4),(22,9),(22,20),(11,24),(2,19)],'x',0)
    c.p([(3,10),(12,5),(21,9),(11,14)],'o');c.p([(3,11),(11,15),(11,22),(3,18)],'w');c.p([(12,15),(21,10),(21,19),(12,22)],'w')
    c.l([(4,12),(10,20)],'o');c.l([(4,17),(10,16)],'o');c.l([(14,15),(20,18)],'o');return c


def fighter(faction, pose):
    c=Art(40,40)
    # Native anchors; silhouettes differ before equipment and palette treatment.
    if pose=='crouch': head=(21,16);torso=(19,25);hip=(17,28);legs=[[(17,28),(10,30),(7,35)],[(20,28),(27,31),(31,34)]]
    elif pose=='leap': head=(20,8);torso=(17,17);hip=(17,23);legs=[[(16,22),(9,26),(18,29)],[(19,22),(27,25),(34,21)]]
    elif pose=='guard': head=(19,9);torso=(18,18);hip=(18,26);legs=[[(16,26),(13,31),(11,36)],[(21,26),(24,31),(28,36)]]
    elif pose=='archer': head=(18,9);torso=(17,18);hip=(16,26);legs=[[(14,26),(11,31),(9,36)],[(18,26),(22,30),(25,35)]]
    else: head=(21,10);torso=(18,19);hip=(16,26);legs=[[(15,25),(10,30),(6,35)],[(19,25),(25,29),(31,32)]]
    hx,hy=head;tx,ty=torso;px,py=hip
    near='t' if faction=='ninja' else 'e' if faction=='knight' else 'B'
    far='s' if faction=='ninja' else 'u' if faction=='knight' else 'D'
    for i,leg in enumerate(legs):
        c.l(leg,'i',5,0);c.l(leg,near if i==0 else far,3,1)
        x,y=leg[-1];c.l([(x-2,y+1),(x+3,y+1)],'i',2,0)
        if faction=='skeleton': c.r((x-2,y,x+2,y),'B',2)
    if faction=='skeleton':
        c.l([(tx,ty-3),(px,py+1)],'D',2,0)
        c.p([(tx-5,ty-3),(tx+5,ty-3),(tx+4,ty+4),(tx-3,ty+5)],'i',0)
        c.l([(tx,ty-4),(tx,ty+5)],'B',2,1)
        for yy in (ty-2,ty+1,ty+4): c.l([(tx-4,yy),(tx-2,yy+1),(tx+3,yy)],'B',1,1)
        c.l([(px-3,py),(px,py+2),(px+3,py)],'D',2,1)
    else:
        c.p([(tx-5,ty-5),(tx+4,ty-6),(tx+6,ty+2),(px+4,py+2),(px-5,py+1),(tx-6,ty+1)],'i',0)
        c.p([(tx-4,ty-4),(tx+2,ty-5),(tx+4,ty+1),(px+2,py),(px-4,py-1)],near)
        c.p([(tx+1,ty-4),(tx+4,ty-3),(tx+4,ty+2),(px+3,py),(px,py-1)],far)
        if faction=='knight':
            c.p([(tx-3,ty),(tx+3,ty),(px+3,py+4),(px-2,py+4),(px-4,py+1)],'c');c.l([(tx-2,ty+1),(px-1,py+2)],'C',2)
            c.r((tx-5,ty-5,tx-1,ty-2),'b');c.r((tx+3,ty-4,tx+6,ty-1),'u')
        c.l([(px-4,py-1),(px+3,py-1)],'w',2,2)
    # Back arm and a weapon tied to a visible hand.
    arm=[(tx-3,ty-2),(tx-8,ty+2),(tx-10,ty-2)]
    c.l(arm,'i',4,0);c.l(arm,far,2,1)
    if pose=='archer':
        c.l([(tx+3,ty-3),(tx+10,ty-3)],'i',4,0);c.l([(tx+3,ty-3),(tx+10,ty-3)],near,2,1)
        c.l([(tx+10,ty-13),(tx+15,ty-8),(tx+16,ty-3),(tx+15,ty+3),(tx+10,ty+8)],'o',2)
        c.l([(tx+10,ty-13),(tx+10,ty+8)],'D');c.l([(tx+1,ty-4),(tx+18,ty-4)],'l');c.p([(tx+18,ty-5),(tx+20,ty-4),(tx+18,ty-3)],'b')
    elif faction=='knight' and pose=='guard':
        c.p([(23,17),(34,15),(36,25),(31,32),(25,28)],'i',0);c.p([(25,18),(33,17),(34,24),(30,29),(27,26)],'c');c.l([(26,19),(29,26)],'C',2);c.r((28,19,30,24),'g',2)
        c.l([(9,20),(7,5)],'b',2);c.l([(5,19),(12,19)],'g',2)
    else:
        c.l([(tx+3,ty-3),(tx+8,ty),(tx+11,ty-3)],'i',4,0);c.l([(tx+3,ty-3),(tx+8,ty),(tx+11,ty-3)],near,2,1)
        if faction=='ninja':
            c.l([(tx+10,ty-2),(37,5 if pose!='crouch' else 14)],'i',3,0);c.l([(tx+11,ty-3),(37,5 if pose!='crouch' else 14)],'b',2);c.l([(tx+9,ty-5),(tx+13,ty-1)],'o')
        elif faction=='skeleton':
            c.l([(tx+9,ty-2),(34,6)],'D',2);c.p([(32,5),(38,5),(37,12),(33,14),(34,9)],'m');c.l([(37,6),(37,11)],'b')
        else:
            c.l([(tx+10,ty-3),(37,8)],'b',2);c.l([(tx+8,ty-5),(tx+12,ty-1)],'g',2)
    # Skull, mask and visor use distinct constructions, not a shared recolored face.
    if faction=='skeleton':
        c.p([(hx-4,hy-5),(hx+3,hy-5),(hx+5,hy-2),(hx+4,hy+3),(hx+1,hy+5),(hx-3,hy+4),(hx-5,hy)],'i',0)
        c.p([(hx-3,hy-4),(hx+3,hy-4),(hx+4,hy),(hx+2,hy+2),(hx-3,hy+2),(hx-4,hy-1)],'B');c.r((hx-2,hy+2,hx+2,hy+4),'D');c.r((hx-3,hy-1,hx-1,hy),'i',2);c.r((hx+2,hy-1,hx+3,hy),'i',2);c.r((hx,hy+1,hx,hy+2),'i',2)
        c.l([(hx-2,hy+4),(hx+2,hy+4)],'B')
    elif faction=='ninja':
        c.p([(hx-4,hy-4),(hx+2,hy-5),(hx+5,hy-2),(hx+4,hy+3),(hx,hy+5),(hx-4,hy+2)],'i',0)
        c.p([(hx-3,hy-3),(hx+2,hy-4),(hx+4,hy-1),(hx+3,hy+3),(hx-2,hy+3)],'t');c.r((hx-1,hy-1,hx+4,hy),'D');c.r((hx+2,hy-1,hx+3,hy-1),'a',2);c.r((hx-2,hy+1,hx+4,hy+3),'s')
        c.p([(hx-3,hy+4),(hx-7,hy+2),(hx-13,hy+4),(hx-17,hy+1),(hx-14,hy+8),(hx-8,hy+7),(hx-4,hy+7)],'R',1);c.l([(hx-15,hy+4),(hx-10,hy+6),(hx-5,hy+5)],'H',2)
    else:
        c.p([(hx-5,hy-3),(hx-2,hy-6),(hx+3,hy-5),(hx+5,hy-2),(hx+4,hy+4),(hx-3,hy+4)],'i',0)
        c.p([(hx-4,hy-3),(hx-1,hy-5),(hx+3,hy-4),(hx+4,hy+2),(hx,hy+4),(hx-3,hy+2)],'e');c.l([(hx-3,hy-3),(hx,hy-4),(hx+2,hy-3)],'b',2)
        c.r((hx-3,hy,hx+4,hy+1),'i',2);c.l([(hx,hy+2),(hx+1,hy+3)],'b')
        c.p([(hx-1,hy-5),(hx-3,hy-8),(hx-8,hy-7),(hx-10,hy-4),(hx-6,hy-5)],'c',1)
    return c


def ground():
    c=Art(480,320);c.r((0,0,479,319),'n',0)
    c.r((8,8,471,311),'p',0)
    # Streets frame buildings; quieter central paving carries the combat silhouettes.
    c.r((155,38,331,319),'q',0);c.r((0,140,479,218),'q',0)
    for x in (150,333): c.r((x,36,x+3,317),'h');c.r((x+4,38,x+6,319),'d')
    for y in (135,219): c.r((4,y,476,y+3),'h');c.r((5,y+4,475,y+6),'d')
    for y in range(19,319,12):
        for x in range(7+(y//12%2)*12,478,24):
            # Sparse paired cobble edges, deterministic rhythm with quiet combat zones.
            if 171<x<324 and 136<y<301: continue
            if (x//24+y//12)%3: c.l([(x,y),(min(479,x+16),y)],'d',1,1)
            if (x//24+2*y//12)%5==0: c.l([(x,y),(x,y+2)],'h',1,2)
    c.p([(183,152),(250,130),(319,160),(331,228),(272,271),(185,242),(164,193)],'p',0)
    c.p([(188,157),(250,135),(313,163),(325,225),(271,265),(190,237),(170,194)],'q')
    for points in ([(180,196),(187,210),(192,221)],[(264,145),(278,151)],[(290,245),(301,235)],[(204,240),(217,245)]): c.l(points,'h',1,2)
    # Narrow drainage channel through the western lane, with interrupted highlights.
    c.r((128,113,136,315),'s',0);c.r((130,114,134,314),'t')
    for y in (121,151,181,232,257,288): c.l([(131,y),(133,y+5)],'u')
    for y in (145,198,276): c.r((122,y,142,y+8),'w');c.l([(122,y),(142,y)],'o');c.l([(123,y+4),(140,y+4)],'x')
    for x,y in ((177,273),(285,109),(326,184),(99,183),(430,176),(301,301)):
        c.p([(x,y),(x+15,y-2),(x+24,y+2),(x+18,y+6),(x+2,y+5)],'t');c.l([(x+3,y+2),(x+14,y+1)],'u')
    # Dark border gardens and a few moss clusters belong to wall bases.
    for x,y in ((13,126),(65,132),(426,132),(337,94),(52,207),(410,305)):
        c.l([(x,y),(x+6,y-2),(x+10,y)],'c',2,1);c.l([(x+3,y-1),(x+3,y-4)],'m',1,2)
    return c


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();root=args.output
    if root.exists(): parser.error('output must be a new directory')
    root.mkdir(parents=True)
    assets={};placements=[]
    def save(name,art):
        spec=art.spec(name);folder=root/'masters'/name
        folder.mkdir(parents=True)
        (folder/'source.json').write_text(json.dumps(spec,indent=2),encoding='utf-8')
        canonical=core.compile_spec(spec);core.write_artifact(canonical,folder,1)
        if not name.startswith('ground-'):
            for stage, label in ((0, 'block'), (1, 'planes')):
                core.write_artifact(core.compile_spec(art.spec(name+' '+label,stage)),folder/'checkpoints'/label,1)
        assets[name]=f'masters/{name}/pixel-art.json'
        return name
    def put(name,x,y,depth,group=None,flip=False,subject=False):
        placements.append(dict(asset=name,x=x,y=y,depth=depth,flip_x=flip,subject=subject,**({'group':group} if group else {})))
    floor=ground()
    # The world is assembled from exact chunks; individual masters retain the 128px contract.
    for y in range(0,320,80):
        for x in range(0,480,120):
            part=Art(120,80);im=floor.image().crop((x,y,x+120,y+80))
            part.image=lambda stage=2, im=im:im
            put(save(f'ground-{x}-{y}',part),x,y,0)
    structures=[('inn',house('inn'),10,27,139),('gate',gate(),176,0,124),('guild',house('guild'),340,29,141),('market',market(),5,222,310),('crypt',crypt(),349,211,312),('fountain',monument(),212,173,238)]
    for name,art,x,y,depth in structures: put(save(name,art),x,y,depth)
    save('lantern',lantern());save('crate',crate())
    for x,y in ((158,90),(319,105),(82,159),(329,267)): put('lantern',x,y,y+46)
    for x,y in ((144,99),(27,182),(420,161),(369,183)): put('crate',x,y,y+24)
    cast=[('ninja','crouch',67,34,140,False),('ninja','leap',177,144,184,False),('ninja','lunge',277,215,254,False),('ninja','archer',106,236,275,False),
          ('knight','guard',226,119,157,False),('knight','lunge',191,156,195,True),('knight','guard',295,173,212,False),('knight','archer',193,247,286,False),
          ('skeleton','lunge',330,172,211,True),('skeleton','guard',308,211,250,True),('skeleton','archer',373,268,319,True),('skeleton','lunge',245,248,287,True)]
    shadow=Art(32,8);shadow.e((1,1,28,5),'n',0);save('foot-shadow',shadow)
    for index,(faction,pose,x,y,depth,flip) in enumerate(cast):
        if pose!='leap': put('foot-shadow',x+5,y+33,depth-1,faction)
        name=save(f'{faction}-{pose}-{index}',fighter(faction,pose));put(name,x,y,depth,faction,flip,True)
    # The scene is a frozen contact moment. Small impact clusters connect the attacks.
    impact=Art(16,16);impact.l([(2,2),(5,6)],'a',1,1);impact.l([(8,1),(8,5)],'g',1,1);impact.l([(12,4),(10,7)],'a',1,1);impact.l([(5,10),(2,12)],'H',1,1)
    save('impact',impact);put('impact',205,159,198);put('impact',324,179,215);put('impact',307,215,255)
    manifest={'title':'La plaza de las tres sombras','subtitle':'Ninjas, caballeros y esqueletos disputan la ciudad al caer la noche.','caption':'Una noche · tres bandos',
              'width':480,'height':320,'background':P['n'],'palette_budget':32,'assets':assets,'placements':placements,
              'groups':[{'id':'ninja','label':'Ninjas · 4','color':P['H']},{'id':'knight','label':'Caballeros · 4','color':P['C']},{'id':'skeleton','label':'Esqueletos · 4','color':P['B']}],
              'focus_points':[{'label':'Los tejados','x':99,'y':91,'zoom':4},{'label':'La plaza','x':254,'y':199,'zoom':4},{'label':'La cripta','x':367,'y':259,'zoom':4}]}
    (root/'scene-source.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    scene=compose_scene.compile_scene(manifest,root);compose_scene.write_scene(scene,root/'view')
    print(json.dumps({'output':str(root),'assets':len(assets),'placements':len(placements),'colors':len(scene['colors'])}))


if __name__=='__main__': main()
