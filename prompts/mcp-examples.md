# MCP Tools Usage Examples for Heltec V2 Meshtastic

## Device Management Prompts

### Device Health Monitoring
```
"Check my Heltec device status"
→ Executes: check_device_status()
→ Returns: Battery level, mesh connectivity, voltage, node count

"Is my device healthy?"
→ Analysis of device metrics and network connectivity

"Show me device diagnostics"
→ Comprehensive health report with recommendations
```

### Power Management
```
"What's my battery level?"
→ Current charge percentage and voltage readings

"How long will my battery last?"
→ AI prediction based on current usage patterns

"Is my device charging properly?"
→ Analysis of charging voltage and power management
```

## Mesh Network Operations

### Messaging
```
"Send 'Meeting at 3pm' to the mesh network"
→ Executes: send_mesh_message("Meeting at 3pm")
→ Broadcasts message to all mesh nodes

"Send emergency alert to node !a1b2c3d4"
→ Targeted message to specific mesh node

"Broadcast weather update: sunny, 75°F"
→ Network-wide weather information sharing
```

### Network Discovery
```
"Show me all mesh nodes"
→ Executes: scan_mesh_network()
→ Lists all discovered nodes with last seen times

"How many devices are in my mesh?"
→ Count of active mesh participants

"Analyze my mesh network topology"
→ AI analysis of network health and connectivity
```

### Message Monitoring
```
"Listen for messages for 30 seconds"
→ Executes: monitor_mesh_messages(30)
→ Real-time message capture and display

"Alert me if anyone sends 'emergency'"
→ Intelligent keyword monitoring with notifications

"Monitor mesh traffic and summarize activity"
→ AI analysis of communication patterns
```

## Development and Maintenance

### Firmware Management
```
"Build and flash latest firmware"
→ Executes: build_and_flash_firmware()
→ Automated compilation and deployment

"Clean build the heltec-v2_1 environment"
→ Fresh firmware compilation with clean state

"Update my device firmware safely"
→ Guided firmware update with safety checks
```

### Network Diagnostics
```
"Scan WiFi for other Meshtastic devices"
→ Executes: scan_wifi_network()
→ Discover devices with web interfaces

"Check my signal quality"
→ Executes: get_signal_quality()
→ Signal strength and performance metrics

"Diagnose connection problems"
→ Comprehensive connectivity troubleshooting
```

## Advanced AI Behaviors

### Predictive Analysis
```
"Predict when my battery will die"
→ AI trend analysis of power consumption

"Suggest optimal mesh node placement"
→ Analysis of signal quality and network topology

"Recommend firmware optimizations"
→ Performance analysis and improvement suggestions
```

### Automated Monitoring
```
"Alert me if mesh network has less than 3 nodes"
→ Continuous network health monitoring

"Notify me of any emergency messages"
→ Intelligent keyword detection and alerting

"Track device performance over time"
→ Long-term trend analysis and reporting
```

### Smart Automation
```
"If battery drops below 20%, send maintenance alert"
→ Conditional automation based on device state

"Auto-relay emergency messages to all nodes"
→ Smart message routing and amplification

"Schedule daily mesh health reports"
→ Automated monitoring and reporting
```

## Context-Aware Interactions

### Conversational Follow-ups
```
User: "Check my device"
Copilot: "Device healthy: 85% battery, connected to 7 nodes"
User: "Why only 7 nodes?"
Copilot: "Network analysis shows normal range. Previous scans: 5-9 nodes"
```

### Multi-Step Operations
```
User: "Prepare for field deployment"
Copilot: 1. Check device health → OK
         2. Verify firmware version → Latest
         3. Test mesh connectivity → 7 nodes active
         4. Confirm battery level → 95% charged
         Result: Ready for deployment
```

### Error Recovery
```
User: "Send message to mesh"
Copilot: "Error: Device not connected. Attempting reconnection..."
         "Reconnected successfully. Please retry your message."
```

## Best Practices

### Prompt Clarity
- **Good**: "Send weather update to mesh network"
- **Better**: "Broadcast 'Sunny, 75°F, light winds' to all mesh nodes"

### Context Inclusion
- **Good**: "Check signal quality"  
- **Better**: "Check signal quality and compare to yesterday's readings"

### Action Specificity
- **Good**: "Monitor messages"
- **Better**: "Monitor mesh messages for emergency keywords for 10 minutes"

---

These examples demonstrate the full range of natural language interactions possible with the Heltec V2 MCP server integration.