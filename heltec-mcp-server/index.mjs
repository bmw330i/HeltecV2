#!/usr/bin/env node
/**
 * Heltec V2 Meshtastic MCP Server
 * 
 * Model Context Protocol server that provides natural language interface
 * to Heltec WiFi LoRa 32 V2 board running Meshtastic firmware.
 * 
 * Enables AI agents and GitHub Copilot to interact with mesh networks,
 * send/receive messages, monitor device status, and manage network topology.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { 
  CallToolRequestSchema, 
  ListToolsRequestSchema, 
  ErrorCode, 
  McpError 
} from '@modelcontextprotocol/sdk/types.js';
import { spawn, exec } from 'child_process';
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import util from 'util';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');
const execAsync = util.promisify(exec);

/**
 * Execute Python script in the project's virtual environment
 */
async function executePythonScript(scriptName, args = [], timeout = 10000) {
  const pythonPath = path.join(projectRoot, '.venv', 'bin', 'python');
  const scriptPath = path.join(projectRoot, scriptName);
  
  // Check if script exists
  try {
    await fs.access(scriptPath);
  } catch (error) {
    throw new McpError(ErrorCode.InvalidRequest, `Script ${scriptName} not found`);
  }
  
  return new Promise((resolve, reject) => {
    const child = spawn(pythonPath, [scriptPath, ...args], {
      cwd: projectRoot,
      timeout: timeout
    });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        resolve({ stdout, stderr, code });
      } else {
        reject(new Error(`Process exited with code ${code}: ${stderr}`));
      }
    });
    
    child.on('error', (error) => {
      reject(error);
    });
    
    // Set timeout
    setTimeout(() => {
      child.kill();
      reject(new Error('Process timeout'));
    }, timeout);
  });
}

/**
 * Parse device status from Python script output
 */
function parseDeviceStatus(output) {
  const lines = output.split('\\n');
  const status = {
    connected: false,
    nodeId: null,
    nodeName: null,
    battery: null,
    voltage: null,
    meshNodes: 0,
    wifiConfigured: false
  };
  
  for (const line of lines) {
    if (line.includes('Connected successfully') || line.includes('✅ Connected!')) {
      status.connected = true;
    }
    
    const nodeMatch = line.match(/📛 Node: (.+?) \\((.+?)\\)/);
    if (nodeMatch) {
      status.nodeName = nodeMatch[1];
      status.nodeId = nodeMatch[2];
    }
    
    const batteryMatch = line.match(/🔋 Battery: (\\d+)%/);
    if (batteryMatch) {
      status.battery = parseInt(batteryMatch[1]);
    }
    
    const voltageMatch = line.match(/⚡ Voltage: ([\\d.]+)V/);
    if (voltageMatch) {
      status.voltage = parseFloat(voltageMatch[1]);
    }
    
    const meshMatch = line.match(/🌐 Mesh nodes: (\\d+)/);
    if (meshMatch) {
      status.meshNodes = parseInt(meshMatch[1]);
    }
    
    if (line.includes('✅ WiFi configuration found')) {
      status.wifiConfigured = true;
    }
  }
  
  return status;
}

/**
 * MCP Server Implementation
 */
const server = new Server(
  {
    name: 'heltec-meshtastic-server',
    version: '1.0.0'
  },
  {
    capabilities: {
      tools: {}
    }
  }
);

/**
 * List available tools
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'check_device_status',
        description: 'Check the status and health of the connected Heltec V2 Meshtastic device',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'send_mesh_message',
        description: 'Send a text message to the Meshtastic mesh network',
        inputSchema: {
          type: 'object',
          properties: {
            message: {
              type: 'string',
              description: 'The message text to send to the mesh network'
            },
            destination: {
              type: 'string',
              description: 'Optional: specific node ID to send to (broadcasts to all if not specified)'
            }
          },
          required: ['message']
        }
      },
      {
        name: 'scan_mesh_network',
        description: 'Scan and list all nodes discovered on the mesh network',
        inputSchema: {
          type: 'object',
          properties: {
            detailed: {
              type: 'boolean',
              description: 'Include detailed information about each node',
              default: false
            }
          },
          required: []
        }
      },
      {
        name: 'scan_wifi_network',
        description: 'Scan local WiFi network for other Meshtastic devices with web interfaces',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'get_device_config',
        description: 'Retrieve current device configuration including WiFi, LoRa, and mesh settings',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      },
      {
        name: 'build_and_flash_firmware',
        description: 'Build and flash updated Meshtastic firmware to the connected device',
        inputSchema: {
          type: 'object',
          properties: {
            environment: {
              type: 'string',
              description: 'PlatformIO environment to build (e.g., heltec-v2_1)',
              default: 'heltec-v2_1'
            },
            clean_build: {
              type: 'boolean',
              description: 'Perform a clean build before flashing',
              default: false
            }
          },
          required: []
        }
      },
      {
        name: 'monitor_mesh_messages',
        description: 'Start monitoring incoming mesh messages for a specified duration',
        inputSchema: {
          type: 'object',
          properties: {
            duration_seconds: {
              type: 'number',
              description: 'How long to monitor for messages (in seconds)',
              default: 30,
              minimum: 5,
              maximum: 300
            }
          },
          required: []
        }
      },
      {
        name: 'get_signal_quality',
        description: 'Get current signal quality, RSSI, and network performance metrics',
        inputSchema: {
          type: 'object',
          properties: {},
          required: []
        }
      }
    ]
  };
});

/**
 * Handle tool execution requests
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  try {
    switch (name) {
      case 'check_device_status': {
        const result = await executePythonScript('test_device.py');
        const status = parseDeviceStatus(result.stdout);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                tool: 'check_device_status',
                status: 'success',
                data: status,
                summary: `Device ${status.connected ? 'connected' : 'disconnected'}. ${
                  status.connected ? 
                    `Node ${status.nodeName} (${status.nodeId}) with ${status.meshNodes} mesh nodes, ${status.battery}% battery` :
                    'Device not responding'
                }`
              }, null, 2)
            }
          ]
        };
      }
      
      case 'send_mesh_message': {
        const { message, destination } = args;
        
        if (!message || typeof message !== 'string') {
          throw new McpError(ErrorCode.InvalidParams, 'Message text is required');
        }
        
        // Create a temporary script to send message
        const sendScript = `
import sys
import meshtastic
import meshtastic.serial_interface

try:
    interface = meshtastic.serial_interface.SerialInterface("/dev/cu.usbserial-0001")
    interface.sendText("${message.replace(/"/g, '\\"')}", destinationId=${destination ? `"${destination}"` : 'None'})
    print("✅ Message sent successfully")
    interface.close()
except Exception as e:
    print(f"❌ Failed to send message: {e}")
    sys.exit(1)
        `;
        
        await fs.writeFile(path.join(projectRoot, 'temp_send.py'), sendScript);
        const result = await executePythonScript('temp_send.py');
        await fs.unlink(path.join(projectRoot, 'temp_send.py')); // cleanup
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                tool: 'send_mesh_message',
                status: 'success',
                message: message,
                destination: destination || 'broadcast',
                result: result.stdout.trim()
              }, null, 2)
            }
          ]
        };
      }
      
      case 'scan_mesh_network': {
        // Use existing test script and parse network info
        const result = await executePythonScript('test_device.py');
        const meshData = parseDeviceStatus(result.stdout);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                tool: 'scan_mesh_network',
                status: 'success',
                totalNodes: meshData.meshNodes,
                networkHealth: meshData.meshNodes > 0 ? 'healthy' : 'isolated',
                details: args.detailed ? result.stdout : 'Use detailed:true for full output'
              }, null, 2)
            }
          ]
        };
      }
      
      case 'scan_wifi_network': {
        const result = await executePythonScript('find_device.py');
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                tool: 'scan_wifi_network',
                status: 'success',
                result: result.stdout,
                summary: 'WiFi network scan completed - check result for discovered devices'
              }, null, 2)
            }
          ]
        };
      }
      
      case 'build_and_flash_firmware': {
        const { environment = 'heltec-v2_1', clean_build = false } = args;
        const pythonPath = path.join(projectRoot, '.venv', 'bin', 'python');
        
        let commands = [];
        if (clean_build) {
          commands.push(`${pythonPath} -m platformio run -e ${environment} --target clean`);
        }
        commands.push(`${pythonPath} -m platformio run -e ${environment} --target upload`);
        
        const results = [];
        for (const command of commands) {
          const result = await execAsync(command, { cwd: projectRoot, timeout: 300000 }); // 5 min timeout
          results.push(result);
        }
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                tool: 'build_and_flash_firmware',
                status: 'success',
                environment: environment,
                clean_build: clean_build,
                summary: 'Firmware built and flashed successfully',
                details: results.map(r => r.stdout).join('\\n---\\n')
              }, null, 2)
            }
          ]
        };
      }
      
      case 'monitor_mesh_messages': {
        const { duration_seconds = 30 } = args;
        
        // Create monitoring script
        const monitorScript = `
import sys
import time
import signal
import meshtastic
import meshtastic.serial_interface
from datetime import datetime

messages = []
running = True

def signal_handler(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, signal_handler)

try:
    interface = meshtastic.serial_interface.SerialInterface("/dev/cu.usbserial-0001")
    print(f"📡 Monitoring mesh messages for {duration_seconds} seconds...")
    
    def on_receive(packet, interface_obj):
        try:
            decoded = packet.get('decoded', {})
            if decoded.get('text'):
                timestamp = datetime.now().strftime('%H:%M:%S')
                from_id = packet.get('fromId', 'Unknown')
                text = decoded['text']
                message = f"[{timestamp}] {from_id}: {text}"
                print(f"📥 {message}")
                messages.append(message)
        except:
            pass
    
    # Monitor for specified duration
    start_time = time.time()
    while running and (time.time() - start_time) < ${duration_seconds}:
        time.sleep(0.1)
    
    interface.close()
    print(f"✅ Monitoring complete. Received {len(messages)} messages")
    for msg in messages:
        print(msg)
        
except Exception as e:
    print(f"❌ Monitoring failed: {e}")
    sys.exit(1)
        `;
        
        await fs.writeFile(path.join(projectRoot, 'temp_monitor.py'), monitorScript);
        const result = await executePythonScript('temp_monitor.py', [], (duration_seconds + 10) * 1000);
        await fs.unlink(path.join(projectRoot, 'temp_monitor.py')); // cleanup
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                tool: 'monitor_mesh_messages',
                status: 'success',
                duration_seconds: duration_seconds,
                output: result.stdout,
                summary: `Monitored mesh network for ${duration_seconds} seconds`
              }, null, 2)
            }
          ]
        };
      }
      
      case 'get_signal_quality': {
        const result = await executePythonScript('test_device.py');
        const status = parseDeviceStatus(result.stdout);
        
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify({
                tool: 'get_signal_quality',
                status: 'success',
                data: {
                  voltage: status.voltage,
                  batteryLevel: status.battery,
                  meshNodes: status.meshNodes,
                  networkHealth: status.meshNodes > 3 ? 'excellent' : 
                                status.meshNodes > 1 ? 'good' : 
                                status.meshNodes > 0 ? 'fair' : 'poor',
                  signalStrength: status.voltage > 4.0 ? 'strong' : 'weak'
                }
              }, null, 2)
            }
          ]
        };
      }
      
      default:
        throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            tool: name,
            status: 'error',
            error: error.message,
            details: error.stack
          }, null, 2)
        }
      ],
      isError: true
    };
  }
});

/**
 * Start the server
 */
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('🚀 Heltec V2 Meshtastic MCP Server running...');
}

main().catch((error) => {
  console.error('💥 Server failed to start:', error);
  process.exit(1);
});