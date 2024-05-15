from modules import rs485_sht20,rs485_energy,snmp_megmeet,snmp_megmeet_alarm,socket_ip
import time
import paho.mqtt.client as mqtt
import multiprocessing
import json
broker1 = '218.235.216.37'
topic1 = 'test'

broker2 = 'mbiot.tower-bersama.com'
username = 'mosdev'
password = 'Des2023!@'
topic2 = 'test'

def read_sensors():
    data_sht20 = rs485_sht20.read_sensor_data(debug=False)
    temperature_value = data_sht20['temperature']['value']
    # print(temperature_value)
    # print(type(temperature_value))
    time.sleep(1)
        
    data_energy = rs485_energy.read_sensor_data(debug=False)
    print(data_energy)
    print(type(data_energy))
    l1_voltage = data_energy['l1_voltage']['value']
    l2_voltage = data_energy['l2_voltage']['value']
    l3_voltage = data_energy['l3_voltage']['value']
    l1_current = data_energy['l1_current']['value']
    l2_current = data_energy['l2_current']['value']
    l3_current = data_energy['l3_current']['value']
    ac_energy_consumption = data_energy['ac_energy_consumption']['value']
    time.sleep(1)
    
    data_megmeet = snmp_megmeet.read_sensor_data(debug=False)
    print(data_megmeet)
    print(type(data_megmeet))
    # system_voltage = data_megmeet['system_voltage']['value']
    # system_current = data_megmeet['system_current']['value']
    # battery_energy = data_megmeet['battery_energy']['value']
    

    # rectifier1_output_current = data_megmeet['rectifier1_output_current']['value']
    # rectifier2_output_current = data_megmeet['rectifier2_output_current']['value']
    # rectifier3_output_current = data_megmeet['rectifier3_output_current']['value']
    # rectifier_total_current = rectifier1_output_current + rectifier2_output_current + rectifier3_output_current
    # rctifier1_voltage = data_megmeet['rctifier1_votlage']['value']
    # l3_voltage = data_megmeet['l3_voltage']['value']
    # l1_current = data_megmeet['l1_current']['value']
    # l3_current = data_megmeet['l3_current']['value']
    # ac_energy_consumption = data_energy['ac_nergy_consumption']['value']
    time.sleep(1)
    data_megmeet_alarm = snmp_megmeet_alarm.read_sensor_data(debug=False)
    time.sleep(1)
    data_ip = socket_ip.read_sensor_data(debug=False)
    ip_value = str(data_ip)
    time.sleep(1)
    
    
    siteid = "BINTARO"
    
    status = {"online": 1,
              "ip":ip_value}
    status = json.dumps(status, indent=4)
    
    parameters = {
        "AC Voltage":{"L1":l1_voltage,
                        "L2":l2_voltage,
                        "L3":l3_voltage},
        "AC Current":{"L1":l1_current,
                        "L2":l2_current,
                        "L3":l3_current},
        
        # "DC Voltage": system_voltage,
        # "DC Current": system_current,
        # "DC Output Voltage":system_voltage,
        # "DC Output Current":system_current, 
        # "DC Total Power":battery_energy,

        # "Rectifier Total Current":rectifier_total_current,
        
        # "Battery Capacity":total_remaining_capacity_percent,
        
        # "Battery Current    ":total_battery_current,
        
        # "Backup Time" : backup_time,
        # "Battery Temperature":{"Battery 1":battery1_temperature,
        #                         "Battery 2":battery2_temperature},
        # "Recitifier Temperature":{"Rectifier 1": rectifier1_temperature,
        #                             "Rectifier 2": rectifier2_temperature,
        #                             "Rectifier 3": rectifier3_temperature},
        # "Rectifier Installed":rectifier_quantity,
        # "Recitifier Serial Number":{"Rectifier 1": rectifier1_serial_number,
        #                             "Rectifier 2": rectifier2_serial_number,
        #                             "Rectifier 3": rectifier3_serial_number},
        # "Recitifier Load Usage":{"Rectifier 1": rectifier1_load_usage,
        #                             "Rectifier 2": rectifier2_load_usage,
        #                             "Rectifier 3": rectifier3_load_usage},
        # "Recitifier Status":{"Rectifier 1": rectifier1_status,
        #                             "Rectifier 2": rectifier2_status,
        #                             "Rectifier 3": rectifier3_status},
        # "Temperature" : "nan",
        # "Humidity" : "nan",
        
        # "total_remaining_capacity":total_remaining_capacity,
        # "total_dc_load_current":total_dc_load_current,
        # "total_dc_load_power":total_dc_load_power,
        # "rectifier_rate_voltage":rectifier_rate_voltage,
        # "battery1_current":battery1_current,
        # "battery2_current":battery2_current,
        # "total_rate_capacity":total_rate_capacity,
        # "system_alarm_status" : system_alarm_status,
        # "battery_charging_status" : battery_charging_status,
        # "total_ac_input_power":total_ac_input_power,
        }
    parameters = json.dumps(parameters, indent=4)
    return siteid,status,parameters


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

def on_publish_bintaro(payload,topic):
    # Buat instance client MQTT
    client = mqtt.Client()

    # Hubungkan ke broker MQTT
    client.connect(broker1, 1883, 60)

    # if topic == 'TBGPower/T00Q56/status':
    #     client.will_set(topic, payload, qos=2, retain=True)
    #     client.publish(topic, payload, qos=2, retain=True)
        
    # elif topic == 'TBGPower/T00Q56/parameters':
    #     client.publish(topic, payload, qos=1, retain=False)
        
    # elif topic == 'TBGPower/T00Q56/alarms':
    #     client.publish(topic, payload, qos=2, retain=False)
        
    # elif topic == 'TBGPower/T00Q56/consumption':
    #     client.publish(topic, payload, qos=2, retain=False)
    # else:
    #     # Kirim pesan ke topik MQTT
    client.publish(topic, payload, qos=1)
    # Tutup koneksi
    client.disconnect()
    
def on_publish_tbg(payload,topic):
    # Buat instance client MQTT
    client = mqtt.Client()
    client.username_pw_set(username, password)
    # Hubungkan ke broker MQTT
    client.connect(broker2, 1884, 60)
    
    # if topic == 'TBGPower/T00Q56/status':
    #     client.will_set(topic, payload, qos=2, retain=True)
    #     client.publish(topic, payload, qos=2, retain=True)
        
    # elif topic == 'TBGPower/T00Q56/parameters':
    #     client.publish(topic, payload, qos=0, retain=False)
        
    # elif topic == 'TBGPower/T00Q56/alarms':
    #     client.publish(topic, payload, qos=2, retain=False)
        
    # elif topic == 'TBGPower/T00Q56/consumption':
    #     client.publish(topic, payload, qos=2, retain=False)
    # else:
        # Kirim pesan ke topik MQTT
    client.publish(topic, payload)
    # Tutup koneksi
    client.disconnect()
    
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

def publish_data():
    while True:
        siteid,status,parameters = read_sensors()
        on_publish_bintaro(siteid,'TBGPower/T00Q56/siteid')
        on_publish_bintaro(status,'TBGPower/T00Q56/status')
        on_publish_bintaro(parameters,'TBGPower/T00Q56/parameters')
        # on_publish_bintaro(status,'TBGPower/T00Q56/alarms')
        # on_publish_bintaro(siteid,'TBGPower/T00Q56/consumption')
        # on_publish_tbg()
        # time.sleep(5)
    # pass
if __name__ == "__main__":
    # Buat process untuk menjalankan client MQTT
    mqtt_bintaro_main = multiprocessing.Process(target=mqtt_process_bintaro)
    mqtt_bintaro_main.start()
    mqtt_tbg_main = multiprocessing.Process(target=mqtt_process_tbg)
    mqtt_tbg_main.start()
    publish_data_main = multiprocessing.Process(target=publish_data)
    publish_data_main.start()
    