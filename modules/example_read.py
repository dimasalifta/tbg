# main_script.py
import sht20
import energy

# Read sensor data
temperature, humidity = sht20.read_sensor_data(debug=False)
energy_consumption= energy.read_sensor_data(debug=False)

# Display the values of the variables

print(f"Temperature: {temperature} Celcius")
print(f"Humidity: {humidity} %")
print(f"Energy  : {energy_consumption} kW")

