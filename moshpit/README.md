# Mosh Pit

A physics toy of a mosh pit. You're one body in a packed crowd of about 200 at a Skull Hammer gig in a small dive bar: brick walls, neon beer signs, a low stage, a sticky checkered floor and a bar at the back. Everyone is an active ragdoll, so arms and legs swing with momentum, hair whips when people headbang, and a hard enough hit knocks you over until you get back up (or someone helps you up).

Open `index.html` in a modern browser. A set lasts three minutes and the band calls out pit events as it goes. Touch controls appear on phones.

## Controls

| Action | Keyboard | Touch |
|---|---|---|
| Move | WASD / arrows | Drag on the left half |
| Run | Shift | RUN (or push the stick to its edge) |
| Jump (a dive if you're on the stage or the bar) | Space | JUMP |
| Keep your balance while crowd surfing | A / D | Stick left / right |
| Shove | J | SHOVE |
| Helicopter spin (hold; too long and you get dizzy) | K | SPIN |
| Kick | L | KICK |
| Get lifted to crowd surf / help up someone who fell | E | LIFT |
| Mute | M | |
| Pause | Esc / P | II |

## What happens in the pit

- **Mosh**: the floor is shoulder to shoulder. Moshers barge about in the middle, shoving, spinning and kicking, and anyone who crashes into the crowd gets shoved back. Shove someone hard and they stay where they land, so you open up space by knocking people around. When a gap opens in front of someone, they step forward into it.
- **Circle pit**: the pit runs in a ring, with arrows on the floor showing which way. Run with it for points; run against it and you're a salmon.
- **Wall of death**: the crowd splits down a red line into two walls. The music builds, stops, then everyone charges.
- **Breakdown**: half-time chugs and strobes. The crowd jumps on the beat and the pit windmills. Jumping on the beat scores.
- **Crowd surf**: people get passed overhead. Press E with at least two people next to you to get thrown up. Nearby people rush under anyone falling or diving and hold them up.
- **The balance game**: while you're up there, a meter shows your balance. The crowd keeps knocking you off centre, and you fight it with A / D (or the stick), like a grind in Tony Hawk. The longer you stay up, the more points you get and the harder it gets: you tip faster and the crowd jolts you harder. Lose it and you wipe out. Drift over an empty bit of floor and you get dropped. Reach the front and security catches you.
- **Stage and bar dives**: jump up onto the low stage or the bar, then jump off into the crowd. Hang around and security, or the bartender, throws you back in.

**The band** runs through stage moves all set. The guitarist and bassist wander their side of the stage, headbang, throw devil horns, put a foot up on the monitors and spin round. The singer roams from one side of the stage to the other, screams, points at the crowd and calls out each pit. The drummer flails on the crashes. They all jump when a new section kicks in.

**Hype** (the score) comes from hits, people you knock down, airtime, crowd surfing, stage dives and helping people up. Keep it coming and the multiplier climbs. Your best set is saved in your browser.

## How it works

Everything is in `index.html`: plain canvas and Web Audio, with no libraries or image files.

- **Bodies**: each person is an upright body (a circle on the floor with a height) plus an 11-point skeleton. Every frame the skeleton is pulled towards a pose (walking, headbanging, shoving, kicking, spinning, windmilling, lifting, surfing) by springs. Then stick constraints keep the limbs the right length. Knock someone down and the springs switch off, which turns them into a loose ragdoll. When they stand up, the springs fade back in.
- **Hits**: bodies bounce off each other with impulses. Fast-moving hands and feet hit whoever they pass through. Every hit adds to a stagger meter, and when it overflows, down you go.
- **Music**: the band is synthesised live (kick, snare, hats, crash and distorted saw-wave guitars) at 172 BPM. The crowd's headbanging and jumping follow the same clock. The set's sections are planned in bars, so each event starts on the downbeat with its own riff.
