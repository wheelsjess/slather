# Mosh Pit

A physics toy of a mosh pit. You're one body in a crowd of about 170 at a Skull Hammer gig. Everyone is an active ragdoll, so arms and legs swing with momentum, hair whips when people headbang, and a hard enough hit knocks you over until you get back up (or someone helps you up).

Open `index.html` in a modern browser. A set lasts three minutes and the band calls out pit events as it goes. Touch controls appear on phones.

## Controls

| Action | Keyboard | Touch |
|---|---|---|
| Move | WASD / arrows | Drag on the left half |
| Run | Shift | RUN (or push the stick to its edge) |
| Jump (a stage dive if you're on the stage) | Space | JUMP |
| Shove | J | SHOVE |
| Helicopter spin (hold; too long and you get dizzy) | K | SPIN |
| Kick | L | KICK |
| Get lifted to crowd surf / help up someone who fell | E | LIFT |
| Mute | M | |
| Pause | Esc / P | II |

## What happens in the pit

- **Mosh**: the core of the crowd mills about the pit, shoving, spinning and kicking. The people round the edge shove anyone who crashes into them back in.
- **Circle pit**: the pit runs in a ring, with arrows on the floor showing which way. Run with it for points; run against it and you're a salmon.
- **Wall of death**: the crowd splits down a red line into two walls. The music builds, stops, then everyone charges.
- **Breakdown**: half-time chugs and strobes. The crowd jumps on the beat and the pit windmills. Jumping on the beat scores.
- **Crowd surf**: people get passed overhead towards the stage. Press E with at least two people next to you to get thrown up. Nearby people rush under anyone falling or diving and hold them up, and security catches surfers at the front. Drift over an empty bit of floor and you get dropped.
- **Stage diving**: jump up onto the stage from the front of the crowd, then jump off it. Hang around too long and security throws you back in.

**Hype** (the score) comes from hits, people you knock down, airtime, crowd surfing, stage dives and helping people up. Keep it coming and the multiplier climbs. Your best set is saved in your browser.

## How it works

Everything is in `index.html`: plain canvas and Web Audio, with no libraries or image files.

- **Bodies**: each person is an upright body (a circle on the floor with a height) plus an 11-point skeleton. Every frame the skeleton is pulled towards a pose (walking, headbanging, shoving, kicking, spinning, windmilling, lifting, surfing) by springs. Then stick constraints keep the limbs the right length. Knock someone down and the springs switch off, which turns them into a loose ragdoll. When they stand up, the springs fade back in.
- **Hits**: bodies bounce off each other with impulses. Fast-moving hands and feet hit whoever they pass through. Every hit adds to a stagger meter, and when it overflows, down you go.
- **Music**: the band is synthesised live (kick, snare, hats, crash and distorted saw-wave guitars) at 172 BPM. The crowd's headbanging and jumping follow the same clock. The set's sections are planned in bars, so each event starts on the downbeat with its own riff.
