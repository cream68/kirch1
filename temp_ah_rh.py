import numpy as np
import matplotlib.pyplot as plt

# Constants
temperature_range = np.arange(-10, 31, 1)  # Temperature from -10 to 30°C
absolute_humidity_range = np.linspace(0, 20, 100)  # Absolute humidity from 0 to 20 g/m³


# Function to calculate saturation vapor pressure (E_s) using Magnus formula
def magnus_formula(temp):
    """
    Calculate the saturation vapor pressure using the Magnus formula.

    Parameters:
    - temp: Temperature in Celsius

    Returns:
    - Saturation vapor pressure (E_s) in hPa
    """
    if temp >0:
        return 288.68*(1.098+temp/100)**8.02/100
    else:
        return 4.689*(1.486+temp/100)**12.3/100


# Function to calculate relative humidity
def calculate_relative_humidity(temperature, absolute_humidity):
    # Saturation vapor pressure (es) in hPa using Magnus formula
    es = magnus_formula(temperature)

    # Actual vapor pressure (ea) in hPa
    Mw = 18.016  # Molecular weight of water vapor in kg/kmol
    R = 8314.3  # Universal gas constant in J/(kmol·K
    ea = absolute_humidity*(273.15+temperature)*R/Mw/10 ** 5

    # Relative humidity calculation
    RH = (ea / es) * 100

    return RH

def calculate_absolute_humidity(temp, rel_humidity):
    """
    Calculate the absolute humidity given temperature and relative humidity.

    Parameters:
    - temp: Temperature in Celsius
    - rel_humidity: Relative humidity in percentage

    Returns:
    - Absolute humidity in g/m³
    """
    E_s = magnus_formula(temp)
    E_a = (rel_humidity / 100.0) * E_s
    # Constants
    Mw = 18.016  # Molecular weight of water vapor in kg/kmol
    R = 8314.3  # Universal gas constant in J/(kmol·K)
    return 10 ** 5 * Mw / R * E_a / (temp + 273.15)
# Calculate relative humidity for each combination of temperature and absolute humidity
relative_humidity_values = np.zeros((len(temperature_range), len(absolute_humidity_range)))

for i, temperature in enumerate(temperature_range):
    for j, absolute_humidity in enumerate(absolute_humidity_range):
        RH = calculate_relative_humidity(temperature, absolute_humidity)
        relative_humidity_values[i, j] = RH

# Plotting
plt.figure(figsize=(8, 6))

# Plot contours of relative humidity for specific RH levels
RH_levels = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
CS = plt.contour(absolute_humidity_range, temperature_range, relative_humidity_values, levels=RH_levels, colors='b')
plt.clabel(CS, inline=True, fmt='%d', fontsize=10)

# Set labels and title
plt.xlabel('Absolute Humidity (g/m³)')
plt.ylabel('Temperature (°C)')
plt.title('Psychrometric Chart')

# Add temperature ticks every 2 degrees
plt.yticks(np.arange(-10, 31, 2))

temp=20.1
rh=69
ah = calculate_absolute_humidity(temp,rh)
print(ah)

# Add grid lines
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()
