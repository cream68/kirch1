import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, BoxAnnotation, LinearAxis, Range1d, DatetimeTickFormatter, Span
from datetime import timedelta

def find_sundays_in_range(start_date, end_date):
    sundays = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.day_name() == 'Sunday':
            sundays.append(current_date)
        current_date += timedelta(days=1)
    return sundays

def create_tslope_plot(df, start_date, end_date, show_sunday_marker, x_range, nutz_df,grund_df):
    # Filter dataframe based on selected date range
    filtered_df = df.loc[(df['date'] >= start_date) & (df['date'] < end_date)]
    filtered_nutz_df = nutz_df.loc[(nutz_df['date'] >= start_date) & (nutz_df['date'] < end_date)]
    filtered_grund_df = grund_df.loc[(grund_df['date'] >= start_date) & (grund_df['date'] < end_date)]

    # Create Bokeh plot
    plot = figure(title='Orgel', x_axis_label='Time', width=1200, height=600,
                  x_axis_type='datetime', tools="pan,box_zoom,reset,save", x_range=x_range)

    plot.yaxis.axis_label = 'Temperature (°C)'

    # Customize axis labels and title font sizes for readability
    plot.title.text_font_size = '16pt'
    plot.xaxis.axis_label_text_font_size = '14pt'
    plot.yaxis.axis_label_text_font_size = '14pt'
    plot.xaxis.major_label_text_font_size = '12pt'
    plot.yaxis.major_label_text_font_size = '12pt'


    # x-Axis format
    plot.xaxis.formatter = DatetimeTickFormatter(
        hours=["%d %B %Y-%H:%M"],
        days=["%d %B %Y-%H:%M"],
        months=["%d %B %Y-%H:%M"],
        years=["%d %B %Y-%H:%M"],
    )
    plot.xaxis.major_label_orientation = 3.1415 / 4
    plot.xaxis.ticker.desired_num_ticks = 10

    # Plot temperature slope
    #temp_slope_line = plot.line('date', 'temp_slope', source=ColumnDataSource(filtered_df), legend_label="∆θ / ∆h", line_width=2, color='blue')
    #plot.add_tools(HoverTool(renderers=[temp_slope_line], tooltips=[
    #    ('Date', '@date{%F %H:%M}'),
    #    ('Temperature Slope', '@temp_slope{0.2f} [K/h]')
    #], formatters={'@date': 'datetime'}, mode='vline'))


    ## Add a second y-axis for temperature
    #temp_range = Range1d(0.9 * filtered_df["temp"].min(), 1.1 * filtered_df["temp"].max())
    #plot.extra_y_ranges["temp_range"] = temp_range
    #temp_axis = LinearAxis(y_range_name="temp_range", axis_label="Temperature °C")
    #temp_axis.axis_label_text_font_size = '14pt'
    #temp_axis.major_label_text_font_size = '12pt'
    #plot.add_layout(temp_axis, 'right')

    # Plot temperature
    temp_line = plot.line('date', 'temp', source=ColumnDataSource(filtered_df), legend_label="θ", line_width=2, color='blue')
    plot.add_tools(HoverTool(renderers=[temp_line], tooltips=[
        ('Date', '@date{%F %H:%M}'),
        ('Temperature', '@temp{0.2f} °C')
    ], formatters={'@date': 'datetime'}, mode='vline'))

    horizontal_line = Span(location=9.5, dimension='width', line_color='black', line_width=1, line_dash='dashed')
    plot.renderers.extend([horizontal_line])
    horizontal_line = Span(location=14, dimension='width', line_color='black', line_width=1, line_dash='dashed')
    plot.renderers.extend([horizontal_line])

    # Plot temperature slope
    #temp_slope_line = plot.line('date', 'temp_slope', source=ColumnDataSource(filtered_df), legend_label="∆θ / ∆h", line_width=2, color='blue')
    #plot.add_tools(HoverTool(renderers=[temp_slope_line], tooltips=[
    #    ('Date', '@date{%F %H:%M}'),
    #    ('Temperature Slope', '@temp_slope{0.2f} [K/h]')
    #], formatters={'@date': 'datetime'}, mode='vline'))


    # Add Sunday markers
    if show_sunday_marker:
        sundays = find_sundays_in_range(start_date, end_date)
        for sunday in sundays:
            plot.add_layout(
                BoxAnnotation(left=sunday, right=sunday + timedelta(days=1), fill_alpha=0.1, fill_color='green'))

    # Find all intervals where heating_bool is 1
    intervals = []
    current_interval = None

    for _, row in filtered_nutz_df.iterrows():
        if row['interval_bool'] == 1:
            if current_interval is None:
                current_interval = {'start': row['date'], 'end': row['date']}
            else:
                current_interval['end'] = row['date']
        else:
            if current_interval is not None:
                intervals.append(current_interval)
                current_interval = None

    if current_interval is not None:
        intervals.append(current_interval)

    # Create a BoxAnnotation for each interval
    for interval in intervals:
        box = BoxAnnotation(left=interval['start'], right=interval['end'],
                            fill_alpha=0.1, fill_color='red')
        plot.add_layout(box)


    # Find all intervals where heating_bool is 1
    intervals = []
    current_interval = None

    for _, row in filtered_grund_df.iterrows():
        if row['base_heat'] == True:
            if current_interval is None:
                current_interval = {'start': row['date'], 'end': row['date']}
            else:
                current_interval['end'] = row['date']
        else:
            if current_interval is not None:
                intervals.append(current_interval)
                current_interval = None

    if current_interval is not None:
        intervals.append(current_interval)

    # Create a BoxAnnotation for each interval
    for interval in intervals:
        box = BoxAnnotation(left=interval['start'], right=interval['end'],
                            fill_alpha=0.1, fill_color='gray')
        plot.add_layout(box)

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
