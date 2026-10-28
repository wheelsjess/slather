"""Sun Fighter social trailer: composes recorded gameplay + caption cards into a 1080x1920 video with a synthesised trailer score."""
import bisect, json, math, subprocess, sys, wave
import numpy as np
from PIL import Image

D = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer'
OUT = sys.argv[1] if len(sys.argv) > 1 else D + '/sun-fighter-trailer.mp4'
W, H, FPS, BAND_Y, SR = 1080, 1920, 30, 555, 44100
BAND = (1080, 811)          # the game, cropped to 4:3 so it fills more of a phone screen
DEFAULT_CROP = (135, 0, 810, 608)

# ---------------- edit decision list ----------------
# kind: 'card' (black + card), 'clip' (game band + optional card); src=(clip, start); crop=(x, y, w, h) zooms into the 1080x608 frame
SEG = [
    dict(kind='card', dur=2.4, card='world', fade=0.5, hit='braam'),
    dict(kind='clip', dur=2.8, src=('title', 0.6), card='sun', fade=0.4),
    dict(kind='clip', dur=1.9, src=('lasers', 3.1), card='enough', punch=True, flash=True, hit='braam'),
    dict(kind='clip', dur=1.8, src=('title', 5.2), crop=(50, 330, 371, 278), card='bogan', punch=True, flash=True, hit='braam'),
    dict(kind='clip', dur=2.0, src=('title', 10.6), crop=(170, 308, 400, 300), card='tube', punch=True, flash=True, hit='braam'),
    dict(kind='card', dur=2.0, card='summer', fade=0.3, hit='braam'),
    dict(kind='clip', dur=1.35, src=('lasers', 3.7), card='m_lasers', top='m_top', flash=True, hit='hit', music=True),
    dict(kind='clip', dur=1.35, src=('lasers', 6.3), card='m_rays', top='m_top', flash=True, hit='hit', music=True),
    dict(kind='clip', dur=1.35, src=('phase3', 5.0), card='m_dome', top='m_top', flash=True, hit='hit', music=True),
    dict(kind='clip', dur=1.6, src=('grab', 4.0), card='m_hug', top='m_top', flash=True, hit='hit', music=True),
    dict(kind='clip', dur=1.5, src=('eshay', 2.6), card='m_eshay', top='m_top', flash=True, hit='hit', music=True),
    dict(kind='clip', dur=1.7, src=('van', 3.9), card='m_van', top='m_top', flash=True, hit='hit', music=True),
    dict(kind='clip', dur=2.4, src=('finish', 2.35), flash=True, hit='gong'),
    dict(kind='card', dur=1.8, card='quote1', fade=0.2, hit='tick'),
    dict(kind='card', dur=1.6, card='quote2', fade=0.2, hit='tick'),
    dict(kind='clip', dur=2.8, src=('finish', 7.8), card='win', fade=0.4, hit='win'),
    dict(kind='clip', dur=5.0, src=('title', 8.25), freeze=True, push=0.06, crop=(30, 0, 810, 608), card='end', punch=True, flash=True, hit='end', fadeout=0.6),
]
t = 0.0
for s in SEG: s['t0'] = t; t += s['dur']
TOTAL = t

# ---------------- footage ----------------
class Clip:
    def __init__(self, name):
        self.name, self.times, self.cache = name, json.load(open(f'{D}/clips/{name}/times.json')), {}
    def frame(self, at):
        i = min(max(bisect.bisect_left(self.times, at), 0), len(self.times) - 1)
        if i not in self.cache:
            if len(self.cache) > 40: self.cache.clear()
            self.cache[i] = Image.open(f'{D}/clips/{self.name}/{i:05d}.jpg').convert('RGB')
        return self.cache[i]
CLIPS = {}
def footage(name, at):
    if name not in CLIPS: CLIPS[name] = Clip(name)
    return CLIPS[name].frame(at)
CARDS = {}
def card(name):
    if name not in CARDS: CARDS[name] = Image.open(f'{D}/cards/{name}.png').convert('RGBA')
    return CARDS[name]

def place_card(canvas, name, u, seg):
    im = card(name)
    if seg.get('punch') and u < 0.16:   # slams in from 120% size
        k = 1 + 0.2 * (1 - u / 0.16) ** 2; w, h = int(W * k), int(H * k)
        im = im.resize((w, h), Image.BILINEAR).crop(((w - W) // 2, (h - H) // 2, (w - W) // 2 + W, (h - H) // 2 + H))
    a = min(1.0, u / seg['fade']) if seg.get('fade') else 1.0
    if a < 1: im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * a)))
    canvas.alpha_composite(im)

def render(T):
    seg = next(s for s in reversed(SEG) if T >= s['t0']); u = T - seg['t0']
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    if seg['kind'] == 'clip':
        name, start = seg['src']; fr = footage(name, start + (0 if seg.get('freeze') else u))
        x, y, w, h = seg.get('crop', DEFAULT_CROP)
        if seg.get('push'):   # slow push-in over the shot
            k = 1 - seg['push'] * u / seg['dur']; nw, nh = w * k, h * k; x, y, w, h = x + (w - nw) / 2, y + (h - nh) / 2, nw, nh
        fr = fr.crop((round(x), round(y), round(x + w), round(y + h))).resize(BAND, Image.NEAREST if not seg.get('push') else Image.BILINEAR)
        canvas.paste(fr, (0, BAND_Y))
    if seg.get('top'): canvas.alpha_composite(card(seg['top']))
    if seg.get('card'): place_card(canvas, seg['card'], u, seg)
    rgb = canvas.convert('RGB')
    if seg.get('flash') and u < 0.12: rgb = Image.blend(rgb, Image.new('RGB', (W, H), (255, 250, 225)), 0.85 * (1 - u / 0.12))
    left = seg['dur'] - u
    if seg.get('fadeout') and left < seg['fadeout']: rgb = Image.blend(Image.new('RGB', (W, H)), rgb, max(0, left / seg['fadeout']))
    return rgb

# ---------------- score ----------------
N = int((TOTAL + 1.5) * SR); mix = np.zeros(N)
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

# drone under the opening cards
dt = tt(SEG[6]['t0']); drone = (np.sin(2 * np.pi * 55 * dt) + 0.5 * np.sin(2 * np.pi * 82.4 * dt) + 0.3 * saw(110.3, dt) * 0.3)
at(0, drone * np.minimum(1, dt / 1.5) * 0.18)
at(SEG[6]['t0'] - 1.6, riser(1.6), 0.7)

# the fight theme, chiptune, under the montage (LEAD_A from the game)
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def midi(s): return 12 * (int(s[-1]) + 1) + NOTE[s[0]] + (1 if '#' in s else 0)
LEAD = ('A4 . . E5 . . A5 . G5 . E5 . C5 . D5 E5 F5 . . C5 . . A4 . C5 . F5 . E5 . C5 . '
        'D5 . . G4 . . B4 . D5 . G5 . F5 . D5 . E5 . G#5 . B5 . G#5 . E5 . D5 . C5 . B4 .').split()
ROOTS = [midi(x) for x in ('A2', 'F2', 'G2', 'E2')]
m0 = SEG[6]['t0']; m1 = SEG[12]['t0']; step = 60 / 150 / 4; hz = lambda m: 440 * 2 ** ((m - 69) / 12)
k = 0
while m0 + k * step < m1:
    s = m0 + k * step; i = k % 64; bar = (k // 16) % 4
    if LEAD[i] != '.': nt = tt(step * 1.9); at(s, pulse(hz(midi(LEAD[i])), nt) * np.exp(-nt * 4), 0.10); at(s, pulse(hz(midi(LEAD[i])) * 1.003, nt, 0.5) * np.exp(-nt * 4), 0.04)
    if k % 2 == 0: bt = tt(step * 1.8); at(s, tri(hz(ROOTS[bar] + (12 if k % 4 == 2 else 0)), bt) * np.exp(-bt * 3), 0.22)
    if k % 4 == 0: kt = tt(0.18); at(s, np.sin(2 * np.pi * np.cumsum(45 + 110 * np.exp(-kt * 30)) / SR) * np.exp(-kt * 14), 0.55)
    if k % 8 == 4: st = tt(0.15); at(s, lowpass(rng.standard_normal(len(st)), 3500) * np.exp(-st * 22), 0.35)
    if k % 2 == 1: ht = tt(0.04); at(s, rng.standard_normal(len(ht)) * np.exp(-ht * 90), 0.06)
    k += 1

HITS = {'braam': lambda: braam(), 'hit': hit, 'tick': tick,
        'gong': gong,
        'win': lambda: chord([98, 147, 196, 247], 2.8) * 1.2,
        'end': lambda: braam(3.4) * 0.8}
for s in SEG:
    h = s.get('hit')
    if not h: continue
    at(s['t0'], HITS[h](), {'braam': 0.55, 'hit': 0.5, 'tick': 0.5, 'gong': 0.6, 'win': 0.5, 'end': 0.55}[h])
    if h == 'gong': at(s['t0'], hit(), 0.6)
# end card: the coin chime and a little arcade arpeggio, then a last thump
e = SEG[-1]['t0']
for n, f in enumerate([988, 1319, 1568, 1976]): ct = tt(0.25); at(e + 0.9 + n * 0.08, pulse(f, ct, 0.5) * np.exp(-ct * 10), 0.08)
at(e + 0.05, chord([174.6, 220, 261.6, 349.2], 4.5, saw) * 0.5, 0.35)
# a low pad under the critic quotes and the win, so the back half never drops to silence
q0, q1 = SEG[13]['t0'], SEG[16]['t0']; pt = tt(q1 - q0)
at(q0, (np.sin(2 * np.pi * 49 * pt) + 0.6 * np.sin(2 * np.pi * 73.4 * pt) + 0.25 * np.sin(2 * np.pi * 146.8 * pt)) * np.minimum(1, pt / 0.4) * np.minimum(1, (pt[-1] - pt) / 0.5), 0.16)
mix = mix[:int((TOTAL + 0.05) * SR)]
fade = int(0.6 * SR); mix[-fade:] *= np.linspace(1, 0, fade)
mix = mix / (np.max(np.abs(mix)) + 1e-9); mix = np.tanh(2.2 * mix) / np.tanh(2.2) * 0.93   # glue it together and lift the quiet bits
pcm = (np.stack([mix, mix], 1) * 32767).astype('<i2')
with wave.open(D + '/score.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('score', round(TOTAL, 2), 's')

# ---------------- encode ----------------
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-i', D + '/score.wav', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                       '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
nf = int(TOTAL * FPS)
for f in range(nf):
    ff.stdin.write(render(f / FPS).tobytes())
    if f % 150 == 0: print('frame', f, '/', nf, flush=True)
ff.stdin.close(); ff.wait(); print('done', OUT)
