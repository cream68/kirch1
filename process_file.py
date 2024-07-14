

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
