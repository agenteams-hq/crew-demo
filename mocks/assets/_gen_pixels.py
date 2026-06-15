#!/usr/bin/env python3
"""
Hand-authored crisp pixel-art asset generator for the Crew meadow scene.
Everything is drawn on a true low-res pixel grid (no AI blur, no smoothing).
Outputs:
  tiles-px.png        : 6-tile ground tileset spritesheet (each tile 32x32)
  prop-mailbox-px.png : Inbox space
  prop-calendar-px.png: Calendar space
  prop-coin-px.png    : Payments space
  prop-sign-px.png    : Booking space
  prop-shelf-px.png   : Research bookshelf space
All props isolated on transparent bg.
"""
from PIL import Image
import random

# ---- palette (vivid Grab-green family + warm earthy props) ----
# grass
G_DK  = (54,138,58)    # deep grass shadow
G_MD  = (74,176,58)    # base lush green (pops)
G_LT  = (108,206,80)   # highlight grass
G_LT2 = (138,222,104)  # brightest blades
# dirt
D_DK  = (120,86,52)
D_MD  = (158,116,70)
D_LT  = (186,146,94)
# accents
FLOW_Y = (248,216,72)
FLOW_W = (250,250,238)
FLOW_C = (252,140,170)
PEB    = (150,150,150)
PEB_LT = (190,190,190)
# wood / props
W_DK = (120,78,44)
W_MD = (158,108,60)
W_LT = (196,148,92)
PAPER= (244,238,222)
INK  = (60,52,40)
RED  = (214,72,58)
COIN = (244,200,72)
COIN_D=(204,156,40)
GREEN= (0,177,79)
BLUE = (90,150,210)
BOOK1=(196,72,64); BOOK2=(72,128,196); BOOK3=(80,170,96); BOOK4=(214,170,72)
BLACK=(36,30,24)

def newimg(w,h):
    return Image.new("RGBA",(w,h),(0,0,0,0))

def px(im,x,y,c):
    if 0<=x<im.width and 0<=y<im.height:
        if len(c)==3: c=c+(255,)
        im.putpixel((x,y),c)

def rect(im,x0,y0,x1,y1,c):
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            px(im,x,y,c)

# ---------------- GROUND TILE GENERATORS (32x32 each) ----------------
TS=32
def base_grass(seed, variant=0):
    """A seamless-ish 32x32 grass tile with subtle texture + tiny blades."""
    rnd=random.Random(seed)
    im=Image.new("RGBA",(TS,TS),G_MD+(255,))
    # mottled patches of light/dark for organic variety
    for _ in range(34):
        x=rnd.randint(0,TS-1); y=rnd.randint(0,TS-1)
        c=rnd.choice([G_DK,G_LT,G_MD,G_MD,G_LT])
        # small 1-2px clusters
        px(im,x,y,c)
        if rnd.random()<0.5: px(im,(x+1)%TS,y,c)
        if rnd.random()<0.35: px(im,x,(y+1)%TS,c)
    # upright blade highlights (little grass tufts)
    for _ in range(10+variant*4):
        x=rnd.randint(1,TS-2); y=rnd.randint(3,TS-2)
        px(im,x,y,G_LT2); px(im,x,y-1,G_LT2)
        if rnd.random()<0.5: px(im,x,y-2,G_LT)
    # darker base specks for depth
    for _ in range(14):
        x=rnd.randint(0,TS-1); y=rnd.randint(0,TS-1)
        px(im,x,y,G_DK)
    return im

def grass_flowers(seed):
    im=base_grass(seed,1)
    rnd=random.Random(seed+99)
    spots=[(6,8),(20,5),(13,20),(25,22),(9,26)]
    cols=[FLOW_Y,FLOW_W,FLOW_C,FLOW_Y,FLOW_W]
    for (fx,fy),fc in zip(spots,cols):
        # 5-petal tiny flower: center + 4 around
        px(im,fx,fy,fc); px(im,fx-1,fy,fc); px(im,fx+1,fy,fc)
        px(im,fx,fy-1,fc); px(im,fx,fy+1,fc)
        px(im,fx,fy,(252,236,140))  # bright center
    return im

def grass_pebbles(seed):
    im=base_grass(seed,0)
    rnd=random.Random(seed+33)
    for _ in range(6):
        x=rnd.randint(3,TS-4); y=rnd.randint(3,TS-4)
        rect(im,x,y,x+1,y+1,PEB)
        px(im,x,y,PEB_LT)
    return im

def dirt_path(seed):
    """Dirt tile (full dirt) - used for path center."""
    rnd=random.Random(seed)
    im=Image.new("RGBA",(TS,TS),D_MD+(255,))
    for _ in range(46):
        x=rnd.randint(0,TS-1); y=rnd.randint(0,TS-1)
        px(im,x,y,rnd.choice([D_DK,D_LT,D_MD,D_LT]))
    # a few embedded pebbles
    for _ in range(5):
        x=rnd.randint(2,TS-3); y=rnd.randint(2,TS-3)
        px(im,x,y,PEB); px(im,x+1,y,PEB_LT)
    return im

def dirt_edge(seed):
    """Grass-to-dirt edge tile: dirt on the left, grass on the right, fuzzy seam."""
    rnd=random.Random(seed)
    im=base_grass(seed,0)
    dirt=dirt_path(seed+7)
    for y in range(TS):
        # wavy seam around x=16
        seam=16+rnd.randint(-2,2)
        for x in range(0,seam):
            im.putpixel((x,y),dirt.getpixel((x,y)))
        # speckle the seam
        px(im,seam,y,rnd.choice([D_LT,G_DK]))
    return im

# build tileset sheet: [grass, grass-dark-variant, flowers, pebbles, dirt, edge]
def grass_variant(seed):
    # darker, denser variant
    im=base_grass(seed,2)
    # overlay a faint darker wash
    rnd=random.Random(seed+5)
    for _ in range(40):
        x=rnd.randint(0,TS-1); y=rnd.randint(0,TS-1)
        px(im,x,y,G_DK)
    return im

tiles=[
    base_grass(101),
    grass_variant(202),
    grass_flowers(303),
    grass_pebbles(404),
    dirt_path(505),
    dirt_edge(606),
]
sheet=Image.new("RGBA",(TS*len(tiles),TS),(0,0,0,0))
for i,t in enumerate(tiles):
    sheet.paste(t,(i*TS,0))
sheet.save("tiles-px.png")
print("tiles-px.png", sheet.size, len(tiles),"tiles")

# ---------------- CAPABILITY PROPS (transparent, ~40-44px tall) ----------------
def shadow_oval(im,cx,cy,rw,rh):
    for y in range(-rh,rh+1):
        for x in range(-rw,rw+1):
            if (x*x)/(rw*rw+0.01)+(y*y)/(rh*rh+0.01)<=1.0:
                px(im,cx+x,cy+y,(20,38,12,70))

# MAILBOX (inbox)
def mailbox():
    im=newimg(40,44)
    sh=newimg(40,44); shadow_oval(sh,20,40,11,4); im.alpha_composite(sh)
    # post
    rect(im,18,26,21,40,W_DK)
    rect(im,18,26,18,40,W_MD)
    # box body (rounded-ish)
    rect(im,10,12,30,26,GREEN)
    rect(im,10,12,30,13,(60,200,110))  # top highlight
    rect(im,10,25,30,26,(0,140,62))    # bottom shade
    # rounded top corners
    px(im,10,12,(0,0,0,0)); px(im,30,12,(0,0,0,0))
    # door
    rect(im,12,16,22,24,(244,238,222))
    rect(im,12,16,22,16,(210,204,190))
    px(im,21,20,INK)  # knob
    # red flag up
    rect(im,29,13,29,22,(120,78,44))
    rect(im,30,13,34,17,RED)
    rect(im,30,13,34,13,(240,120,108))
    # outline darken
    return im

# CALENDAR notice board
def calendar():
    im=newimg(40,46)
    sh=newimg(40,46); shadow_oval(sh,20,42,12,4); im.alpha_composite(sh)
    # two posts
    rect(im,9,24,11,42,W_DK); rect(im,28,24,30,42,W_DK)
    rect(im,9,24,9,42,W_MD); rect(im,28,24,28,42,W_MD)
    # board frame
    rect(im,7,6,33,26,W_MD)
    rect(im,7,6,33,7,W_LT)
    rect(im,7,25,33,26,W_DK)
    # paper
    rect(im,10,9,30,23,PAPER)
    # header bar
    rect(im,10,9,30,12,RED)
    # grid dots (calendar days)
    for ry in range(15,23,3):
        for rx in range(12,30,4):
            px(im,rx,ry,INK)
    return im

# COIN STAND (payments)
def coin_stand():
    im=newimg(40,44)
    sh=newimg(40,44); shadow_oval(sh,20,40,12,4); im.alpha_composite(sh)
    # little counter/stall base
    rect(im,8,28,32,40,W_MD)
    rect(im,8,28,32,29,W_LT)
    rect(im,8,39,32,40,W_DK)
    rect(im,8,28,9,40,W_DK)
    # stack of coins on top
    for i,yy in enumerate(range(24,30,2)):
        rect(im,14,yy,22,yy+1,COIN_D)
        rect(im,14,yy,22,yy,COIN)
    # big coin floating with $ - the icon
    cx,cy=26,16
    for y in range(-6,7):
        for x in range(-6,7):
            if x*x+y*y<=36: px(im,cx+x,cy+y,COIN)
            if 30<=x*x+y*y<=36: px(im,cx+x,cy+y,COIN_D)
    # $ glyph
    rect(im,cx-1,cy-4,cx,cy+4,COIN_D)
    rect(im,cx-3,cy-2,cx+2,cy-2,COIN_D)
    rect(im,cx-3,cy+2,cx+2,cy+2,COIN_D)
    return im

# SIGNPOST (booking)
def signpost():
    im=newimg(40,46)
    sh=newimg(40,46); shadow_oval(sh,20,42,8,4); im.alpha_composite(sh)
    # post
    rect(im,18,12,22,42,W_DK)
    rect(im,18,12,19,42,W_MD)
    # two directional arrow signs
    # top sign pointing right
    rect(im,8,14,28,21,GREEN)
    rect(im,8,14,28,15,(60,200,110))
    # arrow tip
    for i in range(4):
        rect(im,28+i,15+i,28+i,20-i,GREEN)
    rect(im,12,17,24,18,PAPER)  # text line
    # bottom sign pointing left
    rect(im,12,24,32,31,BLUE)
    rect(im,12,24,32,25,(140,190,235))
    for i in range(4):
        rect(im,12-i,25+i,12-i,30-i,BLUE)
    rect(im,16,27,28,28,PAPER)
    return im

# BOOKSHELF (research)
def bookshelf():
    im=newimg(42,44)
    sh=newimg(42,44); shadow_oval(sh,21,40,13,4); im.alpha_composite(sh)
    # cabinet
    rect(im,6,8,36,40,W_DK)
    rect(im,6,8,36,9,W_LT)
    rect(im,7,9,35,39,W_MD)
    # two shelves
    rect(im,7,22,35,23,W_DK)
    rect(im,7,38,35,39,W_DK)
    # books row 1
    bx=9; cols=[BOOK1,BOOK2,BOOK3,BOOK4,BOOK1,BOOK2]
    for i,c in enumerate(cols):
        h=random.Random(i).randint(9,11)
        rect(im,bx,22-h,bx+3,21,c)
        rect(im,bx,22-h,bx,21,(255,255,255,90))
        bx+=4
        if bx>33: break
    # books row 2
    bx=9
    for i,c in enumerate([BOOK3,BOOK4,BOOK1,BOOK2,BOOK4,BOOK3]):
        h=random.Random(i+9).randint(9,12)
        rect(im,bx,38-h,bx+3,37,c)
        bx+=4
        if bx>33: break
    return im

props={
 "prop-mailbox-px.png":mailbox(),
 "prop-calendar-px.png":calendar(),
 "prop-coin-px.png":coin_stand(),
 "prop-sign-px.png":signpost(),
 "prop-shelf-px.png":bookshelf(),
}
for name,im in props.items():
    im.save(name); print(name, im.size)
print("done")
