import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.Br(),
    html.Br(),
    html.H3(
        'Welcome to ItrLOG', style={'textAlign': 'center'}),
    html.Div(id='app-1-display-value'),
])

