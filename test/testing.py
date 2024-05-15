import paho.mqtt.client as mqtt

# Define the MQTT broker address and port
broker = '218.235.216.37' # Replace with your broker's address
port = 1883  # Commonly used MQTT port

# Define the topic and the message
topic = 'test/topic'
message = 'Hello, MQTT with QoS 1!'

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")

# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_connect and on_publish callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(broker, port, 60)

# Start the MQTT client
client.loop_start()

# Publish a message with QoS level 1
result = client.publish(topic, message, qos=1)

# Wait for the publish to complete
result.wait_for_publish()

# Stop the MQTT client
client.loop_stop()
client.disconnect()
