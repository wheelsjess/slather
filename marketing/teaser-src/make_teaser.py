"""Sun Fighter teaser, 16:9 full-frame: gameplay shots (some slowed) cut against black title cards in the game's yellow pixel font."""
import bisect, json, subprocess, sys, wave
import numpy as np
from PIL import Image

D = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer2'
OUT = sys.argv[1] if len(sys.argv) > 1 else D + '/sun-fighter-teaser.mp4'
W, H, FPS, SR = 1920, 1080, 30, 44100
LOW = (0, 640, 782, 440)    # bottom-left of the title screen: the bogan, no logo
OLD = (130, 600, 853, 480)  # wider, so the old man and his whole speech bubble fit

# kind 'card' = black + caption; 'clip' = full-frame footage. speed < 1 is slow motion; freeze holds src; push = slow zoom-in
SEG = [
    dict(kind='card', dur=2.4, card='world', hit='braam'),
    dict(kind='clip', dur=3.2, src=('title', 1.0), speed=0.6, fadein=0.5),
    dict(kind='card', dur=2.2, card='sun', hit='braam'),
    dict(kind='clip', dur=3.2, src=('lasers', 2.6), speed=0.5, fadein=0.25),
    dict(kind='card', dur=2.4, card='friend', hit='braam'),
    dict(kind='clip', dur=1.4, src=('phase3', 4.5), flash=True, hit='hit'),
    dict(kind='clip', dur=2.4, src=('grab', 3.7), speed=0.65, flash=True, hit='hit'),
    dict(kind='clip', dur=1.3, src=('phase3', 11.9), flash=True, hit='hit'),
    dict(kind='card', dur=2.0, card='man', hit='braam'),
    dict(kind='clip', dur=1.1, src=('title', 4.3), crop=LOW, fadein=0.2),
    dict(kind='clip', dur=2.0, src=('title', 5.4), crop=LOW, speed=0.5),
    dict(kind='card', dur=2.6, card='tube', hit='braam'),
    dict(kind='clip', dur=1.8, src=('title', 10.9), crop=OLD, fadein=0.2),
    dict(kind='clip', dur=2.6, src=('title', 13.3), crop=OLD, speed=0.6, hit='aloft'),
    dict(kind='card', dur=2.4, card='ready', hit='braam'),
    dict(kind='clip', dur=2.6, src=('attack', 3.9), flash=True, music=True),
    dict(kind='clip', dur=2.3, src=('finish', 2.4), flash=True, hit='gong'),
    dict(kind='card', dur=2.2, card='summer', hit='braam'),
    dict(kind='clip', dur=4.3, src=('title', 3.15), hit='title'),
    dict(kind='clip', dur=4.0, src=('title', 7.45), freeze=True, push=0.05, over='coming', overin=0.4, fadeout=0.8, hit='end'),
]
t = 0.0
for s in SEG: s['t0'] = t; t += s['dur']
TOTAL = t

class Clip:
    def __init__(self, name):
        self.name, self.times, self.cache = name, json.load(open(f'{D}/clips/{name}/times.json')), {}
    def frame(self, at):
        i = min(max(bisect.bisect_left(self.times, at), 0), len(self.times) - 1)
        if i not in self.cache:
            if len(self.cache) > 30: self.cache.clear()
            self.cache[i] = Image.open(f'{D}/clips/{self.name}/{i:05d}.jpg').convert('RGB')
        return self.cache[i]
CLIPS, CARDS = {}, {}
def footage(name, at):
    if name not in CLIPS: CLIPS[name] = Clip(name)
    return CLIPS[name].frame(at)
def card(name):
    if name not in CARDS: CARDS[name] = Image.open(f'{D}/cards/{name}.png').convert('RGBA')
    return CARDS[name]
BLACK = Image.new('RGB', (W, H))

def render(T):
    seg = next(s for s in reversed(SEG) if T >= s['t0']); u = T - seg['t0']; left = seg['dur'] - u
    if seg['kind'] == 'card':
        im = Image.new('RGBA', (W, H), (0, 0, 0, 255)); im.alpha_composite(card(seg['card']))
        a = min(1, u / 0.25, left / 0.2)    # fade up, cut out
        return Image.blend(BLACK, im.convert('RGB'), max(0, a))
    name, start = seg['src']; fr = footage(name, start + (0 if seg.get('freeze') else u * seg.get('speed', 1)))
    x, y, w, h = seg.get('crop', (0, 0, W, H))
    if seg.get('push'):
        k = 1 - seg['push'] * u / seg['dur']; nw, nh = w * k, h * k; x, y, w, h = x + (w - nw) / 2, y + (h - nh) / 2, nw, nh
    if (x, y, w, h) != (0, 0, W, H):
        fr = fr.crop((round(x), round(y), round(x + w), round(y + h))).resize((W, H), Image.BILINEAR if seg.get('push') else Image.NEAREST)
    if seg.get('over'):
        im = fr.convert('RGBA'); ov = card(seg['over']); a = min(1, max(0, (u - seg.get('overin', 0)) / 0.4))
        if a < 1: ov = ov.copy(); ov.putalpha(ov.getchannel('A').point(lambda v: int(v * a)))
        im.alpha_composite(ov); fr = im.convert('RGB')
    if seg.get('flash') and u < 0.12: fr = Image.blend(fr, Image.new('RGB', (W, H), (255, 250, 225)), 0.8 * (1 - u / 0.12))
    if seg.get('fadein') and u < seg['fadein']: fr = Image.blend(BLACK, fr, u / seg['fadein'])
    if seg.get('fadeout') and left < seg['fadeout']: fr = Image.blend(BLACK, fr, max(0, left / seg['fadeout']))
    return fr

# ---------------- score ----------------
N = int((TOTAL + 4) * SR); mix = np.zeros(N)
def at(t0, sig, vol=1.0):
    i = int(t0 * SR); j = min(N, i + len(sig)); mix[i:j] += sig[:j - i] * vol
def tt(dur): return np.arange(int(dur * SR)) / SR
def lowpass(x, cut):   # one-pole, cutoff may be an array
    a = np.exp(-2 * np.pi * np.broadcast_to(cut, x.shape) / SR); y = np.zeros_like(x); p = 0.0
    for k in range(len(x)): p = (1 - a[k]) * x[k] + a[k] * p; y[k] = p
    return y
def saw(f, t): return 2 * ((f * t) % 1) - 1
def pulse(f, t, duty=0.25): return np.where((f * t) % 1 < duty, 1.0, -1.0)
def tri(f, t): return 2 * np.abs(2 * ((f * t) % 1) - 1) - 1
rng = np.random.default_rng(7)

def braam(dur=2.6):
    t = tt(dur); sig = sum(saw(f * (1 + d), t) for f in (43.65, 65.41, 87.31, 130.8) for d in (-0.004, 0.004))
    sig = lowpass(sig, 180 + 1400 * np.exp(-t * 2.2)); sig = np.tanh(sig * 1.6)
    return sig * np.minimum(1, t / 0.015) * np.exp(-t * 1.25)
def hit():
    t = tt(0.7); f = 38 + 110 * np.exp(-t * 9); body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5.5)
    return np.tanh(1.8 * body) + lowpass(rng.standard_normal(len(t)), 1800) * np.exp(-t * 30) * 0.8
def gong():
    t = tt(4.0); parts = [(110, 1), (173, .6), (237, .45), (331, .3), (468, .2), (590, .15)]
    return sum(a * np.sin(2 * np.pi * f * t + a) * np.exp(-t * (0.8 + f / 500)) for f, a in parts) * 0.5
def tick():
    t = tt(0.5); return np.sin(2 * np.pi * 1318 * t) * np.exp(-t * 9) * 0.5 + np.sin(2 * np.pi * 659 * t) * np.exp(-t * 6) * 0.3
def chord(freqs, dur, kind=tri):
    t = tt(dur); return sum(kind(f, t) for f in freqs) / len(freqs) * np.minimum(1, t / 0.05) * np.exp(-t * 0.9)
def riser(dur):
    t = tt(dur); n = lowpass(rng.standard_normal(len(t)), 300 + 5000 * (t / dur) ** 2); return n * (t / dur) ** 2 * 0.6


# a low drone under the slow, ominous first half; risers into the big cards
first = next(s for s in SEG if s.get('card') == 'man')['t0']; dt = tt(first)
at(0, (np.sin(2 * np.pi * 55 * dt) + 0.5 * np.sin(2 * np.pi * 82.4 * dt)) * np.minimum(1, dt / 1.5) * np.minimum(1, (dt[-1] - dt) / 1.0), 0.2)
mid = next(s for s in SEG if s.get('card') == 'tube')['t0']; ht = tt(next(s for s in SEG if s.get('card') == 'ready')['t0'] - first)
at(first, (np.sin(2 * np.pi * 65.4 * ht) + 0.5 * np.sin(2 * np.pi * 98 * ht)) * np.minimum(1, ht / 0.8) * np.minimum(1, (ht[-1] - ht) / 0.6), 0.16)   # a warmer, hopeful pad for the hero
for name in ('friend', 'ready', 'summer'):
    s0 = next(s for s in SEG if s.get('card') == name)['t0']; at(s0 - 1.4, riser(1.4), 0.6)

# the fight theme (LEAD_A from the game), fast chiptune, while the bogan fights back
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def midi(s): return 12 * (int(s[-1]) + 1) + NOTE[s[0]] + (1 if '#' in s else 0)
LEAD = ('A4 . . E5 . . A5 . G5 . E5 . C5 . D5 E5 F5 . . C5 . . A4 . C5 . F5 . E5 . C5 . '
        'D5 . . G4 . . B4 . D5 . G5 . F5 . D5 . E5 . G#5 . B5 . G#5 . E5 . D5 . C5 . B4 .').split()
ROOTS = [midi(x) for x in ('A2', 'F2', 'G2', 'E2')]; hz = lambda m: 440 * 2 ** ((m - 69) / 12)
ms = next(s for s in SEG if s.get('music')); m0, m1, step = ms['t0'], ms['t0'] + ms['dur'], 60 / 160 / 4
k = 0
while m0 + k * step < m1:
    s = m0 + k * step; i = k % 64; bar = (k // 16) % 4
    if LEAD[i] != '.': nt = tt(step * 1.9); at(s, pulse(hz(midi(LEAD[i])), nt) * np.exp(-nt * 4), 0.12)
    if k % 2 == 0: bt = tt(step * 1.8); at(s, tri(hz(ROOTS[bar] + (12 if k % 4 == 2 else 0)), bt) * np.exp(-bt * 3), 0.24)
    if k % 4 == 0: kt = tt(0.18); at(s, np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-kt * 30)) / SR) * np.exp(-kt * 14), 0.6)
    if k % 8 == 4: st = tt(0.15); at(s, lowpass(rng.standard_normal(len(st)), 3500) * np.exp(-st * 22), 0.35)
    k += 1

def sparkle():   # the item-get jingle-ish twinkle for the bogan holding the tube aloft
    out = np.zeros(int(1.4 * SR))
    for n, f in enumerate([784, 988, 1175, 1568]):
        t = tt(0.6); s = (np.sin(2 * np.pi * f * t) + 0.3 * pulse(f, t, 0.5)) * np.exp(-t * 5); i = int(n * 0.12 * SR); out[i:i + len(s)] += s[:len(out) - i]
    return out * 0.5
def slam():
    return np.concatenate([hit() * 1.2, np.zeros(10)]) 
HITS = {'braam': (lambda: braam(), 0.55), 'hit': (hit, 0.5), 'gong': (gong, 0.65), 'aloft': (sparkle, 0.6),
        'title': (lambda: np.concatenate([np.zeros(int(0.05 * SR)), hit() * 1.3]), 0.7),
        'end': (lambda: chord([174.6, 220, 261.6, 349.2], 4.0, saw), 0.4)}
for s in SEG:
    h = s.get('hit')
    if h: f, v = HITS[h]; at(s['t0'], f(), v)
    if h == 'gong': at(s['t0'], hit(), 0.6)
# the end: coin chime as COMING THIS SUMMER lands, and a last BRAAAM
e = SEG[-1]['t0']
for n, f in enumerate([988, 1319, 1568, 1976]): ct = tt(0.25); at(e + 0.4 + n * 0.08, pulse(f, ct, 0.5) * np.exp(-ct * 10), 0.09)
at(e + 0.4, braam(3.4), 0.5)
mix = mix[:int((TOTAL + 0.05) * SR)]
fade = int(0.8 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
mix = mix / (np.max(np.abs(mix)) + 1e-9); mix = np.tanh(2.2 * mix) / np.tanh(2.2) * 0.93
pcm = (np.stack([mix, mix], 1) * 32767).astype('<i2')
with wave.open(D + '/score.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('score', round(TOTAL, 2), 's')

ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-i', D + '/score.wav', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                       '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
nf = int(TOTAL * FPS)
for f in range(nf):
    ff.stdin.write(render(f / FPS).tobytes())
    if f % 300 == 0: print('frame', f, '/', nf, flush=True)
ff.stdin.close(); ff.wait(); print('done', OUT)
