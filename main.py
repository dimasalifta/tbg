from dotenv import load_dotenv
import multiprocessing
import os
load_dotenv()
import paho.mqtt.client as mqtt
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
import json
import time
import struct
import minimalmodbus
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
# slave address (in decimal)
DEVICE_ADDRESS_SHT20 = 1
DEVICE_ADDRESS_ENERGY_METER = 2

# ENABLE/DISABLE communication debug mode
DEVICE_DEBUG = False
# Master PORT name -- Change as needed for your host.
PORT_NAME = '/dev/ttyUSB0'

# MODBUS instrument initialization
sht20 = minimalmodbus.Instrument(PORT_NAME, DEVICE_ADDRESS_SHT20, debug=DEVICE_DEBUG)
energy_meter = minimalmodbus.Instrument(PORT_NAME, DEVICE_ADDRESS_ENERGY_METER, debug=DEVICE_DEBUG)

# MODBUS instrument connection settings
# Change as needed depending on your Hardware requirements
sht20.serial.baudrate = 9600
sht20.serial.bytesize = 8
sht20.serial.parity   = minimalmodbus.serial.PARITY_NONE
sht20.serial.stopbits = 1
sht20.mode = minimalmodbus.MODE_RTU
sht20.serial.timeout = 1

energy_meter.serial.baudrate = 9600
energy_meter.serial.bytesize = 8
energy_meter.serial.parity   = minimalmodbus.serial.PARITY_NONE
energy_meter.serial.stopbits = 1
energy_meter.mode = minimalmodbus.MODE_RTU
energy_meter.serial.timeout = 1

REGISTER_NUMBER_DECIMALS_SHT20 = 1
REGISTER_NUMBER_DECIMALS_ENERGY_METER = 0
ModBus_Command = 4

list_register_sht20 = {
    "temperature" : [1," Celcius"],
    "humidity" : [2," %"] 
}


list_register_energy_meter = {
    "l1_voltage" : [0," V"],
    "l2_voltage" : [2," V"],
    "l3_voltage" : [4," V"],

    "total_ampere" : [6," A"],
    "l1_ampere" : [8," A"],
    "l2_ampere" : [10," A"],
    "l3_ampere" : [12," A"],
    
    "total_power" : [16," kW"],
    "l1_power" : [18," kW"],
    "l2_power" : [20," kW"],
    "l3_power" : [22," kW"],
    
    "total_kvarh" : [24," kVArh"],
    "l1_kvarh" : [26," kVArh"],
    "l2_kvarh" : [28," kVArh"],
    "l3_kvarh" : [30," kVArh"],
    
    "l1_power_factor" : [42," theta"],
    "l2_power_factor" : [44," theta"],
    "l3_power_factor" : [46," theta"],
    
    "3phase_frequency" : [54," Hz"],
    "energy_consumption" : [80," kWh"]
    
}
def convert_decimal(x):
    angka = int(x)
    hasil_pembagian = angka / 1000
    # hasil_bulatan = round(hasil_pembagian)  
    hasil = str(hasil_pembagian)
    return hasil   

def int_to_float(data):
    # Convert 16-bit integer to bytes (2 bytes)
    data_bytes = data.to_bytes(2, byteorder='big', signed=True)
    # Extend the bytes to 4 bytes by adding 2 more bytes of zero
    data_bytes += b'\x00\x00'
    # Convert bytes to 32-bit float
    float_value = struct.unpack('>f', data_bytes)[0]
    # Bulatkan nilai float menjadi 3 angka di belakang koma
    rounded_float_value = round(float_value, 3)
    return rounded_float_value

def hitung_backup_time(kapasitas_baterai_Ah, beban_Watt):
    kapasitas_baterai = 100 # Ah
    beban = 500 # Watt
    konsumsi_daya_Watt = beban_Watt
    backup_time_hours = kapasitas_baterai_Ah / konsumsi_daya_Watt
    return backup_time_hours

def read_rs485():
    try:
        energy_meter_data = {}
    # for key, values in list_register_sht20.items():
    #     address = values[0]  # Ambil alamat register dari elemen pertama dalam daftar
    #     unit = values[1]     # Ambil unit dari elemen kedua dalam daftar
    #     value = sht20.read_register(address, REGISTER_NUMBER_DECIMALS_SHT20, ModBus_Command)
    #     print(f"{key}: {value}{unit}")
        
        for key, values in list_register_energy_meter.items():
            address = values[0]  # Ambil alamat register dari elemen pertama dalam daftar
            unit = values[1]     # Ambil unit dari elemen kedua dalam daftar
            value = energy_meter.read_register(address, REGISTER_NUMBER_DECIMALS_ENERGY_METER, ModBus_Command)
            try:
                value = int_to_float(value)
                energy_meter_data[key] = value
                # print(f"{key}: {value}{unit}")
            except OverflowError:
                print(f"{value}{unit} Nilai dari {key} terlalu besar untuk dikonversi menjadi float.")
    except Exception as e:
        print(f"Failed to read from instrument ------ {e}")
    return energy_meter_data
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

def snmp_process():
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
                        val = convert_decimal(val.prettyPrint())
                        data[param_name] = val
                    else:
                        data[param_name] = val.prettyPrint()

            print(read_rs485())
            print(data)
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
    snmp_main = multiprocessing.Process(target=snmp_process) 
    snmp_main.start() 
