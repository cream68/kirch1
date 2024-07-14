from magnus import magnus_formula
from scipy.optimize import newton

def calculate_temp_rh_60(rh, ah, initial_temp, tolerance=0.0001, max_iterations=100):
    """
    Calculate the temperature required to achieve 60% relative humidity for a given absolute humidity using Newton's method.

    Parameters:
    - rh: Current relative humidity in percentage
    - ah: Absolute humidity in g/m³
    - initial_temp: Initial guess for temperature in Celsius
    - tolerance: Tolerance for Newton's method (default: 0.0001)
    - max_iterations: Maximum number of iterations for Newton's method (default: 100)

    Returns:
    - Temperature in Celsius that achieves the desired 60% RH for the given AH
    """
    if rh > 60:
        rh_desired = 0.6
        rh_decimal = rh / 100.0

        def f(temp):
            e_s = magnus_formula(temp)
            e_a = ah * 8314.3 * (temp + 273.15) / 18.016 / (10 ** 5)
            return (e_a / e_s) - rh_desired

        return newton(f, initial_temp, tol=tolerance, maxiter=max_iterations)
    else:
        return initial_temp