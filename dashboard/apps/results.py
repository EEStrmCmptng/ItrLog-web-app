from distutils import core
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from app import app
import plotly.express as px
import json


LINUX_COLS = ['i', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions', 'cycles', 'ref_cycles', 'llc_miss', 'c1', 'c1e', 'c3', 'c6', 'c7', 'joules', 'timestamp']
JOULE_CONVERSION = 0.00001526 #counter * constant -> JoulesOB
TIME_CONVERSION_khz = 1./(2899999*1000)

log_loc ='./current-raw-log'
dvfs = '0x1d00'
rapl = '135'
itr = '1'

def read_log(log_loc, core, itr, dvfs, rapl):
    fname = f'{log_loc}/linux.mcd.dmesg.0_{core}_{itr}_{dvfs}_{rapl}'
    df = pd.read_csv(fname, sep=' ', names=LINUX_COLS)
    df['timestamp'] = df['timestamp'] - df['timestamp'].min()
    df['instructions'] = df['instructions'].diff()
    df['cycles'] = df['cycles'].diff()
    df['ref_cycles'] = df['ref_cycles'].diff()
    df['timestamp'] = df['timestamp'] * TIME_CONVERSION_khz
    df_non0j = df[df['joules'] > 0
                  & (df['instructions'] > 0)
                  & (df['cycles'] > 0)
                  & (df['ref_cycles'] > 0)
                  & (df['llc_miss'] > 0)].copy()
    df_non0j['joules'] = df_non0j['joules'].diff() * JOULE_CONVERSION
    return df, df_non0j

def read_latency(log_loc, itr, dvfs, rapl):
    fname = f'{log_loc}/flink-latency.0_{itr}_{dvfs}_{rapl}'
    latency_str = open(fname, 'r').read()
    latencies = json.loads(latency_str)
    latencies = [int(latency) for latency in latencies]
    fig = px.line(
        x=range(len(latencies)),
        y=latencies,
    )
    return fig




cores = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
y_axis_options =  ['rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions', 'cycles', 'ref_cycles', 'joules', 'timestamp']

core_dfs = []
core_dfs_non0j = []

for core in cores:
    df, df_non0j = read_log(log_loc, core, itr, dvfs, rapl)
    core_dfs.append(df)
    core_dfs_non0j.append(df_non0j)

latency_fig = read_latency(log_loc, itr, dvfs, rapl)


layout = html.Div([
    html.Br(),
    html.Br(),
    html.H3('Per Core Timeline plot', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Div([
        dbc.Row([
            dbc.Col(html.Div([
                html.H5('Select core'),
                dcc.Dropdown(id='core-selector', value='0', options=cores),
            ])), 
                
            dbc.Col(html.Div([
                html.H5('Select Y-axis'),
                dcc.Dropdown(id='y-axis-selector', value='joules', options=['joules', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes']),
            ])),
        ]),
    ], style={'margin-left': '250px', 'margin-right': '250px', 'align-items': 'left'}),
    html.Div([
        dcc.Graph(
            id='core-figure',
            style={'display': 'inline-block', 'width': '100%', 'height': '100%'},
        ),   
    ], style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '60%'}),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.H3('Latency Timeline Plot', style={'textAlign': 'center'}),
    html.Br(),
    html.Div([
        dcc.Graph(
            id='flink-latency-timeline',
            figure=latency_fig,
            style={'display': 'inline-block', 'width': '100%', 'height': '100%'},
        ),
    ], style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '60%'}),
])


@app.callback(
    Output('core-figure', 'figure'),
    [Input('core-selector', 'value'),
     Input('y-axis-selector', 'value')]
)
def update_custom_scatter(core, y_axis):
    if y_axis == 'joules':
        df = core_dfs_non0j[int(core)]
    else:
        df = core_dfs[int(core)]
    fig = px.line(df, x='timestamp', y=y_axis, ) 
    print(df.tail())
    return fig