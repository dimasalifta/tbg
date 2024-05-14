
import minimalmodbus
import struct
# slave address (in decimal)
DEVICE_ADDRESS_ENERGY_METER = 2

# ENABLE/DISABLE communication debug mode
DEVICE_DEBUG = False
# Master PORT name -- Change as needed for your host.
PORT_NAME = '/dev/ttyUSB0'

# MODBUS instrument initialization
energy_meter = minimalmodbus.Instrument(PORT_NAME, DEVICE_ADDRESS_ENERGY_METER, debug=DEVICE_DEBUG)

# MODBUS instrument connection settings
# Change as needed depending on your Hardware requirements
energy_meter.serial.baudrate = 9600
energy_meter.serial.bytesize = 8
energy_meter.serial.parity   = minimalmodbus.serial.PARITY_NONE
energy_meter.serial.stopbits = 1
energy_meter.mode = minimalmodbus.MODE_RTU
energy_meter.serial.timeout = 1

REGISTER_NUMBER_DECIMALS_ENERGY_METER = 0
ModBus_Command = 4

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

try:
    for key, values in list_register_energy_meter.items():
        address = values[0]  # Ambil alamat register dari elemen pertama dalam daftar
        unit = values[1]     # Ambil unit dari elemen kedua dalam daftar
        value = energy_meter.read_register(address, REGISTER_NUMBER_DECIMALS_ENERGY_METER, ModBus_Command)
        try:
            value = int_to_float(value)
            print(f"{key}: {value}{unit}")
        except OverflowError:
            print(f"{value}{unit} Nilai dari {key} terlalu besar untuk dikonversi menjadi float.")
except Exception as e:
    print(f"Failed to read from instrument ------ {e}")

