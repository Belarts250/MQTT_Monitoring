# 🌡️ IoT Temperature & Humidity Monitoring System

A complete embedded systems project that reads temperature and humidity from a DHT11 sensor using Arduino Uno, displays the data on an LCD with a scrolling candidate name, and publishes the data to an MQTT broker via a Python PC client with a real-time web dashboard.

---

## 📋 Table of Contents

- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Hardware Components](#hardware-components)
- [Wiring Diagram](#wiring-diagram)
- [Software Overview](#software-overview)
- [System Flow](#system-flow)
- [Screenshots](#screenshots)
- [Communication Details](#communication-details)
- [Testing](#testing)
- [Requirements Checklist](#requirements-checklist)
- [Troubleshooting](#troubleshooting)
- [Libraries Used](#libraries-used)
- [Links](#links)
- [Author](#author)

---

## 🏗️ System Architecture

### Workflow

```
DHT11 Sensor
      ↓
Arduino Uno
      ↓
LCD Display + USB Serial
      ↓
PC Python Client
      ↓
VPS MQTT Broker
      ↓
Web Dashboard
```

```mermaid
graph LR
    A[DHT11 Sensor] -->|Analog/Digital| B[Arduino Uno]
    B -->|I2C| C[16x2 LCD with I2C]
    B -->|USB Serial| D[PC Python Client]
    D -->|MQTT| E[VPS MQTT Broker]
    E -->|WebSocket| F[Web Dashboard]
```

**Data Flow:**

1. DHT11 sensor reads temperature and humidity
2. Arduino processes data and displays on LCD with scrolling candidate name
3. Arduino sends data via Serial (USB) to PC
4. Python program reads Serial data and publishes to MQTT broker on VPS
5. Web dashboard subscribes to MQTT topics and displays real-time data

### Concepts Covered

- Wireless control systems
- Interactive visualization
- Automation scripts
- Real-time rendering

---

## 📁 Project Structure

```
EMBEDDED_SYSTEM/
├── dashboard.html              # Web dashboard interface
├── Mqtt_monitoring_exam.ino    # Arduino firmware
└── pc_client.py                # Python PC client application
```

---

## 🛠️ Hardware Components

| Component              | Quantity | Description                                              |
|------------------------|----------|----------------------------------------------------------|
| Arduino Uno            | 1        | Microcontroller board                                    |
| DHT11 Sensor           | 1        | Temperature and humidity sensor                          |
| 16x2 LCD with I2C Module | 1      | Display with I2C backpack                                |
| Jumper Wires           | Several  | For connections                                          |
| 10kΩ Resistor          | 1        | Pull-up resistor for DHT11 (if using bare sensor)        |

---

## 🔌 Wiring Diagram

### LCD (I2C) to Arduino

| LCD Pin | Arduino Pin |
|---------|-------------|
| VCC     | 5V          |
| GND     | GND         |
| SDA     | A4          |
| SCL     | A5          |

### DHT11 to Arduino

| DHT11 Pin    | Arduino Pin    |
|--------------|----------------|
| VCC (Pin 1)  | 5V             |
| DATA (Pin 2) | Digital Pin 2  |
| GND (Pin 4)  | GND            |

> **Note:** If using a bare DHT11 sensor (4 pins), add a 10kΩ pull-up resistor between DATA (Pin 2) and VCC (5V). If using a DHT11 module (3 pins), the resistor is already built-in.

---

## 💻 Software Overview

### 1. Arduino Firmware (`Mqtt_monitoring_exam.ino`)

**Features:**
- Reads temperature and humidity from DHT11 sensor every 2 seconds
- Displays candidate name on first row of LCD (scrolling if >16 characters)
- Displays temperature and humidity on second row
- Sends data via Serial in format: `TEMP:25.4,HUM:65`

**LCD Display Format:**

```
Row 1: IGIHOZO Belise      (scrolls if >16 chars)
Row 2: T:25.4C H:65%
```

### 2. Python PC Client (`pc_client.py`)

**Features:**
- Reads Serial data from Arduino via USB
- Parses temperature and humidity values
- Displays data in real-time on PC console
- Publishes both temperature and humidity to separate MQTT topics
- Connects to MQTT broker on VPS

**Console Output Example:**

```
✅ MQTT client started
✅ Connected to MQTT Broker at 157.173.101.159
✅ Connected to Arduino on COM12
📡 Listening to Arduino... Press Ctrl+C to stop.

🌡️  Temperature: 24.1 °C | 💧 Humidity: 65 %
   📤 Published to 'sensor/temperature'
   📤 Published to 'sensor/humidity'
```

### 3. Web Dashboard (`dashboard.html`)

**Features:**
- Real-time temperature and humidity display
- Live streaming chart with historical data
- Connection status indicator
- Auto-updates every second
- Mobile-responsive design

**Dashboard Components:**
- **Temperature Card:** Shows current temperature with timestamp
- **Humidity Card:** Shows current humidity with timestamp
- **Live Chart:** Displays temperature (red line) and humidity (blue line) over time

---

## 🔄 System Flow

```
Temperature Sensor → Arduino Uno → LCD + USB Serial → PC Program → MQTT Broker → Web Dashboard
```

**Detailed Steps:**

1. **Sensor Reading:** DHT11 captures temperature and humidity
2. **Processing:** Arduino reads sensor data every 2 seconds
3. **Display:** LCD shows candidate name (scrolling) and sensor values
4. **Serial Transmission:** Arduino sends data via USB Serial
5. **PC Reception:** Python script reads Serial data from COM port
6. **Console Display:** Python shows real-time values on PC
7. **MQTT Publishing:** Python publishes to VPS broker
8. **Web Dashboard:** Browser subscribes and displays live data

---

## 📸 Screenshots

### Visual Preview Section

#### Repository Visuals

| Project | Preview |
|---------|---------|
| Arduino Serial Monitor output | ![Hardware Setup](images/arduino_mqtt.png) |
| PC Client Running | ![PC Client](images/python_output.png) |
| MQTT Subscriber (VPS) | ![MQTT Subscriber](images/mosquitto_subscribe.png) |
| Web Dashboard | ![Web Dashboard](images/dashboard.png) |


## 📡 Communication Details

### Serial Communication (Arduino ↔ PC)

| Parameter   | Value                           |
|-------------|---------------------------------|
| Protocol    | USB CDC UART (Virtual COM Port) |
| Baud Rate   | 9600                            |
| Data Bits   | 8                               |
| Stop Bits   | 1                               |
| Parity      | None                            |
| Data Format | ASCII text                      |
| Example     | `TEMP:24.1,HUM:65`              |

### MQTT Communication (PC ↔ VPS)

| Parameter  | Value               |
|------------|---------------------|
| Protocol   | MQTT                |
| Broker IP  | `157.173.101.159`   |
| Port       | `1883`              |
| QoS        | 0 (Fire and forget) |

**Topics:**

| Topic                 | Description          |
|-----------------------|----------------------|
| `sensor/temperature`  | Temperature readings |
| `sensor/humidity`     | Humidity readings    |

### WebSocket Communication (Dashboard ↔ VPS)

| Parameter     | Value                                        |
|---------------|----------------------------------------------|
| Protocol      | MQTT over WebSocket                          |
| Port          | `9001`                                       |
| Dashboard URL | http://157.173.101.159:9219/dashboard.html   |

---

## 🧪 Testing

| Test               | Method                                                    | Expected Result                               | Status |
|--------------------|-----------------------------------------------------------|-----------------------------------------------|--------|
| Serial Communication | Open Arduino Serial Monitor                             | `TEMP:24.1,HUM:65` updating every 2s         | ✅     |
| Python Script      | Run `pc_client.py`                                        | Console displays values and publish confirmations | ✅  |
| MQTT Broker        | `mosquitto_sub -h localhost -t sensor/temperature`        | Temperature values appear in terminal         | ✅     |
| Web Dashboard      | Open http://157.173.101.159:9219/dashboard.html           | Live data with real-time chart                | ✅     |

---

## 📋 Requirements Checklist

- [x] Temperature reading from DHT11 sensor
- [x] LCD display with candidate name (scrolling if >16 chars)
- [x] Serial transmission to PC
- [x] PC program reads serial data
- [x] Real-time display on PC
- [x] MQTT publishing to VPS broker
- [x] Web dashboard with real-time updates
- [x] System architecture diagram
- [x] Documentation and screenshots
- [x] GitHub repository with all files

---

## 🔧 Troubleshooting

### LCD Not Displaying Text
- Check I2C address (try `0x27` or `0x3F`)
- Adjust contrast potentiometer on I2C module
- Verify wiring: SDA→A4, SCL→A5, VCC→5V, GND→GND

### DHT11 Sensor Error
- Add 10kΩ pull-up resistor between DATA and VCC
- Check wiring: VCC→5V, DATA→Pin 2, GND→GND
- Verify DHT library is installed

### Python Can't Open COM Port
- Close Arduino Serial Monitor
- Check correct COM port in Device Manager
- Change `COM_PORT` in Python script

### MQTT Connection Failed
- Verify VPS IP address is correct
- Check if Mosquitto is running on VPS
- Ensure firewall allows port 1883

### Dashboard Not Accessible
- Check if web server is running: `ps aux | grep http.server`
- Try a different port (e.g., 9275, 8080)
- Use SSH tunneling if firewall blocks port

---

## 📚 Libraries Used

### Arduino
- LiquidCrystal_I2C by Frank de Brabander
- DHT sensor library by Adafruit

### Python
```bash
pip install pyserial paho-mqtt
```

### Web Dashboard
CDN-loaded libraries (no installation needed):
- Chart.js
- Paho MQTT
- Moment.js

---

## 🔗 Links

- **Dashboard:** http://157.173.101.159:9219/dashboard.html
- **GitHub Repository:** [[Github Link](https://github.com/Belarts250/MQTT_Monitoring)]
- **VPS IP:** 157.173.101.159
- **MQTT Broker:** mqtt://157.173.101.159:1883

---

## 👨‍💻 Author

| Field          | Details                                      |
|----------------|----------------------------------------------|
| Candidate Name | IGIHOZO Belise                               |
| Trade Code     | SPE (Embedded Systems Software Integration)  |
| Date           | June 16, 2026                                |
