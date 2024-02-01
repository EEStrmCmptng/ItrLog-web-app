from importlib.resources import path
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


from dash.dependencies import Input, Output
import pandas as pd

from app import app
from apps import *
from apps import homepage, flink11_3_2023_100K, flink11_3_2023_300K, flink11_3_2023_200K, flink11_3_2023_400K, flink11_16_2023, flink11_28_2023, flink_query1tscnopin, flink_query1tsc1357, flink_query1tsc2468, results, launch 

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
                                #dbc.NavLink("Flink200K10_12_2023", href="/apps/flink10_12_2023_200K", active="exact"),
                                #dbc.NavLink("Flink300K_10_12_2023", href="/apps/flink10_12_2023", active="exact"),
                                #dbc.NavLink("Flink300K_10_19_2023", href="/apps/flink10_19_2023", active="exact"),
                                #dbc.NavLink("Flink_10_24_2023", href="/apps/flink10_24_2023", active="exact"),
                                dbc.NavLink("Flink_11_3_2023_100K", href="/apps/flink11_3_2023_100K", active="exact"),
                                dbc.NavLink("Flink_11_3_2023_200K", href="/apps/flink11_3_2023_200K", active="exact"),
                                dbc.NavLink("Flink_11_3_2023_300K", href="/apps/flink11_3_2023_300K", active="exact"),
                                dbc.NavLink("Flink_11_3_2023_400K", href="/apps/flink11_3_2023_400K", active="exact"),
                                dbc.NavLink("Flink_11_16_2023", href="/apps/flink11_16_2023", active="exact"),
                                dbc.NavLink("Flink_11_28_2023", href="/apps/flink11_28_2023", active="exact"), 
                                dbc.NavLink("Flink_query1tscnopin", href="/apps/flink_query1tscnopin", active="exact"),
                                dbc.NavLink("Flink_query1tsc1357", href="/apps/flink_query1tsc1357", active="exact"),
                                dbc.NavLink("Flink_query1tsc2468", href="/apps/flink_query1tsc2468", active="exact"),
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
    #elif pathname == '/apps/flink10_12_2023_200K':
    #    return flink10_12_2023_200K.layout
    #elif pathname == '/apps/flink10_12_2023':
    #    return flink10_12_2023.layout    
    #elif pathname == '/apps/flink10_19_2023':
    #    return flink10_19_2023.layout
    #elif pathname == '/apps/flink10_24_2023':
    #    return flink10_24_2023.layout
    elif pathname == '/apps/flink11_3_2023_100K':
        return flink11_3_2023_100K.layout
    elif pathname == '/apps/flink11_3_2023_200K':
        return flink11_3_2023_200K.layout
    elif pathname == '/apps/flink11_3_2023_300K':
        return flink11_3_2023_300K.layout
    elif pathname == '/apps/flink11_3_2023_400K':
        return flink11_3_2023_400K.layout
    elif pathname == '/apps/flink11_16_2023':
        return flink11_16_2023.layout
    elif pathname == '/apps/flink11_28_2023':
        return flink11_28_2023.layout
    elif pathname == '/apps/flink_query1tscnopin':
        return flink_query1tscnopin.layout
    elif pathname == '/apps/flink_query1tsc1357':
        return flink_query1tsc1357.layout
    elif pathname == '/apps/flink_query1tsc2468':
        return flink_query1tsc2468.layout
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
