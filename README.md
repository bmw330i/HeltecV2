# Meshtastic for TTGO LoRa32 V1 (26MHz) – Reliable Flash Kit

This folder contains a minimal, reproducible kit to flash Meshtastic onto a TTGO LoRa32 V1 with a 26MHz crystal. These boards often fail at high baud with: `Invalid head of packet (0x00)`. The fix is to upload at 115200 baud.

# Meshtastic for Heltec WiFi LoRa 32 V2 / V2.1 – Optimized Build

This repository contains a Meshtastic firmware build specifically optimized for Heltec WiFi LoRa 32 V2 and V2.1 boards. Features proper 8MB flash support, conservative battery charging, and corrected hardware specifications.

## Hardware Specifications (Corrected)
- **ESP32 Main Crystal**: 40MHz (not 26MHz as incorrectly stated in some early documentation)
- **LoRa Radio Crystal**: 32MHz (SX1276/SX1278 reference)
- **Flash Memory**: 8MB SPI Flash (typical for V2/V2.1)
- **Battery Management**: Built-in LiPo charging with BQ25896 (conservative 4.2V charge limit)
- **Display**: 0.96" 128×64 OLED
- **Connectivity**: WiFi, Bluetooth, LoRa (433/868/915MHz depending on region)

## What's here
- `platformio.ini` – configured with `heltec-v2_1` as default environment
- `partition-table-8mb.csv` – optimized 8MB flash partition layout  
- `variants/esp32/heltec_v2.1/` – board-specific configurations
- Conservative battery charging voltage (4.2V instead of 4.288V)
- Both 8MB and 4MB build variants for different hardware revisions

## Prerequisites
- PlatformIO CLI installed (`pio`) or VS Code with PlatformIO extension
- Python virtual environment (automatically configured)
- Data-capable USB-C cable for V2 boards
- Heltec WiFi LoRa 32 V2 or V2.1 board

## Quick start
1) Connect your Heltec board via USB-C
2) Build and flash the firmware:

```bash
# Build for 8MB Heltec V2.1 (default)
pio run -e heltec-v2_1 --target upload

# Or for rare 4MB hardware
pio run -e heltec-v2_1_4mb --target upload
```

The firmware will auto-detect your board on `/dev/cu.usbserial-*` or `/dev/cu.SLAB_USBtoUART`.

## Port discovery (macOS)
The Heltec V2 uses CP2102 USB-to-UART bridge. Check connected devices:

```bash
# List available devices
pio device list
```

Typical ports:
- `/dev/cu.usbserial-0001`
- `/dev/cu.SLAB_USBtoUART`

## Build environments available
- `heltec-v2_0` – Heltec V2.0 support
- `heltec-v2_1` – Heltec V2.1 with 8MB flash (default)
- `heltec-v2_1_4mb` – Heltec V2.1 with 4MB flash (rare hardware)

## Battery Safety Features
- **Charging Voltage**: Conservative 4.2V limit (safe for 1S LiPo)
- **Current Limit**: 1024mA charging current
- **Protection**: Over-charge, under-voltage protection via BQ25896
- **Monitoring**: Real-time voltage and charge percentage via ADC

## Troubleshooting
- **Connection issues**: Try 115200 baud rate (conservative setting)
- **Build errors**: Ensure you're using `heltec-v2_1` environment
- **Flash size errors**: Use `heltec-v2_1_4mb` for older 4MB hardware
- **Battery not charging**: Check LiPo polarity and JST connector
- **OLED blank**: Power cycle board after first flash

## Hardware Correction Notice
Early documentation incorrectly stated 26MHz crystal frequency. The ESP32 on Heltec V2/V2.1 uses a standard **40MHz crystal**. The LoRa module (SX1276/SX1278) has its own **32MHz reference crystal**.

## Next steps
- Monitor device: `pio device monitor --port <PORT> --baud 115200`
- Configure via [Meshtastic mobile app](https://meshtastic.org/docs/getting-started)
- Join the [Meshtastic Discord](https://discord.com/invite/ktMAKGBnBs) for support

## GitHub Repository
This optimized build will be pushed to: https://github.com/bmw330i/HeltecV2

## Prerequisites
- PlatformIO CLI installed (`pio`). If not, install the VS Code PlatformIO extension or use `pipx install platformio`.
- Meshtastic firmware source available. If using the parent workspace layout, the Meshtastic project is in `../firmware` from the repo root. Adjust the `-d` flag accordingly.
- A data-capable USB cable.

## Quick start
1) Identify your Meshtastic project root (contains `platformio.ini`). Commonly:
   - `…/Ansible/firmware` in this workspace
2) Ensure the override is present (already provided here):
   - `platformio_override.ini` contains:
     
     [env:ttgo-lora32-oled]
     upload_speed = 115200

3) Put board in bootloader (if needed): Hold BOOT, tap RESET, release RESET, release BOOT.

4) Flash using the helper script:

```bash
# From this folder
./flash_ttgo.sh -d ../firmware
```

The script will auto-detect the serial port (via unplug/plug delta) and upload to the `ttgo-lora32-oled` environment at 115200.

## Manual flash (no script)
If you prefer manual control:

```bash
# Ensure override exists in <project_root>/platformio_override.ini
# Then run (replace PORT):
pio run -d <project_root> -e ttgo-lora32-oled --target upload --upload-port /dev/cu.usbserial-XXXXXXXX
```

If you encounter the 0x00 packet error at higher speeds, drop to 115200 (already enforced by the override).

## Port discovery (macOS)
- Unplug the board, list ports:

```bash
ls /dev/cu.*
```

- Plug the board in, list again; the new entry is the port. Examples:
  - `/dev/cu.usbserial-531C0092231`
  - `/dev/cu.SLAB_USBtoUART`

## Why 115200?
Older TTGO LoRa32 V1 units with 26MHz crystals are flaky at 921600. Dropping to 115200 eliminates packet corruption (“Invalid head of packet (0x00)”). It’s slower but reliable.

## Troubleshooting
- Connecting… and times out:
  - Re-enter bootloader (hold BOOT, tap RESET).
  - Try a different USB port/cable.
- Port busy:
  - Close serial monitors (VS Code, `pio device monitor`, `screen`).
- Still failing with 0x00 head:
  - Confirm `platformio_override.ini` has `upload_speed = 115200` under `[env:ttgo-lora32-oled]`.
  - Try another USB cable/port.
- Blank OLED after success:
  - Power cycle the board. If still blank, reflash once more.

## Next steps
- Use `pio device monitor --port <PORT> --baud 115200` to see logs after flashing.
- Configure Meshtastic via the mobile app or CLI as needed.
