"""v10: v9's picture and audio unchanged, except the end frame (SLATHER / SUN FIGHTER / COMING THIS SUMMER) slams in over black."""
import math, random, subprocess, sys
from PIL import Image, ImageDraw
D = sys.argv[1]; SRC = sys.argv[2]; OUT = sys.argv[3]
W, H, FPS, BAR = 1080, 1920, 30, 1.5
END_T0, END_DUR = 26.25, 4 * BAR
BLACK = Image.new('RGB', (W, H)); WHITE = Image.new('RGB', (W, H), (255, 251, 224))
SLAT = Image.open(D + '/slat.png').convert('RGBA'); FIGHT = Image.open(D + '/fight.png').convert('RGBA')
SLAT4 = SLAT.resize((SLAT.width * 3, SLAT.height * 3), Image.NEAREST); FIGHT3 = FIGHT.resize((FIGHT.width * 3, FIGHT.height * 3), Image.NEAREST)
WORDS = {k: (lambda im: im.crop(im.getbbox()))(Image.open(f'{D}/cards/{k}.png').convert('RGBA')) for k in ('w_coming', 'w_this', 'w_summer')}
def overlay(base, img, a=1.0, dx=0, dy=0):
    im = base.convert('RGBA')
    if a < 1: img = img.copy(); img.putalpha(img.getchannel('A').point(lambda v: int(v * a)))
    im.paste(img, (dx, dy), img); return im.convert('RGB')
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
    d = ImageDraw.Draw(img); r = 80 + u * 2400; w = int(36 * (1 - u / 0.45)) + 2
    d.ellipse([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5], outline=(255, 240, 190), width=w); return img
SLAMS = [(0.0, 'slat'), (BAR, 'fight'), (2 * BAR, 'w_coming'), (2.5 * BAR, 'w_this'), (3 * BAR, 'w_summer')]
def render_end(u):   # same slams, flashes, shockwaves and shake as v9, but over black instead of the Sun and the beach
    out = BLACK.copy()
    out = slam_in(out, SLAT4, u, 620, big=3.4, dur=0.2)
    out = slam_in(out, FIGHT3, u - BAR, 1000, big=2.4, dur=0.14, x=W // 2 + 40)
    for k, (t0, name) in enumerate(SLAMS[2:]):
        out = slam_in(out, WORDS[name], u - t0, 1300 + k * 170, big=2.2, dur=0.12)
    for t0, _ in SLAMS:
        v = u - t0
        if 0 <= v < 0.2: out = Image.blend(out, WHITE, 0.75 * (1 - v / 0.2) * (1 if t0 == 0 else 0.5))
        out = ring(out, v, W // 2, 620 if t0 == 0 else 1000)
    amt = max([max(0, 40 * (1 - (u - t0) / 0.35)) if u >= t0 else 0 for t0, _ in SLAMS] + [0])
    return shake(out, amt, int(u * 60))
mid = D + '/end.mp4'
ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', mid], stdin=subprocess.PIPE)
for f in range(int(END_DUR * FPS)): ff.stdin.write(render_end(f / FPS).tobytes())
ff.stdin.close(); ff.wait()
# splice: v9 up to the end frame + the new end frame + v9's black tail, with v9's audio untouched
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-i', mid, '-filter_complex',
    f'[0:v]trim=0:{END_T0},setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[0:v]trim=start={END_T0 + END_DUR},setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]',
    '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', OUT], check=True)
print('done', OUT)
