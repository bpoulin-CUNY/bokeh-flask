from flask import Flask, render_template 
import pandas as pd
from bokeh.plotting import figure, show 
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import components
import pickle
import math
import os

app = Flask(__name__)




usgs = pickle.load( open( "/Volumes/Document_Drive/ODSC/notebooks/02336000.p", "rb" ) )

site = '02336000'

sensor_dict ={'63680':'Turbidity' ,'00095':'Conductivity', '00060':'Discharge Cubic-per-Second','00065':'Gage Height feet','00010':'Temperature Celsius'}

location_dict ={'02336000': 'Chatahooche River Atlanta', '02335000': 'Chatahooche River Near Norcross'}


def sourcer(data):
    source = ColumnDataSource(data={
        'date'      : data.index,
        '00060' : data['00060'],
        '00065'    : data['00065'],
        '00010'  : data['00010'],
        '63680': data['63680'],
        '00095': data['00095']
    })
    
    hov= HoverTool(
    tooltips=[('Date', '@date{%F}'),
              ( 'Discharge (cubic feet/second)','@00060' ),
             ('Gage Height (feet) ', '@00065'),
             ('Water Temperature (Celsius)', '@00010'),
             ('Condcutivity', '@00095'),
             ('Turbidity', '@63680')],
        formatters={
        'date'      : 'datetime', #
        'discharge' : 'printf', 
        'gage' : 'printf',
        'temp_c' : 'printf'
    },
    mode = 'vline'
    )
    return(source, hov)

source, hov = sourcer(usgs)


def date_plot(sensor, site = site, sensor_dict=sensor_dict, location_dict=location_dict, source=source, hov=hov):
    p = figure(plot_width=900, plot_height=400, title="{} at \t Site number: {} \t Location: {}".format(site, location_dict[site], sensor_dict[sensor]), x_axis_type="datetime")
    p.line(x='date', y = sensor, color='#eb1736', legend= sensor_dict[sensor].split()[0], source = source)
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = sensor_dict[sensor]
    p.xaxis.major_label_orientation = math.pi/4
    p.add_tools(hov)
    return(p)
    
@app.route("/")
def home():
    #Build HTML Table from list of lists
    flies = [['Gold Ribbed Hares Ear', 18,16, 20], ['Purple Haze',14, 16, 12], ['Pheasant Tail',18, 20, 22]]
    
    #convert to HTML
    test_table = pd.DataFrame(flies, columns = ['Fly', 'Best Size', 'Alternate Size', 'Last Resort Size']).to_html(table_id='best-flies')
    

    plot = date_plot(sensor = '00065')
    script, div = components(plot)

    print(div)
    print(script)
    return render_template('index.html', 
                           test_table=test_table,
                           script = script,
                           div=div)

if __name__ == "__main__":
    app.run(debug=True)