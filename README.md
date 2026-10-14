# Slather Ring

A 16-bit-style boss fight in the browser. A bogan with a Slather bottle takes on The Sun, which looms out of the sea from the waist up and attacks with its giant hands.

Open `index.html` in any modern browser. On a computer, use the keyboard and mouse. On a phone, on-screen touch controls appear; it plays best with the phone turned sideways.

## Controls

| Action | Keyboard | Touch |
|---|---|---|
| Move | W A S D / arrows | Drag on the left side |
| Squirt sunscreen (one squirt per click) | Click, or press J | Tap SQUIRT |
| Roll (dodge, with a moment of invincibility) | Space | ROLL |
| Pause | Esc / P | PAUSE |

## Title and loading screens

The game opens on an arcade attract screen. It's a standalone illustrated frame, separate from the game view, with a teal sky, big painted clouds, a curving golden beach and surf rolling in. The Sun rises out of the sea in a blaze of flame, smiling. **SLATHER** slams onto the screen in sunset chrome, and a ripple of light runs across the metal every few seconds. The bogan runs in, cigarette going, and flips the Sun the bird (it looks suitably shocked). Then **SUN FIGHTER** is slapped on in red brush capitals beside him. Then it says **HIT ENTER TO INSERT COIN** (or TAP on a phone), with the top five times underneath. Press Enter (or tap) to skip straight to that.

Inserting a coin goes to a **Skyrim-style loading screen**. The battle-ready bogan, with a tube of Slather in each fist, stands in the dark while smoke drifts along the floor and the camera slowly pushes in. HOW TO PLAY sits in the top right, with the in-game sprites beside each item, and a TIP fades through some skin cancer facts in the bottom right, under a thin loading bar. The text is set in a serif over the canvas so it stays crisp. When it's loaded, press Enter (or tap) to start. To add tips, edit the `LOADING_TIPS` list in `index.html`.

## The intro

Starting from the title screen plays a short cutscene. The bogan wanders onto a busy beach and stretches. Then the Sun rises out of the sea on the horizon, laughing, with its eyes glowing red. It stomps toward the shore and wrecks everything on the way: the first stomp flips a jet ski into the air, its eye lasers blow up a fishing boat, and it plucks a dolphin out of the water and hurls it at the camera. Then it fires a warning ray across the sand, and the beachgoers scream and run. Press Enter (or tap) to skip it. Retrying after a death goes straight back into the fight.

## The fight

- **Fire:** every hit sets the bogan on fire. He throws his arms up with his mullet in flames, and his skin reddens. Slams, sweeps, grabs, fireballs and laser beams all leave patches of burning sand behind them.
- **Sunburn:** with no SPF, the sunburn meter fills over time, faster in later phases, and fire hits add to it. Your skin reddens as it fills. When it's full, you get SUNBURNT: you take damage, catch fire and slow down for 2 seconds, then the meter resets. SPF stops it filling, and picking up Slather knocks most of it off.
- **Lifesavers** jog onto the beach and drop a **Slather bottle**. Running over one gives 8 seconds of **SPF50+ UV shield**. While it's on, attacks bounce off you and hurt the Sun, the sunburn stops, and the fire goes out. The Solar Flare still gets through the shield, at half damage. Sometimes they drop **twin bottles**, which also give 10 seconds of **dual-wield**: two streams of sunscreen at once.
- **Slather bucket hat:** every minute or so a black Slather bucket hat blows in across the sand. Picking it up announces **SLATHER BUCKET HAT EQUIPPED** and **UV PROTECTION + STYLE BONUS**. For 20 seconds you can't be hurt at all and your sunburn stops. The beachgoers crowd round, then stand watching, pointing and commenting ("DAMN HE LOOKS GOOD", "THIS GUY RULES ASS", "SLATHER IS MY BRAND OF PREFERENCE"). When the hat wears off, they wander away. They're still in the firing line though.
- **Seagulls** fly past and drop a **potato cake** (+20 health) or a **dim sim** (+14).
- **Beach life:** crabs scuttle about the wet sand and seaweed lines the shore. Mates throw a frisbee to each other. Two sandcastles sit on the sand; run over one and it falls apart (someone builds a new one elsewhere later). A lifeguard jeep drives past now and then. If the Sun hits it, the jeep goes up in flames and the lifeguard crawls out on fire.
- **Beachgoers** wander through, about half women and half men, and around half of them tattooed: bikinis, one-pieces, boardies, surfers and bodyboarders of both kinds, dog walkers, a musclehead, and a leathery old bloke in budgie smugglers who loves a sunbake. An eshay lad with a bumbag across his chest stops to gabber dance (if he's torched: "I'M COOKED ADLAAAAAAY!"). An influencer poses by the water while her boyfriend crouches beside her with his phone ("BABE, MAKE SURE I LOOK HOT AF"). A curly-haired guy lays out his towel and announces "I'M 1/8TH ITALIAN, I DON'T NEED SUNSCREEN", right up until he goes "MAMA MIA!". Some lay down a towel and sunbake. None of them are safe. If an attack hits them, they burn to a skeleton, then to ash. Surfers, dolphins, a fishing boat and a jet ski pass by out at sea, behind the Sun. A big Bass Strait ferry pokes in from the right on the horizon. Its passengers wander the sun deck, and now and then one lurches to the rail and spews over the side.
- **Phase 1, Morning:** flaming Sunny Slap fist slams, Beach Sweep, the Eye Laser (the Sun's favourite attack), UV Rain fireballs, and Sun Ray columns.
- **The Grab:** a hand shadows you, then snatches you up (or sometimes a beachgoer). The Sun cackles ("YOU'RE MINE NOW, GARY!!!") and lasers you point-blank, its hardest hit, its most devastating attack. A beachgoer it grabs doesn't survive. Roll out of the way, or have your UV shield up to bounce it off.
- **Phase 2, High Noon** (at 60% health): double slams and sweeps, more fireballs, and more grabs.
- **Phase 3, Heat Dome** (at 25% health): triple slams with shockwaves, two laser beams at once, faster attacks, and the Solar Flare. Get under an umbrella before it goes off.

## The clock and the leaderboard

A timer at the top of the screen counts the fight, starting when you take control after the intro. It stops the moment the Sun dies or you do. Win, and you enter three initials, arcade style: type them, or use up and down to change a letter and left and right to move, then press Enter. On a phone, tap the arrows above and below each letter, then OK. Then the leaderboard, "OFFICIAL SICKEST PEOPLE IN THE UNIVERSE", ranks the quickest kills, with your new run flashing. The top five also show on the title screen as **Legendary Slatherers**.

When the game is played from its claude.ai page, the board is shared. Everyone who opens the page and is allowed to add to it lands on the same board, and each player keeps their 10 best runs. People who can only view the page see the shared board, but their own times are saved on their device. Opened anywhere else, such as straight from `index.html`, the board only keeps times on that device.

## Easter eggs

- **The old man:** on the title screen, after the bogan flips off the Sun, a Zelda-style old man in a red robe shuffles in. He says "IT'S DANGEROUS TO GO ALONE! TAKE THIS." and lobs him a tube of Slather. The bogan catches it and holds it aloft, with sparkles and the item-get jingle.
- **A wild ESHAY appeared!** When an eshay turns up mid-fight, the screen strobes and the blinds open like a Pokémon encounter, then the text box types it out. While he's on the beach the music switches to hard gabber (distorted four-on-the-floor kick and a hoover lead at 184 BPM). It drops back to the normal fight music when he leaves or gets torched.
- **Loot:** when the bogan dies, his pockets spray out Diablo-style: VELCRO WALLET, CRACKED PHONE, COMMON KEYS, DARTS (HALF PACK), and a legendary-orange SLATHER SPF50+ with a light beam. Each lands with a rarity-coloured name plate.
- **Bin chickens:** leave a pickup on the sand for more than about 5 seconds and an ibis strolls in, grabs it and makes off. "BIN CHICKEN STOLE THE POTATO CAKE" shows up small in the top right.
- **The British backpacker:** milk-pale except for a lobster face, neck and arms, with a singlet tan line, socks and sandals and a huge pack. He wanders through saying "BIT HOT HERE, INNIT?" and if he's torched: "IT'S NOT COMING HOME!"

## Death and victory

Both are styled after Elden Ring. If you die, a dark band fades in across the screen with **YOU GOT BURNT** in big blood-red Roman capitals, slowly growing, then a parting line and "press Enter to try again". If you kill the Sun, **GREAT ENEMY SLATHERED** appears in gold as it sinks, with a fading ghost of the words swelling behind it and a low chord. Then the stats, the initials and the leaderboard follow.

## The boss name

Like a Souls boss, the Sun's name sits over its health bar in an off-white serif, left-aligned. It changes at each phase shift, fading out and back in with a golden flash:

| Phase | Name |
|---|---|
| 1, Morning | THE SUN, SCORCHER OF BACKS |
| 2, High Noon | THE SUN, MELTER OF THONGS |
| 3, Heat Dome | THE SUN, BRINGER OF MELANOMA |

## The Sun's personality

The Sun shows its lines in yellow speech bubbles. It doesn't speak them aloud.

| When | Lines |
|---|---|
| It torches a beachgoer and heals 55 HP (`KILL_HEAL`) | "ANOTHER SACRIFICE TO THE SUN GOD! HAHAHAH!" / "MMMM... LOBSTER!!!" |
| You hit it (every 75 damage, it also pulls a face, reels back and gets angry) | "ARRGGHHHH! SPF 50+" / "IT HURTS! AND IT'S SO SMOOTH AND EASY TO APPLY!" / "MY EYES!!! THEY STING!!!" |
| It gets caked in sunscreen (40+ splats), loses it, scrubs itself clean and flings the gunk across the beach. A glob that lands on you is a free 3-second top-up of SPF. | "GET THIS SPECIALLY FORMULATED SPF OFF OF ME!!!" / "I DO NOT APPROVE OF THIS INCREDIBLE SUNSCREEN PRODUCT!" |
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
| `PLAYER_TAKES` / `SUN_TAKES` | Multipliers on the damage each side takes (0.7 and 0.62). Lower both to make the fight last longer without changing the difficulty. |
| `HAT_TIME` | How long the bucket hat lasts |
| `HEAL` | Health restored by each snack |
| `BOSS_MAX` | The Sun's health |
| `UV_RATE` | How fast the sunburn meter fills |
| `GAP` | Rest time between the Sun's attacks |
| `SPF_TIME` | How long SPF lasts |
| `DUAL_TIME` | How long dual-wield lasts |
| `HIT_INVULN` | How long you're protected after being hit |

## Saved versions

- `versions/slather-ring-v1.html` is a frozen copy of the game with the stand-in pixel art, saved before the real art references came in. Open it in a browser to play it. In git it's commit `bb40042` on this branch.
- `legacy-3d.html` is the earlier 3D prototype, kept for reference.
