import numpy as np
import serial
import pandas as pd
import time
import sqlite3

import flask
from flask import request
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_html_components as html
from dash.exceptions import PreventUpdate


import plotly.express as px
import plotly.graph_objects as go

#Initialize getdata 
from getdata import GetData
getdata = GetData()
#plot generator
from components.PlotGenerator.PlotGenerator import scatter_data, get_lsc


#Get Bootstrap
from style.bootstrap import Bootstrap
external_scripts = Bootstrap().getScripts()
external_stylesheets = Bootstrap().getStylesheet()

#Initilize Layouts
from components.ShowTable.ShowTable import showdata_layout
from components.Home.Home import home_layout
from components.CalibrationLayout.CalibrationLayout import calibration_layout

from flaskwebgui import FlaskUI #get the FlaskUI class
server = flask.Flask(__name__)
#ui = FlaskUI(server, port=2020)

app = dash.Dash(
    __name__,
    title='Plate Load Test',
    server=server,
    suppress_callback_exceptions = True,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets
)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

#[APP MAIN LAYOUT]
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Location(id='url2', refresh=False),
    html.Div(id='page-content')
])


   
#START TEST CALLBACK  
@app.callback(
    [Output('disp-sensor', 'figure'),
     Output('load-sensor', 'figure'),
     Output('test-indicator', 'children'),
     Output('start-an-btn', 'style')],
    [Input('start-btn', 'n_clicks'),
     Input('port', 'value'),
     Input('test-id', 'value'),
     Input('inc-no', 'value'),
     Input('time-input', 'value'),
     Input('view1', 'n_clicks'),
     Input('inp-sc', 'value'),
     Input('view2', 'n_clicks'),
     Input('inp-csv', 'value'),
     Input('plate-area', 'value'),
     Input('ini-set-1', 'value'),
     Input('ini-set-2', 'value'),
     Input('factor-safety', 'value'),
     Input('csv-type', 'value'),
     Input('plate-width', 'value'),
     Input('width-footing', 'value')]    
 )
def startTestHandler(btn1, port, id, inc, time_s, btn2, t_id, btn3, t_csv, p_area, ini1, ini2, fs, csv_type, pw, wf):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    try:
        if ('start-btn' in changed_id 
            and port is not None
            and id is not None
            and inc is not None
            and time_s is not None
            and p_area is not None
            and ini1 is not None
            and ini2 is not None
            and fs is not None
            and pw is not None
            and wf is not None):
            print('haiya')
            df = getdata.upload_generate(port= port, baud=9600, n=time_s, table=id, inc=inc, area=p_area, set1=ini1, set2=ini2,
                                         w_footing=wf, w_plate = pw, fs = fs)
            ind = 'Process running.'
            fig1, fig2 = scatter_data(df)
            return  fig1, fig2, ind, {'display': 'block'}
            
        elif 'view1' in changed_id:
            try:
                df = getdata.get_dataframe(table=t_id)
                ind = 'Click the button to start a test.'
                fig1, fig2 = scatter_data(df)
                return  fig1, fig2, ind, {'display': 'none'}
            except:
                raise PreventUpdate
        
        elif 'view2' in changed_id:
            if csv_type == 'complete':
              df = getdata.get_dataframe(table=t_csv)
              df.to_csv('./excelfiles/'+t_csv+'.csv')
              raise PreventUpdate
            elif csv_type == 'summary':
              df = getdata.get_dataframe(table=t_csv)
              df,_, __ = getdata.get_PS(df)
              df = df[['P', 'S1', 'S2', 'S', 'TS']]
              df.columns = ['Pressure', 'Dial Gauge-1 Reading', 
                            'Dial Gauge-2 Reading',
                            'Avereage Settlement',
                            'Total Settlement']
              df.to_csv('./excelfiles/'+t_csv+'.csv')
              raise PreventUpdate
        else:
            raise PreventUpdate
    except:
        print('START ERR')
        raise PreventUpdate


#[TIMER HANDLER]
@app.callback([Output('start-test', 'style'),
               Output('timer-div', 'children'),
               Output('p-test-id', 'children'),
               Output('p-inc-no', 'children'),
               Output('dg-1', 'children'),
               Output('dg-2', 'children'),
               Output('p-fs', 'children'),
               Output('p-time', 'children'),
               Output('summary', 'style'),
               Output('s-width-footing', 'children')],
        [Input('start-btn', 'n_clicks'),
        Input('port', 'value'),
        Input('test-id', 'value'),
        Input('inc-no', 'value'),
        Input('time-input', 'value'),
        Input('view1', 'n_clicks'),
        Input('inp-sc', 'value'),
        Input('view2', 'n_clicks'),
        Input('inp-csv', 'value'),
        Input('ini-set-1', 'value'),
        Input('ini-set-2', 'value'),
        Input('plate-area', 'value'),
        Input('factor-safety', 'value'),
        Input('plate-width', 'value'),
        Input('width-footing', 'value')])
def showtimer(btn1, port, 
              id, inc, time_s, 
              btn2, t_id, btn3, 
              t_csv, set1, set2,
              p_area, fs, pw, wf):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if ('start-btn' in changed_id 
    and port is not None
    and id is not None
    and inc is not None
    and time_s is not None
    and p_area is not None
    and set1 is not None
    and set2 is not None
    and fs is not None
    and pw is not None
    and wf is not None):
        try:

          style_test = {'display': 'none'}
          id = 'Test ID: ' + id 
          inc = 'Increment no: ' + str(inc)
          set1 = 'Initial DG-1: ' + str(set1) + 'cm'
          set2 = 'Initial DG-2: ' + str(set2) + 'cm'
          wf = 'Width of Footing: ' + str(wf) + 'm'
          fs = 'Factor of Safety: ' + str(fs)
          time_x = 'Time: ' + str(time_s) + ' minute/s'
          plus = 1000 + (4000/int(time_s* 60)) 
          return style_test,[dbc.Progress(value=0, id='progressb',color='success',
                                          style={'height': '30px',
                                                  'fontSize': '10px'}),
                             dcc.Interval(id="progress-interval", n_intervals=0, interval=plus)], \
                             id, inc,set1,set2,fs, time_x, {'display': 'inline-block'}, wf
        except:
          print('ERROR')
          raise PreventUpdate
    else:
        print('TIMER ERR')
        raise PreventUpdate

#PROGRESS BAR CALLBACK
@app.callback([Output('progressb', 'value'),
               Output('progressb', 'children')],
              [Input('time-input', 'value'),
               Input('progress-interval', 'n_intervals')])
def update_progress(time_s,n):
    coef = 100 / int(time_s * 60)
    value = coef * n
    if value <=100:
        return value,str(round(value)) +'%' 
    else:
        raise PreventUpdate

#RESULTS CALLBACK
@app.callback([Output('lsc', 'figure'),
               Output('measurements', 'style'),
               Output('m1', 'children'),
               Output('m2', 'children'),
               Output('m3', 'children')],
             [Input('gen-res', 'n_clicks'),
              Input('inp-sc', 'value')])
def generateUBC(n, inp):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'gen-res' in changed_id:
        try:
          data = [[11.5, 23, 35,46,57.5, 80.5, 103.5, 120],
              [0.07,0.34,0.845,1.55,2.09,3.2,6.06,7.55]]
          dummy = pd.DataFrame(data).T
          dummy.columns = ['P', 'S']

          dataf  = getdata.get_dataframe(table=inp)
          fos = dataf.FOS.iloc[-1]
          ps, bp, b = getdata.get_PS(dataf)
          

          ubc,sett, idx = getdata.get_ubc(df=ps)
          sf = round(sett*(b/bp), 2)
          m1 = 'Ultimate Bearing Capacity: ' + str(round(ubc, 2))
          m2 = 'Safe Bearing Capacity: ' + str(round(ubc/fos, 2))
          m3 = 'Settlement of Footing: ' + str(sf)
          fig = get_lsc(ps, ubc=ubc, ubc_s=sett)
          return fig, {'display': 'block', 'marginLeft': '10%'}, m1, m2, m3
        except:
          raise PreventUpdate
        
    else:
        raise PreventUpdate

#CALIBRATION CALLBACK
@app.callback([Output('ca-ind', 'children'),
               Output('ca-ind', 'style')],
              [Input('check-port', 'n_clicks'),
               Input('ca-port-id', 'value')])
def calibrationHandler(btn1, inp):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'check-port' in changed_id:
        try:
            serial.Serial(inp, 9600)
            ind = 'Device found'
            style={'color': 'lightgreen', 'fontSize':'15px'}
            return ind, style
        except:
            ind = 'Device not found'
            style={'color': 'salmon', 'fontSize':'15px'}
            return ind, style
    else:
        raise PreventUpdate
        
#[RUN CALIBRATION]
@app.callback([Output('ca-disp-sensor', 'children')],
              [Input('ca-start-btn', 'n_clicks'),
               Input('ca-port-id', 'value'),
               Input('ca-clear-btn', 'n_clicks')])
def run_calibration(btn,port, clear):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'ca-start-btn' in changed_id:
        
        try:
            print(btn)
            getdata.upload_data(port= port, baud=9600, n=10, table='test', inc='test')
            raise PreventUpdate
        except:
            raise PreventUpdate
    elif 'ca-clear-btn' in changed_id:
        try:
            conn = sqlite3.connect('./databases/serverdb.db')
            c = conn.cursor()

            # delete all rows from table
            c.execute('DELETE FROM test;',);
            conn.commit()
            conn.close()
            raise PreventUpdate
        except:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback([Output('ca-disp-sensor', 'figure'),
               Output('ca-load-sensor', 'figure')],
               [Input('interval-component1', 'n_intervals')])
def update_plot(n):
    try:
        df = getdata.get_dataframe(table='test')
        fig1, fig2 = scatter_data(df, height=400)
        return fig1, fig2
    except:
        print('ERROR')
        raise PreventUpdate
        
#ROUTING CALLBACK
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    
    if pathname == '/calibration':
        return calibration_layout
    elif pathname == '/showdata':
        return showdata_layout
    elif pathname == '/shutdown':
        shutdown_server()
        return 'Server shutting down...'
    else:
        return home_layout

if __name__ == '__main__':
    app.run_server(debug=True, port=2020)
    #ui.run()