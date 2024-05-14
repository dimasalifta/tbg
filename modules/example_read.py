# main_script.py
import sht20
import energy
import time
# Read sensor data
temperature, humidity = sht20.read_sensor_data(debug=False)
time.sleep(1)
phase_frequency, energy_consumption = energy.read_sensor_data(debug=False)

# Display the values of the variables

print(f"Temperature: {temperature} Celcius")
print(f"Humidity: {humidity} %")
print(f"phase  : {phase_frequency} kW")
print(f"Energy  : {energy_consumption} kW")

