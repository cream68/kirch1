import math

def saturation_vapor_pressure(temperature):
    """https://de.wikipedia.org/wiki/S%C3%A4ttigungsdampfdruck"""
    """https://planetcalc.com/2161/"""
    return 6.112 * math.exp((17.62 * temperature) / (243.12 + temperature))

def actual_vapor_pressure(relative_humidity, temperature):
    """Calculate the actual vapor pressure"""
    es = saturation_vapor_pressure(temperature)
    ea = (relative_humidity / 100) * es
    return ea
# Geometry of the Church
V = 6864 #m³
Aw = 50 #m²

# Constants
Rsi = 0.13
Uw = 1.1

# External climate
temperature0 = -1

# Internal climate peak
temperature_i_peak = 15.6
relative_humidity_i_peak = 40

# Internal climate low
temperature_i_low = 9.3
relative_humidity_i_low = 48

# Component temperature peak
D_temp_peak = temperature_i_peak - temperature0
q_peak = Uw * D_temp_peak
temperature_b_peak = temperature_i_peak - q_peak * Rsi

# Component temperature low
D_temp_low = temperature_i_low - temperature0
q_low = Uw * D_temp_low
temperature_b_low = temperature_i_low - q_low * Rsi

# Pressures
actual_pressure_b_peak = actual_vapor_pressure(90, temperature_b_peak) * 100
actual_pressure_b_low = actual_vapor_pressure(90, temperature_b_low) * 100
actual_pressure_i_peak = actual_vapor_pressure(relative_humidity_i_peak, temperature_i_peak) * 100
actual_pressure_i_low = actual_vapor_pressure(relative_humidity_i_low, temperature_i_low) * 100

# Vapor transfer
gv_peak_per_s = 7 * 10 ** (-9) * 1 / Rsi * (actual_pressure_b_peak - actual_pressure_i_peak)
gv_peak_per_h = gv_peak_per_s * 3600
gv_low_per_s = 7 * 10 ** (-9) * 1 / Rsi * (actual_pressure_b_low - actual_pressure_i_low)
gv_low_per_h = gv_low_per_s * 3600

# Average vapor transfer per hour
gv_avg_h = (gv_peak_per_h - gv_low_per_h) / 2
m = gv_avg_h * 7
erf_a = 12 / m

m2 = gv_low_per_h * Aw * 30
result = m2 / V

# Output
print(f"Wall Temperature Peak: {temperature_b_peak:.2f} °C")
print(f"Wall Temperature Low: {temperature_b_low:.2f} °C")
print("\n")
print(f"Actual Vapor Pressure Wall Peak: {actual_pressure_b_peak:.2f} Pa")
print(f"Actual Vapor Pressure Wall Low: {actual_pressure_b_low:.2f} Pa")
print(f"Actual Vapor Pressure Inside Peak: {actual_pressure_i_peak:.2f} Pa")
print(f"Actual Vapor Pressure Inside Low: {actual_pressure_i_low:.2f} Pa")
print("\n")
print(f"Pressure difference Peak: {actual_pressure_b_peak - actual_pressure_i_peak} Pa")
print(f"Pressure difference Low: {actual_pressure_b_low - actual_pressure_i_low} Pa")
print("\n")
print(f"Vapor Transfer Peak (per hour): {gv_peak_per_h:.4f} g/hm²")
print(f"Vapor Transfer Low (per hour): {gv_low_per_h:.4f} g/hm²")
print(f"Average Vapor Transfer (per hour): {gv_avg_h:.4f} g/hm²")
print(f"Mass of Vapor Transfer over 7 hours of 1m²: {m:.2f} g")
print(f"Necessary Area for 12l: {erf_a:.2f} m²")
print("\n")
#(f"Delta in abs. humidity: {result:.2f} g/m³")