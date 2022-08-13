import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from app import app

LINUX_COLS = ['i', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions', 'cycles', 'ref_cycles', 'llc_miss', 'c1', 'c1e', 'c3', 'c6', 'c7', 'joules', 'timestamp']
JOULE_CONVERSION = 0.00001526 #counter * constant -> JoulesOB
TIME_CONVERSION_khz = 1./(2899999*1000)

global_linux_default_df = pd.DataFrame()
global_linux_default_df_non0j = pd.DataFrame()
global_linux_default_name = []

workload_loc='./datasets/1000_120000.csv'
df_comb = pd.read_csv(workload_loc, sep=' ')
axis_values = [{'label': key, 'value': key} for key in df_comb.columns] 

edp_fig = px.scatter(df_comb, 
                     x='latency', 
                     y='joules', 
                     labels={'latency': 'Latency (s)', 'joules': 'Energy (Joules)'}, 
                     hover_data=['i', 'itr', 'rapl', 'dvfs', 'num_interrupts'],
                     custom_data=['i', 'itr', 'rapl', 'dvfs'],
                    )

#df_comb_200k_no_default = df_comb_200k[df_comb_200k['sys'] != 'linux_default']
#df_comb_200k_no_default['opacity'] = (df_comb_200k_no_default['joules'] - df_comb_200k_no_default['joules'].min()) / (df_comb_200k_no_default['joules'].max() - df_comb_200k_no_default['joules'].min())

"""
    html.Div([
        dcc.Graph(
            id='mcd2-edp-scatter',
            figure = edp_fig,
            style={'display': 'inline-block', 'width': '100%', 'height': '100%'},
        ),   
    ], style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '80%'}),
    html.Br(),
"""

layout = html.Div([
    html.Br(),
    html.Br(),
    html.H3('Flink Query 1, 1000 QPS with 2min Runtime', style={'textAlign': 'center'}),
    html.Br(),
    html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='mcd2-xaxis-selector-1', value='latency', className="m-1", options=axis_values),
            ]),
            dbc.Col([
                dcc.Dropdown(id='mcd2-yaxis-selector-1', value='joules', className="m-1", options=axis_values),
            ]),
        ]),
    ], style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '60%'}),
    html.Div([
        dcc.Graph(
            id='mcd2-custom-scatter-1',
            style={'display': 'inline-block', 'width': '100%', 'height': '100%'},
        ),   
    ], style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '60%'}),
])


@app.callback(
    Output('mcd2-custom-scatter-1', 'figure'),
    [Input('mcd2-xaxis-selector-1', 'value'),
        Input('mcd2-yaxis-selector-1', 'value')]
)
def update_custom_scatter(xcol, ycol):
    fig = px.scatter(df_comb, 
                        x=xcol, 
                        y=ycol, 
                        hover_data=['itr', 'rapl', 'dvfs', 'num_interrupts'],
                        custom_data=['itr', 'rapl', 'dvfs', 'num_interrupts'],
                        title=f'X={xcol}\nY={ycol}')    
    return fig