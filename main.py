    
# bokeh imports
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select, RadioButtonGroup
from bokeh.layouts import column
from os.path import dirname, join, basename
from clean_data import create_data

mon_parking, tues_parking, wed_parking, thurs_parking, day_dataframes = create_data()

data = {
        'x': day_dataframes[0]['x'],
        'y': day_dataframes[0]['y'],
        'colors' : day_dataframes[0]['8AM colors'],
        'Scaled Total Spaces': day_dataframes[0]['Scaled Total Spaces'],
        'Total Spaces': day_dataframes[0]['Total Spaces'],
        '% Open Spaces': day_dataframes[0]['8AM % Open Spaces'],
        'Open Spaces' : day_dataframes[0]['8AM'],
        }
source = ColumnDataSource(data)
p = figure(x_range=(0,1700), y_range=(0,1600))
p.image_url(url=[join(basename(dirname(__file__)), 'static', 'map.png')], x=0, y=0,w=1700,h=1600, anchor='bottom_left')
p.diamond(x='x',y='y',color='colors', size = 'Scaled Total Spaces',source=source)
hover = HoverTool(
    tooltips = [
                ('Total Spaces', '@{Total Spaces}'),
                ('% of Open Spaces','@{% Open Spaces}'),
                ('# of Open Spaces','@{Open Spaces}')
])
p.add_tools(hover)


day_select = Select(options = ['Monday','Tuesday', 'Wednesday','Thursday'], value='Monday', title='Select Day')
time_select = Select(options= ['8AM','10AM','12PM','2PM'], value='8AM',title='Select Time')
def update_plot(attr, old, new):
    N = day_select.value
    t = time_select.value
    if N == 'Monday':
        i=0
    elif N == 'Tuesday':
        i=1
    elif N == 'Wednesday':
        i=2
    elif N == 'Thursday':
        i=3
    if t == '8AM':
        new_data = {
                'x': day_dataframes[i]['x'],
                'y': day_dataframes[i]['y'],
                'colors' : day_dataframes[i]['8AM colors'],
                'Scaled Total Spaces': day_dataframes[i]['Scaled Total Spaces'],
                'Total Spaces': day_dataframes[i]['Total Spaces'],
                '% Open Spaces': day_dataframes[i]['8AM % Open Spaces'],
                'Open Spaces': day_dataframes[i]['8AM'],
        }
    elif t == '10AM':
        new_data = {
                'x': day_dataframes[i]['x'],
                'y': day_dataframes[i]['y'],
                'colors' : day_dataframes[i]['10AM colors'],
                'Scaled Total Spaces': day_dataframes[i]['Scaled Total Spaces'],
                'Total Spaces': day_dataframes[i]['Total Spaces'],
                '% Open Spaces': day_dataframes[i]['10AM % Open Spaces'],
                'Open Spaces': day_dataframes[i]['10AM'],
        }
    elif t == '12PM':
        new_data = {
                'x': day_dataframes[i]['x'],
                'y': day_dataframes[i]['y'],
                'colors' : day_dataframes[i]['12PM colors'],
                'Scaled Total Spaces': day_dataframes[i]['Scaled Total Spaces'],
                'Total Spaces': day_dataframes[i]['Total Spaces'],
                '% Open Spaces': day_dataframes[i]['12PM % Open Spaces'],
                'Open Spaces': day_dataframes[i]['12PM'],
        }
    elif t == '2PM':
        new_data = {
                'x': day_dataframes[i]['x'],
                'y': day_dataframes[i]['y'],
                'colors' : day_dataframes[i]['2PM colors'],
                'Scaled Total Spaces': day_dataframes[i]['Scaled Total Spaces'],
                'Total Spaces': day_dataframes[i]['Total Spaces'],
                '% Open Spaces': day_dataframes[i]['2PM % Open Spaces'],
                'Open Spaces': day_dataframes[i]['2PM'],
        }       
    source.data = new_data

day_select.on_change('value',update_plot)
time_select.on_change('value', update_plot)
layout = column(day_select, time_select, p)
curdoc().add_root(layout)
