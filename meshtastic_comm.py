#!/usr/bin/env python3
"""
Meshtastic Communication Script for Heltec V2
Connects to the Heltastic device via serial or TCP/IP for messaging
"""

import time
import sys
import signal
import threading
from datetime import datetime

try:
    import meshtastic
    import meshtastic.serial_interface
    import meshtastic.tcp_interface
except ImportError:
    print("❌ Meshtastic Python library not found!")
    print("📦 Installing meshtastic library...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "meshtastic"], check=True)
    import meshtastic
    import meshtastic.serial_interface
    import meshtastic.tcp_interface

class MeshtasticComm:
    def __init__(self):
        self.interface = None
        self.running = False
        
    def find_serial_device(self):
        """Find the Heltec device on serial port"""
        import glob
        import serial.tools.list_ports
        
        # Look for common ESP32 device patterns
        possible_ports = []
        
        # Check for specific device
        for port in serial.tools.list_ports.comports():
            if 'usbserial' in port.device or 'CP210' in port.description:
                possible_ports.append(port.device)
                
        # Also check common patterns
        for pattern in ['/dev/cu.usbserial*', '/dev/ttyUSB*', '/dev/ttyACM*']:
            possible_ports.extend(glob.glob(pattern))
            
        return list(set(possible_ports))
    
    def connect_serial(self, port=None):
        """Connect via serial interface"""
        if port is None:
            ports = self.find_serial_device()
            if not ports:
                print("❌ No serial devices found")
                return False
            port = ports[0]
            print(f"📱 Using serial port: {port}")
        
        try:
            print(f"🔌 Connecting to {port}...")
            self.interface = meshtastic.serial_interface.SerialInterface(port)
            print("✅ Serial connection established!")
            return True
        except Exception as e:
            print(f"❌ Serial connection failed: {e}")
            return False
    
    def connect_tcp(self, ip="meshtastic.local"):
        """Connect via TCP/IP interface"""
        try:
            print(f"🌐 Connecting to {ip} via TCP...")
            self.interface = meshtastic.tcp_interface.TCPInterface(hostname=ip)
            print("✅ TCP connection established!")
            return True
        except Exception as e:
            print(f"❌ TCP connection failed: {e}")
            return False
    
    def scan_wifi_devices(self):
        """Scan for Meshtastic devices on local network"""
        import socket
        import threading
        import ipaddress
        
        def check_host(ip):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((str(ip), 4403))  # Meshtastic TCP port
                sock.close()
                if result == 0:
                    print(f"🎯 Found Meshtastic device at {ip}:4403")
                    return str(ip)
            except:
                pass
            return None
        
        print("🔍 Scanning for WiFi-connected Meshtastic devices...")
        
        # Get local network
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
        
        threads = []
        found_devices = []
        
        def worker(ip):
            result = check_host(ip)
            if result:
                found_devices.append(result)
        
        # Scan network
        for ip in list(network.hosts())[:50]:  # Scan first 50 IPs
            thread = threading.Thread(target=worker, args=(ip,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Wait for all threads
        for thread in threads:
            thread.join(timeout=2)
        
        return found_devices
    
    def connect(self):
        """Connect to device (try TCP first, then serial)"""
        print("🚀 Starting Meshtastic Communication")
        print("=" * 50)
        
        # Try to find WiFi devices first
        wifi_devices = self.scan_wifi_devices()
        if wifi_devices:
            for device_ip in wifi_devices:
                if self.connect_tcp(device_ip):
                    return True
        
        # Try mDNS lookup
        try:
            import socket
            ip = socket.gethostbyname("meshtastic.local")
            print(f"📍 Found meshtastic.local at {ip}")
            if self.connect_tcp(ip):
                return True
        except:
            pass
        
        # Fall back to serial
        print("🔌 Trying serial connection...")
        return self.connect_serial()
    
    def get_node_info(self):
        """Get information about the node"""
        if not self.interface:
            print("❌ Not connected to device")
            return
            
        try:
            print("\n📋 Node Information:")
            print("-" * 30)
            
            # Get node info
            nodeInfo = self.interface.getMyNodeInfo()
            if nodeInfo:
                print(f"📛 Node ID: {nodeInfo.get('user', {}).get('id', 'Unknown')}")
                print(f"👤 Long Name: {nodeInfo.get('user', {}).get('longName', 'Unknown')}")
                print(f"📝 Short Name: {nodeInfo.get('user', {}).get('shortName', 'Unknown')}")
                print(f"🔋 Battery: {nodeInfo.get('deviceMetrics', {}).get('batteryLevel', 'Unknown')}%")
                print(f"📡 Channel Utilization: {nodeInfo.get('deviceMetrics', {}).get('channelUtilization', 'Unknown')}%")
                print(f"🌐 Wifi Enabled: {nodeInfo.get('user', {}).get('isLicensed', False)}")
            
            # Get mesh info
            nodes = self.interface.nodes
            print(f"\n🌐 Mesh Network: {len(nodes)} nodes discovered")
            
            for nodeId, node in nodes.items():
                user = node.get('user', {})
                pos = node.get('position', {})
                lastHeard = node.get('lastHeard', 0)
                
                if lastHeard:
                    last_seen = datetime.fromtimestamp(lastHeard).strftime('%H:%M:%S')
                else:
                    last_seen = "Never"
                    
                print(f"  📱 {user.get('longName', 'Unknown')}: {last_seen}")
                    
        except Exception as e:
            print(f"❌ Error getting node info: {e}")
    
    def send_message(self, text, destination=None):
        """Send a message"""
        if not self.interface:
            print("❌ Not connected to device")
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
            print(f"❌ Failed to send message: {e}")
            return False
    
    def start_listening(self):
        """Start listening for messages"""
        print("\n👂 Listening for messages... (Ctrl+C to stop)")
        print("-" * 40)
        
        def on_receive(packet, interface):
            try:
                if packet.get('decoded', {}).get('text'):
                    text = packet['decoded']['text']
                    fromId = packet.get('fromId', 'Unknown')
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    print(f"[{timestamp}] 📥 From {fromId}: {text}")
                    
            except Exception as e:
                print(f"❌ Error processing message: {e}")
        
        # Subscribe to messages
        self.interface.onReceive(on_receive)
        self.running = True
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n👋 Stopping...")
            self.running = False
    
    def interactive_mode(self):
        """Interactive messaging mode"""
        print("\n💬 Interactive Mode")
        print("-" * 20)
        print("Commands:")
        print("  /info    - Show node information")
        print("  /quit    - Exit")
        print("  anything else - Send as message")
        print()
        
        while True:
            try:
                user_input = input("📝 Message: ").strip()
                
                if user_input.lower() in ['/quit', '/exit', '/q']:
                    break
                elif user_input.lower() == '/info':
                    self.get_node_info()
                elif user_input:
                    self.send_message(user_input)
                    
            except KeyboardInterrupt:
                break
        
        print("\n👋 Goodbye!")
    
    def close(self):
        """Close connection"""
        if self.interface:
            self.interface.close()

def main():
    comm = MeshtasticComm()
    
    # Set up signal handler for clean exit
    def signal_handler(sig, frame):
        print("\n🛑 Interrupted")
        comm.running = False
        comm.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Connect to device
    if not comm.connect():
        print("❌ Failed to connect to Meshtastic device")
        print("💡 Make sure the device is connected via USB or WiFi")
        return 1
    
    # Get initial info
    comm.get_node_info()
    
    # Start interactive mode
    try:
        comm.interactive_mode()
    finally:
        comm.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())