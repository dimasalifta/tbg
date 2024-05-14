from modules import rs485_sht20,rs485_energy,snmp_megmeet
import time
# Read sensor data
data_sht20      = rs485_sht20.  read_sensor_data(debug=True)
time.sleep(1)
data_energy     = rs485_energy. read_sensor_data(debug=True)
time.sleep(1)
data_megmeet    = snmp_megmeet. read_sensor_data(debug=True)
time.sleep(1)

