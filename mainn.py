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

main_topic="TBGPower"
sub_topic=""
def read_sensors():
    data_sht20 = rs485_sht20.read_sensor_data(debug=False)
    temperature = data_sht20['temperature']['value']
    humidity = data_sht20['temperature']['value']
    # print(temperature_value)
    # print(type(temperature_value))
    time.sleep(1)
        
    data_energy = rs485_energy.read_sensor_data(debug=False)
    # print(data_energy)
    # print(type(data_energy))
    l1_voltage = data_energy['l1_voltage']['value']
    l2_voltage = data_energy['l2_voltage']['value']
    l3_voltage = data_energy['l3_voltage']['value']
    l1_current = data_energy['l1_current']['value']
    l2_current = data_energy['l2_current']['value']
    l3_current = data_energy['l3_current']['value']
    ac_energy_consumption = data_energy['ac_energy_consumption']['value']
    time.sleep(1)
    global site_id
    data_megmeet = snmp_megmeet.read_sensor_data(debug=False)
    # print(data_megmeet)
    # print(type(data_megmeet))
    site_id = data_megmeet['site_id']['value']
    system_voltage = data_megmeet['system_voltage']['value']
    system_current = data_megmeet['system_current']['value']
    battery1_current = data_megmeet['battery1_current']['value']
    battery2_current = data_megmeet['battery2_current']['value']
    total_battery_current = data_megmeet['total_battery_current']['value']
    battery1_temperature = data_megmeet['battery1_temperature']['value']
    battery2_temperature = data_megmeet['battery1_temperature']['value']
    battery1_capacity = data_megmeet['battery1_capacity']['value']
    battery2_capacity = data_megmeet['battery2_capacity']['value']
    battery_energy = data_megmeet['battery_energy']['value']
    total_dc_load_current = data_megmeet['total_dc_load_current']['value']
    total_remaining_capacity_percent = (battery1_capacity+battery2_capacity)/2
    total_rate_capacity = data_megmeet['battery_nominal_capacity']['value']
    total_remaining_capacity = total_rate_capacity * (total_remaining_capacity_percent / 100)
    
    if float(total_dc_load_current) > 0 :
        backup_time = total_remaining_capacity / float(total_battery_current)
    else:
        backup_time = "-"
    rectifier_quantity = data_megmeet['rectifier_slots']['value']
    rectifier1_output_current = data_megmeet['rectifier1_output_current']['value']
    rectifier2_output_current = data_megmeet['rectifier2_output_current']['value']
    rectifier3_output_current = data_megmeet['rectifier3_output_current']['value']
    rectifier_total_current = rectifier1_output_current + rectifier2_output_current + rectifier3_output_current
    
    rectifier1_temperature = data_megmeet['rectifier1_temperature']['value']
    rectifier2_temperature = data_megmeet['rectifier2_temperature']['value']
    rectifier3_temperature = data_megmeet['rectifier3_temperature']['value']
    
    rectifier1_status = data_megmeet['rectifier1_status']['value']
    rectifier2_status = data_megmeet['rectifier2_status']['value']
    rectifier3_status = data_megmeet['rectifier3_status']['value']
    
    rectifier1_load_usage = data_megmeet['rectifier1_load_usage']['value']
    rectifier2_load_usage = data_megmeet['rectifier2_load_usage']['value']
    rectifier3_load_usage = data_megmeet['rectifier3_load_usage']['value']
    
    rectifier1_serial_number = data_megmeet['rectifier1_serial_number']['value']
    rectifier2_serial_number = data_megmeet['rectifier2_serial_number']['value']
    rectifier3_serial_number = data_megmeet['rectifier3_serial_number']['value']

    
    time.sleep(1)
    data_megmeet_alarm = snmp_megmeet_alarm.read_sensor_data(debug=False)
    time.sleep(1)
    data_ip = socket_ip.read_sensor_data(debug=False)
    ip_value = str(data_ip)
    time.sleep(1)
    
    
    siteid = site_id
    
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
        
        "DC Voltage": system_voltage*0.001,
        "DC Current": system_current*0.001,
        "DC Output Voltage":system_voltage*0.001,
        "DC Output Current":system_current*0.001, 
        "DC Total Power":battery_energy*0.001,

        "Rectifier Total Current":rectifier_total_current*0.1,
        
        "AC Consumption":ac_energy_consumption,
        "DC Consumption":battery_energy*0.001,
        
        
        "Battery Capacity":total_remaining_capacity_percent*0.1,
        
        "Battery Current":total_battery_current,
        
        "Battery Voltage":system_voltage*0.001,
        
        "Backup Time" : backup_time,
        "Battery Temperature":{"Battery 1":battery1_temperature*0.001,
                                "Battery 2":battery2_temperature*0.001},
        
        "Recitifier Temperature":{"Rectifier 1": rectifier1_temperature*0.1,
                                    "Rectifier 2": rectifier2_temperature*0.1,
                                    "Rectifier 3": rectifier3_temperature*0.1},
        
        "Rectifier Installed":rectifier_quantity-3,
        "Recitifier Serial Number":{"Rectifier 1": rectifier1_serial_number,
                                    "Rectifier 2": rectifier2_serial_number,
                                    "Rectifier 3": rectifier3_serial_number},
        "Recitifier Load Usage":{"Rectifier 1": rectifier1_load_usage*0.1,
                                    "Rectifier 2": rectifier2_load_usage*0.1,
                                    "Rectifier 3": rectifier3_load_usage*0.1},
        "Recitifier Status":{"Rectifier 1": rectifier1_status,
                                    "Rectifier 2": rectifier2_status,
                                    "Rectifier 3": rectifier3_status},
        "Temperature" : temperature,
        "Humidity" : humidity
        
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
    
    alarms = {"Door Open": 1}
    alarms = json.dumps(alarms, indent=4)
    
    consumptions = {"AC": ac_energy_consumption,
                    "DC":battery_energy*0.001}
    consumptions = json.dumps(consumptions, indent=4)
    return siteid,status,parameters,alarms,consumptions


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
    client.loop_start()
    if topic == f'{main_topic}/{site_id}/status':
        client.will_set(topic, payload, qos=2, retain=True)
        result = client.publish(topic, payload, qos=2, retain=True)
        
    elif topic == f'{main_topic}/{site_id}/parameters':
        result = client.publish(topic, payload, qos=1, retain=False)
        
    elif topic == f'{main_topic}/{site_id}/alarms':
        result = client.publish(topic, payload, qos=2, retain=False)
        
    elif topic == f'{main_topic}/{site_id}/consumption':
        result = client.publish(topic, payload, qos=2, retain=False)
    else:
        # Kirim pesan ke topik MQTT
        result = client.publish(topic=topic, payload=payload, qos=1)
    # Wait for the publish to complete
    result.wait_for_publish()
    # Tutup koneksi
    client.loop_stop()
    client.disconnect()
    
def on_publish_tbg(payload,topic):
    # Buat instance client MQTT
    client = mqtt.Client()
    client.username_pw_set(username, password)
    # Hubungkan ke broker MQTT
    client.connect(broker2, 1884, 60)
    
    client.loop_start()
    if topic == f'{main_topic}/{site_id}/status':
        client.will_set(topic, payload, qos=2, retain=True)
        result = client.publish(topic, payload, qos=2, retain=True)
        
    elif topic == f'{main_topic}/{site_id}/parameters':
        result = client.publish(topic, payload, qos=1, retain=False)
        
    elif topic == f'{main_topic}/{site_id}/alarms':
        result = client.publish(topic, payload, qos=2, retain=False)
        
    elif topic == f'{main_topic}/{site_id}/consumption':
        result = client.publish(topic, payload, qos=2, retain=False)
    else:
        # Kirim pesan ke topik MQTT
        result = client.publish(topic=topic, payload=payload, qos=1)
    # Wait for the publish to complete
    result.wait_for_publish()
    # Tutup koneksi
    client.loop_stop()
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
        siteid,status,parameters,alarms,consumptions = read_sensors()
        # on_publish_bintaro(siteid,f'{main_topic}/{site_id}/siteid')
        on_publish_bintaro(status,f'{main_topic}/{site_id}/status')
        on_publish_bintaro(parameters,f'{main_topic}/{site_id}/parameters')
        on_publish_bintaro(alarms,f'{main_topic}/{site_id}/alarms')
        on_publish_bintaro(consumptions,f'{main_topic}/{site_id}/consumptions')
        
        # on_publish_tbg(siteid,f'{main_topic}/{site_id}/siteid')
        on_publish_tbg(status,f'{main_topic}/{site_id}/status')
        on_publish_tbg(parameters,f'{main_topic}/{site_id}/parameters')
        on_publish_tbg(alarms,f'{main_topic}/{site_id}/alarms')
        on_publish_tbg(consumptions,f'{main_topic}/{site_id}/consumptions')
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
    