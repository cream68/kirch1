from magnus import magnus_formula

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