from dotenv import load_dotenv
import multiprocessing
import os
load_dotenv()
import paho.mqtt.client as mqtt
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
import json
import time
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_PORT=os.getenv("MQTT_PORT")

SNMP_HOST=os.getenv("SNMP_HOST")
SNMP_COMMUNITY=os.getenv("SNMP_COMMUNITY")
SNMP_PORT=os.getenv("SNMP_PORT")

parameter_dict = {
  "site_id": ["identName","1.3.6.1.4.1.40211.1.1.1.4.0"],
  "system_type": ["identModel","1.3.6.1.4.1.40211.1.1.1.2.0"],
#   "system_type": ["identInternalVersion","1.3.6.1.4.1.402141.1.1.1.5.0"],
#   "system_alarm_status":["systemStatus","1.3.6.1.4.1.40211.2.1.1.1.0"],

#   "system_current":["systemCurrent","1.3.6.1.4.1.40211.2.1.1.3.0"],
#   


  "phase_l1_voltage": ["psInputLineAVoltage","1.3.6.1.4.1.40211.4.1.1.1.0"], 
  "phase_l2_voltage": ["psInputLineBVoltage","1.3.6.1.4.1.40211.4.1.1.2.0"],
  "phase_l3_voltage": ["psInputLineCVoltage","1.3.6.1.4.1.40211.4.1.1.3.0"],

  "phase_l1_current": ["psInputLineAVoltage","1.3.6.1.4.1.40211.4.1.1.1.0"],
  "phase_l2_current": ["psInputLineBVoltage","1.3.6.1.4.1.40211.4.1.1.2.0"],
  "phase_l3_current": ["psInputLineCVoltage","1.3.6.1.4.1.40211.4.1.1.3.0"],
#   "phase_frequency": ["psInputFrequency","1.3.6.1.4.1.40211.4.1.1.4.0"],
  "dc_output_voltage":["systemVoltage","1.3.6.1.4.1.40211.2.1.1.2.0"],
  "battery_capacity_ah_1":["battAH","1.3.6.1.4.1.40211.2.1.1.11.0"],
#   "battery_capacity_ah_2":["battAH","1.3.6.1.4.1.40211.2.1.1.11.1"],
  
#   "load_current_1":["loadCurr1","1.3.6.1.4.1.40211.3.1.1.6.0"],
#   "load_current_2":["loadCurr2","1.3.6.1.4.1.40211.3.1.1.7.0"],
#   "load_current_3":["loadCurr2","1.3.6.1.4.1.40211.3.1.1.8.0"],
#   "load_current_4":["loadCurr3","1.3.6.1.4.1.40211.3.1.1.9.0"],
  "total_load_current":["psBatteryCurrent","1.3.6.1.4.1.40211.3.1.1.1.0"],
#   "load_power_1":["load1Energy","1.3.6.1.4.1.40211.3.1.1.17.0"],
#   "load_power_2":["load2Energy","1.3.6.1.4.1.40211.3.1.1.18.0"],
#   "load_power_3":["load3Energy","1.3.6.1.4.1.40211.3.1.1.19.0"],
#   "load_power_4":["load4Energy","1.3.6.1.4.1.40211.3.1.1.20.0"],
  "total_load_power":["battEnergy","1.3.6.1.4.1.40211.3.1.1.21.0"],

 
#   "battery_current_1":["psBatteryCurrent1","1.3.6.1.4.1.40211.3.1.1.2.0"],
#   "battery_current_2":["psBatteryCurrent2","1.3.6.1.4.1.40211.3.1.1.3.0"],
#   "total_battery_current":["psBatteryCurrent","1.3.6.1.4.1.40211.3.1.1.1.0"],
#   "battery_capacity_1":["psBatteryCapacity1","1.3.6.1.4.1.40211.3.1.1.4.0"],
#   "battery_capacity_2":["psBatteryCapacity2","1.3.6.1.4.1.40211.3.1.1.5.0"],
  "dc_energy_consumption":["battEnergy","1.3.6.1.4.1.40211.3.1.1.21.0"],
#   "battery_slots":["battNum","1.3.6.1.4.1.40211.3.1.1.10.0"],
  
#   "battery_temperature_1":["psTemperature1","1.3.6.1.4.1.40211.5.1.1.1.0"],
#   "battery_temperature_2":["psTemperature2","1.3.6.1.4.1.40211.5.1.1.2.0"],

  "rectifier_total_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"],
  "rectifier_rate_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"], 
#   "rectifier_status":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"],
  
#   "rectifier_slots":["rectNum","1.3.6.1.4.1.40211.8.2.1.8.0"],
#   "rectifier_1_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.1"],
#   "rectifier_1_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.1"],
  "rectifier_1_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.1"],
  "rectifier_1_output_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.4.1"],
  "rectifier_1_power":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.1"],
  "rectifier_1_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.1"],
  "rectifier_1_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.1"],
  
#   "rectifier_2_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.2"],
#   "rectifier_2_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.2"],
  "rectifier_2_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.2"],
  "rectifier_2_output_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.4.2"],
  "rectifier_2_power":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.2"],
  "rectifier_2_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.2"],
  "rectifier_2_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.2"],

#   "rectifier_3_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.3"],
#   "rectifier_3_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.3"],
  "rectifier_3_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.3"],
  "rectifier_3_output_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.4.3"],
  "rectifier_3_power":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.3"],
  "rectifier_3_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.3"],
  "rectifier_3_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"],

  "battery_charging_status":["psStatusBatteryMode","1.3.6.1.4.1.40211.2.1.1.5.0"],
"total_battery_current":["psBatteryCurrent","1.3.6.1.4.1.40211.3.1.1.1.0"],
}



list_volt = ["phase_l1_voltage",
             "phase_l2_voltage",
             "phase_l3_voltage",
             "dc_output_voltage",
             "battery_capacity_ah_1",
             "battery_capacity_ah_2"]

def convert_volt(x):
    angka = int(x)
    hasil_pembagian = angka / 1000
    # hasil_bulatan = round(hasil_pembagian)  
    hasil = str(hasil_pembagian)
    return hasil   

# def hitung_backup_time(kapasitas_baterai_Ah, beban_Watt):
#     kapasitas_baterai = 100 # Ah
#     beban = 500 # Watt
#     konsumsi_daya_Watt = beban_Watt
#     backup_time_hours = kapasitas_baterai_Ah / konsumsi_daya_Watt
#     return backup_time_hours


# Fungsi untuk menginisiFalisasi koneksi MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(MQTT_TOPIC)  # Subscribe ke topik "topic/test"
    else:
        print("Connection failed")

# Fungsi yang dipanggil ketika pesan diterima
def on_message(client, userdata, msg):
    print("Received message on topic:", msg.topic)
    try:
        print("Received payload:")
        print(msg.payload)
        
    except ValueError:
        # Jika payload tidak bisa diuraikan sebagai JSON, cetak sebagai string biasa
        print("Received message:", msg.payload)

def on_publish(payload):
    # Buat instance client MQTT
    client = mqtt.Client()

    # Hubungkan ke broker MQTT
    client.connect(MQTT_BROKER, 1883, 60)

    # Kirim pesan ke topik MQTT
    client.publish(MQTT_TOPIC, payload)

    # Tutup koneksi
    client.disconnect()

def mqtt_process():
    # Buat instance client MQTT
    client = mqtt.Client()

    # Atur callback untuk koneksi dan pesan yang diterima
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()

def snmp_process(json_file):
    while True:
        try:
            cmdGen = cmdgen.CommandGenerator()
            auth = cmdgen.CommunityData(SNMP_COMMUNITY)

            # Inisialisasi dictionary untuk menyimpan data
            data = {}

            for param_name, (oid_name, oid_value) in parameter_dict.items():
                try:
                    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                        auth,
                        cmdgen.UdpTransportTarget((SNMP_HOST, SNMP_PORT)),
                        cmdgen.MibVariable(oid_value),
                        lookupMib=False,
                    )
                    if errorIndication:
                        print("Error:", errorIndication)
                        continue
                except Exception as e:
                    print(f"Error Query: {e}")

                for oid, val in varBinds:
                    # print(oid.prettyPrint(), val.prettyPrint())
                    # Menyimpan nilai ke dalam dictionary data
                    if param_name in list_volt:
                        val = convert_volt(val.prettyPrint())
                        data[param_name] = val
                    else:
                        data[param_name] = val.prettyPrint()

            # Mengonversi data menjadi format JSON
            payload = json.dumps(data)
            
            # Mengirim payload JSON ke broker MQTT
            on_publish(payload)
            time.sleep(5)
        except Exception as e:
            print("Exception:", e)

        
        
    
if __name__ == "__main__":
    # Buat process untuk menjalankan client MQTT
    mqtt_main = multiprocessing.Process(target=mqtt_process)
    mqtt_main.start()    
    snmp_main = multiprocessing.Process(target=snmp_process('mc2600_oid_list.json')) 
    snmp_main.start() 
