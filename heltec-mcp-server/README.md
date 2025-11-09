# 🚀 Heltec V2 Meshtastic MCP Server

A **Model Context Protocol (MCP)** server that provides natural language interface to **Heltec WiFi LoRa 32 V2** boards running Meshtastic firmware. This enables AI agents, GitHub Copilot, and other MCP-compatible tools to interact directly with mesh networks.

## 🎯 What This Enables

- **Natural Language Mesh Interaction**: "Send a message to the mesh network"
- **AI-Powered Network Management**: "Check the health of all connected nodes"
- **Intelligent Device Monitoring**: "Monitor for messages and alert me of important ones"
- **Automated Firmware Management**: "Build and flash the latest firmware"
- **Contextual Network Analysis**: "Analyze mesh performance and suggest improvements"

## ⚡ Quick Start

### Prerequisites
- Node.js 18+ installed
- Heltec V2 board connected via USB
- Python virtual environment (auto-created by install script)

### Installation
```bash
# From the project root
./install_prerequisites.sh

# Navigate to MCP server
cd heltec-mcp-server

# Install Node.js dependencies  
npm install

# Test the server
npm test
```

### Usage with GitHub Copilot Chat

1. **Configure MCP in VS Code settings:**
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

2. **Use natural language in Copilot Chat:**
```
@mcp Check my Heltec device status
@mcp Send "Hello mesh!" to the network  
@mcp Show me all connected mesh nodes
@mcp Monitor messages for 60 seconds
```

## 🛠️ Available MCP Tools

### Device Management
- **`check_device_status`** - Get device health, battery, connectivity
- **`get_device_config`** - Retrieve current device configuration
- **`get_signal_quality`** - Check signal strength and network performance

### Mesh Network Operations  
- **`send_mesh_message`** - Send text messages to mesh network
- **`scan_mesh_network`** - Discover and list all mesh nodes
- **`monitor_mesh_messages`** - Real-time message monitoring
- **`scan_wifi_network`** - Find other Meshtastic devices on WiFi

### Firmware Management
- **`build_and_flash_firmware`** - Build and deploy firmware updates

## 🔧 Tool Examples

### Check Device Status
```javascript
// Natural language: "Check my device status"
// MCP Tool: check_device_status
{
  "connected": true,
  "nodeId": "!f7143240", 
  "nodeName": "Meshtastic 3240",
  "battery": 101,
  "voltage": 4.255,
  "meshNodes": 7,
  "wifiConfigured": true
}
```

### Send Mesh Message
```javascript
// Natural language: "Send 'Hello everyone!' to the mesh"
// MCP Tool: send_mesh_message
{
  "message": "Hello everyone!",
  "destination": "broadcast", 
  "result": "✅ Message sent successfully"
}
```

### Monitor Messages
```javascript
// Natural language: "Listen for messages for 30 seconds"  
// MCP Tool: monitor_mesh_messages
{
  "duration_seconds": 30,
  "summary": "Monitored mesh network for 30 seconds",
  "output": "📥 [14:32:15] !a1b2c3d4: Weather update: Sunny, 75°F"
}
```

## 🤖 AI Agent Integration

### Automated Network Health Monitoring
```python
# Example agent workflow
1. check_device_status() → Get current state
2. scan_mesh_network() → Count active nodes  
3. get_signal_quality() → Assess network health
4. → AI decision: Alert if nodes < 3 or battery < 20%
```

### Intelligent Message Routing
```python  
# Smart message handling
1. monitor_mesh_messages(60) → Listen for traffic
2. → AI analysis: Detect emergency keywords
3. send_mesh_message("Emergency confirmed, alerting authorities")
4. → Escalate to external systems
```

### Predictive Maintenance
```python
# Proactive device management
1. check_device_status() → Monitor battery trends
2. get_signal_quality() → Track signal degradation  
3. → AI prediction: "Battery will die in 4 hours"
4. build_and_flash_firmware() → Deploy power optimizations
```

## 📊 Response Format

All tools return structured JSON responses:

```json
{
  "tool": "tool_name",
  "status": "success|error", 
  "data": { /* tool-specific data */ },
  "summary": "Human-readable summary",
  "timestamp": "2024-11-09T15:30:00Z"
}
```

## 🌐 Network Architecture

```
[AI Agent/Copilot] 
    ↕ MCP Protocol
[MCP Server (Node.js)]
    ↕ Python Scripts  
[Heltec V2 Device]
    ↕ LoRa Radio
[Mesh Network] ← → [Other Mesh Nodes]
    ↕ WiFi (AppleNet)
[Internet/MQTT]
```

## 🔒 Security Considerations

- **Local Operation**: All communication happens locally via USB/WiFi
- **No Cloud Dependencies**: MCP server runs entirely on your machine
- **Mesh Encryption**: Meshtastic provides built-in mesh encryption
- **Access Control**: Only authorized MCP clients can execute tools

## 🚀 Development

### Adding New Tools
```javascript
// 1. Add to ListToolsRequestSchema response
{
  name: 'my_new_tool',
  description: 'What this tool does',
  inputSchema: { /* parameters */ }
}

// 2. Add to CallToolRequestSchema handler
case 'my_new_tool': {
  const result = await executePythonScript('my_script.py');
  return { content: [{ type: 'text', text: JSON.stringify(result) }] };
}
```

### Testing Tools
```bash
npm test                    # Run basic tests
node index.mjs --test       # Test specific tool
curl -X POST localhost:3000 # Direct HTTP test
```

### Debugging
```bash
npm run dev  # Start with Node.js inspector
# Then connect Chrome DevTools to debug
```

## 📝 Configuration

### Environment Variables
```bash
export MESHTASTIC_DEVICE="/dev/cu.usbserial-0001"  # Device path
export PYTHON_VENV="../.venv/bin/python"           # Python path  
export MCP_LOG_LEVEL="debug"                       # Logging level
```

### Custom Scripts
Place custom Python scripts in the parent directory. They'll be available via `executePythonScript()`.

## 🆘 Troubleshooting

### Device Not Found
```bash
ls /dev/cu.usbserial*  # Check device path
python3 test_device.py # Test direct connection
```

### Python Environment Issues  
```bash
source ../.venv/bin/activate  # Activate venv manually
pip install meshtastic pyserial # Install missing packages
```

### MCP Connection Problems
```bash
node --version  # Ensure Node.js 18+
npm ls          # Check dependencies
npm run dev     # Debug mode
```

## 📚 Resources

- [Model Context Protocol Docs](https://modelcontextprotocol.io/)
- [Meshtastic Documentation](https://meshtastic.org/)
- [Heltec WiFi LoRa 32 V2](https://heltec.org/project/wifi-lora-32/)
- [GitHub Copilot MCP Integration](https://docs.github.com/copilot)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-tool`
3. Add your MCP tool following existing patterns
4. Test with `npm test`
5. Submit pull request

## 📄 License

MIT License - Feel free to modify and distribute.

---

**🎯 Ready for AI-Powered Mesh Networking!** Your Heltec V2 can now be controlled by natural language through GitHub Copilot and other AI agents.