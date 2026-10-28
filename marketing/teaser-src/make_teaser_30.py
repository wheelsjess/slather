"""Sun Fighter 30-second teaser, 16:9 full-frame, cut to an industrial action-movie score: gameplay shots (some slowed) cut against black title cards in the game's yellow pixel font."""
import bisect, json, subprocess, sys, wave
import numpy as np
from PIL import Image

D = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer2'
OUT = sys.argv[1] if len(sys.argv) > 1 else D + '/sun-fighter-teaser-30.mp4'
W, H, FPS, SR = 1920, 1080, 30, 44100
LOW = (0, 640, 782, 440)    # bottom-left of the title screen: the bogan, no logo
OLD = (130, 600, 853, 480)  # wider, so the old man and his whole speech bubble fit

# kind 'card' = black + caption; 'clip' = full-frame footage. speed < 1 is slow motion; freeze holds src; push = slow zoom-in
# Every cut sits on a 1.5 s bar of the score (13 sixteenths in the industrial DUN DUN DUN DUN-DUN pattern), 20 bars = 30 s.
BAR = 1.5
SEG = [
    dict(kind='card', dur=BAR, card='world'),
    dict(kind='clip', dur=2 * BAR, src=('title', 1.0), speed=0.6, fadein=0.4),
    dict(kind='card', dur=BAR, card='sun'),
    dict(kind='clip', dur=BAR, src=('lasers', 3.0), speed=0.5),
    dict(kind='card', dur=BAR, card='friend'),
    dict(kind='clip', dur=BAR / 2, src=('phase3', 4.6), flash=True),
    dict(kind='clip', dur=BAR, src=('grab', 3.9), speed=0.6, flash=True),
    dict(kind='clip', dur=BAR / 2, src=('phase3', 12.0), flash=True),
    dict(kind='card', dur=BAR, card='man'),
    dict(kind='clip', dur=BAR, src=('title', 5.5), crop=LOW, speed=0.5),
    dict(kind='card', dur=BAR, card='tube'),
    dict(kind='clip', dur=BAR, src=('title', 13.35), crop=OLD, speed=0.55),
    dict(kind='card', dur=BAR, card='ready'),
    dict(kind='clip', dur=BAR, src=('attack', 4.4), flash=True),
    dict(kind='clip', dur=BAR, src=('finish', 2.42), flash=True),
    dict(kind='card', dur=BAR, card='summer', silent=True),
    dict(kind='clip', dur=2 * BAR, src=('title', 3.15), speed=1.35),
    dict(kind='clip', dur=2 * BAR, src=('title', 7.45), freeze=True, push=0.05, over='coming', overin=0.2, fadeout=0.7),
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
bars = int(round(TOTAL / BAR)); card_bars = {int(round(s['t0'] / BAR)) for s in SEG if s['kind'] == 'card'}
silent = {int(round(s['t0'] / BAR)) for s in SEG if s.get('silent')}
end_bar = int(round(SEG[-2]['t0'] / BAR))
hits = np.zeros(N); pads = np.zeros(N)
for b in range(bars):
    t0 = b * BAR
    if b in silent: continue
    intensity = 0.4 + 0.6 * min(1, b / 14)          # builds steadily from a quiet, ominous clank to full force
    for i, st in enumerate(PATTERN):
        if b < 4 and st in (3, 6): continue          # the opening is sparser: DUN ........ DUN-DUN
        at(t0 + st * STEP, dun(big=intensity), (0.2 + 0.8 * intensity ** 2) * (1.15 if st >= 9 else 1.0), hits)
    if b in card_bars and b > 0: at(t0, braam(), 0.3 + 0.4 * intensity, hits)
    if b >= 6: at(t0, brass([A, E * 2, A * 2] if b % 2 == 0 else [F, C * 2, F * 2]), 0.5 * intensity, pads)
    if b >= 10 and b < end_bar: at(t0, strings16(A if b % 2 == 0 else F, BAR, STEP), 0.16, pads)
at(0, braam(3.0), 0.7, hits)                                                     # IN A WORLD...
at(0, choir([A, E * 2, A * 2], 9.0, 3.0), 0.22, pads)                           # ominous choir under the first act
at(6 * BAR, choir([A, C * 2, E * 2, A * 2], 6.0, 1.0), 0.28, pads)              # it swells when the hero turns up
at(10 * BAR, choir([F, A * 2, C * 4, F * 2], 4.5, 0.6), 0.32, pads)
s_bar = min(silent); at(s_bar * BAR - 1.5, riser(1.5), 0.5, hits); at(s_bar * BAR + 0.15, braam(2.0), 0.55, hits)   # dead air, one hit, then...
# the finale: SLATHER slams in, full choir and brass, then DUN DUN DUN DUN-DUN under COMING THIS SUMMER and a last boom
f0 = (s_bar + 1) * BAR
at(f0, dun(1.3), 1.2, hits); at(f0, braam(3.5), 0.8, hits)
at(f0, choir([A / 2 * 2, E * 2, A * 2, C * 4, E * 4], 6.5, 0.4), 0.45, pads)
at(f0, brass([A, E * 2, A * 2, C * 4], 3.0), 0.6, pads)
at(f0 + 2 * BAR, brass([F, C * 2, F * 2, A * 2], 3.0), 0.6, pads)
for b in (end_bar, end_bar + 1):
    for st in PATTERN: at(b * BAR + st * STEP, dun(1.2), 1.1 if st >= 9 else 0.95, hits)
at(TOTAL - 0.35, dun(1.4), 1.3, hits); at(TOTAL - 0.35, braam(3.0), 0.7, hits)
mix = reverb(hits, 2.8, 0.45) + reverb(pads, 3.2, 0.3)
mix = mix[:int((TOTAL + 2.2) * SR)]                                              # let the last boom ring out over black
fade = int(1.6 * SR); mix[-fade:] *= np.linspace(1, 0, fade) ** 2
mix = mix / (np.max(np.abs(mix)) + 1e-9); mix = np.tanh(1.5 * mix) / np.tanh(1.5) * 0.95
pcm = (np.stack([mix, mix], 1) * 32767).astype('<i2')
with wave.open(D + '/score3.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('score', round(TOTAL, 2), 's +2.2 s ring-out')

TAIL = 2.2   # black after the end frame while the last hit rings
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-i', D + '/score3.wav', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
                       '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
nf = int((TOTAL + TAIL) * FPS)
for f in range(nf):
    T = f / FPS
    ff.stdin.write((render(T) if T < TOTAL else BLACK).tobytes())
    if f % 300 == 0: print('frame', f, '/', nf, flush=True)
ff.stdin.close(); ff.wait(); print('done', OUT)
