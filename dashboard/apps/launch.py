import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import time

global running_state
running_state = False

query_input = dbc.Row(
    [
        dbc.Label(html.H5("Query"), width=6),
        dbc.Col(
            dcc.Dropdown(id="query-selector", options=["1","3","5","8"], value="1", style={"width": "89%"}),
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
    ], style={'margin-left': '200px', 'margin-right': '200px'}),
    html.Div([
        dbc.Button("Submit", id="submit-button", color="primary",  style={'margin': 'auto'})
    ], style={'display': 'flex', 'margin': '20px'}),
    html.Hr(),
    html.Div(id='if-running', style={'margin': '10px'}),
    html.Br(),
    html.Br(),
    dbc.Spinner(
        html.Div(id='if-done'),
        color="primary",
        spinner_style={"width": "3rem", "height": "3rem"},
    ),
    html.Div(id='experiment-summary'),
    html.Br(),
    html.Hr(),
],style={'margin-left': 'auto', 'margin-right': 'auto', 'width': '60%'})

@app.callback(
    [Output('if-done', 'children'),
    Output('experiment-summary', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('query-selector', 'value'),
    State('rate-list', 'value'),    
    State('duration-list', 'value')]
)
def run_experiment(n_clicks, query, rate, duration):
    if n_clicks is None:
        return None, None
    else:
        time.sleep(3)
        return html.Div([
            html.H3("Experiment Finished"),
            html.H5(["Query: " + query], style={'textAlign': 'center', 'margin': '10px'}),
            html.H5(["Rate: " + rate + " qps"], style={'textAlign': 'center', 'margin': '10px'}),
            html.H5(["Duration: " + duration + " s"], style={'textAlign': 'center', 'margin': '10px'}),
            dbc.Button(dbc.NavLink("view results", href="/apps/results", style={'color':'white'}), id="view-results-button", color="primary",  style={'margin': '10px'})
        ], style={'textAlign': 'center', 'align-items':'center'}), None


@app.callback(
    Output('if-running', 'children'),
    [Input('submit-button', 'n_clicks')],
)
def update_if_running(n_clicks):
    if n_clicks is None:
        return None
    else:
        return html.Div([
            html.H3("Experiment is Running"),
        ], style={'textAlign': 'center'})