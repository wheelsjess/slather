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

## The fight

- **Sunburn:** with no SPF, the sunburn meter fills. When it's full, you take damage and slow down.
- **Slather bottles** appear on the sand. Running over one gives 12 seconds of SPF, which stops the burn and halves damage.
- **Seagulls** fly past and drop a **potato cake** (+25 health) or a **dim sim** (+18).
- **Phase 1, Morning:** Sunny Slap fist slams, Beach Sweep, an Eye Laser that chases you, UV Rain fireballs, and Sun Ray columns.
- **Phase 2, High Noon** (at 60% health): double slams and sweeps, more fireballs, and the Grab.
- **Phase 3, Heat Dome** (at 25% health): triple slams with shockwaves, faster attacks, and the Solar Flare. Get under an umbrella before it goes off.

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

`legacy-3d.html` is the earlier 3D prototype, kept for reference.
