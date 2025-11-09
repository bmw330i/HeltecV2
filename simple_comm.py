#!/usr/bin/env python3
"""
Simple Meshtastic Serial Communication Tool for Heltec V2
Direct serial communication without network dependencies
"""

import sys
import time
import signal
import glob
from datetime import datetime

try:
    import meshtastic
    import meshtastic.serial_interface
    import serial.tools.list_ports
except ImportError:
    print("❌ Required libraries not found!")
    print("📦 Installing meshtastic and pyserial...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "meshtastic", "pyserial"], check=True)
    import meshtastic
    import meshtastic.serial_interface
    import serial.tools.list_ports

class SimpleComm:
    def __init__(self):
        self.interface = None
        self.running = False
        
    def find_device(self):
        """Find the Heltec device"""
        print("🔍 Looking for Heltec device...")
        
        # Check for the specific device we know
        if "/dev/cu.usbserial-0001" in glob.glob("/dev/cu.usbserial*"):
            print("✅ Found Heltec at /dev/cu.usbserial-0001")
            return "/dev/cu.usbserial-0001"
        
        # Check all USB serial devices
        ports = []
        for port in serial.tools.list_ports.comports():
            if any(keyword in port.description.lower() for keyword in ['cp210', 'serial', 'usb']):
                ports.append(port.device)
                print(f"📱 Found potential device: {port.device} ({port.description})")
        
        if ports:
            return ports[0]
        
        print("❌ No devices found")
        return None
    
    def connect(self):
        """Connect to device"""
        port = self.find_device()
        if not port:
            return False
            
        try:
            print(f"🔌 Connecting to {port}...")
            self.interface = meshtastic.serial_interface.SerialInterface(port)
            print("✅ Connected successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("💡 Make sure the device is connected and not used by another app")
            return False
    
    def show_info(self):
        """Show device information"""
        if not self.interface:
            return
            
        print("\n📊 Device Information:")
        print("-" * 30)
        
        try:
            # Get my node info
            node_info = self.interface.getMyNodeInfo()
            if node_info:
                user = node_info.get('user', {})
                print(f"📛 Node ID: {user.get('id', 'Unknown')}")
                print(f"👤 Name: {user.get('longName', 'Unknown')}")
                print(f"📝 Short: {user.get('shortName', 'Unknown')}")
                
                # Device metrics
                metrics = node_info.get('deviceMetrics', {})
                if metrics:
                    battery = metrics.get('batteryLevel', 'Unknown')
                    print(f"🔋 Battery: {battery}%")
                    
                    channel_util = metrics.get('channelUtilization', 'Unknown')
                    print(f"📡 Channel Use: {channel_util}%")
                    
                    voltage = metrics.get('voltage', 'Unknown')
                    print(f"⚡ Voltage: {voltage}V")
            
            # Check nodes in mesh
            nodes = self.interface.nodes
            print(f"\n🌐 Mesh nodes: {len(nodes)} discovered")
            
            for node in nodes.values():
                user = node.get('user', {})
                name = user.get('longName', user.get('shortName', 'Unknown'))
                last_heard = node.get('lastHeard', 0)
                
                if last_heard:
                    time_str = datetime.fromtimestamp(last_heard).strftime('%H:%M:%S')
                    print(f"  📱 {name}: {time_str}")
                    
        except Exception as e:
            print(f"❌ Error getting info: {e}")
    
    def send_message(self, text, destination=None):
        """Send a message"""
        if not self.interface:
            print("❌ Not connected")
            return False
            
        try:
            if destination:
                print(f"📤 Sending to {destination}: {text}")
            else:
                print(f"📢 Broadcasting: {text}")
                
            self.interface.sendText(text, destinationId=destination)
            print("✅ Message sent!")
            return True
            
        except Exception as e:
            print(f"❌ Send failed: {e}")
            return False
    
    def listen_for_messages(self):
        """Listen for incoming messages"""
        print("\n👂 Listening for messages...")
        print("   Type messages to send, or /quit to exit")
        print("-" * 40)
        
        def on_receive(packet, interface):
            try:
                decoded = packet.get('decoded', {})
                if decoded.get('text'):
                    text = decoded['text']
                    from_id = packet.get('fromId', 'Unknown')
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"\n[{timestamp}] 📥 {from_id}: {text}")
                    print("📝 Message: ", end="", flush=True)
            except:
                pass
        
        # Subscribe to messages
        self.interface.onReceive(on_receive)
        self.running = True
        
        # Interactive messaging
        try:
            while self.running:
                user_input = input("📝 Message: ").strip()
                
                if user_input.lower() in ['/quit', '/exit', '/q']:
                    break
                elif user_input.lower() == '/info':
                    self.show_info()
                elif user_input.lower() == '/help':
                    print("Commands:")
                    print("  /info  - Show device info")
                    print("  /quit  - Exit")
                    print("  Text   - Send message")
                elif user_input:
                    self.send_message(user_input)
                    
        except KeyboardInterrupt:
            pass
        
        self.running = False
        print("\n👋 Goodbye!")
    
    def close(self):
        """Close connection"""
        if self.interface:
            self.interface.close()

def main():
    print("🚀 Heltec V2 Meshtastic Communication")
    print("=" * 40)
    
    comm = SimpleComm()
    
    # Handle Ctrl+C cleanly
    def signal_handler(sig, frame):
        print("\n🛑 Interrupted")
        comm.running = False
        comm.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Connect
    if not comm.connect():
        print("\n💡 Troubleshooting:")
        print("   1. Ensure device is connected via USB")
        print("   2. Check no other apps are using the device")
        print("   3. Try unplugging and reconnecting")
        return 1
    
    # Show device info
    comm.show_info()
    
    # Start interactive mode
    try:
        comm.listen_for_messages()
    finally:
        comm.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())