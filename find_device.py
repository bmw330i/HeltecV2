#!/usr/bin/env python3
"""
Heltec V2 WiFi Detection and Web Interface Checker
Helps find your Meshtastic device on the network and access its web interface
"""

import socket
import requests
import ipaddress
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def get_local_network():
    """Get the local network range"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
        return network, local_ip
    except Exception as e:
        print(f"❌ Error getting network info: {e}")
        return None, None

def check_meshtastic_device(ip):
    """Check if IP has Meshtastic services"""
    results = {}
    
    # Check TCP port 4403 (Meshtastic API)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((str(ip), 4403)) == 0:
            results['api'] = True
        sock.close()
    except:
        results['api'] = False
    
    # Check HTTP port 80 (Web interface)
    try:
        response = requests.get(f"http://{ip}", timeout=2)
        if 'meshtastic' in response.text.lower() or response.status_code == 200:
            results['web'] = True
            results['web_content'] = response.text[:200]
    except:
        results['web'] = False
    
    # Check HTTPS port 443
    try:
        response = requests.get(f"https://{ip}", timeout=2, verify=False)
        if 'meshtastic' in response.text.lower() or response.status_code == 200:
            results['https'] = True
    except:
        results['https'] = False
    
    return results if any(results.values()) else None

def scan_for_devices():
    """Scan local network for Meshtastic devices"""
    print("🔍 Scanning for Meshtastic devices on local network...")
    
    network, local_ip = get_local_network()
    if not network:
        return []
    
    print(f"📡 Scanning network: {network} (your IP: {local_ip})")
    
    found_devices = []
    
    def worker(ip):
        try:
            result = check_meshtastic_device(ip)
            if result:
                found_devices.append((str(ip), result))
                print(f"🎯 Found device at {ip}")
                if result.get('web'):
                    print(f"   🌐 Web interface: http://{ip}")
                if result.get('https'):
                    print(f"   🔒 HTTPS interface: https://{ip}")
                if result.get('api'):
                    print(f"   📡 API port 4403 open")
        except Exception as e:
            pass
    
    # Scan with thread pool for speed
    with ThreadPoolExecutor(max_workers=50) as executor:
        # Scan first 100 IPs in the network
        ips_to_scan = list(network.hosts())[:100]
        executor.map(worker, ips_to_scan)
    
    return found_devices

def check_specific_ip(ip):
    """Check a specific IP for Meshtastic services"""
    print(f"🔍 Checking {ip} for Meshtastic services...")
    
    result = check_meshtastic_device(ip)
    if result:
        print(f"✅ Meshtastic device found at {ip}!")
        
        if result.get('web'):
            print(f"🌐 Web interface available: http://{ip}")
            print("   You can access the device settings and messaging from your browser")
            
        if result.get('https'):
            print(f"🔒 HTTPS interface available: https://{ip}")
            
        if result.get('api'):
            print(f"📡 API available at: {ip}:4403")
            print("   You can connect Python scripts to this endpoint")
            
        return True
    else:
        print(f"❌ No Meshtastic services found at {ip}")
        return False

def check_connectivity():
    """Check basic connectivity"""
    print("🌐 Checking network connectivity...")
    
    # Check internet
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✅ Internet connectivity: OK")
    except:
        print("❌ No internet connectivity")
    
    # Check local network
    network, local_ip = get_local_network()
    if network:
        print(f"✅ Local network: {network}")
        print(f"✅ Your IP: {local_ip}")
    else:
        print("❌ Cannot determine local network")

def main():
    print("🚀 Heltec V2 Network Scanner")
    print("=" * 40)
    
    # Basic connectivity check
    check_connectivity()
    print()
    
    # Try common Meshtastic hostnames
    common_names = ["meshtastic.local", "meshtastic", "heltec.local"]
    print("🔍 Trying common hostnames...")
    
    found_by_hostname = False
    for hostname in common_names:
        try:
            ip = socket.gethostbyname(hostname)
            print(f"📍 Resolved {hostname} to {ip}")
            if check_specific_ip(ip):
                found_by_hostname = True
                break
        except:
            print(f"❌ Cannot resolve {hostname}")
    
    if not found_by_hostname:
        print("\n🔍 Hostname lookup failed, scanning network...")
        devices = scan_for_devices()
        
        if devices:
            print(f"\n✅ Found {len(devices)} Meshtastic device(s)!")
            for ip, services in devices:
                print(f"\n📱 Device: {ip}")
                if services.get('web'):
                    print(f"   🌐 Open http://{ip} in your browser")
                if services.get('api'):
                    print(f"   📡 API: {ip}:4403")
        else:
            print("\n❌ No Meshtastic devices found on network")
            print("💡 Possible reasons:")
            print("   - Device not connected to WiFi yet")
            print("   - Device on different network/VLAN")
            print("   - WiFi credentials incorrect")
            print("   - Device still booting up")
    
    print("\n💡 Manual check:")
    print("   1. Connect via serial: python3 meshtastic_comm.py")
    print("   2. Check device IP in serial output")
    print("   3. Try: http://[device-ip] in browser")
    
    # Instructions for manual connection
    print("\n📋 Next steps:")
    print("   - If device found: Use web interface or Python script")
    print("   - If not found: Check serial connection with meshtastic_comm.py")
    print("   - For messaging: Run 'python3 meshtastic_comm.py'")

if __name__ == "__main__":
    main()