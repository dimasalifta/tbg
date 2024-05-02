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
                # Buka file JSON
            with open(json_file) as f:
                json_data = json.load(f)
            # Define the CommandGenerator outside the loop
            cmdGen = cmdgen.CommandGenerator()

            # Loop through each JSON object
            for obj in json_data:
                # Ambil OID dari objek JSON
                oid = obj['oid']
                signal_name = obj['signal_name']
                oid = oid[2:]
                # print(oid)
                SYSNAME = oid

                host = '192.168.10.15'
                snmp_ro_comm = 'public'

                # Define a PySNMP CommunityData object named auth, by providing the SNMP community string
                auth = cmdgen.CommunityData(snmp_ro_comm)

                # Query a network device using the getCmd() function, providing the auth object, a UDP transport
                # our OID for SYSNAME, and don't lookup the OID in PySNMP's MIB's
                try:
                    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                        auth,
                        cmdgen.UdpTransportTarget((host, 161)),
                        cmdgen.MibVariable(SYSNAME),
                        lookupMib=False,
                    )
                    # time.sleep(0.5)
                    # Check if there was an error querying the device
                    if errorIndication:
                        print("Error:", errorIndication)
                        continue  # Skip to the next JSON object
                except Exception as e:
                    print(f"Error Query: {e}")
                # We only expect a single response from the host for sysName, but varBinds is an object
                # that we need to iterate over. It provides the OID and the value, both of which have a
                # prettyPrint() method so that you can get the actual string data

                for oid, val in varBinds:
                    print(oid.prettyPrint(), val.prettyPrint(), signal_name)

        except Exception as e:
            print("Exception:", e)

        
        
    
if __name__ == "__main__":
    # Buat process untuk menjalankan client MQTT
    mqtt_main = multiprocessing.Process(target=mqtt_process)
    mqtt_main.start()    
    snmp_main = multiprocessing.Process(target=snmp_process('mc2600_oid_list.json')) 
    snmp_main.start() 
