# from modules import rs485_sht20,rs485_energy,snmp_megmeet
import time
import paho.mqtt.client as mqtt
import multiprocessing

broker1 = '218.235.216.37'
topic1 = 'test'

broker2 = 'mbiot.tower-bersama.com'
username = 'mosdev'
password = 'Des2023!@'
topic2 = 'test'

# # Read sensor data
# data_sht20      = rs485_sht20.  read_sensor_data(debug=True)
# time.sleep(1)
# data_energy     = rs485_energy. read_sensor_data(debug=True)
# time.sleep(1)
# data_megmeet    = snmp_megmeet. read_sensor_data(debug=True)
# time.sleep(1)


def on_connect_bintaro(client, userdata, flags, rc):
    print(f"Connected to {broker1} with result code {rc}")
    client.subscribe(topic1)

def on_connect_tbg(client, userdata, flags, rc):
    print(f"Connected to {broker2} with result code {rc}")
    client.subscribe(topic2)
    
def on_message_bintaro(client, userdata, msg):
    print(f"Broker 1: {msg.topic} {msg.payload}")
  
def on_message_tbg(client, userdata, msg):
    print(f"Broker 2: {msg.topic} {msg.payload}")

def mqtt_process_bintaro():
    bintaro = mqtt.Client()
    bintaro.on_connect = on_connect_bintaro
    bintaro.on_message = on_message_bintaro
    bintaro.connect(broker1, 1883, 60)
    bintaro.loop_forever()

def mqtt_process_tbg():
    tbg = mqtt.Client()
    tbg.on_connect = on_connect_tbg
    tbg.on_message = on_message_tbg
    tbg.username_pw_set(username, password)
    tbg.connect(broker2, 1884, 60)
    tbg.loop_forever()
    

if __name__ == "__main__":
    # Buat process untuk menjalankan client MQTT
    mqtt_bintaro_main = multiprocessing.Process(target=mqtt_process_bintaro)
    mqtt_bintaro_main.start()
    mqtt_tbg_main = multiprocessing.Process(target=mqtt_process_tbg)
    mqtt_tbg_main.start()