from importlib.resources import path
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
import pandas as pd

from app import app
from apps import homepage, flink_viz

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [   
        html.Div([
            html.H5([
                dbc.NavLink("ItrLOG", href="/", style={'text-decoration': 'none', 'color': 'black'}),
            ], className="display-4"),
        ]),
        html.Hr(),
        html.P("An visualization tool for flink energy efficient streaming experiment", className="lead"),
        dbc.Nav(
            [
                dbc.AccordionItem(
                    [
                        dbc.NavLink("viz", href="/apps/flink_viz", active="exact")
                    ], title="Query 1"
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    print(pathname)
    if pathname == "/":
        return homepage.layout
    elif pathname == '/apps/flink_viz':
        return flink_viz.layout
    
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(port=8888, debug=True, host='10.241.31.71')
