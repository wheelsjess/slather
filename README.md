# Slather Ring: Shadow of the Sun

A small browser boss fight. You play a bogan in a fluoro singlet armed with a tube of Slather SPF50+, up against The Sun.

Open `index.html` in any modern browser. Desktop uses the keyboard and mouse; phones get on-screen touch controls.

## Controls

| Action | Keyboard | Touch |
|---|---|---|
| Move | W A S D / arrows | Drag on the left side |
| Squirt sunscreen | Hold J or left mouse | Hold SQUIRT |
| Roll (dodge, brief invincibility) | Space | ROLL |
| Slather (heal, SPF shield, clears sunburn) | E | SLATHER |
| Pause | Esc / P | PAUSE |

## The fight

The camera is always locked on to The Sun. Without SPF, your sunburn meter fills and burns you when full.

- **Phase 1, Morning** (smug face): Sunny Slap fist slams, Eye Laser sweep, UV Rain orbs, Solar Flare fireball rings.
- **Phase 2, High Noon** (60% health, grinning face): everything faster, double lasers and slams, plus Heatwave stomp rings and the Sunburn Charge.
- **Phase 3, Heat Dome** (25% health, laser-eyes rage face): triple slams, combos, faster sunburn, and the Solar Flare. Get under a beach umbrella before it goes off.

## Tuning

All the numbers live near the top of the script in `index.html` (`BOSS_MAX`, `UV_RATE`, `GAP`, `SPF_TIME`) and in each entry of `ATTACKS`.
