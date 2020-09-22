import dash_html_components as html
import dash_core_components as dcc

layout_p = html.Div([
        html.Div(className='progress-bar',
                 role='progressbar',
                 aria-valuenow="25",
                 aria-valuemin="0",
                 aria-valuemax="100")
    ], className='progress')
    
