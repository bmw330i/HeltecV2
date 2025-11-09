# Meshtastic for TTGO LoRa32 V1 (26MHz) – Reliable Flash Kit

This folder contains a minimal, reproducible kit to flash Meshtastic onto a TTGO LoRa32 V1 with a 26MHz crystal. These boards often fail at high baud with: `Invalid head of packet (0x00)`. The fix is to upload at 115200 baud.

# 🚀 Heltec V2 Meshtastic with AI Integration

**AI-powered mesh networking** using **Heltec WiFi LoRa 32 V2** boards with **Meshtastic firmware** and **Model Context Protocol (MCP)** for natural language interactions through **GitHub Copilot**.

## ✨ What This Enables

- **🤖 Natural Language Control**: "Send weather update to mesh network"
- **📡 AI-Powered Monitoring**: "Alert me if emergency messages are received"  
- **🔧 Intelligent Automation**: "Check device health and suggest optimizations"
- **🌐 Mesh Network Management**: "Show me all connected nodes and their status"
- **⚡ Automated Firmware Deployment**: "Build and flash latest firmware"

## 🎯 Quick Start

### 1. Hardware Setup
- Connect **Heltec WiFi LoRa 32 V2** via USB
- Ensure board is detected at `/dev/cu.usbserial-0001`

### 2. One-Command Installation
```bash
git clone https://github.com/bmw330i/HeltecV2.git
cd HeltecV2
./install_prerequisites.sh
```

### 3. Flash Firmware
```bash
source .venv/bin/activate
python -m platformio run -e heltec-v2_1 --target upload
```

### 4. Start AI Integration
```bash
cd heltec-mcp-server
npm install
npm start
```

## 🛠️ Core Features

### ✅ **Working Hardware Configuration**
- **Board**: Heltec WiFi LoRa 32 V2.1 with ESP32-D0WDQ6-V3  
- **Flash**: 8MB optimized partition layout
- **Crystal**: 40MHz (corrected specification)
- **Power**: 4.2V safe charging for 1S LiPo batteries
- **Network**: AppleNet WiFi + 7-node LoRa mesh

### ✅ **Optimized Firmware**  
- **Version**: Meshtastic v2.7.13.5dc42d2
- **Size**: 55.7% flash utilization (plenty of room)
- **Features**: Text messaging, GPS, WiFi bridge, web interface
- **Excluded**: Environmental sensors, audio, powermon (size optimization)

### ✅ **Communication Tools**
- **📱 messenger.py**: Interactive chat with mesh network
- **🔧 test_device.py**: Hardware validation and diagnostics  
- **🌐 find_device.py**: Network discovery and scanning
- **📡 simple_comm.py**: Basic serial communication

### ✅ **MCP Server Integration**
- **🤖 8 AI Tools**: Device management and mesh operations
- **🔌 GitHub Copilot**: Natural language hardware control
- **⚡ Real-time**: Live mesh monitoring and interaction
- **🛡️ Local**: No cloud dependencies, privacy-first

## 🤖 AI-Powered Interactions

### GitHub Copilot Integration
Configure in VS Code settings:
```json
{
  "mcp.servers": {
    "heltec-meshtastic": {
      "command": "node", 
      "args": ["./heltec-mcp-server/index.mjs"]
    }
  }
}
```

### Example Commands
```
@mcp Check my device battery level
@mcp Send "Hello everyone!" to the mesh
@mcp Monitor for emergency messages for 60 seconds  
@mcp Show me all connected mesh nodes
@mcp Build and flash latest firmware
@mcp Analyze mesh network health
```

### Intelligent Automation
```python
# AI can now autonomously:
- Monitor mesh for emergency keywords
- Alert when battery drops below 20%
- Predict optimal node placement
- Automate firmware deployments
- Track network performance trends
```

## 📊 Current Status

### ✅ **Device Health** 
```
Node ID: !f7143240 (Meshtastic 3240)
Battery: 101% charged
Voltage: 4.255V (optimal)
Mesh Nodes: 7 discovered and active
WiFi: Connected to AppleNet
Status: ✅ Fully operational
```

### ✅ **Network Connectivity**
```
LoRa Mesh: 7-node network active
WiFi: AppleNet connection established  
Serial: /dev/cu.usbserial-0001 working
Web Interface: Available when WiFi connected
API Port: 4403 (for advanced integration)
```

## 📁 Project Structure

```
HeltecV2/
├── 🔧 Core Firmware
│   ├── platformio.ini              # Build configuration
│   ├── partition-table-8mb.csv     # 8MB flash layout
│   ├── userPrefs.jsonc             # Device preferences  
│   ├── .env                        # WiFi credentials (secure)
│   └── src/                        # Meshtastic firmware source
│
├── 🐍 Communication Tools  
│   ├── messenger.py                # Interactive chat interface
│   ├── test_device.py              # Device validation
│   ├── find_device.py              # Network discovery
│   └── simple_comm.py              # Basic serial communication
│
├── 🤖 AI Integration
│   ├── heltec-mcp-server/          # MCP server for AI agents
│   │   ├── index.mjs               # Main server implementation
│   │   ├── package.json            # Node.js dependencies
│   │   ├── test.mjs                # Server validation
│   │   └── README.md               # MCP documentation
│   └── prompts/                    # GitHub Copilot templates
│
├── 📚 Documentation
│   ├── README.md                   # This file
│   ├── ARCHITECTURE.md             # System design details
│   ├── COMMUNICATION_GUIDE.md      # Messaging tools guide
│   └── prompts/README.md           # AI integration guide
│
└── ⚙️ Setup & Configuration
    ├── install_prerequisites.sh    # Automated setup
    ├── .gitignore                  # Repository exclusions
    └── variants/esp32/heltec_v2.1/ # Hardware definitions
```

## 🔧 Technical Specifications

### Hardware Platform
- **MCU**: ESP32-D0WDQ6-V3 @ 240MHz dual-core
- **Memory**: 8MB flash, 520KB SRAM  
- **Radio**: SX1276/SX1278 LoRa (915MHz)
- **Display**: SSD1306 OLED 128x64
- **Connectivity**: WiFi 802.11n, Bluetooth 4.2
- **Power**: BQ25896 charger, USB-C connector

### Software Stack
- **Firmware**: Meshtastic v2.7.13 (custom optimized)
- **Python**: 3.13.5 with virtual environment
- **Node.js**: 18+ with MCP SDK integration  
- **Build System**: PlatformIO with ESP32 toolchain
- **AI Integration**: Model Context Protocol server

### Network Architecture
```
[AI Agents] ↔ [MCP Server] ↔ [Python Scripts] ↔ [Heltec V2] ↔ [Mesh Network]
     │                                                               │
     └─ GitHub Copilot                                              └─ 7 Active Nodes
```

## 🚀 Use Cases

### 📡 **Mesh Networking**
- Emergency communications in remote areas
- Community mesh networks  
- Event coordination and logistics
- Off-grid messaging and alerts

### 🤖 **AI-Powered Operations**
- Natural language device control
- Intelligent message filtering and routing
- Predictive maintenance and health monitoring
- Automated emergency response systems

### 🏗️ **Development Platform**
- IoT device prototyping with AI integration
- Mesh network research and experimentation  
- GitHub Copilot extension development
- Educational platform for embedded systems

### 🌍 **Real-World Applications**
- Disaster response coordination
- Rural connectivity solutions
- Smart agriculture monitoring
- Wildlife tracking and conservation

## 📚 Documentation Deep Dive

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Complete system design and technical details
- **[COMMUNICATION_GUIDE.md](COMMUNICATION_GUIDE.md)**: Messaging tools and usage
- **[heltec-mcp-server/README.md](heltec-mcp-server/README.md)**: AI integration details
- **[prompts/README.md](prompts/README.md)**: GitHub Copilot prompt examples

## 🤝 Contributing

1. **Fork & Clone**: Get your copy of the repository
2. **Hardware**: Connect Heltec V2 board via USB
3. **Setup**: Run `./install_prerequisites.sh` for environment
4. **Develop**: Add features, test with `npm test` and `python test_device.py`
5. **Submit**: Create pull request with your improvements

## 🆘 Troubleshooting

### Device Connection Issues
```bash
# Check USB connection
ls /dev/cu.usbserial*

# Test device communication  
python test_device.py

# Validate MCP server
cd heltec-mcp-server && npm test
```

### Network Problems
```bash
# Scan for WiFi devices
python find_device.py

# Check mesh connectivity
python messenger.py  # Use /nodes command
```

### Build Failures
```bash
# Clean and rebuild
source .venv/bin/activate
python -m platformio run -e heltec-v2_1 --target clean
python -m platformio run -e heltec-v2_1 --target upload
```

## 📄 License

MIT License - Free for personal and commercial use.

---

## 🎉 **Ready for AI-Powered Mesh Networking!**

Your Heltec V2 board is now a **fully integrated AI-controllable mesh networking platform**. Use **GitHub Copilot** to naturally interact with your hardware, automate network operations, and explore the future of human-AI-hardware collaboration.

**🎯 Start with**: `@mcp Check my device status` in GitHub Copilot Chat!

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
