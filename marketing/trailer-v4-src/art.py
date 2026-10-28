"""Builds the hero layers for the new trailer scenes from the loading-screen art: a cut-out of the hero, the right-hand tube, and lighting variants."""
import numpy as np
from collections import deque
from PIL import Image, ImageFilter
def components(mask):
    """label 4-connected regions of a boolean mask; returns (labels, sizes)"""
    h, w = mask.shape; lab = np.zeros((h, w), int); sizes = [0]; n = 0
    for sy in range(h):
        for sx in range(w):
            if mask[sy, sx] and not lab[sy, sx]:
                n += 1; q = deque([(sy, sx)]); lab[sy, sx] = n; c = 0
                while q:
                    y, x = q.popleft(); c += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]: lab[ny, nx] = n; q.append((ny, nx))
                sizes.append(c)
    return lab, sizes
def fill_holes(mask):
    lab, sizes = components(~mask); h, w = mask.shape
    edge = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
    return mask | ~np.isin(lab, list(edge))
SRC = '/home/user/slather/assets/loading_bogan.jpg'
im = Image.open(SRC).convert('RGB'); A = np.array(im).astype(int)
# hero mask: everything that isn't the near-black backdrop or the smoke at his feet
lum = A.sum(axis=2); mask = lum > 70
yy = np.arange(A.shape[0])[:, None]; smoke = (yy > 560) & (lum < 200) & (np.abs(A[:, :, 0] - A[:, :, 2]) < 25)
mask &= ~smoke
m = Image.fromarray((mask * 255).astype('uint8')).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
mm = np.array(m) > 0; lab, sizes = components(mm); keep = int(np.argmax(sizes))   # keep only the hero, drop the dirt clumps
mm = lab == keep
xx = np.arange(A.shape[1])[None, :]; boots = ((xx > 135) & (xx < 250)) | ((xx > 380) & (xx < 525))
mm &= ~((yy > 592) & ~boots)                                                       # trim the dirt the boots are standing in
m = Image.fromarray((mm * 255).astype('uint8'))
hero = im.convert('RGBA'); hero.putalpha(m); hero.save('hero_cut.png')
# the right-hand tube: yellow body plus its dark outline and cap, inside its box, minus skin
x0, y0, x1, y1 = 455, 355, 545, 485
box = A[y0:y1, x0:x1]; r, g, b = box[:, :, 0], box[:, :, 1], box[:, :, 2]
yellow = (r > 150) & (g > 120) & (b < 120) & (r - b > 90)
dark = (r + g + b < 260)
skin = (r > 150) & (g > 80) & (g < 170) & (b > 60) & (r - g > 40) & ~yellow
skin_grown = np.array(Image.fromarray((skin * 255).astype('uint8')).filter(ImageFilter.MaxFilter(3))) > 0
tm = np.array(Image.fromarray((yellow * 255).astype('uint8')).filter(ImageFilter.MaxFilter(3))) > 0   # take in the dark outline
tm = fill_holes(tm)                                                                                  # and the black SLATHER lettering
tm &= ~skin_grown; tm &= (r + g + b > 40)
lab, sizes = components(tm); tm = lab == int(np.argmax(sizes))
tube = Image.fromarray(box.astype('uint8')).convert('RGBA'); tube.putalpha(Image.fromarray((tm * 255).astype('uint8')).filter(ImageFilter.MedianFilter(3)))
t = np.array(tube); ys, xs = np.nonzero(t[:, :, 3])
# patch the notch the thumb left in the top edge: copy the tube's own yellow across the gap, row by row, between its outer edges
for y in range(0, 40):
    row = np.nonzero(t[y, :, 3])[0]
    if len(row) < 2: continue
    a, b2 = row[0], row[-1]; gap = [x for x in range(a, b2) if not t[y, x, 3]]
    for x in gap: t[y, x] = t[y, a + 3] if t[y, a + 3, 3] else (230, 200, 40, 255)
tube = Image.fromarray(t); tube.save('tube_cut.png'); print('tube', tube.size, 'hero', hero.size)
