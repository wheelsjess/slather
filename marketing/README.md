# Marketing

## `sun-fighter-teaser-v3-vertical.mp4` (9:16)

The v3 teaser re-cut for Reels, TikTok and Shorts at 1080×1920, with the same edit and score. Every shot is a tight vertical window onto the game (135×240 game pixels at exactly 8×). Text that's too wide for a vertical frame is rebuilt at full size:

- the Pokémon "A wild ESHAY appeared!" box, typed out;
- FINISH HIM !! in Metal Mania;
- the end title, built from the game's own SLATHER and SUN FIGHTER art (exported by `teaser-src/logo_export.js`), slammed over the Sun.

`sun-fighter-teaser-v3-vertical-preview.mp4` is a small 720×1280 copy. The source is `teaser-src/make_teaser_v3_vertical.py`.

## `sun-fighter-teaser-v3.mp4` (current)

33 seconds of picture plus a 2-second ring-out, 16:9 at 1920×1080. It opens wide (the Sun rising, then the whole battlefield) and then cuts to close-ups of the best moments:

- the Sun's fist with the bogan's legs kicking ("YOU'RE MINE NOW, GARY");
- a beachgoer going up in flames, then a skeleton;
- the Sun cackling "ANOTHER SACRIFICE TO THE SUN GOD!";
- "A wild ESHAY appeared!" and his gabber dance;
- the ice cream van exploding;
- "MY EYES!!! THEY STING!!!"

Close-ups on moving characters follow them using a position log recorded with the footage (`teaser-src/rec_tracked.js`).

The score climbs in five stages to a crescendo:

1. a heartbeat and a sparse clank;
2. the full DUN-DUN rhythm, brass and strings;
3. a key change up, taiko drums and a bigger choir for the hero;
4. another key up, frantic strings, and a snare roll and riser into dead silence;
5. the finale, a key higher again, with full choir, brass and drums and a final boom.

`sun-fighter-teaser-v3-preview.mp4` is a small 720p copy. The source is `teaser-src/make_teaser_v3.py`.

## `sun-fighter-teaser-30.mp4` (current)

A 30-second 16:9 teaser (1920×1080), plus a 2-second ring-out on black. It uses the same cards and footage as the longer teaser below, cut tighter and with every cut on the beat. The score is an original, deliberately over-the-top action-movie piece:

- an industrial DUN… DUN… DUN… DUN-DUN rhythm in 13/16, with metal clanks over deep drums and big reverb;
- brass stabs, a swelling choir, BRAAAMs on every card and a driving low-string ostinato;
- a silent bar before THIS SUMMER..., then a full finale on the title.

`sun-fighter-teaser-30-preview.mp4` is a small 720p copy for previewing. The source is `teaser-src/make_teaser_30.py`.

## `sun-fighter-teaser.mp4`

A 48-second 16:9 teaser (1920×1080, 30 fps). Full-frame gameplay, some in slow motion, cuts against black cards in the game's yellow pixel font: IN A WORLD... / WHERE THE SUN... / IS NOT YOUR FRIEND... / ONE MAN / ONE TUBE OF SLATHER SPF 50+ / IS READY TO FIGHT BACK / THIS SUMMER... It ends on the title screen with COMING THIS SUMMER. The footage is recorded at exactly 4× the game's resolution, so the pixels stay crisp.

The scripts are in `teaser-src/` and work the same way as the trailer's (below). `make_teaser.py` holds the edit list (`SEG`): each shot's source clip, start time, speed (under 1 is slow motion) and framing.

## `sun-fighter-trailer.mp4`

A 35-second vertical (1080×1920, 30 fps) parody movie trailer for Reels, TikTok and Shorts. It's real gameplay with trailer captions and a synthesised score: BRAAAM hits, a riser, a chiptune take on the fight theme, a gong for FINISH HIM, and an end card with the URL and prize.

### Rebuilding it

The scripts in `trailer-src/` are what made it. They expect a scratch folder; edit the paths at the top of each before running.

1. `rec.js` (Node + Playwright) plays scripted scenes in a headless browser and saves each as 60 fps JPEG frames with timestamps. It's served a copy of `index.html` with the on-screen buttons and "ENTER TO SKIP" removed.
2. `cards.js` renders the caption cards in `cards.json` (laid out by `cards.html`) as transparent 1080×1920 PNGs.
3. `make_trailer.py` (Python with NumPy and Pillow, plus ffmpeg) holds the edit list (`SEG`), composes every frame, synthesises the score in sync with the cuts, and encodes the MP4.
