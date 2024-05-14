# main_script.py
import sht20

# Read sensor data
temperature, humidity = sht20.read_sensor_data(debug=False)

# Display the values of the variables

print(f"Temperature: {temperature} Celcius")
print(f"Humidity: {humidity} %")

