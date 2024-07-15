import streamlit as st
import pandas as pd
from bokeh.layouts import gridplot
from create_orgel_plot import create_orgel_plot
from create_aussen_plot import create_aussen_plot
from create_bankreihe_plot import create_bankreihe_plot
#from create_orgel_plot_temp_rH60 import create_orgel_temp_rH60
from create_slope_plot import create_slope_plot
from create_temp_slope_plot import create_slope_plot
from bokeh.io import export_svgs

# Set the page layout to wide
st.set_page_config(layout="wide")


# Read Parquet files
orgel_df = pd.read_parquet("orgel.parquet", engine='pyarrow')
aussen_df = pd.read_parquet("aussen.parquet", engine='pyarrow')
bankreihe_df = pd.read_parquet("bankreihe.parquet", engine='pyarrow')

# Ensure datetime index
orgel_df['date'] = pd.to_datetime(orgel_df['date'])
aussen_df['date'] = pd.to_datetime(aussen_df['date'])
bankreihe_df['date'] = pd.to_datetime(bankreihe_df['date'])

def main():
    st.title('Weather Data Analysis')

    # Date range selection using a single range picker
    date_range_key = 'date_range'
    date_range = st.date_input('Select Date Range',
                               min_value=orgel_df['date'].min().date(),
                               max_value=orgel_df['date'].max().date(),
                               value=(orgel_df['date'].min().date(), orgel_df['date'].max().date()),
                               key=date_range_key)

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)

    if st.button('Reset Date Range'):
        start_date = orgel_df['date'].min()
        end_date = orgel_df['date'].max() + pd.Timedelta(days=1)
        date_range = (start_date.date(), end_date.date())

    # Checkbox to show Sunday markers
    show_sunday_marker = st.checkbox('Show Sunday Markers')
    show_hum_box_orgel = st.checkbox('Show Humidity Boundaries Orgel')
    show_hum_box_bankreihe = st.checkbox('Show Humidity Boundaries Bankreihe')

    # Sliders
    # Slider for bounding box limits
    lower_rH_orgel, upper_rH_orgel = st.slider('Select Bounding Humidity Limits for Orgel', 0, 100, (45, 70), key='limit_rh_orgel')
    lower_temp_orgel, upper_temp_orgel = st.slider('Select Bounding Humidity Limits for Orgel', 0, 100, (45, 70), key='limit_temp_orgel')
    lower_rh_bank, upper_rh_bank = st.slider('Select Bounding Humidity Limits for Bankreihe ', 0, 100, (45, 70), key='limit_rh_bank')

    # Filter dataframe based on selected date range
    filtered_aussen = aussen_df.loc[(aussen_df['date'] >= start_date) & (aussen_df['date'] < end_date)]
    filtered_orgel = orgel_df.loc[(orgel_df['date'] >= start_date) & (orgel_df['date'] < end_date)]
    filtered_bankreihe = bankreihe_df.loc[(bankreihe_df['date'] >= start_date) & (bankreihe_df['date'] < end_date)]

    # Create Bokeh plot using the imported function
    p1, p1_x_range, p1_y_range = create_aussen_plot(filtered_aussen, start_date, end_date, show_sunday_marker)

    # Update y-axis range based on slider input

    p2 = create_orgel_plot(filtered_orgel, start_date, end_date, show_sunday_marker, p1_x_range, show_hum_box_orgel,lower_rH_orgel,upper_rH_orgel)
    p3 = create_bankreihe_plot(filtered_bankreihe, start_date, end_date, show_sunday_marker, p1_x_range, show_hum_box_bankreihe,lower_rh_bank,upper_rh_bank)

    #p4 = create_orgel_plot_temp(filtered_orgel, start_date, end_date, show_sunday_marker, p1_x_range)
    p5 = create_orgel_temp_slope(filtered_orgel, start_date, end_date, show_sunday_marker, p1_x_range)


    
    # Display Bokeh plot using st.bokeh_chart
    st.subheader('Efficio Daten Auswertung')
    #st.bokeh_chart(gridplot([[p1],[p2],[p3],[p4],[p5]], toolbar_location="above",sizing_mode='stretch_both'))
    st.bokeh_chart(gridplot([[p1],[p2],[p3],[p5]], toolbar_location="above",sizing_mode='stretch_both'))

if __name__ == "__main__":
    main()
