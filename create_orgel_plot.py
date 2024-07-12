import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, BoxAnnotation, LinearAxis, Range1d, Span, DatetimeTickFormatter
from datetime import timedelta

def find_sundays_in_range(start_date, end_date):
    sundays = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.day_name() == 'Sunday':
            sundays.append(current_date)
        current_date += timedelta(days=1)
    return sundays

def create_orgel_plot(df, start_date, end_date, show_sunday_marker,x_range, show_hum_box,lower_rH,upper_rH):
    # Filter dataframe based on selected date range
    filtered_df = df.loc[(df['date'] >= start_date) & (df['date'] < end_date)]

    # Define plot size optimized for A4 paper
    plot_width = 800
    plot_height = 800  # A4 height divided by 3 (approx 11.69/3 inches)

    # Create Bokeh plot
    plot = figure(title='Orgel', x_axis_label='Time', width=plot_width, height=plot_height,
                  x_axis_type='datetime', tools="pan,box_zoom,reset,save", x_range=x_range)

    plot.yaxis.axis_label = 'Temperature (°C)'

    # Customize axis labels and title font sizes for readability
    plot.title.text_font_size = '16pt'
    plot.xaxis.axis_label_text_font_size = '14pt'
    plot.yaxis.axis_label_text_font_size = '14pt'
    plot.xaxis.major_label_text_font_size = '12pt'
    plot.yaxis.major_label_text_font_size = '12pt'

    plot.y_range = Range1d(filtered_df["temp"].min()-5,filtered_df["temp"].max()+5)

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
    temp_line = plot.line('date', 'temp', source=ColumnDataSource(filtered_df), legend_label=u"\u03B8", line_width=2, color='red')
    plot.add_tools(HoverTool(renderers=[temp_line], tooltips=[
        ('Date', '@date{%F %H:%M}'),
        ('Temperature', '@temp{0.2f} °C')
    ], formatters={'@date': 'datetime'}, mode='vline'))

    horizontal_line = Span(location=14, dimension='width', line_color='black', line_width=1, line_dash='dashed')
    plot.renderers.extend([horizontal_line])

    horizontal_line = Span(location=10, dimension='width', line_color='black', line_width=1, line_dash='dashed')
    plot.renderers.extend([horizontal_line])


    # Add a second y-axis for relative humidity
    rh_range = Range1d(0.9* filtered_df["rH"].min(), 1.1 * filtered_df["rH"].max())
    plot.extra_y_ranges["rh_range"] = rh_range
    rh_axis = LinearAxis(y_range_name="rh_range", axis_label="Relative Humidity (%)")
    rh_axis.axis_label_text_font_size = '14pt'
    rh_axis.major_label_text_font_size = '12pt'
    plot.add_layout(rh_axis, 'right')

    # Plot relative humidity
    rh_line = plot.line('date', 'rH', source=ColumnDataSource(filtered_df), legend_label='rH', line_width=2,
                        color='blue', y_range_name="rh_range")
    plot.add_tools(HoverTool(renderers=[rh_line], tooltips=[
        ('Date', '@date{%F %H:%M}'),
        ('Relative Humidity', '@rH{0.2f} %')
    ], formatters={'@date': 'datetime'}, mode='vline'))

    #rh_line = plot.line('date', 'rH_vent', source=ColumnDataSource(filtered_df), legend_label='Relative Humidity vent.',
    #                    line_width=2,
    #                    color='black', y_range_name="rh_range")
    #plot.add_tools(HoverTool(renderers=[rh_line], tooltips=[
    #    ('Date', '@date{%F %H:%M}'),
    #    ('Relative Humidity vent.', '@rH_vent{0.2f} %')
    #], formatters={'@date': 'datetime'}, mode='vline'))

    if show_hum_box:
        # Create BoxAnnotation for 45% humidity
        box_annotation = BoxAnnotation(top=upper_rH, bottom=lower_rH, fill_alpha=0.1, fill_color='blue', y_range_name="rh_range")
        plot.add_layout(box_annotation)

    # Add extra y-axis for Absolute Humidity
    ah_range = Range1d(0.9* filtered_df["aH"].min(), 1.1 * filtered_df["aH"].max())
    plot.extra_y_ranges["ah_range"] = ah_range
    ah_axis = LinearAxis(y_range_name="ah_range", axis_label="Absolute Humidity (g/m³)")
    ah_axis.axis_label_text_font_size = '14pt'
    ah_axis.major_label_text_font_size = '12pt'
    plot.add_layout(ah_axis, 'right')

    # Plot absolute humidity
    ah_line = plot.line('date', 'aH', source=ColumnDataSource(filtered_df), legend_label='aH',
                        line_width=2, color='green', y_range_name="ah_range")
    plot.add_tools(HoverTool(renderers=[ah_line], tooltips=[
        ('Date', '@date{%F %H:%M}'),
        ('Absolute Humidity', '@aH{0.2f} g/m³')
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
