from modules import rs485_sht20,rs485_energy,snmp_megmeet
import time
# Read sensor data
value = rs485_sht20.read_sensor_data(debug=False)

print(value)