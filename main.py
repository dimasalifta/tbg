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
import datetime
import socket

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_PORT=os.getenv("MQTT_PORT")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD=os.getenv("MQTPASSWORDRT")

SNMP_HOST=os.getenv("SNMP_HOST")
SNMP_COMMUNITY=os.getenv("SNMP_COMMUNITY")
SNMP_PORT=os.getenv("SNMP_PORT")

IMEI=os.getenv("IMEI")

tbg_topic = f"TBGPower/{IMEI}"
parameter_dict = {
  "site_id": ["identName","1.3.6.1.4.1.40211.1.1.1.4.0"],
  "system_type": ["identModel","1.3.6.1.4.1.40211.1.1.1.2.0"],
#   "system_type": ["identInternalVersion","1.3.6.1.4.1.402141.1.1.1.5.0"],
  "system_alarm_status":["systemStatus","1.3.6.1.4.1.40211.2.1.1.1.0"],

#   "system_current":["systemCurrent","1.3.6.1.4.1.40211.2.1.1.3.0"],
#   


#   "phase_l1_voltage": ["psInputLineAVoltage","1.3.6.1.4.1.40211.4.1.1.1.0"], 
#   "phase_l2_voltage": ["psInputLineBVoltage","1.3.6.1.4.1.40211.4.1.1.2.0"],
#   "phase_l3_voltage": ["psInputLineCVoltage","1.3.6.1.4.1.40211.4.1.1.3.0"],

#   "phase_l1_current": ["psInputLineAVoltage","1.3.6.1.4.1.40211.4.1.1.1.0"],
#   "phase_l2_current": ["psInputLineBVoltage","1.3.6.1.4.1.40211.4.1.1.2.0"],
#   "phase_l3_current": ["psInputLineCVoltage","1.3.6.1.4.1.40211.4.1.1.3.0"],
#   "phase_frequency": ["psInputFrequency","1.3.6.1.4.1.40211.4.1.1.4.0"],
  "dc_output_voltage":["systemVoltage","1.3.6.1.4.1.40211.2.1.1.2.0"],
  "total_rate_capacity":["battAH","1.3.6.1.4.1.40211.2.1.1.11.0"],
   #"total_rate_capacity_2":["battAH","1.3.6.1.4.1.40211.2.1.1.11.1"],
  
  "load_current_1":["loadCurr1","1.3.6.1.4.1.40211.3.1.1.6.0"],
  "load_current_2":["loadCurr2","1.3.6.1.4.1.40211.3.1.1.7.0"],
  "load_current_3":["loadCurr2","1.3.6.1.4.1.40211.3.1.1.8.0"],
  "load_current_4":["loadCurr3","1.3.6.1.4.1.40211.3.1.1.9.0"],
#   "total_dc_load_current":["psBatteryCurrent","1.3.6.1.4.1.40211.3.1.1.1.0"],
  "load_power_1":["load1Energy","1.3.6.1.4.1.40211.3.1.1.17.0"],
  "load_power_2":["load2Energy","1.3.6.1.4.1.40211.3.1.1.18.0"],
  "load_power_3":["load3Energy","1.3.6.1.4.1.40211.3.1.1.19.0"],
  "load_power_4":["load4Energy","1.3.6.1.4.1.40211.3.1.1.20.0"],
#   "total_dc_load_power":["battEnergy","1.3.6.1.4.1.40211.3.1.1.21.0"],

 
  "battery1_current":["psBatteryCurrent1","1.3.6.1.4.1.40211.3.1.1.2.0"],
  "battery2_current":["psBatteryCurrent2","1.3.6.1.4.1.40211.3.1.1.3.0"],
  "total_battery_current":["psBatteryCurrent","1.3.6.1.4.1.40211.3.1.1.1.0"],
  "battery1_capacity":["psBatteryCapacity1","1.3.6.1.4.1.40211.3.1.1.4.0"],
  "battery2_capacity":["psBatteryCapacity2","1.3.6.1.4.1.40211.3.1.1.5.0"],
  "dc_energy_consumption":["battEnergy","1.3.6.1.4.1.40211.3.1.1.21.0"],
#   "battery_slots":["battNum","1.3.6.1.4.1.40211.3.1.1.10.0"],
  
  "battery1_temperature":["psTemperature1","1.3.6.1.4.1.40211.5.1.1.1.0"],
  "battery2_temperature":["psTemperature2","1.3.6.1.4.1.40211.5.1.1.2.0"],

  "rectifier_total_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"],
  "rectifier_rate_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"], 
#   "rectifier_status":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"],
  
  "rectifier_slots":["rectNum","1.3.6.1.4.1.40211.8.2.1.8.0"],
#   "rectifier_1_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.1"],
#   "rectifier_1_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.1"],
  "rectifier1_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.1"],
  "rectifier1_output_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.4.1"],
  "rectifier1_load_usage":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.1"],
  "rectifier1_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.1"],
  "rectifier1_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.1"],
  "rectifier1_status":["onoffStatus","1.3.6.1.4.1.40211.8.1.1.7.1"],
  
  
#   "rectifier_2_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.2"],
#   "rectifier_2_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.2"],
  "rectifier2_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.2"],
  "rectifier2_output_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.4.2"],
  "rectifier2_load_usage":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.2"],
  "rectifier2_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.2"],
  "rectifier2_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.2"],
  "rectifier2_status":["onoffStatus","1.3.6.1.4.1.40211.8.1.1.7.2"],
#   "rectifier_3_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.3"],
#   "rectifier_3_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.3"],
  "rectifier3_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.3"],
  "rectifier3_output_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.4.3"],
  "rectifier3_load_usage":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.3"],
  "rectifier3_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.3"],
  "rectifier3_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"],
  "rectifier3_status":["onoffStatus","1.3.6.1.4.1.40211.8.1.1.7.3"],
  
  "battery_charging_status":["psStatusBatteryMode","1.3.6.1.4.1.40211.2.1.1.5.0"],
  "total_battery_current":["psBatteryCurrent","1.3.6.1.4.1.40211.3.1.1.1.0"],
}

alarm_parameter_dict = {
    "alarm_trap_no":["x","1.3.6.1.4.1.40211.10.1.1.1.x"],
    "alarm_time":["x","1.3.6.1.4.1.40211.10.1.1.2.x"],
    "alarm_status_change":["x","1.3.6.1.4.1.40211.10.1.1.3.x"],
    "alarm_severity":["x","1.3.6.1.4.1.40211.10.1.1.4.x"],
    "alarm_description":["x","1.3.6.1.4.1.40211.10.1.1.5.x"],
    "alarm_type":["x","1.3.6.1.4.1.40211.10.1.1.6.x"],
}

list_volt = [
             "dc_output_voltage",
             "battery1_temperature",
             "battery2_temperature",
             "battery_capacity_ah_1",
             "battery_capacity_ah_2",
             "load_current_1",
             "load_current_2",
             "load_current_3",
             "load_current_4",
             "load_power_1",
             "load_power_2",
             "load_power_3",
             "load_power_4",
             "dc_energy_consumption",
             "total_rate_capacity",
             ]

list_volt_2 = [
             "rectifier1_output_current",
             "rectifier2_output_current",
             "rectifier3_output_current",
             "rectifier1_output_voltage",
             "rectifier2_output_voltage",
             "rectifier3_output_voltage",
             "rectifier1_temperature",
             "rectifier2_temperature",
             "rectifier3_temperature",
             "battery1_capacity",
             "battery2_capacity"

             ]
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

    "total_current" : [6," A"],
    "l1_current" : [8," A"],
    "l2_current" : [10," A"],
    "l3_current" : [12," A"],
    
    "total_ac_input_power" : [16," kW"],
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
    "ac_energy_consumption" : [256," kWh"]
    
}

dummy_active_alarm = [{
}]
def convert_decimal(x):
    angka = int(x)
    hasil_pembagian = angka / 1000
    # hasil_bulatan = round(hasil_pembagian)  
    hasil = str(hasil_pembagian)
    return hasil   
def convert_decimal_2(x):
    angka = int(x)
    hasil_pembagian = angka / 10
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

def check_active_alarm():
    oid_template = "1.3.6.1.4.1.40211.10.1.1.%d.%d"   

    # Define a PySNMP CommunityData object named auth, by providing the SNMP community string
    auth = cmdgen.CommunityData(SNMP_COMMUNITY)

    # Define the CommandGenerator, which will be used to send SNMP queries
    cmdGen = cmdgen.CommandGenerator()

    # List to store results
    results = []

    # Iterate over x and y values
    for x in range(1, 7):
        # Dictionary to store values for each iteration of y
        data = {}
        for y in range(1, 7):  # Assuming y ranges from 1 to 6
            # Construct the OID by substituting %d with the iteration numbers
            oid = oid_template % (y, x)
            
            # Query the network device for the current OID
            errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                auth,
                cmdgen.UdpTransportTarget((SNMP_HOST, SNMP_PORT)),
                oid,
                lookupMib=True,
            )
            
            # Check if there was an error querying the device
            if errorIndication:
                sys.exit()
            
            # We only expect a single response from the host for each OID
            for oid, val in varBinds:
                # Assign values to keys based on the prefix
                if y == 1:
                    data["no"] = val.prettyPrint()
                elif y == 2:
                    #print(val.prettyPrint())
                    # Konversi nilai heksadesimal ke integer
                    hex_value = val.prettyPrint()
                    if hex_value.startswith("0x"):
                        hex_value = hex_value[2:]  # Hilangkan awalan '0x' jika ada
                    try:
                        timestamp = int(hex_value, 16)

                        # Konversi timestamp ke format datetime
                        dt_object = datetime.datetime.utcfromtimestamp(timestamp / 10**9)  # Ubah nanosekon menjadi mikrodetik

                        # Format waktu sesuai kebutuhan
                        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                        data["time"] = formatted_time
                        #print("Formatted Time:", formatted_time)
                    except ValueError as e:
                        print("Error converting timestamp:", e)
                    
                elif y == 3:
                    data["status_change"] = val.prettyPrint()
                elif y == 4:
                    data["severity"] = val.prettyPrint()
                elif y == 5:
                    data["desc"] = val.prettyPrint()
                elif y == 6:
                    data["type"] = val.prettyPrint()
        
        # Check if the data already exists in the results list, except for "no" key
        exists = any(item for item in results if all(data[k] == item[k] for k in data if k != "no"))
        
        # If data does not exist (excluding "no" key), append it to results list
        if not exists:
            results.append(data)

    # Convert the results list to JSON
    json_output = json.dumps(results, indent=4)
    print(json_output)
    return json_output

def get_ip():
    
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip
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
        # print(msg.payload)
        
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
    
def on_publish_alarm(payload):
    # Buat instance client MQTT
    client = mqtt.Client()

    # Hubungkan ke broker MQTT
    client.connect(MQTT_BROKER, 1883, 60)

    # Kirim pesan ke topik MQTT
    client.publish("tbg_iot_alarm", payload)

    # Tutup koneksi
    client.disconnect()
    
def on_publish_siteid(payload):
    # Buat instance client MQTT
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    # Hubungkan ke broker MQTT
    client.connect("mbiot.tower-bersama.com", 1884, 60)

    # Kirim pesan ke topik MQTT
    client.publish(f"{tbg_topic}/siteid", payload)

    # Tutup koneksi
    client.disconnect()

def on_publish_status(payload):
    # Buat instance client MQTT
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    # Hubungkan ke broker MQTT
    client.connect("mbiot.tower-bersama.com", 1884, 60)

    # Kirim pesan ke topik MQTT
    client.publish(f"{tbg_topic}/status", payload)

    # Tutup koneksi
    client.disconnect()
    
def on_publish_parameters(payload):
    # Buat instance client MQTT
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    # Hubungkan ke broker MQTT
    client.connect("mbiot.tower-bersama.com", 1884, 60)

    # Kirim pesan ke topik MQTT
    client.publish(f"{tbg_topic}/parameters", payload)

    # Tutup koneksi
    client.disconnect()
    
def on_publish_alarms(payload):
    # Buat instance client MQTT
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    # Hubungkan ke broker MQTT
    client.connect("mbiot.tower-bersama.com", 1884, 60)

    # Kirim pesan ke topik MQTT
    client.publish(f"{tbg_topic}/alarms", payload)

    # Tutup koneksi
    client.disconnect()
    
def on_publish_consumption(payload):
    # Buat instance client MQTT
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    # Hubungkan ke broker MQTT
    client.connect("mbiot.tower-bersama.com", 1884, 60)

    # Kirim pesan ke topik MQTT
    client.publish(f"{tbg_topic}/consumption", payload)

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
                    elif param_name in list_volt_2:
                        val = convert_decimal_2(val.prettyPrint())
                        data[param_name] = val
                    else:
                        data[param_name] = val.prettyPrint()
            pretty_active_alarm = check_active_alarm()
            rs485_data = read_rs485()
            # print(data)           
            site_id = data["site_id"]
            system_type = data["system_type"]
            l1_voltage = rs485_data["l1_voltage"]
            l2_voltage = rs485_data["l2_voltage"]
            l3_voltage = rs485_data["l3_voltage"]
            l1_current = rs485_data["l1_current"]
            l2_current = rs485_data["l2_current"]
            l3_current = rs485_data["l3_current"]
            ac_energy_consumption = rs485_data["ac_energy_consumption"]
            dc_output_voltage = data["dc_output_voltage"]
            
            battery1_temperature = data["battery1_temperature"]
            battery2_temperature = data["battery2_temperature"]
            
            load_current_1 = float(data["load_current_1"])
            load_current_2 = float(data["load_current_2"])
            load_current_3 = float(data["load_current_3"])
            load_current_4 = float(data["load_current_4"])
            total_dc_load_current =str(load_current_1+load_current_2+load_current_3+load_current_4)
            load_power_1 = float(data["load_power_1"])
            load_power_2 = float(data["load_power_2"])
            load_power_3 = float(data["load_power_3"])
            load_power_4 = float(data["load_power_4"])
            total_dc_load_power =str(load_power_1+load_power_2+load_power_3+load_power_4)
            dc_energy_consumption = data["dc_energy_consumption"]
            rectifier_slots = int(data["rectifier_slots"])
            rectifier_quantity = rectifier_slots - 3
            
            rectifier1_output_current = float(data["rectifier1_output_current"])
            rectifier2_output_current = float(data["rectifier2_output_current"])
            rectifier3_output_current = float(data["rectifier3_output_current"])
            rectifier_current = str(rectifier1_output_current+rectifier2_output_current+rectifier3_output_current)
            
            rectifier1_output_voltage = float(data["rectifier1_output_voltage"])
            rectifier2_output_voltage = float(data["rectifier2_output_voltage"])
            rectifier3_output_voltage = float(data["rectifier3_output_voltage"])
            rectifier_rate_voltage = str((rectifier1_output_voltage+rectifier2_output_voltage+rectifier3_output_voltage)/3)
            
            rectifier1_status = data["rectifier1_status"]
            rectifier1_serial_number = data["rectifier1_serial_number"]
            rectifier2_status = data["rectifier2_status"]
            rectifier2_serial_number = data["rectifier2_serial_number"]
            rectifier3_status = data["rectifier3_status"]
            rectifier3_serial_number = data["rectifier3_serial_number"]
 
            total_ac_input_power = rs485_data["total_ac_input_power"]

            rectifier1_load_usage = data["rectifier1_load_usage"]
            rectifier2_load_usage = data["rectifier2_load_usage"]
            rectifier3_load_usage = data["rectifier3_load_usage"]
            
            rectifier1_temperature = data["rectifier1_temperature"]
            rectifier2_temperature = data["rectifier2_temperature"]
            rectifier3_temperature = data["rectifier3_temperature"]
            # battery_disconnect_status = data["battery_disconnect_status"]
            
            battery1_current = data["battery1_current"]
            battery2_current = data["battery2_current"]
            total_battery_current = data["total_battery_current"]
            
            total_rate_capacity = float(data["total_rate_capacity"]) # unit Ah
            
            battery1_capacity = float(data["battery1_capacity"]) # %
            #print(battery1_capacity)
            battery2_capacity = float(data["battery2_capacity"]) # %
            total_remaining_capacity_percent = (battery1_capacity+battery2_capacity)/2
            #print(battery2_capacity)
            total_remaining_capacity = total_rate_capacity * (total_remaining_capacity_percent / 100)
            if float(total_dc_load_current) > 0 :
                backup_time = total_remaining_capacity / float(total_dc_load_current)
            else:
                backup_time = "-"
            
            system_alarm_status = data["system_alarm_status"]
            battery_charging_status = data["battery_charging_status"]
            
            parameter_tbg = {
                "site_id":site_id,
                "system_type":system_type,
                "l1_voltage":l1_voltage,
                "l2_voltage":l2_voltage,
                "l3_voltage":l3_voltage,
                "l1_current":l1_current,
                "l2_current":l2_current,
                "l3_current":l3_current,
                "ac_energy_consumption":ac_energy_consumption,
                "total_ac_input_power":total_ac_input_power,
                "dc_output_voltage":dc_output_voltage,
                
                "battery1_temperature":battery1_temperature,
                "battery2_temperature":battery2_temperature,
                "total_dc_load_current":total_dc_load_current,
                "total_dc_load_power":total_dc_load_power,
                "dc_energy_consumption":dc_energy_consumption,
                "rectifier_quantity":rectifier_quantity,
                "rectifier_current":rectifier_current,
                "rectifier_rate_voltage":rectifier_rate_voltage,
                "rectifier1_serial_number":rectifier1_serial_number,
                "rectifier1_status":rectifier1_status,
                "rectifier2_serial_number":rectifier2_serial_number,
                "rectifier2_status":rectifier2_status,
                "rectifier3_serial_number":rectifier3_serial_number,
                "rectifier3_status":rectifier3_status,
                "rectifier1_load_usage":rectifier1_load_usage,
                "rectifier2_load_usage":rectifier2_load_usage,
                "rectifier3_load_usage":rectifier3_load_usage,
                "rectifier1_temperature":rectifier1_temperature,
                "rectifier2_temperature":rectifier2_temperature,
                "rectifier3_temperature":rectifier3_temperature,
                "battery1_current":battery1_current,
                "battery2_current":battery2_current,
                "total_battery_current":total_battery_current,
                "total_rate_capacity":total_rate_capacity,
                "total_remaining_capacity":total_remaining_capacity,
                "total_remaining_capacity_percent":total_remaining_capacity_percent,
                "backup_time" : backup_time,
                "system_alarm_status" : system_alarm_status,
                "battery_charging_status" : battery_charging_status,
                
            }
            pretty_parameter_tbg = json.dumps(parameter_tbg, indent=4)
            print(pretty_parameter_tbg)
            # print(parameter_tbg)
            # Mengonversi data menjadi format JSON
            payload = json.dumps(data)
            
            # Mengirim payload JSON ke broker MQTT
            on_publish(pretty_parameter_tbg) 
            
            ###############################################################################################3
            on_publish_siteid("Developer Bintaro")
            
            my_ip = get_ip()
            status_payload = {"online": 1,
                              "ip":f"{my_ip}"}
            on_publish_status(status_payload)
            
            
            # example_parameters = {"AC Voltage":{"L1":220,
            #                          "L2":220,
            #                          "L3":220},
            #            "AC Current":{"L1":2,
            #                          "L2":2,
            #                          "L3":2.3},
            #            "DC Voltage":40,
            #            "DC Current":20}
            paramaters_payload = {
                "AC Voltage":{"L1":l1_voltage,
                              "L2":l2_voltage,
                              "L3":l3_voltage},
                "AC Current":{"L1":l1_current,
                              "L2":l2_current,
                              "L3":l3_current},
                
                "DC Output Voltage":dc_output_voltage,  
                
                "Rectifier Total Current":rectifier_current,
                
                "Battery Capacity":total_remaining_capacity_percent,
                
                "Battery Current    ":total_battery_current,
                
                "Backup Time" : backup_time,
                "Battery Temperature":{"Battery 1":battery1_temperature,
                                       "Battery 2":battery2_temperature},
                "Recitifier Temperature":{"Rectifier 1": rectifier1_temperature,
                                          "Rectifier 2": rectifier2_temperature,
                                          "Rectifier 3": rectifier3_temperature},
                "Rectifier Installed":rectifier_quantity,
                "Recitifier Serial Number":{"Rectifier 1": rectifier1_serial_number,
                                          "Rectifier 2": rectifier2_serial_number,
                                          "Rectifier 3": rectifier3_serial_number},
                "Recitifier Load Usage":{"Rectifier 1": rectifier1_load_usage,
                                          "Rectifier 2": rectifier2_load_usage,
                                          "Rectifier 3": rectifier3_load_usage},
                "Recitifier Status":{"Rectifier 1": rectifier1_status,
                                          "Rectifier 2": rectifier2_status,
                                          "Rectifier 3": rectifier3_status},
                "Temperature" : "nan",
                "Humidity" : "nan",
                
                "total_remaining_capacity":total_remaining_capacity,
                "total_dc_load_current":total_dc_load_current,
                "total_dc_load_power":total_dc_load_power,
                "rectifier_rate_voltage":rectifier_rate_voltage,
                "battery1_current":battery1_current,
                "battery2_current":battery2_current,
                "total_rate_capacity":total_rate_capacity,
                "system_alarm_status" : system_alarm_status,
                "battery_charging_status" : battery_charging_status,
                "total_ac_input_power":total_ac_input_power,

                
            }
            
            
            on_publish_parameters(paramaters_payload)
            
            if data['system_alarm_status'] == "4" or "5":
                on_publish_alarm(pretty_active_alarm)
                on_publish_alarms(pretty_active_alarm)
            else:
                on_publish_alarm(dummy_active_alarm)
                on_publish_alarms(dummy_active_alarm)
            
            consumption_payload = {"AC":ac_energy_consumption,
                                  "DC":dc_energy_consumption}
            on_publish_consumption(consumption_payload)
            
            
            time.sleep(2)
        except Exception as e:
            print("Exception:", e)

        
        
    
if __name__ == "__main__":
    # Buat process untuk menjalankan client MQTT
    mqtt_main = multiprocessing.Process(target=mqtt_process)
    mqtt_main.start()    
    snmp_main = multiprocessing.Process(target=snmp_process) 
    snmp_main.start() 
