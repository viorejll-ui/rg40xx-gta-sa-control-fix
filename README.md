# GTA San Andreas Controller Fix — Anbernic RG40XX H (muOS)

An unofficial workaround for random controller inputs in the native Linux
PortMaster-style ARM64 port of **Grand Theft Auto: San Andreas**.

## Tested Configuration

| Component | Version / Device |
| --- | --- |
| Game | Grand Theft Auto: San Andreas |
| Android game assets | 2.10 |
| Device | Anbernic RG40XX H |
| Operating system | muOS 2606.0 Andromeda |
| PortMaster | 2026.11.12-1059 |
| Result | Working — random controller inputs fixed |

**Successfully tested on one RG40XX H.
** Compatibility with other devices, firmware versions, or GTA builds has not been confirmed.

## Problem

GTA San Andreas launched, but its menus navigated and selected options on their own, even without any button presses. Other games worked normally.

The game log showed that `muOS-Keys` was assigned an `RG34XXSP` input profile. Its expected button and analog-axis codes did not match the RG40XX H input events.

## Solution

The workaround includes two files:

- **`axis_remap.py`** — Reads `/dev/input/event3`, translates button and analog-axis codes, filters small stick movements with a deadzone, and creates a virtual `GTASA-Remap` controller using Linux `uinput`. It grabs the source input while running to avoid duplicate events.
- **`Grand Theft Auto San Andreas.sh`** — Starts the remapper before GTA, logs its output, and stops it when the game exits. It also retains the tested `unset SDL_VIDEODRIVER` workaround.

No third-party Python packages or compiler are required.

## Installation

1. **Back up** your existing `roms/Ports/Grand Theft Auto San Andreas.sh` file.
2. Copy `axis_remap.py` into `roms/Ports/gtasa/`.
3. Replace `roms/Ports/Grand Theft Auto San Andreas.sh` with the modified launcher in this repository.
4. If needed, make the launcher executable. From the SD card's root directory, run:

   ```bash
   chmod +x "roms/Ports/Grand Theft Auto San Andreas.sh"
   ```

5. Launch GTA San Andreas normally through the Ports menu.

## Result

After applying the workaround on the tested device:

- GTA San Andreas launches successfully.
- The menu no longer navigates automatically.
- Buttons and analog sticks work correctly.
- The virtual controller starts and stops with the game.

## Important Notes

- **The source controller path is hardcoded to `/dev/input/event3`.** It may differ on other devices or muOS versions.
- Python 3 and permission to access `/dev/input/event3` and `/dev/uinput` are required (typically root).
- Always back up your original launcher so you can restore it if the workaround fails.
- This is not a universal fix and has not been tested on other Anbernic models.
- No GTA binaries, copyrighted game assets, APK/OBB files, or game data are included. Users must provide their own legitimately obtained game assets and compatible port.

## Credits

Troubleshooting, testing, and confirmation performed on a real Anbernic RG40XX H.
