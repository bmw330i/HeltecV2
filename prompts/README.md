# GitHub Copilot Prompts for Heltec V2 Meshtastic

This directory contains prompt templates and conversation summaries for effective GitHub Copilot integration with the Heltec V2 Meshtastic project.

## Using These Prompts

### Basic Device Interaction
```
@mcp Check the status of my Heltec device
@mcp Send "Hello mesh!" to the network
@mcp Show me all connected mesh nodes
@mcp What's my device battery level?
```

### Network Management
```
@mcp Scan for other Meshtastic devices on WiFi
@mcp Monitor incoming messages for 60 seconds
@mcp Check the signal quality of my mesh connection
@mcp How many nodes are in my mesh network?
```

### Development Tasks
```
@mcp Build and flash the latest firmware to my device
@mcp Run a clean build for the heltec-v2_1 environment
@mcp Test my device connection and report status
@mcp Check for any firmware compilation errors
```

### Intelligent Assistance
```
@mcp Analyze my mesh network health and suggest improvements
@mcp Monitor for emergency keywords in mesh messages
@mcp Track battery trends and predict maintenance needs
@mcp Help me troubleshoot connection issues
```

## Conversation Context

Refer to `conversation-summary.md` for complete project development history and technical details.

## MCP Integration

The prompts work through the integrated MCP server (`heltec-mcp-server/`) which provides:
- Direct hardware control
- Mesh network management
- Intelligent monitoring
- Automated firmware deployment

## Tips for Effective Prompts

1. **Be Specific**: "Check battery level" vs "Check device status"
2. **Include Context**: "Monitor for emergency messages for 5 minutes"
3. **Ask for Analysis**: "Why is my mesh network slow?"
4. **Request Automation**: "Alert me when battery drops below 20%"

---

These prompts enable natural language control of your Heltec V2 Meshtastic device through GitHub Copilot.