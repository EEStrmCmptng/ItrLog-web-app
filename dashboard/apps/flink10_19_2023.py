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

loc='/home/handong/flink/10_19_2023_5.15.89_itrlog/'
workload_loc='/home/handong/flink/10_19_2023_5.15.89_itrlog/combined.csv'

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
        dcc.Dropdown(id='flink300K_10_19_2023-xaxis-selector-1', value='SourcenumRecordsOutPerSecond_avg', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id='flink300K_10_19_2023-yaxis-selector-1', value='joules', style={'width':'60%'}, options=axis_values),        
        dcc.Graph(
            id='flink300K_10_19_2023-custom-scatter-1', style={'display': 'inline-block'}
        )
    ], style={'display': 'inline-block'}),
        
    html.Div([
        dcc.Dropdown(id='flink300K_10_19_2023-xaxis-selector-2', value='SourcenumRecordsOutPerSecond_avg', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id='flink300K_10_19_2023-yaxis-selector-2', value='instructions', style={'width':'60%'}, options=axis_values),
        dcc.Graph(
            id='flink300K_10_19_2023-custom-scatter-2', style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(id='flink300K_10_19_2023-xaxis-selector-3', value='SourcenumRecordsOutPerSecond_avg', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id='flink300K_10_19_2023-yaxis-selector-3', value='ref_cycles', style={'width':'60%'}, options=axis_values),
        dcc.Graph(
            id='flink300K_10_19_2023-custom-scatter-3',
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(id='flink300K_10_19_2023-xaxis-selector-4', value='rxBytes', style={'width':'60%'}, options=axis_values),
        dcc.Dropdown(id='flink300K_10_19_2023-yaxis-selector-4', value='rxBytesIntLog', style={'width':'60%'}, options=axis_values),
        dcc.Graph(
            id='flink300K_10_19_2023-custom-scatter-4',
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),

    ## per mapper/source/sink
    html.Div([
        html.Hr(),
        html.Br()
    ]),
    html.P('ITERATION: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-per-mappersourcesink-itera-1',
                     value=0,
                     style={'width':'60%'},
                     options=[x for x in range(0, 10)],
                     placeholder="Select a iteration number"),
    html.P('TYPE: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-per-mappersourcesink-typem-1',
                     value="Mapper",
                     style={'width':'60%'},
                     options=["Mapper", "Sink", "Source"],
                     placeholder="Select type [Mapper, Sink, Source]"),
    html.P('Y-AXIS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-per-mappersourcesink-yaxis-1',
                     value='numRecordsOutPerSecond',
                     style={'width':'60%'},
                     options=['numRecordsInPerSecond', 'numRecordsOutPerSecond', 'busyTimeMsPerSecond', 'backPressuredTimeMsPerSecond', 'idleTimeMsPerSecond', 'duration', 'read-bytes', 'write-bytes', 'read-records', 'write-records'],
                     placeholder="Select y-axis value",),
    html.P('POLICY: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-per-mappersourcesink-policy-1',
                     value="ondemand",
                     style={'width':'60%'},
                     options=["ondemand", "conservative","performance", "schedutil", "powersave", "userspace"]),
    html.P('ITR: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-per-mappersourcesink-itr-1',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 2, 100, 200, 400, 600]),
    html.P('DVFS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-per-mappersourcesink-dvfs-1',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6]),
    
    dcc.Graph(
        id='flink300K_10_19_2023-per-mappersourcesink-1',
        style={'display': 'inline-block'}
    ),
    

    ## itr log
    html.Div([
        html.Hr(),
        html.Br()
    ]),
    html.Div([
        html.P('Y-AXIS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-xaxis-selector-5',
                     value='timestamp_diff',
                     style={'width':'60%'},
                     options=taxis_values,
                     placeholder="Select y-axis value",),
        html.P('CORE: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-yaxis-selector-5',
                     value=0,
                     style={'width':'60%'},
                     options=[x for x in range(0, 16)],
                     placeholder="Select core"),
        
        html.P('ITERATION: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-zaxis-selector-5',
                     value=0,
                     style={'width':'60%'},
                     options=[x for x in range(0, 10)],
                     placeholder="Select a iteration number",),
        html.P('POLICY: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-aaxis-selector-5',
                     value="ondemand",
                     style={'width':'60%'},
                     options=["ondemand", "conservative","performance", "schedutil", "powersave", "userspace"]),
        html.P('ITR: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-baxis-selector-5',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 2, 100, 200, 400, 600]),
        html.P('DVFS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-caxis-selector-5',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6]),
        dcc.Graph(
            id='flink300K_10_19_2023-custom-scatter-5',
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),

    html.Div([
        html.P('Y-AXIS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-xaxis-selector-6',
                     value='timestamp_diff',
                     style={'width':'60%'},
                     options=taxis_values,
                     placeholder="Select y-axis value",),
        html.P('CORE: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-yaxis-selector-6',
                     value=0,
                     style={'width':'60%'},
                     options=[x for x in range(0, 16)],
                     placeholder="Select core"),
        
        html.P('ITERATION: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-zaxis-selector-6',
                     value=0,
                     style={'width':'60%'},
                     options=[x for x in range(0, 10)],
                     placeholder="Select a iteration number",),
        html.P('POLICY: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-aaxis-selector-6',
                     value="ondemand",
                     style={'width':'60%'},
                     options=["ondemand", "conservative","performance", "schedutil", "powersave", "userspace"]),
        html.P('ITR: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-baxis-selector-6',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 2, 100, 200, 400, 600]),
        html.P('DVFS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-caxis-selector-6',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6]),
        dcc.Graph(
            id='flink300K_10_19_2023-custom-scatter-6',
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),

    ## itr log aggregate
    html.Div([
        html.Hr(),
        html.Br()
    ]),

    html.Div([
        html.P('Y-AXIS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-intlogagg-yaxis-1',
                     value='timestamp_diff',
                     style={'width':'60%'},
                     options=taxis_values,
                     placeholder="Select y-axis value",),        
        html.P('ITERATION: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-intlogagg-itera-1',
                     value=0,
                     style={'width':'60%'},
                     options=[x for x in range(0, 10)],
                     placeholder="Select a iteration number",),
        html.P('POLICY: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-intlogagg-policy-1',
                     value="ondemand",
                     style={'width':'60%'},
                     options=["ondemand", "conservative","performance", "schedutil", "powersave", "userspace"]),
        html.P('ITR: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-intlogagg-itr-1',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 2, 100, 200, 400, 600]),
        html.P('DVFS: ', style={'display': 'inline-block'}),
        dcc.Dropdown(id='flink300K_10_19_2023-intlogagg-dvfs-1',
                     value=1,
                     style={'width':'60%'},
                     options=[1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6]),
        dcc.Graph(
            id='flink300K_10_19_2023-intlogagg-1',
            style={'display': 'inline-block'}
        ),
    ], style={'display': 'inline-block'}),


])

for i in range(1, 5):
    @app.callback(
        Output('flink300K_10_19_2023-custom-scatter-'+str(i), 'figure'),
        [Input('flink300K_10_19_2023-xaxis-selector-'+str(i), 'value'),
         Input('flink300K_10_19_2023-yaxis-selector-'+str(i), 'value')]
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

for i in range(1, 2):
    @app.callback(
        Output(f"flink300K_10_19_2023-per-mappersourcesink-{i}", 'figure'),
        [Input(f"flink300K_10_19_2023-per-mappersourcesink-itera-{i}", 'value'),
         Input(f"flink300K_10_19_2023-per-mappersourcesink-typem-{i}", 'value'),
         Input(f"flink300K_10_19_2023-per-mappersourcesink-yaxis-{i}", 'value'),
         Input(f"flink300K_10_19_2023-per-mappersourcesink-policy-{i}", 'value'),
         Input(f"flink300K_10_19_2023-per-mappersourcesink-itr-{i}", 'value'),
         Input(f"flink300K_10_19_2023-per-mappersourcesink-dvfs-{i}", 'value')]
    )
    def update_mappersourcesink(itera, typem, yaxis, policy, itr, dvfs):
        fig = go.Figure()
        fig.update_layout(yaxis_title=yaxis)
        
        if typem == "Mapper":
            for i in range(0, 16):
                kwlist={
                    'cnt':[],
                    'numRecordsInPerSecond':[],
                    'numRecordsOutPerSecond':[],
                    'busyTimeMsPerSecond':[],
                    'backPressuredTimeMsPerSecond':[],
                    'idleTimeMsPerSecond':[],
                    'duration':[],
                    'read-bytes':[],
                    'write-bytes':[],
                    'read-records':[],
                    'write-records':[]
                }
                
                ff = open(f"{loc}/query1_cores16_frate300000_600000_fbuff-1_itr{itr}_{policy}dvfs{rdvfs_dict[dvfs]}_repeat{itera}/Flinklogs/Operator_Mapper_{i}").readlines()
                for _ll, _lc in enumerate(ff):
                    for lc in _lc.split('; '):
                        for kw in kwlist.keys():
                            if(kw in lc):
                                ldict=eval(lc.replace('[','').replace(']',''))
                                kwlist[kw].append(float(ldict['value']))
                kwlist['cnt'] = [x for x in range(len(kwlist[yaxis]))]
                #print(len(kwlist['cnt']), len(kwlist[yaxis]))
                #df = pd.DataFrame(kwlist)
                fig = fig.add_trace(go.Scatter(x=kwlist['cnt'],
                                               y=kwlist[yaxis], name=f"Mapper_{i}"))
        
        elif typem == "Source":
            for i in range(0, 14):
                kwlist={
                    'cnt':[],
                    'numRecordsInPerSecond':[],
                    'numRecordsOutPerSecond':[],
                    'busyTimeMsPerSecond':[],
                    'backPressuredTimeMsPerSecond':[],
                    'idleTimeMsPerSecond':[],
                    'duration':[],
                    'read-bytes':[],
                    'write-bytes':[],
                    'read-records':[],
                    'write-records':[]
                }
                
                ff = open(f"{loc}/query1_cores16_frate300000_600000_fbuff-1_itr{itr}_{policy}dvfs{rdvfs_dict[dvfs]}_repeat{itera}/Flinklogs/Operator_Source: Bids Source_{i}").readlines()
                for _ll, _lc in enumerate(ff):
                    for lc in _lc.split('; '):
                        for kw in kwlist.keys():
                            if(kw in lc):
                                ldict=eval(lc.replace('[','').replace(']',''))
                                kwlist[kw].append(float(ldict['value']))
                kwlist['cnt'] = [x for x in range(len(kwlist[yaxis]))]
                
                #df = pd.DataFrame(kwlist)
                fig = fig.add_trace(go.Scatter(x=kwlist['cnt'],
                                               y=kwlist[yaxis], name=f"Source_{i}"))
                
        elif typem == "Sink":
            for i in range(0, 2):
                kwlist={
                    'cnt':[],
                    'numRecordsInPerSecond':[],
                    'numRecordsOutPerSecond':[],
                    'busyTimeMsPerSecond':[],
                    'backPressuredTimeMsPerSecond':[],
                    'idleTimeMsPerSecond':[],
                    'duration':[],
                    'read-bytes':[],
                    'write-bytes':[],
                    'read-records':[],
                    'write-records':[]
                }
                
                ff = open(f"{loc}/query1_cores16_frate300000_600000_fbuff-1_itr{itr}_{policy}dvfs{rdvfs_dict[dvfs]}_repeat{itera}/Flinklogs/Operator_Latency Sink_{i}").readlines()
                for _ll, _lc in enumerate(ff):
                    for lc in _lc.split('; '):
                        for kw in kwlist.keys():
                            if(kw in lc):
                                ldict=eval(lc.replace('[','').replace(']',''))
                                kwlist[kw].append(float(ldict['value']))
                kwlist['cnt'] = [x for x in range(len(kwlist[yaxis]))]
                #df = pd.DataFrame(kwlist)
                fig = fig.add_trace(go.Scatter(x=kwlist['cnt'],
                                               y=kwlist[yaxis], name=f"Sink_{i}"))
                
            
        
        return fig
        
for i in range(5, 7):
    @app.callback(
        Output('flink300K_10_19_2023-custom-scatter-'+str(i), 'figure'),
        [Input('flink300K_10_19_2023-xaxis-selector-'+str(i), 'value'),
         Input('flink300K_10_19_2023-yaxis-selector-'+str(i), 'value'),
         Input('flink300K_10_19_2023-zaxis-selector-'+str(i), 'value'),
         Input('flink300K_10_19_2023-aaxis-selector-'+str(i), 'value'),
         Input('flink300K_10_19_2023-baxis-selector-'+str(i), 'value'),
         Input('flink300K_10_19_2023-caxis-selector-'+str(i), 'value')]
    )
    def update_custom_scatter2(xcol, ycol, zcol, acol, bcol, ccol):
        df = pd.DataFrame()
        fname=f"/home/handong/flink/10_19_2023_5.15.89_itrlog/query1_cores16_frate300000_600000_fbuff-1_itr{bcol}_{acol}dvfs{rdvfs_dict[ccol]}_repeat{zcol}/ITRlogs/linux.flink.dmesg._{ycol}_{zcol}"
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

for i in range(1, 2):
    @app.callback(
        Output('flink300K_10_19_2023-intlogagg-'+str(i), 'figure'),
        [Input('flink300K_10_19_2023-intlogagg-yaxis-'+str(i), 'value'),
         Input('flink300K_10_19_2023-intlogagg-itera-'+str(i), 'value'),
         Input('flink300K_10_19_2023-intlogagg-policy-'+str(i), 'value'),
         Input('flink300K_10_19_2023-intlogagg-itr-'+str(i), 'value'),
         Input('flink300K_10_19_2023-intlogagg-dvfs-'+str(i), 'value')]
    )
    def update_intlogagg(yaxis, itera, policy, itr, dvfs):
        fig1 = go.Figure()
        fig1.update_layout(xaxis_title="i", yaxis_title=yaxis)
        
        for core in range(0, 16):            
            df = pd.DataFrame()
            fname=f"/home/handong/flink/10_19_2023_5.15.89_itrlog/query1_cores16_frate300000_600000_fbuff-1_itr{itr}_{policy}dvfs{rdvfs_dict[dvfs]}_repeat{itera}/ITRlogs/linux.flink.dmesg._{core}_{itera}"
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

            fig1.add_trace(go.Scatter(x=df_non0j['i'], y=df_non0j[yaxis], name=f"Core {core}"))
        return fig1
