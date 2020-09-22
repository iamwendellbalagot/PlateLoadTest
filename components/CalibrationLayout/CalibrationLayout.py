import dash_html_components as html
import dash_core_components as dcc


import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../../')
from getdata import GetData
sys.path.insert(1, './components/PlotGenerator')
from PlotGenerator import scatter_data, get_lsc
getdata = GetData(path='./databases/serverdb.db')

df = getdata.get_dataframe(table='test',path='./databases/serverdb.db')
fig1,fig2 = scatter_data(df, height=400)

calibration_layout = html.Div(
    id = 'calib-id',
    style={
        'textAlign': 'center',
        'margin': '0 auto',
        'backgroundColor': '#050505',
        'position': 'relative',
        'height': '100vh'
    },
    className='row',
    
    children=[
        
        html.Div([
            html.Button(id='start-an-btn', style={'display': 'none'}),
            html.Button(id='calib-link', style={'display': 'none'}),
        
            html.H6('CHECK DEVICE CONNECTION',
                        style={'display': 'block',
                                'color': 'white',
                                'marginTop': '20px',
                                'fontSize': '14px'}),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Button(
                                children='Check',
                                id = 'check-port',
                                className='btn btn-dark'
                            )
                        ],
                        className='input-group-prepend'
                    ),
                    dcc.Input(
                        id= 'ca-port-id',
                        placeholder='Port',
                        type='text',
                        className='form-control'
                    )
                ],
                className='input-group mb-3',
                style={'width': '100%', 'margin': '10px auto 30px auto'}
            ),
            
            html.Div(children='',
                     id='ca-ind', 
                     style={'color': 'lightgreen', 'fontSize':'15px'}),
            
            html.H6('CHECK SENSORS OUTPUT',
                        style={'display': 'block',
                                'color': 'white',
                                'margin': '10px auto',
                                'fontSize': '14px'}),
            
            
            html.Button(
                'Generate',
                className='btn btn-dark btn-lg btn-block',
                id = 'ca-start-btn',
                n_clicks=0,
                style = {
                    'display': 'block',
                    'position': 'relative'
                }),
            html.Div(children='Click the button to start a test',
                 id='ca-test-indicator', 
                 style={'color': 'white', 
                        'borderBottom': '1px solid grey',
                        'padding': '10px 0 20px 0',
                        'fontSize': '10px', 'color': 'grey'}),
                        
            dcc.Link('Back to Dashboard',
                    id='back-dash',
                    style={'textDecoration': 'underline',
                           'color':'white',
                           'fontSize': '15px',
                           'position':'absolute',
                           'bottom': '20px',
                           'cursor': 'pointer',
                           'left': '10%'},
                    href = '/'
            ),
            
        ],
            style={'width': '50%',
                   'margin': '0 auto',
                   'marginTop':'10px',
                   'paddingTop': '120px',
                   'backgroundColor': '#1b1c25',
                   'paddingTop': '100px'},
            className='col-6 col-md-2'
        ),
    
        html.Div([
            html.H2(children='LIVE PLOTTER',
                    style={'color':'white',
                           'fontFamily': 'sans-serif',
                           'fontWeight': '700',
                           'padding': '10px'}),
                           
            html.Div(
                children=[
                    dcc.Graph(
                        id = 'ca-disp-sensor',
                        figure=fig1
                    ),
                    dcc.Interval(
                        id='interval-component1',
                        interval=1000, # in milliseconds
                        n_intervals=0
                    )
                ],
                id = 'ca-1',
                style={'width': '40%', 'display':'inline-block'}
                
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id = 'ca-load-sensor',
                        figure=fig2
                    ),
                    dcc.Interval(
                        id='interval-component2',
                        interval=1000, # in milliseconds
                        n_intervals=0
                    )
                ],
                id='ca-2',
                style={'width': '40%', 'display':'inline-block'}),
            html.Button(
                'Clear output',
                className='btn btn-dark btn-lg btn-block',
                id = 'ca-clear-btn',
                n_clicks=0,
                style = {
                    'display': 'block',
                    'position': 'relative',
                    'width': '80%',
                    'margin': '0 auto'
                }),
            
        ],
            className='col-md-10',
            style={'padding': '50px 0 0 0'}
        ),
        
        
])

