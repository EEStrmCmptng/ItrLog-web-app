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

itrlist = [1, 2, 50, 100, 200, 400, 600, 800]

loc='/home/handong/flink/11_16_2023_5.15.89_itrlog/'
workload_loc='/home/handong/flink/11_16_2023_5.15.89_itrlog/combined.csv'

TIME_CONVERSION_khz = 1./(2600000*1000)
JOULE_CONVERSION = 0.00001526

df_comb = pd.read_csv(workload_loc, sep=',')
#df_comb = df_comb[df_comb['rate'] == 100000].copy()
df_comb = df_comb[df_comb['i'] > 0]
df_comb = df_comb[df_comb['joules'] > 0]
df_comb = df_comb[df_comb['instructions'] > 0]
df_comb = df_comb[df_comb['ref_cycles'] > 0]
#df_comb = df_comb[df_comb['SourcenumRecordsOutPerSecond_avg'] > 90000]
axis_values = [{'label': key, 'value': key} for key in df_comb.columns]

LINUX_COLS = ['i', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions', 'cycles', 'ref_cycles', 'llc_miss', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7', 'joules', 'timestamp']

taxis_values=['i', 'rx_desc', 'rx_bytes', 'tx_desc', 'tx_bytes', 'instructions',
       'cycles', 'ref_cycles', 'llc_miss', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7',
       'joules', 'timestamp', 'instructions_diff', 'cycles_diff',
       'ref_cycles_diff', 'llc_miss_diff', 'joules_diff', 'c0_diff', 'c1_diff',
              'c1e_diff', 'c3_diff', 'c6_diff', 'c7_diff', 'timestamp_diff', 'idle_diff']

def genfigtype1(i):
    return html.Div([
        dcc.Dropdown(id=f'figtype1-xselector-{i}', value='SourcenumRecordsOutPerSecond_avg', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id=f'figtype1-yselector-{i}', value='joules', style={'width':'60%'}, options=axis_values),        
        dcc.Graph(
            id=f'figtype1-scatter-{i}', style={'display': 'inline-block'}
        )
    ], style={'display': 'inline-block'})
'''
def genintlogfig(i):
    return html.Div([
        dcc.Textarea(
            id='intlogfig-textarea-'+str(i),
            value=str(i-1),
            style={'width': '10%'},
            #disabled=True,
            readOnly=True,
            hidden='true'
        ),
        html.P('RATE: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id=f'intlogfig-rate-{i}',
                     value=100000,
                     style={'width':'60%'},
                     options=[100000, 200000, 300000, 400000]),
        html.P('ITERATION: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id=f'intlogfig-itera-{i}',
                     value=1,
                     style={'width':'60%'},
                     options=[x for x in range(0, 10)]),
        html.P('NMAPPERS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id=f'intlogfig-nmappers-{i}',
                     value=4,
                     style={'width':'60%'},
                     options=[4, 8, 12, 16]),
        
        html.P('Y-AXIS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='intlogfig-yaxis-'+str(i),
                     value='rx_bytes',
                     style={'width':'60%'},
                     options=taxis_values,
                     placeholder="Select y-axis value",),        
        dcc.Graph(
            id='intlogfig-'+str(i),
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'})
'''

def genintlogfig(i):
    if i == 1:
        return html.Div([
            dcc.Textarea(
                id='intlogfig-textarea-'+str(i),
                value=str(i-1),
                style={'width': '10%'},
            #disabled=True,
                readOnly=True,
                hidden='true'
            ),
            html.P('RATE: ', style={'display': 'inline-block'}),
            dcc.Dropdown(id=f'intlogfig-rate-{i}',
                         value=100000,
                         style={'width':'60%'},
                         options=[100000, 200000, 300000, 400000]),
            html.P('ITERATION: ', style={'display': 'inline-block'}),
            dcc.Dropdown(id=f'intlogfig-itera-{i}',
                         value=1,
                         style={'width':'60%'},
                         options=[x for x in range(0, 10)]),
            html.P('NMAPPERS: ', style={'display': 'inline-block'}),
            dcc.Dropdown(id=f'intlogfig-nmappers-{i}',
                         value=4,
                         style={'width':'60%'},
                         options=[4, 8, 12, 16]),
            
            html.P('Y-AXIS: ', style={'display': 'inline-block'}),
            dcc.Dropdown(id='intlogfig-yaxis-'+str(i),
                         value='rx_bytes',
                         style={'width':'60%'},
                         options=taxis_values,
                         placeholder="Select y-axis value",),        
            dcc.Graph(
                id='intlogfig-'+str(i),
                style={'display': 'inline-block'}
            ),
        ], style={'display': 'inline-block'})
    else:
        return html.Div([
            dcc.Textarea(
                id='intlogfig-textarea-'+str(i),
                value=str(i-1),
                style={'width': '10%'},
            #disabled=True,
                readOnly=True,
                hidden='true'
            ), dcc.Graph(
                id='intlogfig-'+str(i),
                style={'display': 'inline-block'}
            ),
        ], style={'display': 'inline-block'})


layout = html.Div([
    dcc.Link('Home', href='/'),
    html.Br(),
        
    dbc.Row([        
        dbc.Col(children=[genfigtype1(i) for i in range(1,3)])
    ]),
    
    ## itr log aggregate
    html.Div([
        html.Hr(),
        html.Br()
    ]),
    dbc.Row([        
        dbc.Col(children=[genintlogfig(i) for i in range(1,17)])
    ])
])

for i in range(1, 3):
    @app.callback(
        Output('figtype1-scatter-'+str(i), 'figure'),
        [Input('figtype1-xselector-'+str(i), 'value'),
         Input('figtype1-yselector-'+str(i), 'value')]
    )
    def update_custom_scatter(xcol, ycol):
        fig = px.scatter(df_comb, 
                         x=xcol, 
                         y=ycol, 
                         color='rate',
                         hover_data=['i', 'nmappers', 'rate'],
                         custom_data=['i', 'nmappers', 'rate'],
                         title=f'X={xcol}\nY={ycol}')    
        return fig
'''
for i in range(1, 3):
    @app.callback(
        Output(f'intlogfig-{i}', 'figure'),
        [Input(f'intlogfig-rate-{i}', 'value'),
         Input(f'intlogfig-itera-{i}', 'value'),
         Input(f'intlogfig-nmappers-{i}', 'value'),
         Input(f'intlogfig-yaxis-{i}', 'value'),
         Input(f'intlogfig-textarea-{i}', 'value')]
    )
    def update_intlogagg(rate, itera, nmappers, yaxis, core):
        fig1 = go.Figure(
            layout=go.Layout(
                title=go.layout.Title(text=f"Core {core}")
            )
        )
        
        fig1.update_layout(xaxis_title=f"timestamp", yaxis_title=yaxis,  font=dict(
            family="Courier New, monospace",
            size=18
        ))
            
        for cc in range(0, 16):         
            df = pd.DataFrame()
            fname=f"/home/handong/flink/11_16_2023_5.15.89_itrlog/query1_cores16_frate{rate}_300000_fbuff-1_itr1_ondemanddvfs1_source16_mapper{nmappers}_sink16_repeat{itera}/ITRlogs/linux.flink.dmesg._{cc}_{itera}"
            df = pd.read_csv(fname, sep=' ', names=LINUX_COLS)
            df_non0j = df[(df['joules']>0) & (df['instructions'] > 0) & (df['cycles'] > 0) & (df['ref_cycles'] > 0) & (df['llc_miss'] > 0)]
        
            df_non0j['timestamp'] = df_non0j['timestamp'] - df_non0j['timestamp'].min()
            df_non0j['timestamp'] = df_non0j['timestamp'] * TIME_CONVERSION_khz
            df_non0j['ref_cycles'] = df_non0j['ref_cycles'] * TIME_CONVERSION_khz
            df_non0j['joules'] = df_non0j['joules'] * JOULE_CONVERSION
            df_non0j = df_non0j[(df_non0j['timestamp'] > 120) & (df_non0j['timestamp'] < 300)]
            
            tmp = df_non0j[['instructions', 'cycles', 'ref_cycles', 'llc_miss', 'joules', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7','timestamp']].diff()
            tmp.columns = [f'{c}_diff' for c in tmp.columns]
            tmp['idle_diff'] = tmp['ref_cycles_diff'] / tmp['timestamp_diff']
            df_non0j = pd.concat([df_non0j, tmp], axis=1)
            df_non0j.dropna(inplace=True)
            df_non0j = df_non0j[df_non0j['joules_diff'] > 0]
            fig1.add_trace(go.Scatter(x=df_non0j['timestamp'], y=df_non0j[yaxis], fill='tozeroy',
                                      mode='none'))
            #fig1.update_layout(
            #    autosize=False,
            #    width=320,
            #    height=320,
            #)
            #figs.append(fig1)
        return fig1
    '''


@app.callback(
    [Output('intlogfig-1', 'figure'),
     Output('intlogfig-2', 'figure'),
     Output('intlogfig-3', 'figure'),
     Output('intlogfig-4', 'figure'),
     Output('intlogfig-5', 'figure'),
     Output('intlogfig-6', 'figure'),
     Output('intlogfig-7', 'figure'),
     Output('intlogfig-8', 'figure'),
     Output('intlogfig-9', 'figure'),
     Output('intlogfig-10', 'figure'),
     Output('intlogfig-11', 'figure'),
     Output('intlogfig-12', 'figure'),
     Output('intlogfig-13', 'figure'),
     Output('intlogfig-14', 'figure'),
     Output('intlogfig-15', 'figure'),
     Output('intlogfig-16', 'figure')],
    [Input('intlogfig-rate-1', 'value'),
     Input('intlogfig-itera-1', 'value'),
     Input('intlogfig-nmappers-1', 'value'),
     Input('intlogfig-yaxis-1', 'value'),
     Input('intlogfig-textarea-1', 'value')]
)
def update_intlogagg(rate, itera, nmappers, yaxis, core):
    figs = []
    for cc in range(1, 17):
        fig1 = go.Figure(
            layout=go.Layout(
                title=go.layout.Title(text=f"Core {cc-1}")
            )
        )
        
        fig1.update_layout(xaxis_title=f"timestamp", yaxis_title=yaxis,  font=dict(
            family="Courier New, monospace",
            size=18
        ))
        
        #print(ii)
        df = pd.DataFrame()
        #fname=f"/users/hand32/netpipe_intlog/linux.intlog.{ii}"
        fname=f"/home/handong/flink/11_16_2023_5.15.89_itrlog/query1_cores16_frate{rate}_300000_fbuff-1_itr1_ondemanddvfs1_source16_mapper{nmappers}_sink16_repeat{itera}/ITRlogs/linux.flink.dmesg._{cc-1}_{itera}"
        df = pd.read_csv(fname, sep=' ', names=LINUX_COLS)
        df_non0j = df[(df['joules']>0) & (df['instructions'] > 0) & (df['cycles'] > 0) & (df['ref_cycles'] > 0) & (df['llc_miss'] > 0)]
        
        df_non0j['timestamp'] = df_non0j['timestamp'] - df_non0j['timestamp'].min()
        df_non0j['timestamp'] = df_non0j['timestamp'] * TIME_CONVERSION_khz
        df_non0j['ref_cycles'] = df_non0j['ref_cycles'] * TIME_CONVERSION_khz
        df_non0j['joules'] = df_non0j['joules'] * JOULE_CONVERSION
        df_non0j = df_non0j[(df_non0j['timestamp'] > 120) & (df_non0j['timestamp'] < 300)]
        
        tmp = df_non0j[['instructions', 'cycles', 'ref_cycles', 'llc_miss', 'joules', 'c0', 'c1', 'c1e', 'c3', 'c6', 'c7','timestamp']].diff()
        tmp.columns = [f'{c}_diff' for c in tmp.columns]
        tmp['idle_diff'] = tmp['ref_cycles_diff'] / tmp['timestamp_diff']
        df_non0j = pd.concat([df_non0j, tmp], axis=1)
        df_non0j.dropna(inplace=True)
        df_non0j = df_non0j[df_non0j['joules_diff'] > 0]
        fig1.add_trace(go.Scatter(x=df_non0j['timestamp'], y=df_non0j[yaxis], mode='markers',  marker={'sizemin':1}))
        fig1.update_layout(
            autosize=False,
            width=320,
            height=320,
        )
        figs.append(fig1)
    return figs
