import dash_html_components as html
from getdata import GetData

getdata = GetData()

#[Generate Table]
def generate_table(max_rows=-1):
    dataframe = getdata.get_dataframe()
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col,style={'border': '1px solid white'}) for col in dataframe.columns]),
   
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col], 
                        style={'border': '1px solid white',
                               'textAlign':'left',
                               'marginLeft': '20px'}) for col in dataframe.columns
            ]) for i in range(len(dataframe))
        ], style={'border': '1px solid white'})
    ], style={'border': '1px solid white', 
              'borderCollapse': 'collapse',
              'fontFamily': 'sans-serif',
              'color':'white',
              'width': '60%'})


#COLLECTED DATA LAYOUT
showdata_layout = html.Div(
    style={
        'textAlign': 'center',
        'margin': '0 auto',
        'backgroundColor': 'black',
        'position': 'relative',
        'padding': '10px'
    },
    
    children=[
        html.H1(children='PLATE LOAD TEST',
                style={'color':'white',
                       'fontFamily': 'sans-serif'}),
        
        html.Div(children=[
            html.H3(children='COLLECTED DATA', 
            style={'color':'white', 
                   'fontFamily': 'sans-serif',
                   'textAlign': 'left'}),
            generate_table()
        ], style={'position': 'relative',
                  'marginLeft':'25%'})
])