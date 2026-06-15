#!/usr/bin/env python3
"""
Bake a varied ground TILEMAP from tiles-px.png into a single crisp low-res PNG.
The scene loads this as the meadow ground. A winding dirt path is laid through it.
Output internal res: 176 x 192 (11 x 12 tiles of 16px each -> we use 16px display tiles
by downscaling the 32px source tiles to 16px first for chunkier pixels).
Actually we keep tiles at 16px in the map for true low-res; source tiles are 32px so
we downscale 2x with NEAREST to keep them crisp + chunky.
"""
from PIL import Image
import random

SRC=Image.open("tiles-px.png")  # 192x32, six 32x32 tiles
TS_SRC=32
TILE=16  # final tile size in the map (chunky)
def tile(i):
    t=SRC.crop((i*TS_SRC,0,i*TS_SRC+TS_SRC,TS_SRC)).convert("RGBA")
    return t.resize((TILE,TILE),Image.NEAREST)

GRASS=tile(0); GRASS_D=tile(1); FLOW=tile(2); PEB=tile(3); DIRT=tile(4); EDGE=tile(5)
EDGE_R=EDGE.transpose(Image.FLIP_LEFT_RIGHT)

COLS=12; ROWS=13
W=COLS*TILE; H=ROWS*TILE
m=Image.new("RGBA",(W,H),(0,0,0,0))

rnd=random.Random(2026)

# 1) base grass field with sprinkled variety
grid=[[0]*COLS for _ in range(ROWS)]  # 0 grass,1 grassdark,2 flowers,3 pebbles,4 dirt
for r in range(ROWS):
    for c in range(COLS):
        x=rnd.random()
        if x<0.10: grid[r][c]=2      # flowers
        elif x<0.18: grid[r][c]=3    # pebbles
        elif x<0.42: grid[r][c]=1    # dark variant clumps
        else: grid[r][c]=0

# 2) carve a CONTINUOUS winding dirt path down the map (a clear 2-wide walkway).
# smooth wander: change direction rarely so the path reads as one connected trail.
pc=4.5
path_cells=set()
drift=0.0
for r in range(ROWS):
    drift+=rnd.uniform(-0.4,0.4); drift=max(-0.75,min(0.75,drift))
    pc+=drift; pc=max(2,min(COLS-4,pc))
    base=int(round(pc))
    # always 2 tiles wide -> a real walkable trail, never a broken patch
    for cc in (base,base+1):
        if 0<=cc<COLS:
            grid[r][cc]=4; path_cells.add((r,cc))

# 3) paint (randomly flip/rotate tiles to break visible repetition)
TM={0:GRASS,1:GRASS_D,2:FLOW,3:PEB,4:DIRT}
def variant_tile(t,seed):
    r=random.Random(seed)
    op=r.choice([0,1,2,3])
    if op==1: t=t.transpose(Image.FLIP_LEFT_RIGHT)
    elif op==2: t=t.transpose(Image.FLIP_TOP_BOTTOM)
    elif op==3: t=t.transpose(Image.ROTATE_90)
    return t
for r in range(ROWS):
    for c in range(COLS):
        base=TM[grid[r][c]]
        # keep flowers upright; flip/rotate grass+dirt for variety
        t=base if grid[r][c]==2 else variant_tile(base, r*97+c*31+grid[r][c]*7)
        m.alpha_composite(t,(c*TILE,r*TILE))

# 4) draw soft grass->dirt seam tiles on the GRASS cells that border the path.
# EDGE source = dirt on LEFT half, grass on RIGHT half (with a fuzzy seam).
# For a grass cell whose RIGHT neighbor is dirt, we want dirt creeping in from the
# right -> use EDGE_R (dirt on right). For a grass cell whose LEFT neighbor is dirt,
# use EDGE (dirt on left). This feathers the trail into the grass.
for r in range(ROWS):
    for c in range(COLS):
        if grid[r][c]==4: continue
        right_dirt = c+1<COLS and grid[r][c+1]==4
        left_dirt  = c-1>=0 and grid[r][c-1]==4
        if right_dirt:
            m.alpha_composite(EDGE_R,(c*TILE,r*TILE))
        elif left_dirt:
            m.alpha_composite(EDGE,(c*TILE,r*TILE))

m=m.convert("RGB")
m.save("ground-tilemap-px.png")
print("ground-tilemap-px.png", m.size)
# big preview
m.resize((W*5,H*5),Image.NEAREST).save("/tmp/prev_tilemap.png")
