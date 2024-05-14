# main_script.py
import sht20

# Read sensor data
temperature, humidity = sht20.read_sensor_data()

# Display the values of the variables
if temperature is not None and humidity is not None:
    print(f"Temperature: {temperature} Celcius")
    print(f"Humidity: {humidity} %")
else:
    print("Failed to retrieve sensor data")
