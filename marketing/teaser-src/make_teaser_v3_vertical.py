"""Sun Fighter teaser v3, vertical 9:16 cut (1080x1920): every shot a tight vertical crop at 8x the game pixels, same edit and score as the 16:9 v3: gameplay shots (some slowed) cut against black title cards in the game's yellow pixel font."""
import bisect, json, subprocess, sys, wave
import numpy as np
from PIL import Image

D = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer4'
D3 = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer3'
D2 = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer2'   # older clips live here
OUT = sys.argv[1] if len(sys.argv) > 1 else D + '/sun-fighter-teaser-v3-vertical.mp4'
W, H, FPS, SR = 1080, 1920, 30, 44100
GW, GH = 135, 240     # a vertical window onto the 480x270 game; 135x240 game pixels at 8x is exactly 1080x1920
LOW = (0, 640, 782, 440)    # bottom-left of the title screen: the bogan, no logo
OLD = (130, 600, 853, 480)  # wider, so the old man and his whole speech bubble fit

# kind 'card' = black + caption; 'clip' = full-frame footage. speed < 1 is slow motion; freeze holds src; push = slow zoom-in
# Every cut sits on a 1.5 s bar of the score (13 sixteenths in the industrial DUN DUN DUN DUN-DUN pattern), 20 bars = 30 s.
BAR = 1.5
# vc=(cx, cy): where the vertical window sits, in game pixels. follow=kind: keep a character centred (from the clip's position log).
# box: type out the Pokemon text box over the shot. over: a card laid over the shot. logo: the finale, built from the game's own title art.
SEG = [
    dict(kind='card', dur=BAR, card='world'),
    dict(kind='clip', dur=2 * BAR, src=('title', 1.0), speed=0.6, vc=(400, 135), fadein=0.4),          # the Sun rises
    dict(kind='card', dur=BAR, card='sun'),
    dict(kind='clip', dur=BAR, src=('lasers', 3.0), speed=0.55, vc=(240, 130)),                         # towering over the beach, eyes firing
    dict(kind='card', dur=BAR, card='friend'),
    dict(kind='clip', dur=BAR, src=('grab', 4.1), speed=0.7, vc=(240, 120), flash=True),                # the fist, legs dangling
    dict(kind='clip', dur=BAR / 2, src=('fire', 4.75), follow='boardies', cy=125, flash=True),          # "MY TAN!" and up he goes
    dict(kind='clip', dur=BAR / 2, src=('fire', 5.6), follow='boardies', cy=125),                       # ...skeleton
    dict(kind='clip', dur=BAR, src=('eshay', 6.0), follow='eshay', cy=135, box=True, flash=True),                # gabber dancing as A wild ESHAY appeared! types out
    dict(kind='card', dur=BAR, card='man'),
    dict(kind='clip', dur=BAR, src=('title', 5.5), speed=0.5, vc=(80, 150)),                            # the bird, under the giant SLATHER
    dict(kind='card', dur=BAR, card='tube'),
    dict(kind='clip', dur=BAR, src=('title', 13.35), speed=0.55, vc=(125, 150)),                        # the catch
    dict(kind='card', dur=BAR, card='ready'),
    dict(kind='clip', dur=BAR, src=('attack', 4.6), vc=(255, 120), flash=True),                          # "MY EYES!!!"
    dict(kind='clip', dur=BAR, src=('attack', 5.75), vc=(240, 120), over='finish', flash=True),          # FINISH HIM over the furious, caked Sun
    dict(kind='card', dur=BAR, card='summer', silent=True),
    dict(kind='logo', dur=2 * BAR, src=('title', 3.05), phase=1),        # held just before the game's own logo slam, so ours is the only one
    dict(kind='logo', dur=2 * BAR, src=('title', 3.1), phase=2, over='coming', fadeout=0.7),
]
t = 0.0
for s in SEG: s['t0'] = t; t += s['dur']
TOTAL = t

class Clip:
    def __init__(self, name):
        import os
        self.dir = f'{D3}/clips/{name}' if os.path.exists(f'{D3}/clips/{name}/times.json') else f'{D2}/clips/{name}'
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

def render(T):
    seg = next(s for s in reversed(SEG) if T >= s['t0']); u = T - seg['t0']; left = seg['dur'] - u
    if seg['kind'] == 'card':
        im = Image.new('RGBA', (W, H), (0, 0, 0, 255)); im.alpha_composite(card(seg['card']))
        return Image.blend(BLACK, im.convert('RGB'), max(0, min(1, u / 0.25, left / 0.2)))
    name, start = seg['src']; at = start + u * seg.get('speed', 1); fr = footage(name, at)
    if seg['kind'] == 'logo':   # the finale, rebuilt for a tall screen from the game's own title art
        p1 = seg['phase'] == 1; push = 1.0 if p1 else 1 + 0.05 * u / seg['dur']
        out = window(footage(name, start), 400, 135, push)
        e = min(1, u / 0.22) if p1 else 1; sc = 1 + (1 - e) ** 2 * 2.4
        logo = SLAT3 if sc == 1 else SLAT3.resize((int(SLAT3.width * sc), int(SLAT3.height * sc)), Image.NEAREST)
        out = overlay(out, logo, 0.4 + 0.6 * e, (W - logo.width) // 2, 300 + (SLAT3.height - logo.height) // 2)
        rev = min(1, max(0, (u - 0.9) / 1.0)) if p1 else 1          # SUN FIGHTER writes on, left to right
        if rev > 0:
            f = FIGHT3.crop((0, 0, max(1, int(FIGHT3.width * rev)), FIGHT3.height)); out = overlay(out, f, 1, (W - FIGHT3.width) // 2 + 60, 730)
        if p1 and 0.22 <= u < 0.6: out = Image.blend(out, WHITE, 0.6 * (1 - (u - 0.22) / 0.38))   # the slam flash
        if seg.get('over'): out = overlay(out, card(seg['over']), min(1, max(0, (u - 0.3) / 0.4)))
        if seg.get('fadeout') and left < seg['fadeout']: out = Image.blend(BLACK, out, max(0, left / seg['fadeout']))
        return out
    if seg.get('follow'):
        CLIPS[name] if name in CLIPS else footage(name, at); cx, _ = where(name, seg['follow'], at); cy = seg.get('cy', 135)
    else: cx, cy = seg['vc']
    out = window(fr, cx, cy)
    if seg.get('box'):          # type the Pokemon box out once the encounter flash has cleared
        n = int(min(22, max(0, (u - 0.2) / 0.03)))
        if u > 0.15: out = overlay(out, card(f'box_{n:02d}'))
    if seg.get('over'): out = overlay(out, card(seg['over']))
    if seg.get('flash') and u < 0.12: out = Image.blend(out, WHITE, 0.8 * (1 - u / 0.12))
    if seg.get('fadein') and u < seg['fadein']: out = Image.blend(BLACK, out, u / seg['fadein'])
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

A, C, E, F = 55.0, 65.41, 82.41, 87.31   # note frequencies (D is taken: the output folder)
STEP = BAR / 13; PATTERN = [0, 3, 6, 9, 10]     # DUN . . DUN . . DUN . . DUN DUN . .
bars = int(round(TOTAL / BAR)); bar_of = lambda s: int(round(s['t0'] / BAR))
card_bars = {bar_of(s) for s in SEG if s['kind'] == 'card'}
s_bar = min(bar_of(s) for s in SEG if s.get('silent')); fin = s_bar + 1; end_bar = bar_of(SEG[-1])
man_bar = bar_of(next(s for s in SEG if s.get('card') == 'man')); ready_bar = bar_of(next(s for s in SEG if s.get('card') == 'ready'))
def stage(b):   # 0 ominous, 1 the Sun's rampage, 2 the hero, 3 fighting back, 4 finale
    return 0 if b < 5 else 1 if b < man_bar else 2 if b < ready_bar else 3 if b < s_bar else 4
KEY = [1.0, 1.0, 2 ** (2 / 12), 2 ** (3 / 12), 1.0]          # step up a key for the hero, again for the fight
hits = np.zeros(N); pads = np.zeros(N)
def snare_roll(dur):   # accelerating snare roll, getting louder
    out = np.zeros(int(dur * SR)); t = 0.0; gap = 0.16
    while t < dur:
        n = tt(0.08); s = rng.standard_normal(len(n)) * np.exp(-n * 50) + 0.4 * np.sin(2 * np.pi * 190 * n) * np.exp(-n * 30)
        at(t, s * (0.25 + 0.75 * (t / dur) ** 1.5), 1.0, out); t += gap; gap = max(0.035, gap * 0.93)
    return out
def taiko():
    t = tt(0.9); return np.tanh(2 * np.sin(2 * np.pi * np.cumsum(60 + 70 * np.exp(-t * 20)) / SR) * np.exp(-t * 6))
for b in range(bars):
    t0 = b * BAR; st_ = stage(b); k = KEY[st_]
    if b == s_bar or b >= fin: continue
    I = min(1.0, 0.3 + 0.7 * b / (s_bar - 1))             # one long climb from the first bar to the silence
    for st in PATTERN:
        if st_ == 0 and st in (3, 6): continue                # the opening is sparse: DUN ........ DUN-DUN
        at(t0 + st * STEP, dun(big=I), (0.15 + 0.85 * I ** 1.6) * (1.15 if st >= 9 else 1.0), hits)
    if st_ >= 2:                                               # taiko answering on the off-beats
        for st in (2, 5, 8, 12): at(t0 + st * STEP, taiko(), 0.35 * I, hits)
    if st_ >= 3:                                               # and every sixteenth, flat out
        for st in range(13): at(t0 + st * STEP, taiko(), 0.18 * I, hits)
    if b in card_bars and b > 0: at(t0, braam(), 0.25 + 0.6 * I, hits)
    if st_ >= 1: at(t0, brass([x * k for x in ([A, E * 2, A * 2] if b % 2 == 0 else [F, C * 2, F * 2])]), 0.55 * I, pads)
    if st_ >= 1: at(t0, strings16((A if b % 2 == 0 else F) * k, BAR, STEP), 0.12 + 0.12 * I, pads)
    if st_ >= 3: at(t0, strings16((A if b % 2 == 0 else F) * k * 2, BAR, STEP), 0.1 * I, pads)   # octave up: frantic
# a quiet heartbeat sub under the opening
for b in range(0, 5):
    for off in (0, 0.28): ht = tt(0.4); at(b * BAR + off, np.sin(2 * np.pi * 45 * ht) * np.exp(-ht * 9), 0.35 if off == 0 else 0.22, hits)
# the choir climbs with every stage
at(0, choir([A, E * 2, A * 2], 7.5, 3.0), 0.16, pads)
at(5 * BAR, choir([A, C * 2, E * 2], (man_bar - 5) * BAR + 0.6, 1.0), 0.24, pads)
at(man_bar * BAR, choir([x * KEY[2] for x in (A, C * 2, E * 2, A * 2)], (ready_bar - man_bar) * BAR + 0.6, 0.6), 0.3, pads)
at(ready_bar * BAR, choir([x * KEY[3] for x in (A, C * 2, E * 2, A * 2, C * 4)], (s_bar - ready_bar) * BAR, 0.3), 0.4, pads)
# everything piles into the silence: snare roll, riser, then nothing
at(ready_bar * BAR, snare_roll((s_bar - ready_bar) * BAR), 0.5, hits)
at(ready_bar * BAR, riser((s_bar - ready_bar) * BAR), 0.6, hits)
at(s_bar * BAR + 0.75, braam(1.6), 0.35, hits)                                 # one distant hit in the dark
# FINALE: SLATHER slams in a key higher still, full choir, brass, the pattern at full weight, one last boom
kf = 2 ** (5 / 12); f0 = fin * BAR
at(f0, dun(1.5), 1.4, hits); at(f0, braam(4.0), 1.0, hits); at(f0, taiko(), 1.0, hits)
at(f0, choir([x * kf for x in (A, E * 2, A * 2, C * 4, E * 4)], (bars - fin) * BAR + 1.5, 0.25), 0.55, pads)
for i, b in enumerate(range(fin, bars)):
    at(b * BAR, brass([x * kf for x in ([A, E * 2, A * 2, C * 4] if i % 2 == 0 else [F, C * 2, F * 2, A * 2])], 2.0), 0.7, pads)
    for st in PATTERN: at(b * BAR + st * STEP, dun(1.3), 1.1 if st >= 9 else 0.95, hits)
    for st in (2, 5, 8, 12): at(b * BAR + st * STEP, taiko(), 0.5, hits)
at(TOTAL - 0.35, dun(1.6), 1.5, hits); at(TOTAL - 0.35, braam(3.5), 0.9, hits); at(TOTAL - 0.35, taiko(), 1.0, hits)
mix = reverb(hits, 2.8, 0.45) + reverb(pads, 3.2, 0.3)
mix = mix[:int((TOTAL + 2.2) * SR)]                                              # let the last boom ring out over black
fade = int(1.6 * SR); mix[-fade:] *= np.linspace(1, 0, fade) ** 2
mix = mix / (np.max(np.abs(mix)) + 1e-9); mix = np.tanh(1.5 * mix) / np.tanh(1.5) * 0.95
pcm = (np.stack([mix, mix], 1) * 32767).astype('<i2')
with wave.open(D + '/score5.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('score', round(TOTAL, 2), 's +2.2 s ring-out')

TAIL = 2.2   # black after the end frame while the last hit rings
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-i', D + '/score5.wav', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                       '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
nf = int((TOTAL + TAIL) * FPS)
for f in range(nf):
    T = f / FPS
    ff.stdin.write((render(T) if T < TOTAL else BLACK).tobytes())
    if f % 300 == 0: print('frame', f, '/', nf, flush=True)
ff.stdin.close(); ff.wait(); print('done', OUT)
