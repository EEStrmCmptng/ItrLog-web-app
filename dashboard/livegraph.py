import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import random
import os
from os import path
from subprocess import Popen, PIPE, call

logs="/users/hand32/experiment-scripts/logs/query1_cores16_frate100000_6000000_fbuff-1_itr1_ondemanddvfs1_source16_mapper4_sink16_repeat0/"
flinklogs=f"{logs}/Flinklogs/"

nsources=16
# Initial x-axis value
xs = []
ys = []
xpower=[]
ypower=[]
lastfig={}

app = dash.Dash(__name__)

def runGetCmd(cmd):
    #print('------------------------------------------------------------')
    #print(cmd)
    res=os.popen(cmd).read()
    return res
    #print('------------------------------------------------------------')

victim='10.10.1.3'       # scp logs from victim to bootstrap

# Function to read data from file
def read_power():
    try:
        p = float(runGetCmd(f"ssh {victim} tail -1 /data/rapl_log.log"))
        return p
    except Exception as error:
        print(error)
        return 0.0    

'''
   if not path.exists(f"{logs}/server2_rapl.log"):
        return 0.0
    else:
        lastline=""
        f = open(f"{logs}/server2_rapl.log", "r")
        for line in f:
            lastline=line
        return float(lastline)
'''
    
def read_data_from_file():
    global flinklogs, nsources
    #kwlist={'numRecordsInPerSecond':[], 'numRecordsOutPerSecond':[], 'busyTimeMsPerSecond':[], 'backPressuredTimeMsPerSecond':[]}
    
    kwlist={'numRecordsOutPerSecond':[]}
    ret = []

    for i in range(0, nsources):    
        lastline=""
        if not path.exists(f"{flinklogs}/Operator_Source: Bids Source_{i}"):
            ret.append(0.0)
        else:
            f = open(f"{flinklogs}/Operator_Source: Bids Source_0", "r")
            for line in f:
                lastline=line
            for lc in lastline.split('; '):
                for kw in kwlist.keys():
                    if(kw in lc):
                        ldict=eval(lc.replace('[','').replace(']',''))
                        ret.append(float(ldict['value']))
    #print(len(ret))
    return ret

# Layout of the application
app.layout = html.Div([
    dcc.Graph(id='live-update-graph'),
    dcc.Graph(id='live-power'),
    
    dcc.Interval(
        id='interval-1',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    ),
    
    dcc.Interval(
        id='interval-2',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update the graph every second
@app.callback(
    Output('live-update-graph', 'figure'),
    #Output('live-power', 'figure'),
    [Input('interval-1', 'n_intervals')]
)
def update_graph(n):
    global nsources, xs, ys, xpower, ypower, lastfig
    #print(n)
    '''
    y = read_power()
    # Update x-axis
    xpower.append(xpower[-1] + 1)
    ypower.append(y)

    figpower = {
        'data': [{'x':xpower, 'y':ypower, 'type': 'line', 'name': "Power"}],
        'layout': {
            'yaxis': {'title': 'Power (J/sec)'}            
        }
    }

    if n % 10 == 0:
    '''
    # Read data from file
    ret = read_data_from_file()
    
    # Update x-axis
    xs.append(xs[-1] + 1)

    mdata = []
    # Update y-axis
    for i in range(nsources):
        ys[i].append(ret[i])
        mdata.append({'x':xs, 'y':ys[i], 'type': 'line', 'name': f"Source {i}"})
        
    fig = {
        'data': mdata,
        'layout': {
            'xaxis': {'title': 'Every 10 Second'},
            'yaxis': {'title': 'Source Records-Out-per-Second'}            
        }
    }
    return fig

#    lastfig=fig
#    return fig, figpower
#else:
#    return lastfig, figpower

# Callback to update the graph every second
@app.callback(
    Output('live-power', 'figure'),
    [Input('interval-2', 'n_intervals')]
)
def update_power(n):
    global xpower, ypower
    y = read_power()
    # Update x-axis
    xpower.append(xpower[-1] + 1)
    ypower.append(y)

    fig = {
        'data': [{'x':xpower, 'y':ypower, 'type': 'line', 'name': "Power"}],
        'layout': {
            'yaxis': {'title': 'Power (J/sec)'}            
        }
    }
    
    return fig
    
if __name__ == '__main__':
    xs.append(0)
    xpower.append(0)
    ypower.append(0)
    for i in range(nsources):
        ys.append([0])
    app.run_server(port=8888, debug=True, host='128.110.96.4')
