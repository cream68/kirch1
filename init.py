import pandas as pd
import numpy as np
from scipy.optimize import newton

def magnus_formula(temp):
    """
    Calculate the saturation vapor pressure using the Magnus formula.

    Parameters:
    - temp: Temperature in Celsius

    Returns:
    - Saturation vapor pressure (E_s) in hPa
    """
    return 6.112 * np.exp((17.62 * temp) / (temp + 243.12))

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

def process_file(file_path, calculate_temp_60=False):
    """
    Load data from an Excel file, calculate absolute humidity, and optionally calculate temperature for 60% RH.

    Parameters:
    - file_path: Path to the Excel file
    - calculate_temp_60: Whether to calculate temperature for 60% RH (default: False)

    Returns:
    - DataFrame with calculated columns
    """
    df_temp = pd.read_excel(file_path, engine='openpyxl')
    df = pd.DataFrame()
    df["date"] = pd.to_datetime(df_temp.iloc[:, 0])
    df["temp"] = df_temp.iloc[:, 5]
    df["rH"] = df_temp.iloc[:, 3]
    df["aH"] = calculate_absolute_humidity(df["temp"], df["rH"])

    if calculate_temp_60:
        df["temp_60"] = df.apply(lambda row: calculate_temp_rh_60(row["rH"], row["aH"], row["temp"]), axis=1)
        df['ah_slope'] = df['aH'].diff() / (df['date'].diff().dt.total_seconds() / 3600)
        df['temp_slope'] = df['temp'].diff() / (df['date'].diff().dt.total_seconds() / 3600)

    return df

# Process and save data for 'aussen'
aussen_df = process_file('aussen.xlsx')
aussen_df.to_parquet('aussen.parquet', engine='pyarrow')

# Process and save data for 'orgel', including temperature calculation for 60% RH
orgel_df = process_file('orgel.xlsx', calculate_temp_60=True)
orgel_df.to_parquet('orgel.parquet', engine='pyarrow')

# Process and save data for 'bankreihe'
bankreihe_df = process_file('bankreihe.xlsx')
bankreihe_df.to_parquet('bankreihe.parquet', engine='pyarrow')
