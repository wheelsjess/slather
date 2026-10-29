"""Sun Fighter trailer v5, vertical 9:16: beach, the Sun rising, its eyes heating up, his silhouette against the Sun,
a reveal with his mullet in the wind, the tube in his hand, ONE FIGHT TO THE DEATH, a rapid-fire montage, darkness, then the title slams in."""
import bisect, json, subprocess, sys, wave
import numpy as np
from PIL import Image

D = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer5'
D3 = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer3'
D2 = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer2'   # older clips live here
OUT = sys.argv[1] if len(sys.argv) > 1 else D + '/sun-fighter-trailer-v8-vertical.mp4'
W, H, FPS, SR = 1080, 1920, 30, 44100
GW, GH = 135, 240     # a vertical window onto the 480x270 game; 135x240 game pixels at 8x is exactly 1080x1920
LOW = (0, 640, 782, 440)    # bottom-left of the title screen: the bogan, no logo
OLD = (130, 600, 853, 480)  # wider, so the old man and his whole speech bubble fit


class Clip:
    def __init__(self, name):
        import os
        self.dir = next(f'{r}/clips/{name}' for r in (D, D3, D2) if os.path.exists(f'{r}/clips/{name}/times.json'))
        self.name, self.times, self.cache = name, json.load(open(f'{self.dir}/times.json')), {}
        self.track = json.load(open(f'{self.dir}/track.json')) if os.path.exists(f'{self.dir}/track.json') else []
    def frame(self, at):
        i = min(max(bisect.bisect_left(self.times, at), 0), len(self.times) - 1)
        if i not in self.cache:
            if len(self.cache) > 30: self.cache.clear()
            self.cache[i] = Image.open(f'{self.dir}/{i:05d}.jpg').convert('RGB')
        return self.cache[i]
CLIPS, CARDS = {}, {}
def footage(name, at):
    if name not in CLIPS: CLIPS[name] = Clip(name)
    return CLIPS[name].frame(at)
def where(name, kind, at):
    """a character's game position at clip time `at`, averaged over a short window so the camera doesn't jitter"""
    if kind == 'player':
        pts = [tuple(o['p']) for o in CLIPS[name].track if abs(o['t'] - at) < 0.15]
        return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)) if pts else (240, 200)
    pts = [(n[2], n[3]) for o in CLIPS[name].track if abs(o['t'] - at) < 0.25 for n in o['npcs'] if n[0] == kind]
    if not pts:
        pts = [(n[2], n[3]) for o in CLIPS[name].track if o['t'] <= at for n in o['npcs'] if n[0] == kind][-1:]
    return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)) if pts else (240, 135)
def card(name):
    if name not in CARDS: CARDS[name] = Image.open(f'{D}/cards/{name}.png').convert('RGBA')
    return CARDS[name]
BLACK = Image.new('RGB', (W, H))

SLAT = Image.open(D + '/slat.png').convert('RGBA'); FIGHT = Image.open(D + '/fight.png').convert('RGBA')
SLAT3 = SLAT.resize((SLAT.width * 3, SLAT.height * 3), Image.NEAREST); FIGHT3 = FIGHT.resize((FIGHT.width * 3, FIGHT.height * 3), Image.NEAREST)
WHITE = Image.new('RGB', (W, H), (255, 251, 224))
def window(fr, cx, cy, zoom=1.0):
    gw, gh = GW / zoom, GH / zoom; x = min(max(cx - gw / 2, 0), 480 - gw); y = min(max(cy - gh / 2, 0), 270 - gh)
    return fr.crop((round(x * 4), round(y * 4), round((x + gw) * 4), round((y + gh) * 4))).resize((W, H), Image.NEAREST if zoom == 1 else Image.BILINEAR)
def overlay(base, img, a=1.0, dx=0, dy=0):
    im = base.convert('RGBA')
    if a < 1: img = img.copy(); img.putalpha(img.getchannel('A').point(lambda v: int(v * a)))
    im.alpha_composite(img, (dx, dy)) if dx >= 0 and dy >= 0 else im.paste(img, (dx, dy), img)
    return im.convert('RGB')


import scenes
BAR = 1.5; HB = BAR / 2
# kinds: card (black + caption), clip (game footage in a vertical window; vc=(cx, cy), follow=character, zoom), scene (new art), end (the title slam)
SEG = [
    dict(kind='card', dur=BAR, card='world', hit='braam'),
    dict(kind='clip', dur=1.5 * BAR, src=('beachsun', 0.6), speed=0.9, vc=(400, 135), fadein=0.5),                    # just the beach, waves lapping
    dict(kind='card', dur=BAR, card='sun', hit='braam'),
    dict(kind='clip', dur=2 * BAR, src=('beachsun', 4.05), speed=0.75, vc=(400, 135)),                               # the Sun emerges from the water
    dict(kind='card', dur=BAR, card='friend', hit='braam'),
    dict(kind='clip', dur=1.5 * BAR, src=('glare', 5.3), speed=1.3, vc=(240, 82), zoom=1.3, zoom2=1.55),            # his face; the eyes heat up red... and fire
    dict(kind='card', dur=HB, card='summer', hit='braam'),
    dict(kind='scene', dur=BAR, fn=lambda u: scenes.reveal(u + 0.3), name='reveal'),                              # our hero, mullet in the wind
    dict(kind='card', dur=HB, card='man', hit='braam'),
    dict(kind='scene', dur=BAR, fn=lambda u: scenes.tube_shot(u * 2, 3.0), name='tube'),                         # the Slather in his hand, SHING
    dict(kind='card', dur=BAR, card='isready', hit='braam'),
    dict(kind='clip', dur=HB, src=('lasers', 3.3), vc=(240, 130), flash=True),                                      # rapid fire
    dict(kind='clip', dur=HB, src=('roll', 3.95), follow='player', cy=150, flash=True),
    dict(kind='clip', dur=HB, src=('slam', 3.95), vc=(240, 150), flash=True),
    dict(kind='clip', dur=HB, src=('fire', 4.75), follow='boardies', cy=125, flash=True),
    dict(kind='clip', dur=HB, src=('grab', 4.1), speed=0.8, vc=(240, 120), flash=True),
    dict(kind='clip', dur=BAR, src=('eshay', 6.0), follow='eshay', cy=135, box=True, flash=True),
    dict(kind='clip', dur=HB, src=('van', 4.15), vc=(175, 125), flash=True),
    dict(kind='clip', dur=HB, src=('attack', 4.6), vc=(255, 120), flash=True, fadeout=0.6),
    dict(kind='black', dur=BAR),                                                                                    # darkness
    dict(kind='end', dur=4 * BAR),
]
t = 0.0
for s in SEG: s['t0'] = t; t += s['dur']
TOTAL = t
SC = {s['name']: s['t0'] for s in SEG if s['kind'] == 'scene'}
DARK_T0 = next(s for s in SEG if s['kind'] == 'black')['t0']; END_T0 = SEG[-1]['t0']
MONT = [s for s in SEG if s['kind'] == 'clip' and s['t0'] > SC['tube']]

WORDS = {k: (lambda im: im.crop(im.getbbox()))(card(k)) for k in ('w_coming', 'w_this', 'w_summer')}
SLAT4 = SLAT.resize((SLAT.width * 3, SLAT.height * 3), Image.NEAREST)
import math, random
def shake(img, amt, seed):
    if amt < 1: return img
    r = random.Random(seed); dx, dy = r.randint(-int(amt), int(amt)), r.randint(-int(amt), int(amt))
    out = Image.new('RGB', (W, H)); out.paste(img, (dx, dy)); return out
def slam_in(base, img, u, y, big=2.6, dur=0.16, x=None):
    if u < 0: return base
    e = min(1, u / dur); sc = 1 + (1 - e) ** 2 * (big - 1)
    im = img if sc == 1 else img.resize((int(img.width * sc), int(img.height * sc)), Image.NEAREST)
    x = (W - im.width) // 2 if x is None else x - im.width // 2
    return overlay(base, im, 0.35 + 0.65 * e, x, int(y - im.height / 2))
def ring(img, u, cx, cy):
    if not 0 <= u < 0.45: return img
    from PIL import ImageDraw
    d = ImageDraw.Draw(img); r = 80 + u * 2400; w = int(36 * (1 - u / 0.45)) + 2
    d.ellipse([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5], outline=(255, 240, 190), width=w); return img
SHADE = Image.linear_gradient('L').resize((W, H)).point(lambda v: int(max(0, (v - 125) * 1.6) * 0.85))
SLAMS = [(0.0, 'slat'), (BAR, 'fight'), (2 * BAR, 'w_coming'), (2.5 * BAR, 'w_this'), (3 * BAR, 'w_summer')]
def render_end(u):
    bg = window(footage('title', 3.05), 400, 135, 1 + 0.04 * u / (4 * BAR))
    lit = min(1, u / 0.08)
    out = Image.blend(BLACK, bg, 0.25 + 0.75 * lit)
    out = Image.composite(BLACK, out, SHADE)                      # darken the bottom so COMING THIS SUMMER reads
    out = slam_in(out, SLAT4, u, 520, big=3.4, dur=0.2)
    out = slam_in(out, FIGHT3, u - BAR, 900, big=2.4, dur=0.14, x=W // 2 + 40)
    for k, (t0, name) in enumerate(SLAMS[2:]):
        out = slam_in(out, WORDS[name], u - t0, 1290 + k * 170, big=2.2, dur=0.12)
    for t0, _ in SLAMS:
        v = u - t0
        if 0 <= v < 0.2: out = Image.blend(out, WHITE, 0.75 * (1 - v / 0.2) * (1 if t0 == 0 else 0.5))
        out = ring(out, v, W // 2, 520 if t0 == 0 else 900)
    amt = max([max(0, 40 * (1 - (u - t0) / 0.35)) if u >= t0 else 0 for t0, _ in SLAMS] + [0])
    return shake(out, amt, int(u * 60))
def render(T):
    seg = next(s for s in reversed(SEG) if T >= s['t0']); u = T - seg['t0']; left = seg['dur'] - u
    if seg['kind'] == 'black': return BLACK
    if seg['kind'] == 'end': return render_end(u)
    if seg['kind'] == 'card':
        im = Image.new('RGBA', (W, H), (0, 0, 0, 255)); im.alpha_composite(card(seg['card'])); im = im.convert('RGB')
        quick = seg['dur'] < BAR                       # the snappy cards punch in and out
        a = min(1, u / (0.06 if quick else 0.25)) if not seg.get('fadeout') else min(1, u / 0.12)
        b_ = min(1, left / (0.08 if quick else 0.2)) if not seg.get('fadeout') else min(1, left / seg['fadeout'])
        return Image.blend(BLACK, im, max(0, min(a, b_)))
    if seg['kind'] == 'scene':
        out = seg['fn'](u)
        if u < 0.12 and seg['name'] == 'sil': out = Image.blend(BLACK, out, u / 0.12)
        return out
    name, start = seg['src']; at = start + u * seg.get('speed', 1); fr = footage(name, at)
    if seg.get('follow'):
        cx, _ = where(name, seg['follow'], at); cy = seg.get('cy', 135)
    else: cx, cy = seg['vc']
    z = seg.get('zoom', 1.0); z = z + (seg.get('zoom2', z) - z) * u / seg['dur']
    out = window(fr, cx, cy, z)
    if seg.get('box'):
        n = int(min(22, max(0, (u - 0.2) / 0.03)))
        if u > 0.15: out = overlay(out, card(f'box_{n:02d}'))
    if seg.get('flash') and u < 0.1: out = Image.blend(out, WHITE, 0.7 * (1 - u / 0.1))
    if seg.get('fadein') and u < seg['fadein']: out = Image.blend(BLACK, out, u / seg['fadein'])
    if seg.get('fadeout') and left < seg['fadeout']: out = Image.blend(BLACK, out, max(0, left / seg['fadeout']))
    return out

# ---------------- score: overly dramatic industrial action-movie theme ----------------
N = int((TOTAL + 5) * SR); mix = np.zeros(N); rng = np.random.default_rng(7)
def tt(dur): return np.arange(int(dur * SR)) / SR
def at(t0, sig, vol=1.0, buf=None):
    buf = mix if buf is None else buf; i = int(t0 * SR); j = min(len(buf), i + len(sig)); buf[i:j] += sig[:j - i] * vol
def env(t, a, d): return np.minimum(1, t / a) * np.exp(-t * d)
def additive(f, t, fc, n=40, vib=0.0):
    """band-limited saw-ish tone: harmonics rolled off above fc (fc may move over time)"""
    ph = 2 * np.pi * f * (t + vib * np.sin(2 * np.pi * 5.2 * t) / (2 * np.pi * 5.2))
    return sum(np.sin(k * ph) / k * np.exp(-(k * f) / np.maximum(fc, 30)) for k in range(1, n + 1) if k * f < 12000)
def dun(big=1.0):            # the hit: deep drum + metal clank + sub
    t = tt(1.6); f = 42 + 90 * np.exp(-t * 14)
    drum = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    clank = sum(a * np.sin(2 * np.pi * fr * t) * np.exp(-t * dc) for fr, a, dc in [(311, .5, 9), (742, .45, 14), (1183, .35, 18), (1867, .25, 24), (2733, .15, 30)])
    noise = rng.standard_normal(len(t)) * np.exp(-t * 40) * 0.5
    return np.tanh(1.6 * (drum * 1.2 + clank * 0.6 * big + noise))
def braam(dur=2.4):
    t = tt(dur); fc = 220 + 1800 * np.exp(-t * 2.4)
    s = sum(additive(f * d, t, fc, 60) for f in (36.7, 55, 73.4, 110) for d in (0.996, 1.004))
    return np.tanh(1.3 * s) * env(t, 0.02, 1.1)
def brass(freqs, dur=1.2):
    t = tt(dur); fc = 300 + 1500 * np.exp(-t * 5)
    return sum(additive(f, t, fc, 50, vib=0.002) for f in freqs) / len(freqs) * env(t, 0.03, 1.6)
def choir(freqs, dur, attack=0.8):
    t = tt(dur); out = np.zeros(len(t)); forms = [(700, 1.0, 110), (1220, 0.5, 130), (2600, 0.25, 180)]
    for f0 in freqs:
        for d in (0.994, 1.0, 1.006):    # three voices per note
            f = f0 * d; ph = 2 * np.pi * f * (t + 0.004 * np.sin(2 * np.pi * (4.8 + d) * t))
            for k in range(1, int(4000 / f)):
                a = sum(g * np.exp(-((k * f - F) / bw) ** 2) for F, g, bw in forms) + 0.05 / k
                out += a * np.sin(k * ph)
    out /= np.max(np.abs(out)) + 1e-9
    return out * np.minimum(1, t / attack) * np.minimum(1, (t[-1] - t) / 0.5)
def strings16(root, dur, step):     # driving low-string ostinato, every sixteenth
    out = np.zeros(int(dur * SR))
    k = 0
    while k * step < dur:
        n = tt(step * 0.9); s = additive(root * (2 if k % 4 == 3 else 1), n, 900, 30) * env(n, 0.005, 9)
        at(k * step, s, 1.0, out); k += 1
    return out
def riser(dur):
    t = tt(dur); s = sum(np.sin(2 * np.pi * (200 + 1800 * (t / dur) ** 2) * m * t) / m for m in (1, 1.5, 2))
    return (s * 0.3 + rng.standard_normal(len(t)) * 0.4) * (t / dur) ** 3
def reverb(x, secs=2.6, wet=0.35):
    ir = rng.standard_normal(int(secs * SR)) * np.exp(-np.arange(int(secs * SR)) / SR * 3.2); ir[:int(0.01 * SR)] *= 0.2
    n = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    y = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[:len(x)]
    return x + y / (np.max(np.abs(y)) + 1e-9) * np.max(np.abs(x)) * wet

def snare_roll(dur):   # accelerating snare roll, getting louder
    out = np.zeros(int(dur * SR)); t = 0.0; gap = 0.16
    while t < dur:
        n = tt(0.08); s = rng.standard_normal(len(n)) * np.exp(-n * 50) + 0.4 * np.sin(2 * np.pi * 190 * n) * np.exp(-n * 30)
        at(t, s * (0.25 + 0.75 * (t / dur) ** 1.5), 1.0, out); t += gap; gap = max(0.035, gap * 0.93)
    return out
def taiko():
    t = tt(0.9); return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(60 + 70 * np.exp(-t * 20)) / SR) * np.exp(-t * 6))

A, C, E, F = 55.0, 65.41, 82.41, 87.31
hits = np.zeros(N); pads = np.zeros(N); fx = np.zeros(N)
# ---- SFX ----
def noise(d): return rng.standard_normal(int(d * SR))
def bandsweep(d, f0, f1, q=6):          # filtered noise sweeping f0 -> f1 (whooshes, squirts)
    t = tt(d); n = noise(d); f = f0 * (f1 / f0) ** (t / d); out = np.zeros_like(n); y1 = y2 = 0.0
    for i in range(len(n)):
        w0 = 2 * np.pi * f[i] / SR; al = np.sin(w0) / (2 * q); cs = np.cos(w0); b0 = al; a0 = 1 + al
        y = (b0 * n[i] - b0 * (n[i - 2] if i > 1 else 0) + 2 * cs * y1 - (1 - al) * y2) / a0; y2, y1 = y1, y; out[i] = y
    return out / (np.max(np.abs(out)) + 1e-9)
def waves(d):
    t = tt(d); n = noise(d); sw = 0.5 + 0.5 * np.sin(2 * np.pi * t / 3.2 - 1.5)
    lp = np.zeros_like(n); p = 0.0; a = np.exp(-2 * np.pi * 900 / SR)
    for i in range(len(n)): p = (1 - a) * n[i] + a * p; lp[i] = p
    return lp / (np.max(np.abs(lp)) + 1e-9) * (0.25 + 0.75 * sw ** 2)
def rumble(d):
    t = tt(d); return np.tanh(2 * (np.sin(2 * np.pi * 32 * t) + 0.6 * np.sin(2 * np.pi * 47 * t) + 0.3 * noise(d))) * (t / d) ** 1.5
def charge(d):                           # the eyes heating up: a rising whine with a pulsing tremolo
    t = tt(d); f = 180 * (8 ** (t / d)); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.4 * np.sin(2 * ph)) * (0.2 + 0.8 * t / d) * (0.6 + 0.4 * np.sin(2 * np.pi * (6 + 18 * t / d) * t))
def zap():
    t = tt(0.9); f = 2400 * np.exp(-t * 3) + 200; return (np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + noise(0.9) * 0.5) * np.exp(-t * 4)
def click():
    t = tt(0.12); return (noise(0.12) * np.exp(-t * 120) + np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 80)) * 0.9
def clack():                             # metal-on-metal, for racking
    t = tt(0.3); return (noise(0.3) * np.exp(-t * 70) * 0.8 + sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 25) for f in (1400, 2100, 3300)) * 0.4 + np.sin(2 * np.pi * 90 * t) * np.exp(-t * 18))
def squirt_fx():
    return bandsweep(0.45, 2600, 500, 4) * np.exp(-tt(0.45) * 3) * 0.9
def whoosh(d=0.35, up=True):
    return bandsweep(d, 300 if up else 3000, 3000 if up else 300, 3) * np.sin(np.pi * tt(d) / d)
def shing():                             # the glint
    t = tt(1.4); return sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * dc) for f, a, dc in [(2637, 1, 3), (3951, .6, 4), (5274, .4, 5), (1318, .3, 2)]) + noise(1.4) * np.exp(-t * 60) * 0.5
def thunk():
    t = tt(0.5); return np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(70 + 90 * np.exp(-t * 25)) / SR) * np.exp(-t * 9)) + noise(0.5) * np.exp(-t * 40) * 0.3
def heartbeat(t0, n, gap):
    for i in range(n):
        for off, v in ((0, 0.5), (0.26, 0.32)): ht = tt(0.4); at(t0 + i * gap + off, np.sin(2 * np.pi * 45 * ht) * np.exp(-ht * 9), v, hits)
def power_chord(f, d=1.6):               # an overdriven synth guitar stab for the hero's turn
    t = tt(d); s = sum(additive(f * m, t, 2500, 40) for m in (1, 1.5, 2)); return np.tanh(3 * s) * env(t, 0.005, 1.2)

S = lambda name: next(s for s in SEG if s.get('card') == name)['t0']
# 1) ominous opening: waves, drone, a braam on every card
at(0, waves(S('sun') + 2.0), 0.35, fx)
dt_ = tt(S('summer')); at(0, (np.sin(2 * np.pi * 55 * dt_) + 0.5 * np.sin(2 * np.pi * 82.4 * dt_)) * np.minimum(1, dt_ / 2) * np.minimum(1, (dt_[-1] - dt_) / 0.4), 0.16, pads)
at(S('sun') + BAR, rumble(2 * BAR), 0.55, hits)                                                      # the Sun breaking the surface
at(S('sun') + BAR, choir([A, E * 2, A * 2], 2 * BAR + 0.6, 1.2), 0.22, pads)
heartbeat(S('friend'), 5, 0.75)
glare = next(s for s in SEG if s.get('src', ('',))[0] == 'glare')
at(glare['t0'], charge(glare['dur'] - 0.25), 0.3, fx); at(glare['t0'] + glare['dur'] - 0.3, zap(), 0.5, fx)
# 2) THIS SUMMER...: the silhouette; a slow drum pulse
for st in (0, 6, 9, 10): at(S('summer') - BAR + st * BAR / 13, dun(0.55), 0.4, hits)
# 3) ONE MAN: whoosh into the turn, a power chord as the light hits him, then the wind howling through his mullet
at(SC['reveal'] - 0.3, whoosh(0.35), 0.6, fx); at(SC['reveal'], power_chord(A, 3.0), 0.42, pads); at(SC['reveal'], dun(1.2), 1.0, hits)
at(SC['reveal'] + 0.15, choir([A, C * 2, E * 2, A * 2], BAR + 0.6, 0.3), 0.32, pads); at(SC['reveal'] + 0.15, brass([A, E * 2, A * 2], 2.4), 0.5, pads)
wl = BAR; at(SC['reveal'] + 0.3, bandsweep(wl - 0.3, 500, 900, 2) * np.sin(np.pi * tt(wl - 0.3) / (wl - 0.3)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.33 * tt(wl - 0.3))), 0.35, fx)
for b in range(0):
    for st in (0, 9, 10): at(SC['reveal'] + b * BAR / 2 * 2 + st * BAR / 13, dun(0.8), 0.55, hits) if b < 3 else None
# 4) ONE TUBE...: the light sweeping the label, a SHING off the cap
at(SC['tube'] + 0.25, whoosh(0.55, True) * 0.6, 0.3, fx); at(SC['tube'] + 0.85, shing(), 0.45, fx)
dl = tt(BAR); at(SC['tube'], np.sin(2 * np.pi * 41.2 * dl) * np.minimum(1, dl / 0.3), 0.25, pads)
heartbeat(SC['tube'], 2, 0.75)
# 5) ONE FIGHT TO THE DEATH: the full theme for the rapid-fire montage
m0, m1 = S('isready'), DARK_T0; STEP = BAR / 13; PATTERN = [0, 3, 6, 9, 10]
for b in range(int(round((m1 - m0) / BAR))):
    t_ = m0 + b * BAR; I = 0.7 + 0.3 * b / 5
    for st in PATTERN: at(t_ + st * STEP, dun(I), 0.9 * I * (1.15 if st >= 9 else 1), hits)
    for st in range(13): at(t_ + st * STEP, taiko(), 0.2 * I, hits)
    at(t_, brass([A, E * 2, A * 2] if b % 2 == 0 else [F, C * 2, F * 2]), 0.6 * I, pads)
    at(t_, strings16(A if b % 2 == 0 else F, BAR, STEP), 0.22, pads); at(t_, strings16((A if b % 2 == 0 else F) * 2, BAR, STEP), 0.12, pads)
at(m0, choir([A, C * 2, E * 2, A * 2, C * 4], m1 - m0, 0.4), 0.38, pads)
at(m0 + BAR, snare_roll(m1 - m0 - BAR), 0.55, hits); at(m0 + BAR, riser(m1 - m0 - BAR), 0.6, hits)
for s_ in MONT: at(s_['t0'], whoosh(0.18, False), 0.25, fx)
for s_ in SEG:
    if s_.get('hit') == 'braam' and s_['t0'] > 0: at(s_['t0'], braam(), 0.55 if s_['t0'] < SC['reveal'] else 0.7, hits)
at(0, braam(3.0), 0.6, hits)
# 6) the end frame: everything back on, every word a slam
for t_, name in SLAMS:
    T_ = END_T0 + t_; big = name == 'slat'
    at(T_, dun(1.6 if big else 1.3), 1.4 if big else 1.0, hits); at(T_, taiko(), 1.0, hits)
    if big or name == 'fight': at(T_, braam(3.5 if big else 2.5), 1.0 if big else 0.7, hits)
at(END_T0, choir([A, E * 2, A * 2, C * 4, E * 4], 4 * BAR + 1.5, 0.15), 0.55, pads)
for i in range(4): at(END_T0 + i * BAR, brass([A, E * 2, A * 2, C * 4] if i % 2 == 0 else [F, C * 2, F * 2, A * 2], 2.0), 0.7, pads)
at(END_T0, power_chord(A, 3.0), 0.35, pads)
at(TOTAL - 0.25, dun(1.6), 1.5, hits); at(TOTAL - 0.25, braam(3.5), 0.9, hits); at(TOTAL - 0.25, taiko(), 1.0, hits)
mix = reverb(hits, 2.8, 0.45) + reverb(pads, 3.2, 0.3) + reverb(fx, 1.6, 0.25)
# the drop-out: the music fades with the picture and the darkness is silent until the BOOM
s0, s1 = int((DARK_T0 - 0.6) * SR), int(END_T0 * SR); ramp = int(0.6 * SR)
mix[s0:s0 + ramp] *= np.linspace(1, 0, ramp); mix[s0 + ramp:s1] = 0
mix = mix[:int((TOTAL + 2.2) * SR)]
fade = int(1.6 * SR); mix[-fade:] *= np.linspace(1, 0, fade) ** 2
mix = mix / (np.max(np.abs(mix)) + 1e-9); mix = np.tanh(1.5 * mix) / np.tanh(1.5) * 0.95
pcm = (np.stack([mix, mix], 1) * 32767).astype('<i2')
with wave.open(D + '/score10.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('score', round(TOTAL, 2), 's')

TAIL = 2.2
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-i', D + '/score10.wav', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                       '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
nf = int((TOTAL + TAIL) * FPS)
for f in range(nf):
    T = f / FPS
    ff.stdin.write((render(T) if T < TOTAL else BLACK).tobytes())
    if f % 300 == 0: print('frame', f, '/', nf, flush=True)
ff.stdin.close(); ff.wait(); print('done', OUT)
