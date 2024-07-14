import pandas as pd

def calculate_energy_consumption(aussen_df, orgel_df,heating_temp=9):
    """
    Calculate the energy consumption based on temperature differences between 'aussen' and 'orgel'.
    
    Parameters:
    - aussen_df: DataFrame containing 'aussen' data
    - orgel_df: DataFrame containing 'orgel' data
    - heating_temp: temperature point for which base heating is assumed

    Returns:
    - New DataFrame with columns temp_orgel, temp_aussen, and temp_diff
    - Energy consumption in kWh
    - Average temperature difference Außen - Orgel for Temp Orgel < heating_temp
    - Total time in hours for Temp Orgel < heating_temp
    """
    # Filter data for the specified date range
    start_date = '2023-11-01'
    end_date = '2024-03-31'
    aussen_df = aussen_df[(aussen_df['date'] >= start_date) & (aussen_df['date'] <= end_date)]
    orgel_df = orgel_df[(orgel_df['date'] >= start_date) & (orgel_df['date'] <= end_date)]

    # Merge the data on the 'date' column
    merged_df = pd.merge(aussen_df, orgel_df, on='date', suffixes=('_aussen', '_orgel'))

    # Calculate the temperature difference
    merged_df['temp_diff'] = (merged_df['temp_orgel'] - merged_df['temp_aussen']).round(2)

    # Set temp_diff to zero where temp_orgel is below heating_temp 
    merged_df.loc[(merged_df['temp_orgel'] > heating_temp) | (merged_df['temp_aussen'] > merged_df['temp_orgel']), 'temp_diff'] = 0

  # Filter rows where orgel temperature is below heating_temp and temperature outside is less than temperature inside
    filtered_df = merged_df[merged_df['temp_diff'] > 0]

    # Calculate the number of time intervals where the orgel temperature is below heating_temp
    count_delta_k = filtered_df['temp_diff'].count()

    # Calculate the average temperature difference
    average_delta_k = filtered_df['temp_diff'].mean()

    # Calculate the total time in hours (assuming each interval represents 0.25 hours)
    total_time_hours = count_delta_k * 0.25

    # Integrate the temperature difference over time and multiply by 3.1 = 2.2 + 0.9 kWh/K from HL to get energy consumption in kWh
    energy_integral = 3.1 * average_delta_k * total_time_hours

    energy_consumption = energy_integral

    # Create the new DataFrame with required columns
    result_df = merged_df[['date', 'temp_orgel', 'temp_aussen', 'temp_diff']]
    result_df = result_df.rename(columns={'temp_diff': f'temp_diff_sub_{heating_temp}'})

    #Print
    print(f"Base load calculation for Temp Orgel < {heating_temp:.1f} °C")
    print(f"Base load energy consumption: {energy_consumption:.1f} kWh")
    print(f"average temperature difference: {average_delta_k:.1f} K")
    print(f"total time in hours: {total_time_hours} h")

    return result_df
