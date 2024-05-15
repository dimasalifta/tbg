import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
import json
import numpy as np

list_parameter_megmeet = {
  "site_id": ["identName",
              "1.3.6.1.4.1.40211.1.1.1.4.0",
              " ",
              "string"],
  "system_alarm_status":["systemStatus",
                         "1.3.6.1.4.1.40211.2.1.1.1.0",
                         " ",
                         "integer"],
  "system_voltage":["systemVoltage",
                    "1.3.6.1.4.1.40211.2.1.1.2.0",
                    "mV",
                    "integer32"],
  "system_current":["systemCurrent",
                    "1.3.6.1.4.1.40211.2.1.1.3.0",
                    "mA",
                    "integer32"],
  "battery_charging_state":["psStatusBatteryMode",
                            "1.3.6.1.4.1.40211.2.1.1.5.0",
                            " ",
                            "integer"],
  
  
  "battery_nominal_capacity":["battAH",
                              "1.3.6.1.4.1.40211.2.1.1.11.0",
                              "mAh",
                              "integer32"],

  "load_current_1":["loadCurr1",
                    "1.3.6.1.4.1.40211.3.1.1.6.0",
                    "mA",
                    "integer32"],
  "load_current_2":["loadCurr2",
                    "1.3.6.1.4.1.40211.3.1.1.7.0",
                    "mA",
                    "integer32"],
  "load_current_3":["loadCurr3",
                    "1.3.6.1.4.1.40211.3.1.1.8.0",
                    "mA",
                    "integer32"],
  "load_current_4":["loadCurr4",
                    "1.3.6.1.4.1.40211.3.1.1.9.0",
                    "mA",
                    "integer32"],
  "load_shunt_detection":["loadshuntNum",
                          "1.3.6.1.4.1.40211.3.1.1.11.0",
                          " ",
                          "integer32"],
  "load_power_1":["load1Energy",
                  "1.3.6.1.4.1.40211.3.1.1.17.0",
                  "Wh",
                  "integer32"],
  "load_power_2":["load2Energy",
                  "1.3.6.1.4.1.40211.3.1.1.18.0",
                  "Wh",
                  "integer32"],
  "load_power_3":["load3Energy",
                  "1.3.6.1.4.1.40211.3.1.1.19.0",
                  "Wh",
                  "integer32"],
  "load_power_4":["load4Energy",
                  "1.3.6.1.4.1.40211.3.1.1.20.0",
                  "Wh",
                  "integer32"],
  
  "battery1_temperature":["psTemperature1",
                          "1.3.6.1.4.1.40211.5.1.1.1.0",
                          "Celcius",
                          "integer32"],
  "battery2_temperature":["psTemperature2",
                          "1.3.6.1.4.1.40211.5.1.1.2.0",
                          "Celcius",
                          "integer32"],
  "total_dc_load_current":["psBatteryCurrent",
                           "1.3.6.1.4.1.40211.3.1.1.1.0",
                           "A",
                           "integer32"],

# #   "total_dc_load_power":["battEnergy","1.3.6.1.4.1.40211.3.1.1.21.0"],

 
  "battery1_current":["psBatteryCurrent1",
                      "1.3.6.1.4.1.40211.3.1.1.2.0",
                      "mA",
                      "integer32"],
  "battery2_current":["psBatteryCurrent2",
                      "1.3.6.1.4.1.40211.3.1.1.3.0",
                      "mA",
                      "integer32"],
  "total_battery_current":["psBatteryCurrent",
                           "1.3.6.1.4.1.40211.3.1.1.1.0",
                           "mA",
                           "integer32"],

  "battery1_capacity":["psBatteryCapacity1",
                       "1.3.6.1.4.1.40211.3.1.1.4.0",
                       "%",
                       "integer32"],
  "battery2_capacity":["psBatteryCapacity2",
                       "1.3.6.1.4.1.40211.3.1.1.5.0",
                       "%",
                       "integer32"],
  "battery_energy":["battEnergy",
                    "1.3.6.1.4.1.40211.3.1.1.21.0",
                    "Wh",
                    "integer32"],
# #   "battery_slots":["battNum","1.3.6.1.4.1.40211.3.1.1.10.0"],
  



  
  "rectifier_slots":["rectNum","1.3.6.1.4.1.40211.8.2.1.8.0",
                     " ",
                     "integer32"],
  
#   "rectifier_1_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.1"],
#   "rectifier_1_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.1"],
#   "rectifier1_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.1"],
  "rectifier1_output_current":["rectNum",
                               "1.3.6.1.4.1.40211.8.1.1.4.1",
                               "A",
                               "integer32"],
  "rectifier1_load_usage":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.1",
                               "W",
                               "integer32"],
  "rectifier1_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.1",
                               "Celcius",
                               "integer32"],
  "rectifier1_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.1",
                               " ",
                               "string"],
  "rectifier1_status":["onoffStatus","1.3.6.1.4.1.40211.8.1.1.7.1",
                               " ",
                               "string"],
  
  
#    "rectifier_2_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.2"],
#    "rectifier_2_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.2"],
#   "rectifier2_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.2"],
  "rectifier2_output_current":["rectNum",
                               "1.3.6.1.4.1.40211.8.1.1.4.2",
                               "A",
                               "integer32"],
  "rectifier2_load_usage":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.2",
                               "W",
                               "integer32"],
  "rectifier2_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.2",
                               "Celcius",
                               "integer32"],
  "rectifier2_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.2",
                               " ",
                               "string"],
  "rectifier2_status":["onoffStatus","1.3.6.1.4.1.40211.8.1.1.7.2",
                               " ",
                               "string"],
  
#    "rectifier_3_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.3"],
#   "rectifier_3_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.3"],
#   "rectifier3_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.3"],
  "rectifier3_output_current":["rectNum",
                               "1.3.6.1.4.1.40211.8.1.1.4.3",
                               "A",
                               "integer32"],
  "rectifier3_load_usage":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.3",
                               "W",
                               "integer32"],
  "rectifier3_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.3",
                               "Celcius",
                               "integer32"],
  "rectifier3_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3",
                               " ",
                               "string"],
  "rectifier3_status":["onoffStatus","1.3.6.1.4.1.40211.8.1.1.7.3",
                               " ",
                               "string"],
  
}

def read_sensor_data(debug=False):
    sensor_data = {}
    try:
        cmdGen = cmdgen.CommandGenerator()
        auth = cmdgen.CommunityData('public')

        # Inisialisasi dictionary untuk menyimpan data

        for param_name, (signale_name, oid, unit, val_type) in list_parameter_megmeet.items():
            try:
                errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                    auth,
                    cmdgen.UdpTransportTarget(('192.168.10.15', 161)),
                    cmdgen.MibVariable(oid),
                    lookupMib=False,
                )
                if errorIndication:
                    print("Error:", errorIndication)
                    continue
            except Exception as e:
                print(f"Error Query: {e}")

            for oid, val in varBinds:
                # print(type(val.prettyPrint()))
                # print(oid.prettyPrint(), val.prettyPrint())
                
                if val_type == "string":
                    val = str(val)
                elif val_type == "integer":
                    val = int(val)
                elif val_type == "integer32":
                    val = int(val)
                elif val_type == " ":
                    val = val
            
                sensor_data[param_name] = {"value":val,
                                            "unit":unit,
                                            "type":f"{type(val)}"}
                # print(sensor_data)
        if debug:
            print("##################################################")
            print(f"{__file__}")
            sensor_data = json.dumps(sensor_data, indent=4)
            print(sensor_data)
            print("##################################################")
        return sensor_data
    except Exception as e:
        print(f"Error Query: {e}")
        return sensor_data