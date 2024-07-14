import pandas as pd
from baseload_energy_calculation import calculate_energy_consumption
from absolute_humidity import calculate_absolute_humidity
from calculate_temp_rh_60 import calculate_temp_rh_60
from process_file import process_file

def main():
    #aussen_df = process_file('aussen.xlsx')
    #aussen_df.to_parquet('aussen.parquet', engine='pyarrow')
    aussen_df = pd.read_parquet('aussen.parquet', engine='pyarrow')

    # Process and save data for 'orgel', including temperature calculation for 60% RH
    #orgel_df = process_file('orgel.xlsx', calculate_temp_60=True)
    #orgel_df.to_parquet('orgel.parquet', engine='pyarrow')
    orgel_df = pd.read_parquet('orgel.parquet', engine='pyarrow')

    # Process and save data for 'bankreihe'
    #bankreihe_df = process_file('bankreihe.xlsx')
    #bankreihe_df.to_parquet('bankreihe.parquet', engine='pyarrow')
    bankreihe_df = pd.read_parquet('bankreihe.parquet', engine='pyarrow')

    # Calculate and print the energy consumption
    energy_consumption, average_delta_k, total_time_hours = calculate_energy_consumption(aussen_df, orgel_df)
    print(f"Base load calculation for Temp Orgel < 9.5°C")
    print(f"Base load energy consumption: {energy_consumption:.1f} kWh")
    print(f"average temperature difference: {average_delta_k:.1f} K")
    print(f"total time in hours: {total_time_hours} h")
    pass

main()