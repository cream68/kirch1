import numpy as np
def magnus_formula(temp):
    """
    Calculate the saturation vapor pressure using the Magnus formula.

    Parameters:
    - temp: Temperature in Celsius

    Returns:
    - Saturation vapor pressure (E_s) in hPa
    """
    return 6.112 * np.exp((17.62 * temp) / (temp + 243.12))