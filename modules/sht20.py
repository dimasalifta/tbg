
import minimalmodbus
# slave address (in decimal)
DEVICE_ADDRESS_SHT20 = 1

# ENABLE/DISABLE communication debug mode
DEVICE_DEBUG = False
# Master PORT name -- Change as needed for your host.
PORT_NAME = '/dev/ttyUSB0'

# MODBUS instrument initialization
sht20 = minimalmodbus.Instrument(PORT_NAME, DEVICE_ADDRESS_SHT20, debug=DEVICE_DEBUG)

# MODBUS instrument connection settings
# Change as needed depending on your Hardware requirements
sht20.serial.baudrate = 9600
sht20.serial.bytesize = 8
sht20.serial.parity   = minimalmodbus.serial.PARITY_NONE
sht20.serial.stopbits = 1
sht20.mode = minimalmodbus.MODE_RTU
sht20.serial.timeout = 1

REGISTER_NUMBER_DECIMALS_SHT20 = 1
ModBus_Command = 4

list_register_sht20 = {
    "temperature" : [1," Celcius"],
    "humidity" : [2," %"] 
}

# Initialize variables to None
for key in list_register_sht20.keys():
    globals()[key] = None
    
def read_sensor_data():
    try:
        for key, values in list_register_sht20.items():
            address = values[0]  # Ambil alamat register dari elemen pertama dalam daftar
            unit = values[1]     # Ambil unit dari elemen kedua dalam daftar
            value = sht20.read_register(address, REGISTER_NUMBER_DECIMALS_SHT20, ModBus_Command)
            if key == "temperature":
                temperature = value
            elif key == "humidity":
                humidity = value
            print(f"{key}: {value}{unit}")
        return temperature, humidity
    except Exception as e:
        print(f"Failed to read from instrument ------ {e}")

