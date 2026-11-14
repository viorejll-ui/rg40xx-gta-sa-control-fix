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

## Two San Andreas entries in Ports?

A backup launcher left in `roms/Ports/` can appear as a second game entry.
On our tested device, one entry had working controls; the other still had the original problem.

### Remove the extra entry

1. Open `roms/Ports/` in the muOS web file manager and check the **full filenames**.
2. Keep the modified **`Grand Theft Auto San Andreas.sh`** in this folder.
3. Select the **backup launcher**. On our device, its name began with `Grand Theft Auto San Andreas.sh.b`.
4. Choose **Move**, change the destination from `roms/Ports` to **`roms`**, then confirm **Move**.
5. On the handheld, leave the Ports menu and reopen it. Launch the remaining entry and test the controls.

**Keep the backup** so you can restore it. If the remaining entry has broken controls, move the backup back and check which launcher is being used.

**Leave the `gtasa/` folder where it is.** It contains the game data. Check full filenames before moving anything: the menu showing or hiding `.sh` does not tell you which launcher is correct.

## Original installation guide

[GTA San Andreas 2.10 — R36S Wiki](https://r36swiki.com/wiki-gtasa.html)

We used this guide for the initial installation. It is written for **R36S / ArkOS** using Android game assets **2.10**, so paths and device-specific steps may differ on muOS.

This repository adds the controller fix tested on **Anbernic RG40XX H with muOS**.
