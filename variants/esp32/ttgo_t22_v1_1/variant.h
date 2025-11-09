#pragma once

/*
 * TTGO T22_V1.1 Router Configuration
 * GPS + WiFi enabled headless router
 * No display (headless operation)
 */

// Hardware vendor definitions (required by Meshtastic)
#define HW_VENDOR meshtastic_HardwareModel_TBEAM
#define BUTTON_PIN 38
#define BUTTON_NEED_PULLUP

// No display for this board
#define HAS_SCREEN 0

// WiFi configuration
#define HAS_WIFI 1

// GPS configuration  
#define HAS_GPS 1
#define GPS_RX_PIN 12
#define GPS_TX_PIN 15

// LoRa Radio configuration (SX127x)
#define USE_RF95 1
#define LORA_DIO0 26  
#define LORA_RESET 23
#define LORA_DIO1 33
#define LORA_DIO2 32

// SPI configuration for LoRa
#define LORA_SCK 5
#define LORA_MISO 19
#define LORA_MOSI 27
#define LORA_CS 18

// I2C configuration
#define I2C_SDA 21
#define I2C_SCL 22

// LED configuration
#define LED_PIN 4

// Power management
#define BATTERY_PIN 35
#define ADC_CHANNEL ADC1_GPIO35_CHANNEL
#define VBAT_MESURE_ADC_UNIT 1
#define VBAT_MESURE_ADC_CHANNEL ADC1_GPIO35_CHANNEL

// GPS Serial
#define GPS_SERIAL_NUM 1
#define GPS_BAUDRATE 9600

// Router role optimization
#define DEFAULT_NODE_INFO_BROADCAST_SECS (30 * 60)  // 30 minutes
#define DEFAULT_POSITION_BROADCAST_SECS (15 * 60)   // 15 minutes