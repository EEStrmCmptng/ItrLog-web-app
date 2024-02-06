import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import os
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import app

uname=''
loc=f'flink/{uname}'
workload_loc=f'flink/{uname}/combined.csv'

df_comb = pd.read_csv(workload_loc, sep=',')
df_comb = df_comb[df_comb['i'] > 0]
df_comb = df_comb[df_comb['watts_avg'] > 0]
axis_values = [{'label': key, 'value': key} for key in df_comb.columns]
numfigs = 3

def genfigtype(i):
    return html.Div([
        dcc.Dropdown(id=f'figtype{uname}-xselector-{i}', value='SourcenumRecordsOutPerSecond_avg', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id=f'figtype{uname}-yselector-{i}', value='watts_avg', style={'width':'60%'}, options=axis_values),
        dcc.Graph(
            id=f'figtype{uname}-scatter-{i}', style={'display': 'inline-block'}
        )
    ], style={'display': 'inline-block'})

layout = html.Div([
    dcc.Link('Home', href='/'),
    html.Br(),
        
    dbc.Row([        
        dbc.Col(children=[genfigtype(i) for i in range(0, numfigs)])
    ]),
])

for i in range(0, numfigs):
    @app.callback(
        Output(f'figtype{uname}-scatter-{i}', 'figure'),
        [Input(f'figtype{uname}-xselector-{i}', 'value'),
         Input(f'figtype{uname}-yselector-{i}', 'value')]
    )
    def update_custom_scatter(xcol, ycol):
        fig = px.scatter(df_comb, 
                         x=xcol, 
                         y=ycol, 
                         color='rate',
                         hover_data=['i', 'nmappers', 'SourcenumRecordsOutPerSecond_avg', 'rate', 'policy'],
                         custom_data=['i', 'nmappers', 'SourcenumRecordsOutPerSecond_avg', 'rate', 'policy'],
                         title=f'X={xcol}\nY={ycol}')
        return fig
