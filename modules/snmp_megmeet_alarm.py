import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
import json
import numpy as np
import datetime


def read_sensor_data(debug=False):
    oid_template = "1.3.6.1.4.1.40211.10.1.1.%d.%d"   

    # Define a PySNMP CommunityData object named auth, by providing the SNMP community string
    auth = cmdgen.CommunityData('public')

    # Define the CommandGenerator, which will be used to send SNMP queries
    cmdGen = cmdgen.CommandGenerator()

    # List to store results
    results = []
    sensor_data = {}
    try:
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
                    cmdgen.UdpTransportTarget(('192.168.10.15', 161)),
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

        # # Convert the results list to JSON
        # json_output = json.dumps(results, indent=4)
        # print(json_output)
        if debug:
            print("##################################################")
            print(f"{__file__}")
            sensor_data = json.dumps(results, indent=4)
            print(sensor_data)
            print("##################################################")
        return sensor_data
    except Exception as e:
        print(f"Error Query: {e}")
        return sensor_data