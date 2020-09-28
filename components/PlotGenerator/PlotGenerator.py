import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import sys

sys.path.insert(1, '../../')
from getdata import GetData

getdata = GetData()

def scatter_data(df, height=300):
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=np.arange(len(df)),
                                 y=df.S1,
                                 name='Sensor 1',
                                 marker_color='steelblue'))
        fig1.add_trace(go.Scatter(x=np.arange(len(df)),
                                 y=df.S2,
                                 name='Sensor 2',
                                 marker_color='lightgreen'))
        fig1.update_layout(title=dict(
                          text='<b>DISTANCE SENSORS OUTPUT</b>',
                          font=dict(size=20, color='white')), 
                          template='plotly_dark',
                          height=height,
                          yaxis=dict(range=[0,100]),
                          font=dict(family="Courier",
                                    size=12, color='gray'))                         
        fig1.update_xaxes(title='Time')
        fig1.update_yaxes(title='Centimeter')

        #[Scatterplot 2]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=np.arange(len(df)),
                                 y=df.S3,
                                 name='Sensor 3',
                                 marker_color='salmon'))

        fig2.update_layout(title=dict(
                          text='<b>LOAD SENSOR OUTPUT</b>',
                          font=dict(size=20, color='white')), 
                          template='plotly_dark',
                          height=height,
                          font=dict(family="Courier",
                                    size=12, color='gray'))                         
        fig2.update_xaxes(title='Time')
        fig2.update_yaxes(title='Kg')
        
        return fig1, fig2


        
        
def get_lsc(df, x=[0,50,100,200,300,400,500,600],
            y=[0,1.5,2,4,7.5,12.5, 20, 40.6],
            ubc=500, ubc_s=20):
            
    x = np.append(0,df.P)
    y = np.append(0,df.S)
    max_settlement = df.S.max()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,
                             y=y,
                             name='Result',
                             marker_color='gold'))
    fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=ubc,
            y0=0,
            x1=ubc,
            y1=max_settlement,
            line=dict(
                color="cyan",
                width=4,
                dash='dot'
            )))
    fig.update_shapes(dict(xref='x', yref='y'))
    fig.update_layout(title=dict(
                          text='<b>LOAD SETTLEMENT CURVE</b>',
                          x=0.5,
                          y=0.1,
                          font=dict(size=20, color='white')), 
                      template='plotly_dark',
                      height=300,
                      xaxis={ 'side': 'top'}, 
                      yaxis={'autorange':'reversed', 'side': 'left'},
                      font=dict(family="Courier",
                                size=12, color='gray'))                         
    fig.update_xaxes(title='LOAD IN kg/m^2')
    fig.update_yaxes(title='SETTLEMENT IN mm')
    return fig