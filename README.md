GTA San Andreas Controller Fix — Anbernic RG40XX H (muOS)

Game Compatibility

- Game: Grand Theft Auto: San Andreas (GTA SA)
- Android game version: 2.10
- Port: Native Linux / PortMaster-style ARM64 port
- Device tested: Anbernic RG40XX H
- Operating system: muOS 2606.0 Andromeda
- Status: Working — random controller inputs fixed

Successfully tested on Anbernic RG40XX H running muOS. This is an unofficial workaround. Compatibility with other devices, operating systems, and game versions has not been confirmed.

Problem

GTA San Andreas launched successfully, but the controls were broken. The menu kept navigating and selecting options automatically, even without pressing any buttons.

Other games worked normally.

The game logs showed that "muOS-Keys" was detected using an "RG34XXSP" controller profile, which did not match the actual button and analog-stick layout of the RG40XX H.

Solution

The fix consists of two files:

- "axis_remap.py" — Creates a virtual controller named "GTASA-Remap" using Linux "uinput", remaps buttons and analog axes, and applies a deadzone to prevent unwanted stick movements.
- "Grand Theft Auto San Andreas.sh" — Starts the remapper automatically before launching GTA and stops it when the game exits.

The modified launcher also preserves the "unset SDL_VIDEODRIVER" workaround required by the tested installation.

No additional Python packages or compiler are required.

Installation

1. Back up your original "Grand Theft Auto San Andreas.sh".

2. Copy "axis_remap.py" into "roms/Ports/gtasa/".

3. Replace "roms/Ports/Grand Theft Auto San Andreas.sh" with the modified launcher from this repository.

4. If necessary, make the launcher executable:
   
   "chmod +x "roms/Ports/Grand Theft Auto San Andreas.sh""

5. Launch GTA San Andreas normally from the Ports menu.

Result

After applying the fix:

- GTA San Andreas launches successfully.
- The menu no longer navigates automatically.
- Buttons and analog sticks work correctly.
- The virtual controller starts and stops automatically with the game.

Tested successfully on GTA San Andreas Android version 2.10 assets, Anbernic RG40XX H, and muOS.

Important Notes

- The script uses "/dev/input/event3" as its input source. This path may differ on other devices or muOS versions.
- Python 3 and access to "/dev/uinput" are required.
- Always back up your original launcher before making changes.
- This fix has not been tested on other Anbernic models.
- No copyrighted GTA binaries, APK/OBB files, or game assets are included. Users must provide their own legally obtained game files.

Credits

Troubleshooting, testing, and confirmation performed on a real Anbernic RG40XX H.
