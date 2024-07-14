import pandas as pd
def calculate_energy_consumption(aussen_df, orgel_df):
    """
    Calculate the energy consumption based on temperature differences between 'aussen' and 'orgel'.
    
    Parameters:
    - aussen_df: DataFrame containing 'aussen' data
    - orgel_df: DataFrame containing 'orgel' data
    
    Returns:
    - Energy consumption in kWh
    - Average temperature difference Außen - Orgel for Temp Orgel < 9.5°C
    - Calculate the total time in hours for Temp Orgel < 9.5°C
    """
    # Filter data for the specified date range
    start_date = '2023-11-01'
    end_date = '2024-03-31'
    aussen_df = aussen_df[(aussen_df['date'] >= start_date) & (aussen_df['date'] <= end_date)]
    orgel_df = orgel_df[(orgel_df['date'] >= start_date) & (orgel_df['date'] <= end_date)]

    # Merge the data on the 'date' column
    merged_df = pd.merge(aussen_df, orgel_df, on='date', suffixes=('_aussen', '_orgel'))

    # Filter rows where orgel temperature is below 9.5°C
    filtered_df = merged_df[merged_df['temp_orgel'] < 9.5]

    # Calculate the temperature difference
    filtered_df.loc[:, 'temp_diff'] = filtered_df['temp_orgel'] - filtered_df['temp_aussen']

    # Calculate the number of time intervals where the orgel temperature is below 9.5°C
    count_delta_k = filtered_df['temp_diff'].count()

    # Calculate the average temperature difference
    average_delta_k = filtered_df['temp_diff'].mean()

    # Calculate the total time in hours (assuming each interval represents 0.25 hours)
    total_time_hours = count_delta_k * 0.25

    # Integrate the temperature difference over time and multiply by 3.1 =2.2+0.9 kWh/K from HL to get energy consumption in kWh
    energy_integral = 3.1 * average_delta_k * total_time_hours

    energy_consumption = energy_integral 

    return energy_consumption, average_delta_k, total_time_hours 