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

#loc='/home/handong/flink/11_3_2023_5.15.89_itrlog/'
#workload_loc='/home/handong/flink/11_3_2023_5.15.89_itrlog/combined.csv'

TIME_CONVERSION_khz = 1./(3299997*1000)
JOULE_CONVERSION = 0.00001526

LINUX_COLS = ['i', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions', 'cycles', 'ref_cycles', 'llc_miss', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7', 'joules', 'timestamp']

taxis_values=['i', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions',
       'cycles', 'ref_cycles', 'llc_miss', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7',
       'joules', 'timestamp', 'instructions_diff', 'cycles_diff',
       'ref_cycles_diff', 'llc_miss_diff', 'joules_diff', 'c0_diff', 'c1_diff',
       'c1e_diff', 'c3_diff', 'c6_diff', 'c7_diff', 'timestamp_diff']

def genfig(i):
    return html.Div([
        dcc.Textarea(
            id='netpipe-intlog-textarea-'+str(i),
            value=str(i-1),
            style={'width': '10%'},
            #disabled=True,
            readOnly=True,
            hidden='true'
        ),
        html.P('Y-AXIS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='netpipe-intlog-yaxis-'+str(i),
                     value='rx_bytes',
                     style={'width':'60%'},
                     options=taxis_values,
                     placeholder="Select y-axis value",),        
        dcc.Graph(
            id='netpipe-intlog-'+str(i),
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'})

layout = html.Div([
    #html.H3('Flink Query1 Rate 400K'),
    dcc.Link('Home', href='/'),
    html.Br(),

    ## itr log aggregate
    html.Div([
        html.Hr(),
        html.Br()
    ]),
    dbc.Row([        
        dbc.Col(children=[genfig(i) for i in range(1,16)])
    ])
])

for i in range(1, 16):
    @app.callback(
        Output('netpipe-intlog-'+str(i), 'figure'),
        [Input('netpipe-intlog-yaxis-'+str(i), 'value'),
         Input('netpipe-intlog-textarea-'+str(i), 'value')]
    )
    def update_intlogagg(yaxis, ii):
        fig1 = go.Figure(
            layout=go.Layout(
                title=go.layout.Title(text=f"Core {ii}")
            )
        )
        fig1.update_layout(xaxis_title=f"timestamp", yaxis_title=yaxis,  font=dict(
            family="Courier New, monospace",
            size=25
        ))
        
        #print(ii)
        df = pd.DataFrame()
        fname=f"/users/hand32/netpipe_intlog/linux.intlog.{ii}"
        df = pd.read_csv(fname, sep=' ', names=LINUX_COLS)
        df['timestamp'] = df['timestamp'] - df['timestamp'].min()
        df['timestamp'] = df['timestamp'] * TIME_CONVERSION_khz
        
        if yaxis in ['joules', 'instructions', 'cycles', 'ref_cycles', 'llc_miss', 'instructions_diff', 'cycles_diff',
                     'ref_cycles_diff', 'llc_miss_diff', 'joules_diff', 'c0_diff', 'c1_diff',
                     'c1e_diff', 'c3_diff', 'c6_diff', 'c7_diff', 'timestamp_diff']:
            df_non0j = df[(df['joules']>0) & (df['instructions'] > 0) & (df['cycles'] > 0) & (df['ref_cycles'] > 0) & (df['llc_miss'] > 0)]
            df_non0j['ref_cycles'] = df_non0j['ref_cycles'] * TIME_CONVERSION_khz
            df_non0j['joules'] = df_non0j['joules'] * JOULE_CONVERSION
            tmp = df_non0j[['instructions', 'cycles', 'ref_cycles', 'llc_miss', 'joules', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7','timestamp']].diff()
            tmp.columns = [f'{c}_diff' for c in tmp.columns]
            tmp['idle_diff'] = tmp['ref_cycles_diff'] / tmp['timestamp_diff']
            df_non0j = pd.concat([df_non0j, tmp], axis=1)
            df_non0j.dropna(inplace=True)
            df_non0j = df_non0j[df_non0j['joules_diff'] > 0]
            fig1.add_trace(go.Scatter(x=df_non0j['timestamp'], y=df_non0j[yaxis], mode='markers'))
        else:
            fig1.add_trace(go.Scatter(x=df['timestamp'], y=df[yaxis], mode='markers'))

        return fig1
    
        '''

        
        for core in range(0, 16):            
        df = pd.DataFrame()
            fname=f"/home/handong/flink/11_3_2023_5.15.89_itrlog/query1_cores16_frate400000_600000_fbuff-1_itr{itr}_{policy}dvfs{rdvfs_dict[dvfs]}_source16_mapper16_sink16_repeat{itera}/ITRlogs/linux.flink.dmesg._{core}_{itera}"
            df = pd.read_csv(fname, sep=' ', names=LINUX_COLS)
            df_non0j = df[(df['joules']>0) & (df['instructions'] > 0) & (df['cycles'] > 0) & (df['ref_cycles'] > 0) & (df['llc_miss'] > 0)]
            df_non0j['timestamp'] = df_non0j['timestamp'] - df_non0j['timestamp'].min()
            df_non0j['timestamp'] = df_non0j['timestamp'] * TIME_CONVERSION_khz
            
            df_non0j = df_non0j[(df_non0j['timestamp'] > 300) & (df_non0j['timestamp'] < 600)]
            
            

        
        '''
        
