"""New trailer scenes built from the game's art: the hero reveal (back view pan, turn, mullet flick) and the lock'n'load.
Every function takes u (seconds into the shot) and returns a 1080x1920 RGB frame."""
import math, random
import numpy as np
from PIL import Image, ImageDraw

W, H = 1080, 1920
D = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer5'
HERO = Image.open(D + '/hero_cut.png').convert('RGBA')          # 597x720, from assets/loading_bogan.jpg
TUBE = Image.open(D + '/tube_cut.png').convert('RGBA')          # 90x130, sits at (455, 355) in HERO
TUBE_AT = (455, 355)
EYES = [(328, 95), (363, 97)]                                   # in HERO pixels

def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)
def ease_out(x): x = min(1, max(0, x)); return 1 - (1 - x) ** 3

# ---- the backdrop: dark, a hot glow low behind him (he's facing the Sun), drifting embers; drawn at 1/6 then blown up for chunky pixels
def _backdrop(glow=1.0, seed=3):
    w, h = W // 6, H // 6; yy, xx = np.mgrid[0:h, 0:w]
    d = np.hypot((xx - w * 0.5) / w, (yy - h * 0.62) / h * 0.75)
    k = np.clip(1 - d * 1.9, 0, 1) ** 1.6 * glow
    bayer = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16
    k = np.floor(k * 6 + bayer[yy % 4, xx % 4]) / 6                         # dithered bands, SNES style
    col = np.stack([10 + 210 * k, 6 + 70 * k ** 1.4, 4 + 20 * k ** 2], -1)
    return Image.fromarray(col.clip(0, 255).astype('uint8')).resize((W, H), Image.NEAREST)
BACK = _backdrop(1.0); BACK_DIM = _backdrop(0.55)
rng = random.Random(9); EMBERS = [(rng.random() * W, rng.random() * H, rng.uniform(40, 140), rng.choice([6, 6, 12])) for _ in range(46)]
def embers(img, t, alpha=1.0):
    d = ImageDraw.Draw(img)
    for x0, y0, sp, s in EMBERS:
        y = (y0 - t * sp) % H; x = x0 + math.sin(t * 1.3 + y0) * 18
        c = (255, 170 + int(60 * ((y0 * 7) % 1)), 60)
        if alpha > 0.5: d.rectangle([x // 6 * 6, y // 6 * 6, x // 6 * 6 + s - 1, y // 6 * 6 + s - 1], fill=c)
    return img

# ---- from behind: a backlit silhouette of him against the blazing Sun, rimmed in orange light (a silhouette reads the same from the back)
def _silhouette():
    from art import fill_holes
    m = fill_holes(np.array(HERO)[:, ::-1, 3] > 0)     # mirrored (we're behind him), and solid
    def sh(a, dy, dx): return np.roll(np.roll(a, dy, 0), dx, 1)
    rim_hot = m & ~sh(m, 3, 0)                          # edges facing up, towards the Sun
    rim = m & (~sh(m, 0, 3) | ~sh(m, 0, -3) | ~sh(m, 2, 0) | ~sh(m, -2, 0))
    out = np.zeros(m.shape + (4,), 'uint8'); out[m] = (22, 12, 10, 255)
    out[rim] = (190, 70, 20, 255); out[rim_hot] = (255, 190, 90, 255)
    return Image.fromarray(out)
SIL = _silhouette()
def sunlit(k, cx=W // 2):
    """backdrop with a huge pixel Sun behind him that rises into frame as the camera tilts up (k 0..1)"""
    img = BACK.copy(); d = ImageDraw.Draw(img)
    cy = int(-700 + 1220 * ease(k)); p = 12
    for r, col in [(560, (120, 30, 8)), (470, (200, 70, 12)), (390, (255, 140, 30)), (320, (255, 210, 90)), (250, (255, 245, 200))]:
        for y in range(cy - r, cy + r, p):                  # chunky stepped disc, scanline by scanline
            hw = int(math.sqrt(max(0, r * r - (y - cy) ** 2)) / p) * p
            d.rectangle([cx - hw, y, cx + hw, y + p - 1], fill=col)
    return img
def hero_reveal(u):
    """0-2.25 tilt up his back, silhouetted against the Sun; 2.25-2.55 snap turn into the light; then the mullet flick"""
    x0, _, x1, _ = PORT
    if u < 2.25:
        k = ease(u / 2.25); cw = 420 - 150 * k; ch = cw * H / W                          # tilt up from his boots to his head, pushing in to the portrait framing
        cxm = 296; y0 = (720 - ch) * (1 - k)
        img = sunlit(k, int((249 - (cxm - cw / 2)) * W / cw)); embers(img, u)
        crop = SIL.crop((round(cxm - cw / 2), round(y0), round(cxm + cw / 2), round(y0 + ch))).resize((W, H), Image.NEAREST); img.paste(crop, (0, 0), crop)
        return img
    if u < 2.55:
        v = (u - 2.25) / 0.3
        if v < 0.5:
            img = sunlit(1, int((249 - 161) * W / 270)); embers(img, u)
            crop = SIL.crop((161, 0, 431, 480)).resize((W, H), Image.NEAREST); cw = max(2, int(W * (1 - v * 2)))
            crop = crop.resize((cw, H), Image.NEAREST); img.paste(crop, ((W - cw) // 2, 0), crop)
            return img
        f = portrait(u); cw = max(2, int(W * (v - 0.5) * 2)); sq = f.resize((cw, H), Image.NEAREST)
        img = BACK.copy(); embers(img, u); img.paste(sq, ((W - cw) // 2, 0))
        return Image.blend(img, Image.new('RGB', (W, H), (255, 240, 200)), 0.7 * (1 - (v - 0.5) * 2))   # light floods onto him
    return portrait(u, flick=u - 2.55)

PORT = (165, 0, 435, 480)                          # head to waist, 270x480 hero pixels at exactly 4x
def warp_head(src, ang_deg, pivot=(345, 168), reach=95):
    """bend everything above the neck by up to ang_deg, more the higher it is: the head and mullet whip round without a seam"""
    a = np.array(src); h, w = a.shape[:2]; yy, xx = np.mgrid[0:h, 0:w].astype(float)
    t = np.clip((pivot[1] - yy) / reach, 0, 1) ** 1.3 * math.radians(ang_deg)
    dx, dy = xx - pivot[0], yy - pivot[1]
    sx = pivot[0] + dx * np.cos(-t) - dy * np.sin(-t); sy = pivot[1] + dx * np.sin(-t) + dy * np.cos(-t)
    sx = np.clip(sx.round().astype(int), 0, w - 1); sy = np.clip(sy.round().astype(int), 0, h - 1)
    return Image.fromarray(a[sy, sx])
def sparkle(d, x, y, r, col=(255, 255, 230)):
    p = 6; x, y = x // p * p, y // p * p
    for i in range(-r, r + 1, p):
        a = 1 - abs(i) / (r + 1)
        if a > 0.15: d.rectangle([x + i, y, x + i + p - 1, y + p - 1], fill=col); d.rectangle([x, y + i, x + p - 1, y + i + p - 1], fill=col)
    d.rectangle([x - p, y - p, x + 2 * p - 1, y + 2 * p - 1], fill=col)
def portrait(u, flick=None, push=0.0):
    hero = HERO
    if flick is not None and 0 <= flick < 0.45:      # whip the head back and the mullet round, then settle
        f = flick / 0.45; ang = -24 * math.sin(f * math.pi) * (1 - f) + 7 * math.sin(f * math.pi * 2) * f
        hero = warp_head(HERO, ang)
    x0, y0, x1, y1 = PORT
    if flick is not None and flick > 0.45: push = min(0.06, (flick - 0.45) * 0.03)
    if push: cw, ch = (x1 - x0) * (1 - push), (y1 - y0) * (1 - push); x0, y0 = x0 + (x1 - x0 - cw) / 2, y0 + (y1 - y0 - ch) * 0.3; x1, y1 = x0 + cw, y0 + ch
    img = BACK.copy(); embers(img, u)
    crop = hero.crop((round(x0), round(y0), round(x1), round(y1))).resize((W, H), Image.NEAREST)
    img.paste(crop, (0, 0), crop)
    if flick is not None and 0.4 <= flick < 0.9:     # the glint off the mullet
        s = (flick - 0.4) / 0.5; r = int(70 * math.sin(s * math.pi)) + 6
        sx, sy = (int((292 - x0) * W / (x1 - x0)), int((112 - y0) * H / (y1 - y0)))
        sparkle(ImageDraw.Draw(img), sx, sy, r)
    return img

# ---- lock'n'load: tight shots on the hand and the tube, clacks on every cut
HAND = (440, 300, 575, 510)                        # hand + tube, 135x210 hero pixels
def _hand_layers():
    base = HERO.crop(HAND); cap_y = TUBE_AT[1] + 101                          # the ribbed cap starts here
    t = np.array(TUBE); tm = t[:, :, 3] > 0
    capmask = np.zeros((HERO.height, HERO.width), bool); capmask[TUBE_AT[1]:TUBE_AT[1] + TUBE.height, TUBE_AT[0]:TUBE_AT[0] + TUBE.width] = tm
    capmask[:cap_y, :] = False
    hm = np.array(HERO); cap = hm.copy(); cap[~capmask] = 0; body = hm.copy(); body[capmask] = 0
    return Image.fromarray(body).crop(HAND), Image.fromarray(cap).crop(HAND)
HAND_BODY, HAND_CAP = _hand_layers()
HS = 8                                             # hand shots at 8x
def _place(img, layer, cx, cy, scale=HS, angle=0, alpha=1.0):
    l = layer.resize((layer.width * scale, layer.height * scale), Image.NEAREST)
    if angle: l = l.rotate(angle, resample=Image.NEAREST, expand=True)
    if alpha < 1: l.putalpha(l.getchannel('A').point(lambda v: int(v * alpha)))
    img.paste(l, (int(cx - l.width / 2), int(cy - l.height / 2)), l)
def speedlines(img, t, vertical=True, n=14, col=(255, 230, 160)):
    d = ImageDraw.Draw(img); r = random.Random(int(t * 30))
    for _ in range(n):
        if vertical: x = r.randrange(0, W, 6); y = r.randrange(0, H); d.rectangle([x, y, x + 5, y + r.randint(120, 420)], fill=col)
        else: y = r.randrange(0, H, 6); x = r.randrange(0, W); d.rectangle([x, y, x + r.randint(160, 500), y + 5], fill=col)
def cap_flick(u):
    img = BACK_DIM.copy(); embers(img, u)
    cx, cy = W / 2 + 40, H / 2 - 60 - 30 * ease_out(u / 0.75)
    _place(img, HAND_BODY, cx, cy)
    k = ease_out(max(0, u - 0.18) / 0.2)            # thumb flicks the lid: it swings open on its hinge
    cap = HAND_CAP.copy()
    if k > 0:
        hx, hy = 99, 162                             # hinge, in HAND pixels (the back edge of the flip-top)
        cap = cap.rotate(120 * k, resample=Image.NEAREST, center=(hx, hy))
    _place(img, cap, cx, cy)
    if 0.18 <= u < 0.3: sparkle(ImageDraw.Draw(img), int(cx + (99 - 67) * HS), int(cy + (162 - 105) * HS), 50)
    return img
def squirt(u):
    img = BACK_DIM.copy(); embers(img, u)
    sq = 1 - 0.07 * math.sin(min(1, u / 0.25) * math.pi)   # the squeeze
    cx, cy = W / 2 + 40, H / 2 - 120
    body = HAND_BODY.resize((int(HAND_BODY.width * sq), HAND_BODY.height), Image.NEAREST)
    cap = HAND_CAP.rotate(120, resample=Image.NEAREST, center=(99, 162)).resize(body.size, Image.NEAREST)
    _place(img, body, cx, cy); _place(img, cap, cx, cy)
    d = ImageDraw.Draw(img); nx, ny = cx + (78 - 67) * HS, cy + (158 - 105) * HS    # the nozzle
    if u > 0.12:                                     # a rope of SPF 50+ shoots out
        s = min(1, (u - 0.12) / 0.3)
        for i in range(int(26 * s)):
            p = i / 26; x = nx + p * 520 * s + math.sin(p * 9) * 20; y = ny + p * 640 * s + (p * s) ** 2 * 200
            r = 44 * (1 - p * 0.55); d.ellipse([x - r, y - r, x + r, y + r], fill=(250, 250, 244)); d.ellipse([x - r * 0.4, y - r * 0.7, x, y - r * 0.2], fill=(255, 255, 255))
    return img
def rack(u):
    img = BACK_DIM.copy(); embers(img, u)
    pulses = [(0.08, 0.2), (0.38, 0.5)]              # CHK... CHK
    off = sum(-90 * math.sin(min(1, max(0, (u - a) / (b - a))) * math.pi) for a, b in pulses)
    moving = any(a <= u < b for a, b in pulses)
    if moving: speedlines(img, u)
    cx, cy = W / 2 + 40, H / 2 - 60 + off
    if moving:
        for g in (1, 2): _place(img, HAND_BODY, cx, cy - off * 0.35 * g, alpha=0.25)
    _place(img, HAND_BODY, cx, cy); _place(img, HAND_CAP.rotate(120, resample=Image.NEAREST, center=(99, 162)), cx, cy)
    return img
def spin(u):
    img = BACK_DIM.copy(); embers(img, u)
    k = ease_out(min(1, u / 0.55)); ang = 900 * k
    cx, cy = W / 2, H / 2 - 120 * math.sin(min(1, u / 0.55) * math.pi)
    if u < 0.55: speedlines(img, u, vertical=False, n=18)
    _place(img, TUBE, cx, cy, scale=9, angle=ang)
    if 0.55 <= u < 0.7: sparkle(ImageDraw.Draw(img), int(cx), int(cy - 420), 90)
    return img
HIP = (175, 280, 345, 582)                          # his hip and thigh: 170x302 hero pixels
POCKET_Y = 368                                      # the tube goes in behind the shorts below this line
def holster(u):
    img = BACK_DIM.copy(); embers(img, u)
    s = W / (HIP[2] - HIP[0])                        # ~6.35x
    hip = HERO.crop(HIP); front = np.array(hip); front[:POCKET_Y - HIP[1], :, 3] = 0; front = Image.fromarray(front)
    bump = 14 * math.sin(min(1, max(0, (u - 0.42) / 0.12)) * math.pi)       # the pat
    hipS = hip.resize((W, int(hip.height * s)), Image.NEAREST); frS = front.resize(hipS.size, Image.NEAREST)
    oy = int((H - hipS.height) / 2 + bump)
    img.paste(hipS, (0, oy), hipS)
    k = ease_out(min(1, u / 0.42)); ty = -500 + (POCKET_Y - HIP[1] + 40) * s * k + 520 * k     # slides down into the pocket
    tube = TUBE.resize((int(TUBE.width * 6), int(TUBE.height * 6)), Image.NEAREST).rotate(-28, resample=Image.NEAREST, expand=True)   # cap end first, label upright
    img.paste(tube, (int(W * 0.47 - tube.width / 2), int(oy + ty - tube.height / 2)), tube)
    img.paste(frS, (0, oy), frS)
    if u > 0.42:                                      # a puff of dust off the pat
        d = ImageDraw.Draw(img); p = (u - 0.42) / 0.33; r = random.Random(4)
        for _ in range(16):
            a = r.random() * math.pi * 2; dist = 60 + p * r.randint(80, 260); x = W * 0.47 + math.cos(a) * dist; y = oy + (POCKET_Y - HIP[1]) * s + math.sin(a) * dist * 0.5
            if p < 0.9: d.rectangle([x // 6 * 6, y // 6 * 6, x // 6 * 6 + 17, y // 6 * 6 + 17], fill=(200, 170, 120))
    return img
def ready_glare(u):                                  # back on his face: eyes glint
    img = portrait(u, push=0.04 + 0.03 * u)
    x0, y0, x1, y1 = PORT
    if 0.1 <= u < 0.6:
        s = (u - 0.1) / 0.5; r = int(60 * math.sin(s * math.pi)) + 6; d = ImageDraw.Draw(img)
        for ex, ey in EYES: sparkle(d, int((ex - x0) * W / (x1 - x0) * 0.96 + 20), int((ey - y0) * H / (y1 - y0) * 0.96 + 8), r)
    return img
LOCK = [(0.75, cap_flick, 'click'), (0.75, squirt, 'squirt'), (0.75, rack, 'rack'), (0.75, spin, 'spin'), (0.75, holster, 'thunk'), (0.75, ready_glare, 'shing')]
def lockload(u):
    t = 0
    for d, f, _ in LOCK:
        if u < t + d: return f(u - t)
        t += d
    return LOCK[-1][1](LOCK[-1][0])

# ================= v5: silhouette / reveal with the mullet in the wind / the tube in his hand =================
def silhouette(u, dur=2.25):
    """THIS SUMMER...: tilt up his back, silhouetted against the rising Sun"""
    return hero_reveal(min(u, dur - 0.001) * 2.25 / dur)

_HA = np.array(HERO); _hr, _hg, _hb, _ha = [_HA[:, :, i].astype(int) for i in range(4)]
_hairish = ((_hr > 95) & (_hr - _hb > 45) & (_hg < 160) & ~((_hr > 170) & (_hg > 110) & (_hb > 80))) | (_ha == 0)   # hair, or empty air
_yy, _xx = np.mgrid[0:HERO.height, 0:HERO.width].astype(float)
_face = (((_xx - 347) / 46) ** 2 + ((_yy - 112) / 62) ** 2) < 1                                                # never touch the face
_dist = np.hypot((_xx - 347) / 1.0, (_yy - 100) / 1.15)
_WIND_W = np.clip((_dist - 40) / 55, 0, 1) * (_yy < 178) * _hairish * ~_face                             # how free each pixel is to blow about
_WIND_W = np.array(Image.fromarray((_WIND_W * 255).astype('uint8')).filter(__import__('PIL.ImageFilter', fromlist=['x']).GaussianBlur(3))) / 255.0
def wind_hero(t):
    """the mullet and the spikes streaming out to the left in a gusting wind (an inverse warp, weighted so roots stay put and the face never moves)"""
    gust = 0.75 + 0.25 * math.sin(t * 2.1)
    dx = _WIND_W * (16 * gust + 8 * np.sin(t * 17 + _yy * 0.18 - _xx * 0.05))
    dy = _WIND_W * (3 * np.sin(t * 13 + _xx * 0.12))
    sx = np.clip((_xx + dx).round().astype(int), 0, HERO.width - 1); sy = np.clip((_yy + dy).round().astype(int), 0, HERO.height - 1)
    return Image.fromarray(_HA[sy, sx])
def windlines(img, t, n=10):
    d = ImageDraw.Draw(img); r = random.Random(7)
    for _ in range(n):
        y = r.randrange(0, H, 6); sp = r.uniform(1800, 3200); ln = r.randint(140, 420); x = W - ((t * sp + r.random() * W * 2) % (W * 2 + ln))
        d.rectangle([x, y, x + ln, y + 5], fill=(255, 220, 170))
def reveal(u):
    """ONE MAN: he snaps round into the light, then stands there with his mullet flapping in the wind"""
    if u < 0.3:
        v = u / 0.3
        if v < 0.5:
            img = sunlit(1, int((249 - 161) * W / 270)); embers(img, u)
            crop = SIL.crop((161, 0, 431, 480)).resize((W, H), Image.NEAREST); cw = max(2, int(W * (1 - v * 2)))
            crop = crop.resize((cw, H), Image.NEAREST); img.paste(crop, ((W - cw) // 2, 0), crop); return img
        f = wind_portrait(u); cw = max(2, int(W * (v - 0.5) * 2)); sq = f.resize((cw, H), Image.NEAREST)
        img = BACK.copy(); embers(img, u); img.paste(sq, ((W - cw) // 2, 0))
        return Image.blend(img, Image.new('RGB', (W, H), (255, 240, 200)), 0.7 * (1 - (v - 0.5) * 2))
    out = wind_portrait(u, push=min(0.08, (u - 0.3) * 0.025))
    if u < 0.5: out = Image.blend(out, Image.new('RGB', (W, H), (255, 240, 200)), 0.35 * (1 - (u - 0.3) / 0.2))
    return out
def wind_portrait(u, push=0.0):
    hero = wind_hero(u); x0, y0, x1, y1 = PORT
    if push: cw, ch = (x1 - x0) * (1 - push), (y1 - y0) * (1 - push); x0, y0 = x0 + (x1 - x0 - cw) / 2, y0 + (y1 - y0 - ch) * 0.3; x1, y1 = x0 + cw, y0 + ch
    img = BACK.copy()
    d = ImageDraw.Draw(img); r = random.Random(9)                       # embers blown sideways too
    for x0e, y0e, sp, s in EMBERS:
        x = (x0e - u * sp * 4) % W; y = y0e + math.sin(u * 2 + x0e) * 30
        d.rectangle([x // 6 * 6, y // 6 * 6, x // 6 * 6 + s - 1, y // 6 * 6 + s - 1], fill=(255, 190, 70))
    windlines(img, u, 6)
    crop = hero.crop((round(x0), round(y0), round(x1), round(y1))).resize((W, H), Image.NEAREST)
    img.paste(crop, (0, 0), crop)
    windlines(img, u + 0.37, 4)                                          # a few streaks in front of him
    return img

TUBE_SHOT = (420, 260, 580, 545)                    # forearm, hand and tube: 160x285 hero pixels
def tube_shot(u, dur=3.0):
    """ONE TUBE OF SLATHER SPF 50+: the tube in his hand, a slow push-in, a sweep of light across the label, a glint"""
    img = BACK_DIM.copy(); embers(img, u)
    k = u / dur; z = 1 + 0.12 * ease(k)
    x0, y0, x1, y1 = TUBE_SHOT; cw, ch = (x1 - x0) / z, (y1 - y0) / z; cx, cy = (x0 + x1) / 2 + 6 * k, (y0 + y1) / 2 + 30 * k
    box = (round(cx - cw / 2), round(cy - ch / 2), round(cx + cw / 2), round(cy + ch / 2))
    hero = HERO.crop(box)
    sweep = (u - 0.5) / 1.1                         # a band of light sliding across the tube
    if 0 <= sweep <= 1:
        t = np.array(TUBE)[:, :, 3] > 0; lay = np.zeros((HERO.height, HERO.width), bool)
        lay[TUBE_AT[1]:TUBE_AT[1] + TUBE.height, TUBE_AT[0]:TUBE_AT[0] + TUBE.width] = t
        band = np.abs((_xx - TUBE_AT[0]) * 0.8 - (_yy - TUBE_AT[1]) * 0.5 - (-40 + 170 * sweep)) < 9
        a = np.array(HERO).astype(int); m = lay & band
        a[m, :3] = np.minimum(255, a[m, :3] + 120); hero = Image.fromarray(a.astype('uint8')).crop(box)
    im = hero.resize((W, int(W * (box[3] - box[1]) / (box[2] - box[0]))), Image.NEAREST)
    img.paste(im, (0, (H - im.height) // 2), im)
    if 1.7 <= u < 2.4:                              # glint off the cap
        s = (u - 1.7) / 0.7; r = int(90 * math.sin(s * math.pi)) + 6
        gx = int(((TUBE_AT[0] + 80) - box[0]) * W / (box[2] - box[0])); gy = int((H - im.height) / 2 + ((TUBE_AT[1] + 112) - box[1]) * im.height / (box[3] - box[1]))
        sparkle(ImageDraw.Draw(img), gx, gy, r)
    return img
