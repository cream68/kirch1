import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, BoxAnnotation, LinearAxis, Range1d, DatetimeTickFormatter
from datetime import timedelta

def find_sundays_in_range(start_date, end_date):
    sundays = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.day_name() == 'Sunday':
            sundays.append(current_date)
        current_date += timedelta(days=1)
    return sundays

def create_slope_plot(df, start_date, end_date, show_sunday_marker, x_range):
    # Filter dataframe based on selected date range
    filtered_df = df.loc[(df['date'] >= start_date) & (df['date'] < end_date)]

    # Create Bokeh plot
    plot = figure(title='Orgel', x_axis_label='Zeitstempel', width=1200, height=600,
                  x_axis_type='datetime', tools="pan,box_zoom,reset,save", x_range=x_range)

    plot.yaxis.axis_label = '∆ah / ∆h [g/m³h]'


    # x-Axis format
    plot.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y-%H:%M"],
        days=["%d %B %Y-%H:%M"],
        months=["%d %B %Y-%H:%M"],
        years=["%d %B %Y-%H:%M"],
    )
    plot.xaxis.major_label_orientation = 3.1415 / 4
    plot.xaxis.ticker.desired_num_ticks = 10

    # Plot temperature
    temp_slope_line = plot.line('date', 'ah_slope', source=ColumnDataSource(filtered_df), legend_label="ah/h", line_width=2, color='blue')
    plot.add_tools(HoverTool(renderers=[temp_slope_line], tooltips=[
        ('Date', '@date{%F %H:%M}'),
        ('Temperature', '@ah_slope{0.2f} g/m³h')
    ], formatters={'@date': 'datetime'}, mode='vline'))


    # Add Sunday markers
    if show_sunday_marker:
        sundays = find_sundays_in_range(start_date, end_date)
        for sunday in sundays:
            plot.add_layout(
                BoxAnnotation(left=sunday, right=sunday + timedelta(days=1), fill_alpha=0.1, fill_color='green'))

    # Style the plot
    plot.legend.location = "top_left"
    plot.legend.click_policy = "hide"

    # Hide x-axis ticks
    # plot.xaxis.major_tick_line_color = None  # Hides major ticks
    # plot.xaxis.minor_tick_line_color = None  # Hides minor ticks

    # Hide y-axis ticks
    # plot.yaxis.major_tick_line_color = None  # Hides major ticks
    # plot.yaxis.minor_tick_line_color = None  # Hides minor ticks

    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None

    return plot
