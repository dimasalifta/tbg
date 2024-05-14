import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen
import json

list_parameter_megmeet = {
  "site_id": ["identName","1.3.6.1.4.1.40211.1.1.1.4.0"," "],
  "system_alarm_status":["systemStatus","1.3.6.1.4.1.40211.2.1.1.1.0"," "],
  "system_voltage":["systemVoltage","1.3.6.1.4.1.40211.2.1.1.2.0", "mV"],
  "system_current":["systemCurrent","1.3.6.1.4.1.40211.2.1.1.3.0", "mA"],
  "battery_charging_state":["psStatusBatteryMode","1.3.6.1.4.1.40211.2.1.1.5.0", " "],
  
  
#   "total_rate_capacity":["battAH","1.3.6.1.4.1.40211.2.1.1.11.0"],
#    #"total_rate_capacity_2":["battAH","1.3.6.1.4.1.40211.2.1.1.11.1"],
  
#   "load_current_1":["loadCurr1","1.3.6.1.4.1.40211.3.1.1.6.0"],
#   "load_current_2":["loadCurr2","1.3.6.1.4.1.40211.3.1.1.7.0"],
#   "load_current_3":["loadCurr2","1.3.6.1.4.1.40211.3.1.1.8.0"],
#   "load_current_4":["loadCurr3","1.3.6.1.4.1.40211.3.1.1.9.0"],
# #   "total_dc_load_current":["psBatteryCurrent","1.3.6.1.4.1.40211.3.1.1.1.0"],
#   "load_power_1":["load1Energy","1.3.6.1.4.1.40211.3.1.1.17.0"],
#   "load_power_2":["load2Energy","1.3.6.1.4.1.40211.3.1.1.18.0"],
#   "load_power_3":["load3Energy","1.3.6.1.4.1.40211.3.1.1.19.0"],
#   "load_power_4":["load4Energy","1.3.6.1.4.1.40211.3.1.1.20.0"],
# #   "total_dc_load_power":["battEnergy","1.3.6.1.4.1.40211.3.1.1.21.0"],

 
#   "battery1_current":["psBatteryCurrent1","1.3.6.1.4.1.40211.3.1.1.2.0"],
#   "battery2_current":["psBatteryCurrent2","1.3.6.1.4.1.40211.3.1.1.3.0"],
#   "total_battery_current":["psBatteryCurrent","1.3.6.1.4.1.40211.3.1.1.1.0"],
#   "battery1_capacity":["psBatteryCapacity1","1.3.6.1.4.1.40211.3.1.1.4.0"],
#   "battery2_capacity":["psBatteryCapacity2","1.3.6.1.4.1.40211.3.1.1.5.0"],
#   "dc_energy_consumption":["battEnergy","1.3.6.1.4.1.40211.3.1.1.21.0"],
# #   "battery_slots":["battNum","1.3.6.1.4.1.40211.3.1.1.10.0"],
  
#   "battery1_temperature":["psTemperature1","1.3.6.1.4.1.40211.5.1.1.1.0"],
#   "battery2_temperature":["psTemperature2","1.3.6.1.4.1.40211.5.1.1.2.0"],

#   "rectifier_total_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"],
#   "rectifier_rate_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"], 
# #   "rectifier_status":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"],
  
#   "rectifier_slots":["rectNum","1.3.6.1.4.1.40211.8.2.1.8.0"],
# #   "rectifier_1_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.1"],
# #   "rectifier_1_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.1"],
#   "rectifier1_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.1"],
#   "rectifier1_output_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.4.1"],
#   "rectifier1_load_usage":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.1"],
#   "rectifier1_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.1"],
#   "rectifier1_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.1"],
#   "rectifier1_status":["onoffStatus","1.3.6.1.4.1.40211.8.1.1.7.1"],
  
  
# #   "rectifier_2_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.2"],
# #   "rectifier_2_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.2"],
#   "rectifier2_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.2"],
#   "rectifier2_output_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.4.2"],
#   "rectifier2_load_usage":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.2"],
#   "rectifier2_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.2"],
#   "rectifier2_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.2"],
#   "rectifier2_status":["onoffStatus","1.3.6.1.4.1.40211.8.1.1.7.2"],
# #   "rectifier_3_address":["rectNum","1.3.6.1.4.1.40211.8.1.1.1.3"],
# #   "rectifier_3_input_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.2.3"],
#   "rectifier3_output_voltage":["rectNum","1.3.6.1.4.1.40211.8.1.1.3.3"],
#   "rectifier3_output_current":["rectNum","1.3.6.1.4.1.40211.8.1.1.4.3"],
#   "rectifier3_load_usage":["rectNum","1.3.6.1.4.1.40211.8.1.1.5.3"],
#   "rectifier3_temperature":["rectNum","1.3.6.1.4.1.40211.8.1.1.6.3"],
#   "rectifier3_serial_number":["rectNum","1.3.6.1.4.1.40211.8.1.1.8.3"],
#   "rectifier3_status":["onoffStatus","1.3.6.1.4.1.40211.8.1.1.7.3"],
  
  
#   "total_battery_current":["psBatteryCurrent","1.3.6.1.4.1.40211.3.1.1.1.0"],
}

def read_sensor_data(debug=False):
    sensor_data = {}
    try:
        cmdGen = cmdgen.CommandGenerator()
        auth = cmdgen.CommunityData('public')

        # Inisialisasi dictionary untuk menyimpan data

        for param_name, (signale_name, oid, unit) in list_parameter_megmeet.items():
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
                print(type(val.prettyPrint()))
                print(oid.prettyPrint(), val.prettyPrint())
                sensor_data[param_name] = {"value":val,
                                            "unit":unit,
                                            "type":f"{type(val)}"}
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