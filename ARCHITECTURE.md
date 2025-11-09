# Heltec V2 Meshtastic System Architecture

This document describes the complete architecture of the Heltec V2 Meshtastic system, including the hardware platform, firmware optimization, communication interfaces, and the integrated Model Context Protocol (MCP) server for AI-powered interactions.

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   AI/Agent Layer                             │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ GitHub Copilot  │  │   Claude/GPT    │                  │
│  │      Chat       │  │   AI Agents     │                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────┬───────────────────┬───────────────────────────┘
              │                   │
              └───────┬───────────┘
                      │ MCP Protocol
┌─────────────────────┼─────────────────────────────────────┐
│              MCP Server Layer                               │
│  ┌─────────────────┐│┌─────────────────┐                  │
│  │   Node.js MCP   │││  Python Bridge  │                  │
│  │     Server      │││    Scripts      │                  │
│  └─────────────────┘│└─────────────────┘                  │
└─────────────────────┼─────────────────────────────────────┘
                      │ Serial/USB Interface
┌─────────────────────┼─────────────────────────────────────┐
│             Hardware Layer                                  │
│  ┌─────────────────┐│┌─────────────────┐                  │
│  │   Heltec V2     │││  LoRa Mesh      │                  │
│  │   ESP32 Board   │││   Network       │                  │
│  └─────────────────┘│└─────────────────┘                  │
│           │          │                                     │
│  ┌─────────────────┐│┌─────────────────┐                  │
│  │   WiFi Radio    │││  AppleNet WiFi  │                  │
│  │   (802.11)      │││    Network      │                  │
│  └─────────────────┘│└─────────────────┘                  │
└─────────────────────┼─────────────────────────────────────┘
                      │
              ┌───────┴───────┐
              │  Internet &   │
              │  MQTT Broker  │
              └───────────────┘
```

## Hardware Platform

### Heltec WiFi LoRa 32 V2.1 Specifications
- **MCU**: ESP32-D0WDQ6-V3 dual-core @ 240MHz
- **Flash Memory**: 8MB (optimized partition layout)
- **Crystal**: 40MHz (corrected from original 26MHz assumption)
- **LoRa Module**: SX1276/SX1278 (433/868/915 MHz)
- **Display**: SSD1306 OLED 128x64 pixels
- **WiFi**: 802.11 b/g/n (AppleNet network configured)
- **Bluetooth**: BLE 4.2
- **Power Management**: BQ25896 (4.2V safe charging for 1S LiPo)
- **Connectivity**: USB-C via CP2102 bridge

### Power Optimization
```
Battery Management:
├── Charging Voltage: 4.2V (conservative for 1S LiPo safety)
├── Battery Monitoring: Real-time level reporting
├── Deep Sleep: Enabled for power conservation
└── Voltage Regulation: Optimized for mesh operations
```

## Firmware Architecture

### Meshtastic v2.7.13 Custom Build
The firmware is specifically optimized for Heltec V2 hardware with:

#### Core Features Enabled
- **Mesh Networking**: LoRa-based peer-to-peer communication
- **WiFi Connectivity**: Internet bridge and web interface
- **GPS Integration**: Position sharing and routing
- **Text Messaging**: Encrypted mesh communications
- **Device Management**: Remote configuration and monitoring

#### Size-Optimized Configuration
```cpp
// Excluded modules for 8MB efficiency
#define MESHTASTIC_EXCLUDE_ENVIRONMENTAL_SENSOR 1
#define MESHTASTIC_EXCLUDE_AUDIO 1
#define MESHTASTIC_EXCLUDE_POWERMON 1
#define MESHTASTIC_EXCLUDE_STOREFORWARD 1
#define MESHTASTIC_EXCLUDE_CANNEDMESSAGES 1
#define MESHTASTIC_EXCLUDE_RANGETEST 1
```

#### Partition Layout (8MB Flash)
```
Bootloader:     64KB  @ 0x1000
Partition Table: 4KB  @ 0x8000  
Boot App:        8KB  @ 0xe000
Application:  3584KB  @ 0x10000  (Primary firmware)
Flash App:    1024KB  @ 0x390000 (OTA updates)
SPIFFS:       2048KB  @ 0x490000 (File system)
Remaining:    1312KB              (Reserved/alignment)
```

## Communication Interfaces

### 1. LoRa Mesh Network
- **Frequency**: 915MHz (North America)
- **Modulation**: LoRa CSS (Chirp Spread Spectrum)  
- **Range**: 2-15km (depending on terrain)
- **Network**: Currently connected to 7-node mesh
- **Encryption**: AES-256 mesh-wide encryption
- **Topology**: Self-healing mesh with automatic routing

### 2. WiFi Connectivity
- **Network**: AppleNet (configured and working)
- **IP Assignment**: DHCP from home router
- **Services**:
  - Web interface (HTTP port 80)
  - API endpoint (TCP port 4403)
  - MQTT bridge (configurable)
  - OTA firmware updates

### 3. Serial Interface
- **Physical**: USB-C via CP2102 bridge
- **Protocol**: 115200 baud, 8N1
- **Device Path**: `/dev/cu.usbserial-0001` (macOS)
- **Uses**: Firmware flashing, debugging, direct Python API access

## Model Context Protocol (MCP) Integration

### MCP Server Architecture
The system includes a sophisticated MCP server that enables natural language interaction with the Meshtastic hardware through AI agents and GitHub Copilot.

#### Core MCP Tools
```javascript
Available Tools:
├── check_device_status()     // Hardware health monitoring
├── send_mesh_message()       // AI-controlled messaging  
├── scan_mesh_network()       // Network topology discovery
├── monitor_mesh_messages()   // Intelligent message filtering
├── scan_wifi_network()       // Device discovery on LAN
├── get_signal_quality()      // Performance analytics
├── build_and_flash_firmware()// Automated deployment
└── get_device_config()       // Configuration management
```

#### AI Agent Capabilities
The MCP server enables sophisticated agentic behaviors:

1. **Natural Language Control**
   ```
   Human: "Send a weather update to the mesh network"
   Agent: → send_mesh_message("Weather: Sunny, 75°F, winds 5mph NW")
   ```

2. **Intelligent Monitoring**
   ```
   Human: "Alert me if anyone sends an emergency message"
   Agent: → monitor_mesh_messages() + keyword filtering + notifications
   ```

3. **Predictive Maintenance**
   ```
   Agent: → check_device_status() 
          → detect battery < 20%
          → send maintenance alert
          → schedule charging reminder
   ```

4. **Network Health Management**
   ```
   Agent: → scan_mesh_network()
          → analyze node count trends  
          → detect network fragmentation
          → suggest optimal positioning
   ```

#### GitHub Copilot Integration
The MCP server integrates seamlessly with GitHub Copilot Chat:

```json
// VS Code settings.json
{
  "mcp.servers": {
    "heltec-meshtastic": {
      "command": "node",
      "args": ["./heltec-mcp-server/index.mjs"]
    }
  }
}
```

**Example Copilot Interactions:**
- `@mcp Check my device battery level`
- `@mcp Send "Meeting at 3pm" to mesh`
- `@mcp Monitor for emergency keywords for 10 minutes`
- `@mcp Build and flash latest firmware`

## Development Environment

### Python Communication Layer
```python
Core Scripts:
├── messenger.py          // Interactive chat interface
├── test_device.py        // Hardware validation
├── find_device.py        // Network discovery
├── simple_comm.py        // Basic serial communication
└── Communication bridge for MCP server
```

### Node.js MCP Server
```javascript
Architecture:
├── index.mjs             // Main MCP server implementation
├── package.json          // Dependencies and configuration
├── README.md             // MCP-specific documentation  
└── Tool implementations with Python script integration
```

### Build System
```bash
Tools:
├── PlatformIO            // Firmware compilation and flashing
├── install_prerequisites.sh  // Automated environment setup
├── .gitignore            // Excludes build artifacts and dependencies
└── Environment isolation with Python venv and Node.js modules
```

## Security Architecture

### Multi-Layer Security Model
```
Application Layer:  MCP server input validation and sanitization
Transport Layer:    Encrypted mesh communications (AES-256)
Network Layer:      WiFi WPA2/WPA3 encryption (AppleNet)
Physical Layer:     Local-only operation, no cloud dependencies
```

### Credential Management
- **Environment Variables**: Secure credential storage in `.env`
- **Git Exclusion**: Credentials never committed to repository
- **Runtime Security**: MCP tools operate with minimal privileges
- **Mesh Encryption**: All mesh traffic encrypted by default

## Deployment and Operations

### Out-of-Box Setup Process
1. **Hardware Connection**: USB-C cable to development machine
2. **Environment Setup**: `./install_prerequisites.sh` (automated)
3. **Firmware Flash**: PlatformIO build and upload
4. **Network Join**: Automatic WiFi and mesh discovery
5. **MCP Activation**: Node.js server ready for AI integration

### Monitoring and Maintenance
- **Health Checks**: Automated device status monitoring
- **Battery Management**: Real-time power level tracking  
- **Network Analytics**: Mesh performance and topology analysis
- **Firmware Updates**: OTA and USB-based update mechanisms

### Scalability Considerations
- **Multi-Device Support**: MCP server can manage multiple boards
- **Network Growth**: Mesh automatically accommodates new nodes
- **Agent Orchestration**: Multiple AI agents can coordinate actions
- **Integration Flexibility**: REST API and WebSocket support planned

## Future Architecture Evolution

### Planned Enhancements
1. **Multi-Protocol Support**: LoRaWAN, Zigbee, Matter integration
2. **Advanced AI Behaviors**: Learning mesh usage patterns
3. **Edge Computing**: Local LLM integration for offline AI
4. **Sensor Integration**: Environmental monitoring capabilities
5. **Mobile Apps**: Native iOS/Android MCP clients

### Research Directions
- **Mesh AI**: Distributed intelligence across mesh nodes
- **Predictive Routing**: AI-optimized message path selection
- **Emergency Systems**: Automated disaster response coordination
- **IoT Integration**: Smart home and industrial device management

---

This architecture represents a comprehensive integration of hardware capabilities, firmware optimization, communication protocols, and artificial intelligence interfaces, creating a platform for natural language interaction with mesh networks and IoT devices.</content>
<parameter name="filePath">/Users/david/Documents/Meshtastic_LoRa32_26mhz/ARCHITECTURE.md