#note to self:
#cd to Guardian folder
# run using bokeh serve parking --show

# bokeh imports
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.layouts import column, row
from clean_data import create_data
#from os.path import dirname, join, basename

# get the final dataframes
mon_parking, tues_parking, wed_parking, thurs_parking, day_dataframes = create_data()

# create ColumnDataSource
data = {
        'Name': day_dataframes[0]['Name'],
        'x': day_dataframes[0]['x'],
        'y': day_dataframes[0]['y'],
        'colors' : day_dataframes[0]['8AM colors'],
        'sizes': day_dataframes[0]['sizes'],
        'Total Spaces': day_dataframes[0]['Total Spaces'],
        '% Open Spaces': day_dataframes[0]['8AM % Open Spaces'],
        'Open Spaces' : day_dataframes[0]['8AM'],
        }
source = ColumnDataSource(data)

# plot figure
p = figure(x_range=(0,1700), y_range=(0,1600))
p.image_url(url=['parking/static/map.png'], x=0, y=0,w=1700,h=1600, anchor='bottom_left')
#p.image_url(url=[join(basename(dirname(__file__)), 'static', 'map.png')], x=0, y=0,w=1700,h=1600, anchor='bottom_left')
p.circle(x='x',y='y',color='colors', size = 'sizes',source=source,line_color='black')

# legend box
p.rect(x=1225,y=1400,width=900,height=350,fill_color='white',line_color='black')

# legend texts
xtext_pos = [905]*5 + [1330]*3
ytext_pos = list(range(1450,1200,-50)) + [1450,1380,1300]
legtext = ["<5%","5%-25%","25%-50%","50%-75%",">75%"] + ["<230 spots","230-460 spots", ">460 spots"]
p.text(x=xtext_pos,y=ytext_pos,text=legtext)

# legend titles
xtitle_pos = [810,1230]
ytitle_pos = [1515]*2
legtext = ["% Open Spots"] + ["Parking/Lot Size"]
p.text(x=xtitle_pos,y=ytitle_pos,text=legtext,text_font_style='bold')

# color circles
c1_xpos = [850]*5
c1_ypos = list(range(1475,1250,-50))
c1_col = ['darkred','firebrick','orange','khaki','seagreen']
p.circle(x=c1_xpos,y=c1_ypos,color=c1_col,size = 10,line_color='black')

# size circle
c2_xpos = [1270]*3
c2_ypos = [1480,1420,1330]
c2_size = [10,20,30]
p.circle(x=c2_xpos, y=c2_ypos, size=c2_size, fill_color='white', line_color='black')

# add Hovertool
hover = HoverTool(
    tooltips = [
                ('Structure/Lot','@Name'),
                ('Total Spaces', '@{Total Spaces}'),
                ('% of Open Spaces','@{% Open Spaces}'),
                ('# of Open Spaces','@{Open Spaces}')
])
p.add_tools(hover)

# create buttons to select day and time
day_select = Select(options = ['Monday','Tuesday', 'Wednesday','Thursday'], value='Monday', title='Select Day')
time_select = Select(options= ['8AM','10AM','12PM','2PM'], value='8AM',title='Select Time')

# define callback for the day and time buttons
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
                'Name': day_dataframes[0]['Name'],
                'x': day_dataframes[i]['x'],
                'y': day_dataframes[i]['y'],
                'colors' : day_dataframes[i]['8AM colors'],
                'sizes': day_dataframes[i]['sizes'],
                'Total Spaces': day_dataframes[i]['Total Spaces'],
                '% Open Spaces': day_dataframes[i]['8AM % Open Spaces'],
                'Open Spaces': day_dataframes[i]['8AM'],
        }
    elif t == '10AM':
        new_data = {
                'Name': day_dataframes[0]['Name'],
                'x': day_dataframes[i]['x'],
                'y': day_dataframes[i]['y'],
                'colors' : day_dataframes[i]['10AM colors'],
                'sizes': day_dataframes[i]['sizes'],
                'Total Spaces': day_dataframes[i]['Total Spaces'],
                '% Open Spaces': day_dataframes[i]['10AM % Open Spaces'],
                'Open Spaces': day_dataframes[i]['10AM'],
        }
    elif t == '12PM':
        new_data = {
                'Name': day_dataframes[0]['Name'],
                'x': day_dataframes[i]['x'],
                'y': day_dataframes[i]['y'],
                'colors' : day_dataframes[i]['12PM colors'],
                'sizes': day_dataframes[i]['sizes'],
                'Total Spaces': day_dataframes[i]['Total Spaces'],
                '% Open Spaces': day_dataframes[i]['12PM % Open Spaces'],
                'Open Spaces': day_dataframes[i]['12PM'],
        }
    elif t == '2PM':
        new_data = {
                'Name': day_dataframes[0]['Name'],
                'x': day_dataframes[i]['x'],
                'y': day_dataframes[i]['y'],
                'colors' : day_dataframes[i]['2PM colors'],
                'sizes': day_dataframes[i]['sizes'],
                'Total Spaces': day_dataframes[i]['Total Spaces'],
                '% Open Spaces': day_dataframes[i]['2PM % Open Spaces'],
                'Open Spaces': day_dataframes[i]['2PM'],
        }
    source.data = new_data

day_select.on_change('value',update_plot)
time_select.on_change('value', update_plot)

layout = column(row(day_select, time_select), p)
curdoc().add_root(layout)
