from importlib.resources import path
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


from dash.dependencies import Input, Output
import pandas as pd

from app import app
from apps import *
from apps import homepage, flink200K, flink300K, flinktest, results, launch 

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
        html.P(
            "An visualization tool for flink energy efficient streaming experiment", className="lead"
        ),
        dbc.Nav(
            [  
                dbc.Accordion(
                    [   
                        #dbc.AccordionItem(
                        #    [
                        #        dbc.NavLink("Launch", href="/apps/launch", active="exact"),
                        #        dbc.NavLink("Results", href="/apps/results", active="exact"),
                        #    ], title="Launch Experiment", id="launch_link"
                        #),
                        dbc.AccordionItem(
                            [
                                dbc.NavLink("Flink200K", href="/apps/flink200K", active="exact"),
                                dbc.NavLink("Flink300K", href="/apps/flink300K", active="exact"),
                                dbc.NavLink("FlinkTest", href="/apps/flinktest", active="exact"),
                            ], title="Query 1", id="query1"
                        ),
                        dbc.AccordionItem(
                            "No yet Implemented", title="Query 3", id="query3"
                        ),
                        dbc.AccordionItem(
                            "No yet Implemented", title="Query 5", id="query5"
                        ),
                        dbc.AccordionItem(
                            "No yet Implemented", title="Query 8", id="query8"
                        ),
                    ],
                    start_collapsed=False,
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
    elif pathname == '/apps/flink200K':
        return flink200K.layout
    elif pathname == '/apps/flink300K':
        return flink300K.layout
    elif pathname == '/apps/flinktest':
        return flinktest.layout
    elif pathname == '/apps/results':
        return results.layout
    elif pathname == '/apps/launch':
        return launch.layout
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
