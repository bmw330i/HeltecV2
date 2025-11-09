# 📡 Heltec V2 Meshtastic Communication Tools

This directory contains tools for communicating with your **Heltec WiFi LoRa 32 V2** board running Meshtastic firmware with **AppleNet WiFi connectivity**.

## 🎯 Quick Start

### 1. Basic Device Test
```bash
python3 messenger.py
```

### 2. Send Messages
The messenger tool provides an interactive chat interface:
- Type any message to broadcast to the mesh
- Use `/nodes` to see connected devices  
- Use `/status` to check device health
- Use `/quit` to exit

## 📱 Available Tools

### 🔧 `messenger.py` - Interactive Chat (Recommended)
The main communication tool with a user-friendly interface.

**Features:**
- ✅ Real-time mesh messaging
- ✅ See all connected nodes
- ✅ Device status monitoring
- ✅ Battery and signal info
- ✅ Simple commands

**Usage:**
```bash
python3 messenger.py
```

### 🔍 `test_device.py` - Quick Device Check
Simple test to verify your device is working.

```bash
python3 test_device.py
```

### 🌐 `find_device.py` - Network Scanner  
Scans your WiFi network for Meshtastic devices.

```bash
python3 find_device.py
```

## 📊 Device Information

### Your Heltec V2 Configuration:
- **Device ID**: !f7143240
- **Name**: Meshtastic 3240
- **WiFi Network**: AppleNet
- **Battery Charging**: 4.2V (safe for 1S LiPo)
- **Flash Size**: 8MB
- **Crystal**: 40MHz (corrected)
- **USB Port**: `/dev/cu.usbserial-0001`

### Network Status:
- ✅ **Connected to mesh**: 7 nodes discovered
- ✅ **WiFi configured**: AppleNet network
- ✅ **Serial communication**: Working
- ✅ **Message broadcasting**: Functional

## 🌐 WiFi Configuration

Your device is configured to connect to:
- **SSID**: AppleNet  
- **Password**: Configured in firmware
- **Web Interface**: Available when WiFi connected
- **API Port**: 4403 (for advanced users)

## 🔋 Power Management

Your device has optimized power settings:
- **Battery charging voltage**: 4.2V (conservative, safe for 1S LiPo)
- **Power management**: BQ25896 chip
- **Battery monitoring**: Real-time level reporting

## 💬 Messaging Features

### Message Types:
- **📢 Broadcast**: Messages sent to all mesh nodes
- **📥 Receive**: Automatic message reception
- **🕐 Timestamped**: All messages show time received
- **📱 Node tracking**: See who's online and when

### Commands in messenger:
- `/nodes` - Show all mesh network nodes
- `/status` - Display device health info
- `/help` - Show available commands
- `/quit` - Exit the application

## 🔧 Troubleshooting

### Device Not Found:
```bash
# Check USB connection
ls /dev/cu.usbserial*

# Reconnect device
# Unplug USB, wait 5 seconds, plug back in
```

### WiFi Issues:
```bash
# Check if device appears on network
python3 find_device.py

# Look for web interface at device IP
# Default: http://[device-ip]
```

### Message Problems:
- Ensure other Meshtastic devices are nearby
- Check antenna connection
- Verify mesh channel configuration
- Try different locations (away from interference)

## 🚀 Advanced Usage

### Direct API Access:
If you find your device's IP address, you can access:
- **Web Interface**: `http://[device-ip]`
- **API Endpoint**: `[device-ip]:4403`
- **Configuration**: Through web interface or serial

### Custom Scripts:
The Python Meshtastic library is installed and ready:
```python
import meshtastic
import meshtastic.serial_interface

interface = meshtastic.serial_interface.SerialInterface("/dev/cu.usbserial-0001")
interface.sendText("Hello mesh!")
```

## 📋 Dependencies

Auto-installed when you run the tools:
- `meshtastic` - Official Meshtastic Python library
- `pyserial` - Serial communication
- `requests` - HTTP requests for network scanning

## 🎉 Success Indicators

Your setup is working when you see:
- ✅ Device connects via USB
- ✅ Node ID: !f7143240 appears
- ✅ Multiple mesh nodes discovered
- ✅ Messages send successfully
- ✅ Real-time message reception

## 📞 Support

If you encounter issues:
1. Try `python3 test_device.py` for basic diagnostics
2. Check USB cable and connection
3. Verify device is not used by another application
4. Restart device by unplugging USB

---

**🎯 Ready to Chat!** Run `python3 messenger.py` and start communicating with your mesh network!