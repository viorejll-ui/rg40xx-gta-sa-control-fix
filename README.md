# GTA San Andreas controller fix — Anbernic RG40XX H (muOS)

**Tested successfully on one Anbernic RG40XX H running muOS.** This is an unofficial, device-specific workaround for a native GTA San Andreas Linux/PortMaster-style port.

## Problem

GTA San Andreas launched, but the menu moved and selected items on its own. Other games worked normally. The game's log identified `muOS-Keys` using an `RG34XXSP` input profile with button and analog-axis codes that did not match the RG40XX H input events.

## Fix

- `axis_remap.py` reads `/dev/input/event3`, translates RG40XX H muOS button/axis codes into codes expected by the detected game profile, filters small stick movements with a deadzone, and exposes a virtual `GTASA-Remap` controller using Linux `uinput`. It exclusively grabs the source input while running to prevent duplicate events.
- `Grand Theft Auto San Andreas.sh` launches the remapper before GTA, logs its output, and stops it after the game exits. It also retains the `unset SDL_VIDEODRIVER` workaround used in the tested installation and removes the earlier `GTASA_STICK_MAP` override.

## Install

1. **Back up** your existing `roms/Ports/Grand Theft Auto San Andreas.sh` file.
2. Copy `axis_remap.py` to `roms/Ports/gtasa/`.
3. Replace `roms/Ports/Grand Theft Auto San Andreas.sh` with the script in this repository.
4. If needed, make the launcher executable: `chmod +x "roms/Ports/Grand Theft Auto San Andreas.sh"`.
5. Launch GTA San Andreas through your usual Ports menu.

The remapper requires Python 3, permission to read `/dev/input/event3`, and permission to use `/dev/uinput` (typically root). No extra Python packages are needed.

## Compatibility / cautions

- The **source device is hardcoded to `/dev/input/event3`**. Other muOS versions/devices may enumerate the input controller differently.
- This workaround is **not confirmed on other devices or GTA builds**. Back up your launcher first, and restore it if GTA does not start.
- No GTA binaries, copyrighted game assets, APK/OBB files, or game data are included. You need your own legitimate game assets and compatible port.
