# 📱 Canned Messages Setup for Heltec V2 & TTGO LoRa32

## 🎯 **What This Enables**

Your son can send pre-defined messages using just the **single button** on the device:
- "Hi I am off work now"
- "Please come pick me up" 
- "I am still working"
- "Come Urgently Please"
- "Everything is ok"
- "I will walk home"
- "I am walking home"
- "Phone battery died"
- "Please bring food"
- "Please bring money"
- "I am in danger"
- "I am safe"

## 🔧 **How It Works**

### Button Interface:
- **Short Press**: Scroll through messages
- **Long Press**: Send the currently displayed message
- **Display**: Shows current message on screen

### User Experience:
1. Device shows first message: "Hi I am off work now"
2. Short press button → "Please come pick me up"
3. Short press button → "I am still working"
4. Continue until desired message appears
5. **Long press** to send the message to mesh network

## 🚀 **Flash Firmware with Canned Messages**

### Option 1: Use the Pre-configured File
```bash
cd /Users/david/Documents/HeltecV2
source .venv/bin/activate

# Copy the canned message config
cp userPrefs_canned_messages.jsonc userPrefs.jsonc

# Flash firmware
python -m platformio run -e heltec-v2_1 --target upload
```

### Option 2: Configure Manually via Web Interface
1. Connect device to WiFi (AppleNet already configured)
2. Go to device web interface: `http://[device-ip]`
3. Navigate to: **Modules → Canned Messages**
4. Enable the module
5. Add your custom messages

## 🎛️ **Message Configuration**

The messages are stored in order:
```
Message 1: "Hi I am off work now"
Message 2: "Please come pick me up"
Message 3: "I am still working"  
Message 4: "Come Urgently Please"
Message 5: "Everything is ok"
Message 6: "I will walk home"
Message 7: "I am walking home"
Message 8: "Phone battery died"
Message 9: "Please bring food"
Message 10: "Please bring money"
Message 11: "I am in danger"
Message 12: "I am safe"
```

## 📱 **Testing the Interface**

After flashing, test by:
1. **Short press** button → message cycles through list
2. **Long press** button → sends current message
3. Check your receiving device for the message
4. Verify message appears correctly

## 🔧 **Customizing Messages**

Edit `userPrefs_canned_messages.jsonc` and change the messages array:
```json
"messages": [
  "Your custom message 1",
  "Your custom message 2", 
  "Emergency - need help",
  "All good here",
  "Running late"
]
```

## 🎯 **Perfect for Your Son**

This creates a **dead-simple communication device**:
- No typing needed
- One button operation
- Clear visual feedback
- Instant message delivery
- Works anywhere in mesh range

## 📊 **Message Delivery**

When your son sends a message:
1. **His device** broadcasts to mesh
2. **Your device** receives it instantly  
3. **All 10 mesh nodes** also get the message
4. Message includes timestamp and sender ID

## 🔋 **Battery Optimized**

Canned messages use minimal power:
- Display shows current message
- Button press wakes device
- Message sends quickly
- Returns to low power mode

## 🎉 **Ready to Deploy**

This turns your Meshtastic devices into **emergency communicators** perfect for:
- Work pickup coordination
- Safety check-ins  
- Location updates
- Emergency alerts
- Simple family communication

**Flash the firmware and start testing!** 📡