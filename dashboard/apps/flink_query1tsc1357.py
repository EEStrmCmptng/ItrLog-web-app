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

uname='query1tsc1357'
loc='/home/handong/flink/query1tsc1357'
workload_loc='/home/handong/flink/query1tsc1357/combined.csv'

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

def genfigtype(i):
    return html.Div([
        dcc.Dropdown(id=f'figtype{uname}-xselector-{i}', value='SourcenumRecordsOutPerSecond_avg', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id=f'figtype{uname}-yselector-{i}', value='joules', style={'width':'60%'}, options=axis_values),        
        dcc.Graph(
            id=f'figtype{uname}-scatter-{i}', style={'display': 'inline-block'}
        )
    ], style={'display': 'inline-block'})

def genintlogfig(i):
    if i == 1:
        return html.Div([
            dcc.Textarea(
                id=f'intlogfig{uname}-textarea-{i}',
                value=str(i-1),
                style={'width': '10%'},
            #disabled=True,
                readOnly=True,
                hidden='true'
            ),
            html.P('RATE: ', style={'display': 'inline-block'}),
            dcc.Dropdown(id=f'intlogfig{uname}-rate-{i}',
                         value=80000,
                         style={'width':'60%'},
                         options=[80000, 100000, 120000, 200000, 300000, 400000]),
            html.P('ITERATION: ', style={'display': 'inline-block'}),
            dcc.Dropdown(id=f'intlogfig{uname}-itera-{i}',
                         value=1,
                         style={'width':'60%'},
                         options=[x for x in range(0, 10)]),
            html.P('NMAPPERS: ', style={'display': 'inline-block'}),
            dcc.Dropdown(id=f'intlogfig{uname}-nmappers-{i}',
                         value=4,
                         style={'width':'60%'},
                         options=[4, 8, 12, 16]),
            
            html.P('Y-AXIS: ', style={'display': 'inline-block'}),
            dcc.Dropdown(id=f'intlogfig{uname}-yaxis-{i}',
                         value='rx_bytes',
                         style={'width':'60%'},
                         options=taxis_values,
                         placeholder="Select y-axis value",),        
            dcc.Graph(
                id=f'intlogfig{uname}-{i}',
                style={'display': 'inline-block'}
            ),
        ], style={'display': 'inline-block'})
    else:
        return html.Div([
            dcc.Textarea(
                id=f'intlogfig{uname}-textarea-{i}',
                value=str(i-1),
                style={'width': '10%'},
            #disabled=True,
                readOnly=True,
                hidden='true'
            ), dcc.Graph(
                id=f'intlogfig{uname}-{i}',
                style={'display': 'inline-block'}
            ),
        ], style={'display': 'inline-block'})


layout = html.Div([
    dcc.Link('Home', href='/'),
    html.Br(),
        
    dbc.Row([        
        dbc.Col(children=[genfigtype(i) for i in range(1,3)])
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
        Output(f'figtype{uname}-scatter-{i}', 'figure'),
        [Input(f'figtype{uname}-xselector-{i}', 'value'),
         Input(f'figtype{uname}-yselector-{i}', 'value')]
    )
    def update_custom_scatter(xcol, ycol):
        fig = px.scatter(df_comb, 
                         x=xcol, 
                         y=ycol, 
                         color='rate',
                         hover_data=['i', 'nmappers', 'rate', 'policy'],
                         custom_data=['i', 'nmappers', 'rate', 'policy'],
                         title=f'X={xcol}\nY={ycol}')    
        return fig

@app.callback(
    [Output(f'intlogfig{uname}-1', 'figure'),
     Output(f'intlogfig{uname}-2', 'figure'),
     Output(f'intlogfig{uname}-3', 'figure'),
     Output(f'intlogfig{uname}-4', 'figure'),
     Output(f'intlogfig{uname}-5', 'figure'),
     Output(f'intlogfig{uname}-6', 'figure'),
     Output(f'intlogfig{uname}-7', 'figure'),
     Output(f'intlogfig{uname}-8', 'figure'),
     Output(f'intlogfig{uname}-9', 'figure'),
     Output(f'intlogfig{uname}-10', 'figure'),
     Output(f'intlogfig{uname}-11', 'figure'),
     Output(f'intlogfig{uname}-12', 'figure'),
     Output(f'intlogfig{uname}-13', 'figure'),
     Output(f'intlogfig{uname}-14', 'figure'),
     Output(f'intlogfig{uname}-15', 'figure'),
     Output(f'intlogfig{uname}-16', 'figure')],
    [Input(f'intlogfig{uname}-rate-1', 'value'),
     Input(f'intlogfig{uname}-itera-1', 'value'),
     Input(f'intlogfig{uname}-nmappers-1', 'value'),
     Input(f'intlogfig{uname}-yaxis-1', 'value'),
     Input(f'intlogfig{uname}-textarea-1', 'value')]
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
        fname=f"/home/handong/flink/query1tsc1357/query1tsc1357_cores16_frate{rate}_300000_fbuff-1_itr1_ondemanddvfs1_source16_mapper{nmappers}_sink16_repeat{itera}/ITRlogs/linux.flink.dmesg._{cc-1}_{itera}"
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

