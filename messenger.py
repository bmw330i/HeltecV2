#!/usr/bin/env python3
"""
Heltec V2 Meshtastic Messenger
Simple messaging interface for your Heltec V2 board
"""

import sys
import time
import signal
import threading
from datetime import datetime

try:
    import meshtastic
    import meshtastic.serial_interface
except ImportError:
    print("📦 Installing meshtastic library...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "meshtastic"], check=True)
    import meshtastic
    import meshtastic.serial_interface

class HeltecMessenger:
    def __init__(self):
        self.interface = None
        self.running = False
        self.message_count = 0
        
    def connect(self):
        """Connect to Heltec device"""
        device_path = "/dev/cu.usbserial-0001"
        
        try:
            print(f"🔌 Connecting to Heltec V2...")
            self.interface = meshtastic.serial_interface.SerialInterface(device_path)
            print("✅ Connected successfully!")
            
            # Get device info
            node_info = self.interface.getMyNodeInfo()
            if node_info:
                user = node_info.get('user', {})
                print(f"📱 Device: {user.get('longName', 'Unknown')} ({user.get('id', 'Unknown')})")
                
                # Show mesh network
                nodes = self.interface.nodes
                print(f"🌐 Connected to mesh with {len(nodes)} nodes")
                
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def start_message_listener(self):
        """Start background message listener"""
        def message_thread():
            print("👂 Listening for messages...")
            
            def on_receive(packet, interface_obj):
                try:
                    # Check if it's a text message
                    if packet.get('decoded', {}).get('text'):
                        text_msg = packet['decoded']['text']
                        from_id = packet.get('fromId', 'Unknown')
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        
                        # Show received message
                        print(f"\n📥 [{timestamp}] From {from_id}: {text_msg}")
                        print("💬 Your message: ", end="", flush=True)
                        
                except Exception:
                    pass
            
            # Subscribe to messages  
            try:
                sub = self.interface.subscribe()
                for msg in sub:
                    if not self.running:
                        break
                    on_receive(msg, self.interface)
            except Exception:
                pass
        
        # Start listener thread
        listener = threading.Thread(target=message_thread, daemon=True)
        listener.start()
    
    def send_message(self, text, destination=None):
        """Send a message to the mesh"""
        if not self.interface:
            return False
            
        try:
            if destination:
                print(f"📤 Sending to {destination}: {text}")
            else:
                print(f"📢 Broadcasting: {text}")
                
            self.interface.sendText(text, destinationId=destination)
            self.message_count += 1
            print(f"✅ Message #{self.message_count} sent!")
            return True
            
        except Exception as e:
            print(f"❌ Send failed: {e}")
            return False
    
    def show_mesh_nodes(self):
        """Show all nodes in the mesh"""
        if not self.interface:
            return
            
        nodes = self.interface.nodes
        print(f"\n🌐 Mesh Network ({len(nodes)} nodes):")
        print("-" * 40)
        
        for node in nodes.values():
            user = node.get('user', {})
            name = user.get('longName', user.get('shortName', 'Unknown'))
            node_id = user.get('id', 'Unknown')
            last_heard = node.get('lastHeard', 0)
            
            if last_heard:
                time_str = datetime.fromtimestamp(last_heard).strftime('%H:%M:%S')
                status = f"Last seen: {time_str}"
            else:
                status = "Never seen"
                
            print(f"  📱 {name} ({node_id}) - {status}")
    
    def interactive_chat(self):
        """Start interactive chat mode"""
        print("\n💬 Interactive Chat Mode")
        print("=" * 40)
        print("Commands:")
        print("  /nodes   - Show mesh nodes")
        print("  /status  - Show device status") 
        print("  /help    - Show this help")
        print("  /quit    - Exit")
        print("  Anything else - Send as message to mesh")
        print("\n💡 Start typing messages! They'll be sent to all mesh nodes.\n")
        
        self.running = True
        self.start_message_listener()
        
        try:
            while self.running:
                try:
                    user_input = input("💬 Your message: ").strip()
                    
                    if not user_input:
                        continue
                        
                    if user_input.lower() in ['/quit', '/exit', '/q']:
                        break
                    elif user_input.lower() == '/nodes':
                        self.show_mesh_nodes()
                    elif user_input.lower() == '/status':
                        self.show_status()
                    elif user_input.lower() == '/help':
                        print("\nCommands:")
                        print("  /nodes   - Show mesh nodes")
                        print("  /status  - Show device status")
                        print("  /quit    - Exit")
                        print("  Text     - Send message to mesh")
                    else:
                        self.send_message(user_input)
                        
                except KeyboardInterrupt:
                    break
                    
        except Exception as e:
            print(f"❌ Chat error: {e}")
        
        self.running = False
        print("\n👋 Chat ended!")
    
    def show_status(self):
        """Show current device status"""
        if not self.interface:
            return
            
        print("\n📊 Device Status:")
        print("-" * 20)
        
        try:
            node_info = self.interface.getMyNodeInfo()
            if node_info:
                user = node_info.get('user', {})
                print(f"📛 Name: {user.get('longName', 'Unknown')}")
                print(f"🆔 ID: {user.get('id', 'Unknown')}")
                
                metrics = node_info.get('deviceMetrics', {})
                if metrics:
                    battery = metrics.get('batteryLevel')
                    if battery is not None:
                        print(f"🔋 Battery: {battery}%")
                    
                    voltage = metrics.get('voltage') 
                    if voltage:
                        print(f"⚡ Voltage: {voltage}V")
                        
                    uptime = metrics.get('uptimeSeconds')
                    if uptime:
                        hours = uptime // 3600
                        minutes = (uptime % 3600) // 60
                        print(f"⏰ Uptime: {hours}h {minutes}m")
            
            # Network info
            nodes = self.interface.nodes
            print(f"🌐 Mesh nodes: {len(nodes)}")
            print(f"📨 Messages sent: {self.message_count}")
            
        except Exception as e:
            print(f"❌ Status error: {e}")
    
    def close(self):
        """Close connection"""
        self.running = False
        if self.interface:
            try:
                self.interface.close()
            except:
                pass

def main():
    print("🚀 Heltec V2 Meshtastic Messenger")
    print("=" * 40)
    print("💡 Your Heltec V2 board with AppleNet WiFi")
    print()
    
    messenger = HeltecMessenger()
    
    # Handle clean exit
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down...")
        messenger.close()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Connect to device
    if not messenger.connect():
        print("\n❌ Could not connect to Heltec V2")
        print("💡 Make sure the device is plugged in via USB")
        return 1
    
    # Show initial status
    messenger.show_status()
    messenger.show_mesh_nodes()
    
    # Start interactive chat
    try:
        messenger.interactive_chat()
    finally:
        messenger.close()
    
    print("✅ Session complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())