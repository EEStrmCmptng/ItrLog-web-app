from dis import Instruction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from app import app
import plotly.express as px
import json


LINUX_COLS = ['i', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions', 'cycles', 'ref_cycles', 'llc_miss', 'c0','c1', 'c1e', 'c3', 'c6', 'c7', 'joules', 'timestamp']
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
    df['llc_miss'] = df['llc_miss'].diff()
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
    fig = px.scatter(
        x=[x*5 for x in range(len(latencies))],
        y=latencies,
    )
    return fig




cores = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
y_axis_options =  ['rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions', 'cycles', 'ref_cycles', 'joules', 'llc_miss']

core_dfs = []
core_dfs_non0j = []
latency_fig = None
rx_desc_max = 0
rx_bytes_max = 0
tx_desc_max = 0
tx_bytes_max = 0
instructions_max = 0
cycles_max = 0
ref_cycles_max = 0
llc_miss_max = 0
joules_max = 0


layout = html.Div([
    html.Br(),
    html.H3('Per Core Timeline plot', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.H5('Select Y-axis'),
        dcc.Dropdown(id='y-axis-selector', value='joules', options=y_axis_options),
    ], style={'display': 'inline-block'}),
    html.Div([
        dbc.Row([
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-0-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-1-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-2-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-3-figure',
                    style={ 'width': '100%', 'height': '100%'},
                ),
            ])),
        ]),
    ], style={'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Div([
        dbc.Row([
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-4-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-5-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-6-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-7-figure',
                    style={ 'width': '100%', 'height': '100%'},
                ),
            ])),
        ]),
    ], style={'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Div([
        dbc.Row([
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-8-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-9-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-10-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-11-figure',
                    style={ 'width': '100%', 'height': '100%'},
                ),
            ])),
        ]),
    ], style={'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Div([
        dbc.Row([
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-12-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-13-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-14-figure',
                    style={'width': '100%', 'height': '100%'},
                ),
            ])),
            dbc.Col(html.Div([
                dcc.Graph(
                    id='core-15-figure',
                    style={ 'width': '100%', 'height': '100%'},
                ),
            ])),
        ]),
    ], style={'margin-left': 'auto', 'margin-right': 'auto'}),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.H3('Latency Timeline Plot', style={'textAlign': 'center'}),
    html.Br(),
    html.Div(id='empty'),
    html.Div([
        dcc.Graph(
            id='flink-latency-timeline',
            style={'display': 'inline-block', 'width': '100%', 'height': '100%'},
        ),
    ], style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '60%'}),
])


def refresh_df():
    global core_dfs
    global core_dfs_non0j
    global latency_fig
    global rx_desc_max
    global rx_bytes_max
    global tx_desc_max
    global tx_bytes_max
    global instructions_max
    global cycles_max
    global ref_cycles_max
    global llc_miss_max
    global joules_max
    
    core_dfs = []
    core_dfs_non0j=[]

    for core in cores:
        df, df_non0j = read_log(log_loc, core, itr, dvfs, rapl)
        rx_bytes_max = max(rx_bytes_max, df['rx_bytes'].max())
        rx_desc_max = max(rx_desc_max, df['rx_desc'].max())
        tx_bytes_max = max(tx_bytes_max, df['tx_bytes'].max())
        tx_desc_max = max(tx_desc_max, df['tx_desc'].max())
        instructions_max = max(instructions_max, df['instructions'].max())
        cycles_max = max(cycles_max, df['cycles'].max())
        ref_cycles_max = max(ref_cycles_max, df['ref_cycles'].max())
        llc_miss_max = max(llc_miss_max, df['llc_miss'].max())
        joules_max = max(joules_max, df_non0j['joules'].max())
        core_dfs.append(df)
        core_dfs_non0j.append(df_non0j)

    latency_fig = read_latency(log_loc, itr, dvfs, rapl)
    return

@app.callback(
    [Output('core-0-figure', 'figure'),
    Output('core-1-figure', 'figure'),
    Output('core-2-figure', 'figure'),
    Output('core-3-figure', 'figure'),
    Output('core-4-figure', 'figure'),
    Output('core-5-figure', 'figure'),
    Output('core-6-figure', 'figure'),
    Output('core-7-figure', 'figure'),
    Output('core-8-figure', 'figure'),
    Output('core-9-figure', 'figure'),
    Output('core-10-figure', 'figure'),
    Output('core-11-figure', 'figure'),
    Output('core-12-figure', 'figure'),
    Output('core-13-figure', 'figure'),
    Output('core-14-figure', 'figure'),
    Output('core-15-figure', 'figure'),
    Output('flink-latency-timeline', 'figure')],
    [Input('y-axis-selector', 'value')]
)
def update_custom_scatter(y_axis):
    global rx_desc_max
    global rx_bytes_max
    global tx_desc_max
    global tx_bytes_max
    global instructions_max
    global cycles_max
    global ref_cycles_max
    global llc_miss_max
    global joules_max
    global latency_fig
    refresh_df()
    figs = []
    for core in range(0,16):
        if y_axis == 'joules':
            df = core_dfs_non0j[int(core)]
        else:
            df = core_dfs[int(core)]
        fig = px.scatter(df, x='timestamp', y=y_axis, title=f'Core {core}', height=350)
        y_max = eval(y_axis+'_max')
        y_axis_range = [0-y_max/20, y_max+y_max/20]
        fig.update_layout(yaxis_range=y_axis_range)
        figs.append(fig)
    figs.append(latency_fig)
    return figs


