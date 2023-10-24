import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import os
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import app

rdvfs_dict = {
    1 : "1",
    1.2 : "0c00",
    1.3 : "0d00",
    1.4 : "0e00",
    1.5 : "0f00",
    1.6 : "1000",
    1.7 : "1100",
    1.8 : "1200",
    1.9 : "1300",
    2.0 : "1400",
    2.1 : "1500",
    2.2 : "1600",
    2.3 : "1700",
    2.4 : "1800",
    2.5 : "1900",
    2.6 : "1a00",
    2.7 : "1b00",
    2.8 : "1c00",
    2.9 : "1d00",
}

workload_loc='~/flink/10_12_2023_5.15.89_itrlog/combined.csv'

TIME_CONVERSION_khz = 1./(2600000*1000)
JOULE_CONVERSION = 0.00001526

df_comb = pd.read_csv(workload_loc, sep=',')
df_comb = df_comb[df_comb['rate'] == 300000].copy()
df_comb = df_comb[df_comb['joules'] > 0]
df_comb = df_comb[df_comb['instructions'] > 0]
axis_values = [{'label': key, 'value': key} for key in df_comb.columns]

LINUX_COLS = ['i', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions', 'cycles', 'ref_cycles', 'llc_miss', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7', 'joules', 'timestamp']

taxis_values=['i', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions',
       'cycles', 'ref_cycles', 'llc_miss', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7',
       'joules', 'timestamp', 'instructions_diff', 'cycles_diff',
       'ref_cycles_diff', 'llc_miss_diff', 'joules_diff', 'c0_diff', 'c1_diff',
       'c1e_diff', 'c3_diff', 'c6_diff', 'c7_diff', 'timestamp_diff']

layout = html.Div([
    html.H3('Flink Query1 Rate 300K'),
    dcc.Link('Home', href='/'),
    html.Br(),
    
    html.Div([
        dcc.Dropdown(id='mcd3-xaxis-selector-1', value='SourcenumRecordsOutPerSecond_avg', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id='mcd3-yaxis-selector-1', value='joules', style={'width':'60%'}, options=axis_values),        
        dcc.Graph(
            id='mcd3-custom-scatter-1', style={'display': 'inline-block'}
        )
    ], style={'display': 'inline-block'}),
        
    html.Div([
        dcc.Dropdown(id='mcd3-xaxis-selector-2', value='SourcenumRecordsOutPerSecond_avg', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id='mcd3-yaxis-selector-2', value='instructions', style={'width':'60%'}, options=axis_values),
        dcc.Graph(
            id='mcd3-custom-scatter-2', style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(id='mcd3-xaxis-selector-3', value='SourcenumRecordsOutPerSecond_avg', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id='mcd3-yaxis-selector-3', value='ref_cycles', style={'width':'60%'}, options=axis_values),
        dcc.Graph(
            id='mcd3-custom-scatter-3',
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(id='mcd3-xaxis-selector-4', value='rxBytes', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id='mcd3-yaxis-selector-4', value='rxBytesIntLog', style={'width':'60%'}, options=axis_values),
        dcc.Graph(
            id='mcd3-custom-scatter-4',
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),

    html.Div([
        html.Hr(),
        html.Br()
    ]),
    
    html.Div([
        html.Hr(),
        html.Br()
    ]),

    html.Div([
        html.P('Y-AXIS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-xaxis-selector-5',
                     value='timestamp_diff',
                     style={'width':'60%'},
                     options=taxis_values,
                     placeholder="Select y-axis value",),
        html.P('CORE: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-yaxis-selector-5',
                     value=0,
                     style={'width':'60%'},
                     options=[x for x in range(0, 16)],
                     placeholder="Select core"),
        
        html.P('ITERATION: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-zaxis-selector-5',
                     value=0,
                     style={'width':'60%'},
                     options=[x for x in range(0, 10)],
                     placeholder="Select a iteration number",),
        html.P('POLICY: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-aaxis-selector-5',
                     value="ondemand",
                     style={'width':'60%'},
                     options=["ondemand", "conservative","performance", "schedutil", "powersave", "userspace"]),
        html.P('ITR: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-baxis-selector-5',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 2, 100, 200, 400, 600]),
        html.P('DVFS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-caxis-selector-5',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6]),
        dcc.Graph(
            id='mcd3-custom-scatter-5',
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),

    html.Div([
        html.P('Y-AXIS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-xaxis-selector-6',
                     value='timestamp_diff',
                     style={'width':'60%'},
                     options=taxis_values,
                     placeholder="Select y-axis value",),
        html.P('CORE: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-yaxis-selector-6',
                     value=0,
                     style={'width':'60%'},
                     options=[x for x in range(0, 16)],
                     placeholder="Select core"),
        
        html.P('ITERATION: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-zaxis-selector-6',
                     value=0,
                     style={'width':'60%'},
                     options=[x for x in range(0, 10)],
                     placeholder="Select a iteration number",),
        html.P('POLICY: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-aaxis-selector-6',
                     value="ondemand",
                     style={'width':'60%'},
                     options=["ondemand", "conservative","performance", "schedutil", "powersave", "userspace"]),
        html.P('ITR: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-baxis-selector-6',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 2, 100, 200, 400, 600]),
        html.P('DVFS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='mcd3-caxis-selector-6',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6]),
        dcc.Graph(
            id='mcd3-custom-scatter-6',
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),

])

for i in range(1, 5):
    @app.callback(
        Output('mcd3-custom-scatter-'+str(i), 'figure'),
        [Input('mcd3-xaxis-selector-'+str(i), 'value'),
         Input('mcd3-yaxis-selector-'+str(i), 'value')]
    )
    def update_custom_scatter(xcol, ycol):
        fig = px.scatter(df_comb, 
                         x=xcol, 
                         y=ycol, 
                         color='policy',
                         hover_data=['i', 'itr', 'dvfs'],
                         custom_data=['i', 'itr', 'dvfs'],
                         title=f'X={xcol}\nY={ycol}')    
        return fig

for i in range(5, 7):
    @app.callback(
        Output('mcd3-custom-scatter-'+str(i), 'figure'),
        [Input('mcd3-xaxis-selector-'+str(i), 'value'),
         Input('mcd3-yaxis-selector-'+str(i), 'value'),
         Input('mcd3-zaxis-selector-'+str(i), 'value'),
         Input('mcd3-aaxis-selector-'+str(i), 'value'),
         Input('mcd3-baxis-selector-'+str(i), 'value'),
         Input('mcd3-caxis-selector-'+str(i), 'value')]
    )
    def update_custom_scatter2(xcol, ycol, zcol, acol, bcol, ccol):
        df = pd.DataFrame()
        fname=f"/home/handong/flink/10_12_2023_5.15.89_itrlog/query1_cores16_frate300000_600000_fbuff-1_itr{bcol}_{acol}dvfs{rdvfs_dict[ccol]}_repeat{zcol}/ITRlogs/linux.flink.dmesg._{ycol}_{zcol}"
        df = pd.read_csv(fname, sep=' ', names=LINUX_COLS)
        df_non0j = df[(df['joules']>0) & (df['instructions'] > 0) & (df['cycles'] > 0) & (df['ref_cycles'] > 0) & (df['llc_miss'] > 0)]
        df_non0j['timestamp'] = df_non0j['timestamp'] - df_non0j['timestamp'].min()
        df_non0j['timestamp'] = df_non0j['timestamp'] * TIME_CONVERSION_khz
        df_non0j['ref_cycles'] = df_non0j['ref_cycles'] * TIME_CONVERSION_khz
        df_non0j['joules'] = df_non0j['joules'] * JOULE_CONVERSION
        df_non0j = df_non0j[(df_non0j['timestamp'] > 300) & (df_non0j['timestamp'] < 600)]
        
        tmp = df_non0j[['instructions', 'cycles', 'ref_cycles', 'llc_miss', 'joules', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7','timestamp']].diff()
        tmp.columns = [f'{c}_diff' for c in tmp.columns]
        df_non0j = pd.concat([df_non0j, tmp], axis=1)
        df_non0j.dropna(inplace=True)
        df_non0j = df_non0j[df_non0j['joules_diff'] > 0]

        fig = px.scatter(df_non0j, 
                         x='i', 
                         y=xcol)
        #fig1 = go.Figure()
        #fig1.update_layout(xaxis_title="timestamp (s)", yaxis_title=f't')
        #fig1.add_trace(go.Scatter(x=df_non0j['i'], y=df_non0j['timestamp_diff'], name='f', showlegend=True, marker={'sizemin':2, 'color':'red'}))
        
        return fig
