# Art spec for Slather Ring

The game runs at **480 × 270 pixels** and is scaled up to fit the screen with crisp, unsmoothed pixels. Draw everything at that native size: one pixel in your file is one game pixel.

## How to deliver

- Transparent **PNG** with hard pixel edges: no anti-aliasing and no semi-transparent edge pixels.
- Each animation is a **horizontal strip** of equal-size frames, left to right, with no gaps. Frame 0 sits at x = 0.
- Use the exact file names below and put them in an `assets/` folder next to `index.html`.
- Keep the frame size and frame count listed. If you need a different size or count, say so and the code will be adjusted.
- Feet and ground contact go on the **bottom row** of the frame, centred horizontally. The game anchors sprites by their bottom centre.

Once the files are in place, set `USE_ASSET_FILES = true` near the top of `index.html`. Any file that's missing keeps its stand-in art.

## The Sun

The Sun is built from separate parts so the code can animate it. It stands in the sea and is visible from the waist up. The sea line cuts it off around the waist.

| File | Frame size | Frames | Notes |
|---|---|---|---|
| `sun_torso.png` | 140 × 112 | 1 | Waist up, without the head. Shoulders sit about 16 px down from the top. The neck is hidden behind the head. |
| `sun_head.png` | 176 × 140 | 5 | **Done, from your art.** The whole spiky head with the face drawn in, one expression per frame, centred in the frame. The order is: worried, squinting grimace, sly grin, big laugh, rage. The game uses worried when the Sun is defeated or shocked, the grimace when it's hurt or grossed out, the sly grin as its normal face, the laugh when it laughs, and rage for attacks and laser eyes. The lasers fire from 30 px either side of centre and 5 px below the middle, which is where the rage face's eyes are. |
| `sun_hand.png` | 80 × 80 | 5 | **Done, from your art.** The **left** hand (the right is the mirror image), in this order: open claw, fist, then three claws at slightly different tilts (sweep, reaching, grab). The fist is cut from the slam pose. The claws are the raised hand from the arms-up pose, fingers up as in that pose, with the wrist at the bottom right. The bottom of each frame is the point that touches the ground. |

The arms are drawn by code so they can stretch to wherever the hands go. They're thick, with a black outline, orange shading on the underside and a highlight on top, like your art. They bend at the elbow, more when the hand is close in, and come out from behind the head. If you'd like a specific arm shape, such as a muscle bulge, send a straight arm drawn on its own and it can be stretched along the same path.

## The bogan

| File | Frame size | Frames | Notes |
|---|---|---|---|
| `bogan.png` | 32 × 48 | 28 | Seen **from behind**, facing the Sun. |
| `bogan_burnt.png` | 32 × 48 | 28 | The same sheet with lobster-red skin. The game fades it in as his sunburn rises. |

Frame order for both sheets:

| Frames | Animation |
|---|---|
| 0–1 | Idle (breathing bob) |
| 2–7 | Run cycle |
| 8–12 | Roll |
| 13–18 | Run cycle while squirting, with the bottle arm raised and pointing up at the Sun |
| 19 | Hurt |
| 20 | Dead, lying flat |
| 21 | Victory, both arms up |
| 22–27 | Run cycle while dual-wielding, with both arms raised and a bottle in each hand |

## Items, props and effects

| File | Frame size | Frames | Notes |
|---|---|---|---|
| `slather.png` | 16 × 24 | 1 | SPF bottle pickup |
| `slather2.png` | 26 × 24 | 1 | Twin bottles. Picking them up turns on dual-wield mode. |
| `hat.png` | 22 × 13 | 1 | Black Slather bucket hat with the white sun logo (the pickup). When worn, the code draws it on the bogan's head from behind. |
| `potato.png` | 16 × 16 | 1 | Potato cake (heals 20) |
| `dimsim.png` | 16 × 16 | 1 | Dim sim (heals 14) |
| `seagull.png` | 32 × 24 | 4 | Flap cycle, **facing right** |
| `umbrella.png` | 56 × 64 | 1 | Beach umbrella. The pole base is at the bottom centre. This is the shade from the Solar Flare. |
| `fireball.png` | 14 × 14 | 2 | Spat fireball, flicker |
| `splat.png` | 16 × 16 | 3 | Sunscreen splat (currently unused; the code draws blobs) |
| `logo.png` | 44 × 44 | 1 | The Slather line-drawn sun for the title screen |

When the bogan is hit, the code adds the comedy on top of these sprites: flames, eyes popping out on stalks, singed hair and a speech bubble. When he dies, he turns into `skeleton.png` and then `ash.png`, and code draws his mullet and thongs on top.

## Beachgoers, lifesaver and sea life

The beachgoers are seen **side-on, facing right**; the right-to-left walkers are mirrored. The feet go on the bottom row. Each person has a 4-frame walk cycle, then any special poses listed below, then one last frame pointing ahead (used when they crowd round the bogan in the bucket hat), so a plain beachgoer sheet has 5 frames. Anyone the Sun hits catches fire, turns into the skeleton and then into the ash pile. About half the beachgoers have tattoos: each `npc_*.png` also needs a `npc_*_tat.png` version with the same frames plus some ink.

| File | Frame size | Frames | Notes |
|---|---|---|---|
| `npc_bikini.png` | 28 × 40 | 5 | Person in a bikini |
| `npc_boardies.png` | 28 × 40 | 5 | Person in board shorts |
| `npc_surfer.png` | 28 × 40 | 5 | Surfer in a wetsuit, carrying a surfboard |
| `npc_bodyboarder.png` | 28 × 40 | 5 | Person carrying a bodyboard |
| `npc_muscle.png` | 28 × 40 | 5 | Musclehead in red shorts and sunnies |
| `npc_oldie.png` | 28 × 40 | 5 | Old, wrinkly, deeply tanned man in blue speedos, bald on top with grey sides and a pot belly |
| `npc_italian.png` | 28 × 40 | 5 | Man with black curly hair and sunnies in white speedos. He lies on a towel to tan. |
| `npc_walker.png` | 28 × 40 | 5 | Dog walker. The leash is drawn by code. |
| `npc_lifesaver.png` | 28 × 40 | 5 | Lifesaver in the red and yellow cap. Jogs on and drops the Slather. |
| `npc_onepiece.png` | 28 × 40 | 5 | Woman in a one-piece swimsuit |
| `npc_surfergirl.png` | 28 × 40 | 5 | Surfer in a wetsuit with a ponytail, carrying a pink board |
| `npc_bodyboardgirl.png` | 28 × 40 | 5 | Bodyboarder with a ponytail |
| `npc_walkerf.png` | 28 × 40 | 5 | Dog walker in a sun hat |
| `npc_eshay.png` | 28 × 40 | 9 | Eshay in a black tracksuit, cap and white sneakers with a red bumbag across his chest. Frames 0–3 walk, 4–7 gabber dance (bounce, knee up with fist pumped, bounce, other knee up). |
| `npc_influencer.png` | 28 × 40 | 8 | Influencer in a pink bikini and sunnies. Frames 0–3 walk, 4 hand on hip, 5 peace sign, 6 hair flip. |
| `npc_boyfriend.png` | 28 × 40 | 7 | Her boyfriend. Frames 0–3 walk, 4–5 crouched taking a photo on his phone (5 has the screen lit). |
| `npc_lifesaverf.png` | 28 × 40 | 5 | Lifesaver with a ponytail under the cap |
| `sandcastle.png` | 26 × 24 | 2 | Frame 0 standing, frame 1 knocked flat |
| `jeep.png` | 54 × 30 | 3 | Lifeguard jeep facing right. Frames 0–1 are driving (wheels turning); frame 2 has an empty driver's seat, used once it's on fire. |
| `crab.png` | 14 × 10 | 2 | Scuttling crab |
| `crab_cooked.png` | 14 × 10 | 1 | Bright red cooked crab |
| `dog.png` | 18 × 12 | 2 | Walk cycle. It runs away when its owner gets torched. |
| `skeleton.png` | 28 × 40 | 1 | Standing skeleton that the burnt beachgoers become |
| `ash.png` | 24 × 10 | 1 | Ash pile |
| `surfer.png` | 24 × 22 | 1 | Surfer on a board, riding a wave out at sea. The wave is drawn by code. |
| `dolphin.png` | 22 × 14 | 2 | Frame 0 is nose up, rising. Frame 1 is nose down, diving. |
| `boat.png` | 36 × 20 | 1 | Small fishing boat on the horizon |
| `jetski.png` | 26 × 14 | 1 | Jet ski with a rider |

## Background

The current backgrounds are generated by code. To replace them, send one **480 × 270** image per phase:

| Phase | Name | Mood |
|---|---|---|
| 1 | Morning | Blue sky |
| 2 | High Noon | Orange |
| 3 | Heat Dome | Red |
| 4 | Sunset | Purple, used for the victory screen |

Layout lines to keep:

| y (px) | Line |
|---|---|
| 0–104 | Sky |
| 104 | Horizon |
| 104–152 | Sea |
| 152 | Shoreline. The Sun is cut off here. |
| 166–244 | The area the bogan can walk on. Keep it clear of anything that looks solid. |
| 248–270 | Covered by the boss health bar |

The scene is an Australian cove. On the left is one headland, covered in green bush, with gum trees along its ridge, a few knobs of sandstone poking through, and a small beach at its foot where it meets the water. The right side is open sea. The code animates lines of swell rolling in from the horizon toward the beach and breaking on the shore, and wash running up the headland's beach, so the headland is a separate layer drawn over the sea. To replace it, send one **480 × 270** transparent PNG per phase, `land_1.png` to `land_4.png`, containing only the headland and its beach. Keep it to the left of x ≈ 185 so the sea behind the Sun stays clear.

Name the backgrounds `bg_1.png` to `bg_4.png`. They aren't loaded yet; loading them is a one-line change when they arrive.

## Audio

All sound is currently generated by code: SNES-style music and sound effects. The Sun has no spoken voice. Its lines appear as text only.
