from modules import sht20,energy,megmeet

# Read sensor data
temperature, humidity = sht20.read_sensor_data(debug=False)
# Read sensor data
temperature, humidity = energy.read_sensor_data(debug=False)