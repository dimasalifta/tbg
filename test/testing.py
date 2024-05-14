list_register_energy_meter = {
    "l1_voltage" : [0," V"],
    "l2_voltage" : [2," V"],
    "l3_voltage" : [4," V"],

    "total_current" : [6," A"],
    "l1_current" : [8," A"],
    "l2_current" : [10," A"],
    "l3_current" : [12," A"],
    
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
    "energy_consumption" : [256," kWh"]
}

# Initialize variables to None
for key in list_register_energy_meter.keys():
    globals()[key] = None

# Print variables to check their values
for key in list_register_energy_meter.keys():
    print(f"{key}: {globals()[key]}")
