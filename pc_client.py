import serial
import paho.mqtt.client as mqtt
import time


COM_PORT = 'COM12'          
BAUD_RATE = 9600
VPS_IP = '157.173.101.159'   # Your VPS IP
MQTT_PORT = 1883

# MQTT Topics
TEMP_TOPIC = "sensor/temperature"
HUM_TOPIC = "sensor/humidity"
# ========================================

# MQTT Client - Using the NEW API (no deprecation warning)
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f"✅ Connected to MQTT Broker at {VPS_IP}")
    else:
        print(f"❌ Failed to connect, return code {reason_code}")

mqtt_client.on_connect = on_connect

try:
    mqtt_client.connect(VPS_IP, MQTT_PORT, 60)
    mqtt_client.loop_start()  # Start the network loop in background
    print(f"✅ MQTT client started")
except Exception as e:
    print(f"❌ Could not connect to MQTT. Check IP and network.")
    print(f"   Error: {e}")
    exit()

# Connect to Arduino on COM12
try:
    ser = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino to reset
    print(f"✅ Connected to Arduino on {COM_PORT}")
except Exception as e:
    print(f"❌ Could not open {COM_PORT}. Check USB cable.")
    print(f"   Error: {e}")
    exit()

print("📡 Listening to Arduino... Press Ctrl+C to stop.\n")

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        
        if line.startswith("TEMP:"):
            parts = line.split(",")
            temp_part = parts[0]  # "TEMP:25.4"
            hum_part = parts[1]   # "HUM:65"
            
            temp_value = temp_part.split(":")[1]
            hum_value = hum_part.split(":")[1]
            
            # 1. Display in Real-Time on your PC
            print(f"🌡️  Temperature: {temp_value} °C | 💧 Humidity: {hum_value} %")
            
            # 2. Publish BOTH to MQTT Broker on VPS
            # Publish temperature to its topic
            result_temp = mqtt_client.publish(TEMP_TOPIC, temp_value)
            if result_temp.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"   📤 Published to '{TEMP_TOPIC}'")
            else:
                print(f"   ❌ Failed to publish to '{TEMP_TOPIC}'")
            
            # Publish humidity to its topic
            result_hum = mqtt_client.publish(HUM_TOPIC, hum_value)
            if result_hum.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"   📤 Published to '{HUM_TOPIC}'\n")
            else:
                print(f"   ❌ Failed to publish to '{HUM_TOPIC}'\n")
                
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        ser.close()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        break
    except Exception as e:
        print(f"Error: {e}")
        break