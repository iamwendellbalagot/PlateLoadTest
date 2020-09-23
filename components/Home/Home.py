import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

import pandas as pd
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../../')
from getdata import GetData
sys.path.insert(1, './components/PlotGenerator')
from PlotGenerator import scatter_data, get_lsc
getdata = GetData(path='./databases/serverdb.db')

df = getdata.get_dataframe(path='./databases/serverdb.db')
#[Scatterplot 1]
fig1, fig2 = scatter_data(df)

dummy_lsc = [[0,50,100,200,300,400,500,600],
            [0,1.5,2,4,7.5,12.5, 20, 40.6]]
dummy_lsc = pd.DataFrame(dummy_lsc).T
dummy_lsc.columns = ['P', 'S']
lsc = get_lsc(dummy_lsc)

items = [
    dbc.DropdownMenuItem(
        dcc.Link("Calibration", id = 'calib-link', href='/calibration',
                 style = {'color': 'black',
                          ':hover': {'color': 'black'}}),
        style={'height':'20px', 'width': '200px' }
    ),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("View test data", id='view-data-link', style={'height':'20px', 'width': '200px' }),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem(
        dcc.Link("Close application", id = 'exit-app', href='/shutdown',
                 style = {'color': 'black',
                          ':hover': {'color': 'black'}}),
        style={'height':'20px', 'width': '200px' }
    )
]

#HOME LAYOUT
home_layout = html.Div(
    id = 'home-id',
    style={
        'textAlign': 'center',
        'margin': '0 auto',
        'backgroundColor': '#050505',
        'position': 'relative',
        'padding': '0',
        'paddingBottom': '50px',
        'height': '100%'
    },
    className='row',
    
    children=[
        
        html.Div([
            dcc.Input(id = 'check-port-status', style={'display': 'none'}, type='number'),
            html.Div([
                dbc.DropdownMenu(label="Menu", 
                                 bs_size="sm", 
                                 children=items, 
                                 className='m-1',
                                 color='link')
            ], style={'position': 'absolute',
                      'top': '0px',
                      'right': '0px'}),
            html.Div([
                
                #[Device info]
                html.H4('CREATE A TEST',
                        style={'display': 'block',
                                'color': 'white',
                                'margin': '10px auto'}),
                html.Div([
                    dcc.Input(id='port', 
                        debounce=True,
                        placeholder='Device Port',
                        type='text',
                        className='form-control',
                        required=True,
                        style={'height': '20px', 'fontSize':'10px'}),
                        ],
                    className='input-group input-group-sm mb-3 sm',
                    style={'width': '100%', 'margin': '0 auto'}
                ),
                
                html.Div([
                    dcc.Input(id='test-id', 
                        debounce=True,
                        placeholder='Test ID',
                        type='text',
                        className='form-control',
                        required=True,
                        style={'height': '20px', 'fontSize':'10px'}),
                        ],
                    className='input-group input-group-sm mb-3',
                    style={'width': '100%', 'margin': '0 auto'}
                ),
                html.Div([
                    dcc.Input(id='inc-no', 
                        debounce=True,
                        placeholder='Increment no.',
                        type='number',
                        className='form-control',
                        required=True,
                        style={'height': '20px', 'fontSize':'10px'}),
                        ],
                    className='input-group input-group-sm mb-3',
                    style={'width': '100%', 'margin': '0 auto'}
                ),
                
                #[CONSTANTS]
                html.Div([
                    dcc.Input(id='ini-set-1', 
                        debounce=True,
                        placeholder='Initial settlement (DG1) in cm',
                        type='number',
                        className='form-control',
                        required=True,
                        style={'height': '20px', 'fontSize':'10px'}),
                        ],
                    className='input-group input-group-sm mb-3',
                    style={'width': '100%', 'margin': '30px auto 0 auto'}
                ),
                html.Div([
                    dcc.Input(id='ini-set-2', 
                        debounce=True,
                        placeholder='Initial settlement (DG2) in cm',
                        type='number',
                        className='form-control',
                        required=True,
                        style={'height': '20px', 'fontSize':'10px'}),
                        ],
                    className='input-group input-group-sm mb-3',
                    style={'width': '100%', 'margin': '0 auto'}
                ),
                html.Div([
                    dcc.Input(id='plate-area', 
                        debounce=True,
                        placeholder='Plate area in meter squared',
                        type='number',
                        className='form-control',
                        required=True,
                        style={'height': '20px', 'fontSize':'10px'}),
                        ],
                    className='input-group input-group-sm mb-3',
                    style={'width': '100%', 'margin': '0 auto'}
                ),
                html.Div([
                    dcc.Input(id='plate-width', 
                        debounce=True,
                        placeholder='Width of Plate (meter)',
                        type='number',
                        className='form-control',
                        required=True,
                        style={'height': '20px', 'fontSize':'10px'}),
                        ],
                    className='input-group input-group-sm mb-3',
                    style={'width': '100%', 'margin': '0 auto'}
                ),
                html.Div([
                    dcc.Input(id='width-footing', 
                        debounce=True,
                        placeholder='Width of Footing (meter)',
                        type='number',
                        className='form-control',
                        required=True,
                        style={'height': '20px', 'fontSize':'10px'}),
                        ],
                    className='input-group input-group-sm mb-3',
                    style={'width': '100%', 'margin': '0 auto'}
                ),
                html.Div([
                    dcc.Input(id='factor-safety', 
                        debounce=True,
                        placeholder='Factor of safety',
                        type='number',
                        className='form-control',
                        required=True,
                        style={'height': '20px', 'fontSize':'10px'}),
                        ],
                    className='input-group input-group-sm mb-3',
                    style={'width': '100%', 'margin': '0 auto'}
                ),
                #[TIMER]
                html.Div([
                    dcc.Input(id='time-input', 
                        debounce=True,
                        placeholder='Time in minutes',
                        type='number',
                        className='form-control',
                        required=True,
                        style={'height': '20px', 'fontSize':'10px'}),
                        ],
                    className='input-group input-group-sm mb-3',
                    style={'width': '100%', 'margin': '30px auto 10px auto'}
                ),
                
                
                
                html.Button(
                    'Begin',
                    className='btn btn-dark btn-lg btn-block',
                    id = 'start-btn',
                    n_clicks=0,
                    style = {
                        'display': 'block',
                        'position': 'relative',
                        'height': '30px',
                        'fontSize': '12px',
                        'padding': '5px'
                    }),
                html.Div(children='Click the button to start a test',
                     id='test-indicator', 
                     style={'color': 'gray', 
                            'borderBottom': '1px solid grey',
                            'paddingBottom': '20px',
                            'fontSize': '10px'}), 
                ],
            id='start-test'
            ),
            html.Div([
                html.H4('INPUTS SUMMARY', 
                         style={'margin': '0 0 20px 0',
                                'color': 'white', 
                                'borderBottom': '1px solid gray',
                                'marginTop': '20px'}),
                html.P(id='p-test-id', style={'float': 'left',
                                      'display': 'block',
                                      'color': 'gray',
                                      'margin': '0',
                                      'fontSize': '15px'}),
                html.Br(),
                html.P(id='p-inc-no', style={'float': 'left',
                                      'display': 'block',
                                      'color': 'gray',
                                      'margin': '0',
                                      'fontSize': '15px'}),
                html.Br(),                      
                html.P(id='dg-1', style={'float': 'left',
                                      'display': 'block',
                                      'color': 'gray',
                                      'margin': '0',
                                      'fontSize': '15px'}),
                html.Br(),                      
                html.P(id='dg-2', style={'float': 'left',
                                      'display': 'block',
                                      'color': 'gray',
                                      'margin': '0',
                                      'fontSize': '15px'}),
                html.Br(),
                html.P(id='s-width-footing', style={'float': 'left',
                                      'display': 'block',
                                      'color': 'gray',
                                      'margin': '0',
                                      'fontSize': '15px'}),
                html.Br(),                      
                html.P(id='p-fs', style={'float': 'left',
                                      'display': 'block',
                                      'color': 'gray',
                                      'margin': '0',
                                      'fontSize': '15px'}),
                html.Br(),                      
                html.P(id='p-time', style={'float': 'left',
                                      'display': 'block',
                                      'color': 'gray',
                                      'margin': '0',
                                      'fontSize': '15px',
                                      'paddingBottom': '50px'}),

            ], style={'display': 'none'}, id='summary'),
            
            html.Div(children=[
            ],id='timer-div'),
            html.Button(
                    html.A('Create another test?', href ='/'),
                    className='btn btn-dark btn-lg btn-block',
                    id = 'start-an-btn',
                    n_clicks=0,
                    style = {
                        'display': 'none',
                        'position': 'relative',
                        'height': '30px',
                        'fontSize': '12px',
                        'padding': '5px'
                    }),
                 
            html.H4('CHECK TEST RESULTS',
                        style={'display': 'block',
                                'color': 'white',
                                'marginTop': '20px'}),
                 
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Button(
                                children='Check',
                                id = 'view1',
                                className='btn btn-dark',
                                style={'height': '30px',
                                        'fontSize': '12px',
                                        'padding': '5px'}
                            )
                        ],
                        className='input-group-prepend'
                    ),
                    dcc.Input(
                        id= 'inp-sc',
                        placeholder='Test ID',
                        type='text',
                        className='form-control',
                        style={'height': '30px',
                                'fontSize': '12px',
                                'padding': '5px'}
                    )
                ],
                className='input-group mb-3',
                style={'width': '100%', 'margin': '10px auto 30px auto'}
            ),
            
            html.H4('GENERATE A EXCEL FILE',
                        style={'display': 'block',
                                'color': 'white',
                                'marginTop': '20px'}),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Button(
                                children='Generate',
                                id = 'view2',
                                className='btn btn-dark',
                                style={'height': '30px',
                                        'fontSize': '12px',
                                        'padding': '5px'}
                            )
                        ],
                        className='input-group-prepend'
                    ),
                    dcc.Input(
                        id= 'inp-csv',
                        placeholder='Test ID',
                        type='text',
                        className='form-control',
                        style={'height': '30px',
                                'fontSize': '12px',
                                'padding': '5px'}
                    ),
                    html.Div(
                        dbc.RadioItems(
                        options=[
                            {'label': 'Summary', 'value': 'summary'},
                            {'label': 'Complete', 'value': 'complete'}
                        ],
                        value='summary',
                        id = 'csv-type',
                        labelStyle={'display': 'inline-block', 'color': 'gray'}),
                        style = {'display': 'block', 
                                 'top': '40px',
                                 'position': 'absolute'}
                    ),
                ],
                className='input-group mb-3',
                style={'width': '100%', 
                       'margin': '10px auto 30px auto'}
            ),
            html.P('Back to dashboard',
                    id='back-dash',
                    style={'display': 'none'})
        ],
            style={'width': '50%',
                   'margin': '0 auto',
                   'marginTop':'10px',
                   'paddingTop': '20px',
                   'backgroundColor': '#1b1c25',
                   'borderRadius': '5px'},
            className='col-6 col-md-2'
        ),
        
        
    
        html.Div([
            html.H2(children='PLATE LOAD TEST DASHBOARD',
                    style={'color':'white',
                           'fontFamily': 'sans-serif',
                           'fontWeight': '700',
                           'padding': '10px'}),
                           
            html.Div(
                children=[
                    dcc.Graph(
                        id = 'disp-sensor',
                        figure= fig1
                    )
                ],
                id = 'graph-1',
                style={'width': '40%', 'display':'inline-block'}
                
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id = 'load-sensor',
                        figure= fig2
                    )
                ],
                id='graph-2',
                style={'width': '40%', 'display':'inline-block'}),
             
            html.Div(
                children=[
                    dcc.Graph(
                        id = 'lsc',
                        figure= lsc
                    )
                ],
                id = 'graph-2',
                style={'width': '80%', 'display':'inline-block'}
                
            ),
            html.Div([
                dbc.Button("Generate Results", color="dark", block=True, id='gen-res')
            ], style={'margin': '0 auto', 'width': '80%'})
            
        ],
            className='col-md-10'
        ),
        
        
])