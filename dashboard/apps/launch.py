import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import time
import subprocess
from datetime import datetime
import os

script_path = "/mnt/eestreaming/scripts/"

query_input = dbc.Row(
    [
        dbc.Label(html.H5("Query"), width=6),
        dbc.Col(
            dcc.Dropdown(id="query-selector", options=["1","3","5","8"], value="1", style={"width": "185px"}),
            width=6,
        ),
    ],
    className="mb-3",
)

rate_input = dbc.Row(
    [
        dbc.Label(html.H5("Rate (qps)"), width=6),
        dbc.Col(
            dcc.Input(id="rate-list", type="text", value="1000"),
            width=6,
        ),
    ],
    className="mb-3",
)

duration_input = dbc.Row(
    [
        dbc.Label(html.H5("Duration (s)"), width=6),
        dbc.Col(
            dcc.Input(id="duration-list", type="text", value="120"),
            width=6,
        ),
    ],
    className="mb-3",
)

def process_bar_by_time(t):
    n = int(t)*1000
    n += 50000
    n = n//100
    progress = html.Div(
        [
            dcc.Interval(id="progress-interval", n_intervals=0, interval=n),
            dbc.Progress(id="progress",  color="info", animated=False, striped=True, style={"height": "20px"}),
        ], style={"margin": "auto"})
    return progress

layout = html.Div([
    html.Br(),
    html.Br(),
    html.H3('Experiment Control Panel', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Div([
        query_input,
        rate_input,
        duration_input,
    ], style={'margin-left': '20%', 'margin-right': '20%'}),
    html.Div([
        dbc.Button("Submit", id="submit-button", color="primary",  style={'margin': 'auto'})
    ], style={'display': 'flex', 'margin': '20px'}),
    html.Br(),
    html.Div(id='if-running', style={'margin': 'auto', 'textAlign': 'center', 'width': '70%'}),
    html.Br(),
    html.Br(),
    html.Div(id='experiment-summary', style={'margin': '10px', 'textAlign': 'center', 'alignItems': 'center'}),
    html.Br(),
],style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '60%'})

@app.callback(
    Output('experiment-summary', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('query-selector', 'value'),
    State('rate-list', 'value'),    
    State('duration-list', 'value')]
)
def run_experiment(n_clicks, query, rate, duration):
    if n_clicks is None:
        return []
    else:
        #subprocess.call(["sh", "run-example.sh", "-q", query, "-r", rate_list], cwd="/mnt/eestreaming/scripts/")
        if os.path.exists(script_path):
            duration += "000"
            rate_list = rate + "_" + duration
            results = subprocess.check_output(
                    ["sh", "run-example.sh", "-q", query, "-r", rate_list], 
                    cwd=script_path, 
                    universal_newlines=True
                )
            print(results)
        else:
            time.sleep(int(duration))
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S %p")
        return (
                html.Hr(), 
                html.H3("Experiment Finished at " + current_time),
                html.H5(["Query: " + query], style={'textAlign': 'center', 'margin': '10px'}),
                html.H5(["Rate: " + rate + " qps"], style={'textAlign': 'center', 'margin': '10px'}),
                html.H5(["Duration: " + duration + " s"], style={'textAlign': 'center', 'margin': '10px'}),
                dbc.Button(
                    dbc.NavLink("view results", 
                    href="/apps/results", 
                    style={'color':'white'}), 
                    id="view-results-button", 
                    color="primary",  
                    style={'margin': '10px'})
        )
            



@app.callback(
    [Output('if-running', 'children'),Output('submit-button', 'disabled')],
    [Input('submit-button', 'n_clicks')],
    [State('duration-list', 'value')]
)
def update_if_running(n_clicks, duration):
    if n_clicks is None:
        return [], False
    else:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S %p")
        return [
            html.Hr(),
            html.H3("Experiment is Running"),
            html.H5("Started at " + current_time),
            process_bar_by_time(duration)], True
        



@app.callback(
    [Output("progress", "value"), Output("progress", "label"), Output("progress-interval", "disabled")],
    [Input("progress-interval", "n_intervals")],
)
def update_progress(n):
    # check progress of some background process, in this example we'll just
    # use n_intervals constrained to be in 0-100
    
    if n >= 100:
        return 100, "100%", True
    # only add text after 5% progress to ensure text isn't squashed too much
    n = n+1
    return n, f"{n} %" if n >= 5 else "", False
