# Slather Ring: Shadow of the Sun

A 16-bit-style boss fight in the browser. A bogan with a Slather bottle takes on The Sun, which looms out of the sea from the waist up and attacks with its giant hands.

Open `index.html` in any modern browser. On a computer, use the keyboard and mouse. On a phone, on-screen touch controls appear; it plays best with the phone turned sideways.

## Controls

| Action | Keyboard | Touch |
|---|---|---|
| Move | W A S D / arrows | Drag on the left side |
| Squirt sunscreen | Hold J or the left mouse button | Hold SQUIRT |
| Roll (dodge, with a moment of invincibility) | Space | ROLL |
| Pause | Esc / P | PAUSE |

## The intro

Starting from the title screen plays a short cutscene. The bogan wanders onto a busy beach and stretches. Then the Sun rises out of the sea on the horizon, laughing, with its eyes glowing red. It stomps up to the shore and fires a warning ray across the sand, and the beachgoers scream and run. Press Enter (or tap) to skip it. Retrying after a death goes straight back into the fight.

## The fight

- **Fire:** every hit sets the bogan on fire. His eyes pop out, his mullet singes and his skin reddens. Slams, sweeps, grabs, fireballs and laser beams all leave patches of burning sand behind them.
- **Sunburn:** with no SPF, the sunburn meter fills. When it's full, you take damage and slow down.
- **Lifesavers** jog onto the beach and drop a **Slather bottle**. Running over one gives 8 seconds of **SPF50+ UV shield**. While it's on, attacks bounce off you and hurt the Sun, the sunburn stops, and the fire goes out. The Solar Flare still gets through the shield, at half damage. Sometimes they drop **twin bottles**, which also give 10 seconds of **dual-wield**: two streams of sunscreen at once.
- **Seagulls** fly past and drop a **potato cake** (+25 health) or a **dim sim** (+18).
- **Beachgoers** wander through: bikinis, boardies, surfers, bodyboarders, a dog walker and a musclehead with a boom box. Some lay down a towel and sunbake. None of them are safe. If an attack hits them, they burn to a skeleton, then to ash. Surfers, dolphins, a fishing boat and a jet ski pass by out at sea, behind the Sun.
- **Phase 1, Morning:** flaming Sunny Slap fist slams, Beach Sweep, the Eye Laser (the Sun's favourite attack), UV Rain fireballs, and Sun Ray columns.
- **Phase 2, High Noon** (at 60% health): double slams and sweeps, more fireballs, and the Grab.
- **Phase 3, Heat Dome** (at 25% health): triple slams with shockwaves, two laser beams at once, faster attacks, and the Solar Flare. Get under an umbrella before it goes off.

## The Sun's personality

The Sun shows its lines in yellow speech bubbles. It doesn't speak them aloud.

| When | Lines |
|---|---|
| It torches a beachgoer and heals 80 HP (`KILL_HEAL`) | "ANOTHER SACRIFICE TO THE SUN GOD! HAHAHAH!" / "MMMM... LOBSTER!!!" |
| You hit it (every 110 damage, it also pulls a face, reels back and gets angry) | "ARRGGHHHH! SPF 50+" / "IT HURTS! AND IT'S SO SMOOTH AND EASY TO APPLY!" |
| It hits you while your UV shield is up and the attack bounces back | "NOOO! THE SPF... IT'S TOO STRONG!!!" / "THE SPECIALLY FORMULATED SPF 50+ OF SLATHER IS IMPENETRABLE" |

## Sound

- **Music:** SNES-style chiptune. There's a sunny beach tune for the intro, then the boss theme, which gets faster and busier in each phase.
- **Sound effects:** a rising whoosh as a fist or hand winds up, heavy slams, a roaring wall of fire for the sweep and the laser trail, electric buzzing for the lasers, a charging hum and zaps for the sun rays, falling whistles for the fireballs, crackling fire, a croaky laugh and grunts from the Sun, waves in the background, screams, and jingles for winning and losing.

## Art

All art is currently stand-in pixel art drawn by code. See [ASSETS.md](ASSETS.md) for the sprite sizes, frame orders and file names the real art should use.

## Tuning

The numbers near the top of the script in `index.html` control the difficulty:

| Setting | What it controls |
|---|---|
| `DMG` | Damage from each attack |
| `HEAL` | Health restored by each snack |
| `BOSS_MAX` | The Sun's health |
| `UV_RATE` | How fast the sunburn meter fills |
| `GAP` | Rest time between the Sun's attacks |
| `SPF_TIME` | How long SPF lasts |
| `DUAL_TIME` | How long dual-wield lasts |
| `HIT_INVULN` | How long you're protected after being hit |

`legacy-3d.html` is the earlier 3D prototype, kept for reference.
