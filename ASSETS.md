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
| `sun_head.png` | 150 × 140 | 1 | Spiky head **with no face**. The centre of the face circle must be at (75, 80) in the frame. |
| `sun_face.png` | 96 × 72 | 7 | Faces drawn over the head, centred. The order is: smug, toothy grin, rage with laser eyes, hurt, defeated, shocked, grossed out (sunscreen in its mouth). The eyes sit about 18 px either side of centre and 6 px above the middle, because the lasers fire from there. |
| `sun_hand.png` | 64 × 64 | 5 | Poses in this order: open palm, fist, flat palm-down slam, pointing finger, grabbing claw. Draw the **left** hand; the right hand is the mirror image. The wrist goes at the top centre. |

The arms are drawn by code as thick yellow lines with a black outline, so they can stretch to wherever the hands go. If you want a textured arm instead, send one 16 × 16 tile that repeats along the arm.

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
| `potato.png` | 16 × 16 | 1 | Potato cake (heals 25) |
| `dimsim.png` | 16 × 16 | 1 | Dim sim (heals 18) |
| `seagull.png` | 32 × 24 | 4 | Flap cycle, **facing right** |
| `umbrella.png` | 56 × 64 | 1 | Beach umbrella. The pole base is at the bottom centre. This is the shade from the Solar Flare. |
| `fireball.png` | 14 × 14 | 2 | Spat fireball, flicker |
| `splat.png` | 16 × 16 | 3 | Sunscreen splat (currently unused; the code draws blobs) |
| `logo.png` | 44 × 44 | 1 | The Slather line-drawn sun for the title screen |

When the bogan is hit, the code adds the comedy on top of these sprites: flames, eyes popping out on stalks, singed hair and a speech bubble. When he dies, he turns into `skeleton.png` and then `ash.png`, and code draws his mullet and thongs on top.

## Beachgoers, lifesaver and sea life

The beachgoers are seen **side-on, facing right**; the right-to-left walkers are mirrored. The feet go on the bottom row. Each person has a 4-frame walk cycle. Anyone the Sun hits catches fire, turns into the skeleton and then into the ash pile.

| File | Frame size | Frames | Notes |
|---|---|---|---|
| `npc_bikini.png` | 28 × 40 | 4 | Person in a bikini |
| `npc_boardies.png` | 28 × 40 | 4 | Person in board shorts |
| `npc_surfer.png` | 28 × 40 | 4 | Surfer in a wetsuit, carrying a surfboard |
| `npc_bodyboarder.png` | 28 × 40 | 4 | Person carrying a bodyboard |
| `npc_muscle.png` | 28 × 40 | 4 | Musclehead with a boom box on his shoulder. Code adds the music notes. |
| `npc_walker.png` | 28 × 40 | 4 | Dog walker. The leash is drawn by code. |
| `npc_lifesaver.png` | 28 × 40 | 4 | Lifesaver in the red and yellow cap. Jogs on and drops the Slather. |
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

Name them `bg_1.png` to `bg_4.png`. They aren't loaded yet; loading them is a one-line change when they arrive.

## Audio

All sound is currently generated by code: SNES-style music and sound effects. The Sun has no spoken voice. Its lines appear as text only.
