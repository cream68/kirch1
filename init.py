import pandas as pd
from process_file import process_file
from baseload_energy_calculation import calculate_energy_consumption

parseFile = True

def main():
    if parseFile:
        aussen_df = process_file('aussen.xlsx')
        aussen_df.to_parquet('aussen.parquet', engine='pyarrow')

        orgel_df = process_file('orgel.xlsx', calculate_temp_60=True)
        orgel_df.to_parquet('orgel.parquet', engine='pyarrow')

        # Calculate and print the energy consumption
        heiz_df = calculate_energy_consumption(aussen_df, orgel_df,heating_temp=10)
        heiz_df.to_parquet('heiz.parquet', engine='pyarrow')

        bankreihe_df = process_file('bankreihe.xlsx')
        bankreihe_df.to_parquet('bankreihe.parquet', engine='pyarrow')
    else:
        aussen_df = pd.read_parquet('aussen.parquet', engine='pyarrow')
        orgel_df = pd.read_parquet('orgel.parquet', engine='pyarrow')
        bankreihe_df = pd.read_parquet('bankreihe.parquet', engine='pyarrow')
    pass

main()