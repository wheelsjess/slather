# Marketing

## `sun-fighter-trailer.mp4`

A 35-second vertical (1080×1920, 30 fps) parody movie trailer for Reels, TikTok and Shorts. It's real gameplay with trailer captions and a synthesised score: BRAAAM hits, a riser, a chiptune take on the fight theme, a gong for FINISH HIM, and an end card with the URL and prize.

### Rebuilding it

The scripts in `trailer-src/` are what made it. They expect a scratch folder; edit the paths at the top of each before running.

1. `rec.js` (Node + Playwright) plays scripted scenes in a headless browser and saves each as 60 fps JPEG frames with timestamps. It's served a copy of `index.html` with the on-screen buttons and "ENTER TO SKIP" removed.
2. `cards.js` renders the caption cards in `cards.json` (laid out by `cards.html`) as transparent 1080×1920 PNGs.
3. `make_trailer.py` (Python with NumPy and Pillow, plus ffmpeg) holds the edit list (`SEG`), composes every frame, synthesises the score in sync with the cuts, and encodes the MP4.
