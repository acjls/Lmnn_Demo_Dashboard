import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_mantine_components as dmc

from datetime import datetime as dt
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import pytz
import random

from sidebar import get_sidebar
from heute import *
from gestern import *
from woche import *


stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
    "styles.css"
]

# Initialize Dash app
dash._dash_renderer._set_react_version('18.2.0')
app = dash.Dash(__name__, external_stylesheets=stylesheets)
app.title = 'Demo Dashboard | LUMENION'
app._favicon = "favico.ico"
server = app.server


# Interval
interval = dcc.Interval(
        id='interval-component',
        interval=2000,  # in milliseconds
        n_intervals=0
    )
interval2 = dcc.Interval(
        id='interval-component2',
        interval=10000,  # in milliseconds
        n_intervals=0
    )


# sidebar
sidebar = get_sidebar()


# grid
grid_style = {
    "border": f"1px solid rgba(51, 51, 51, 0.5)",
    "textAlign": "center",
    "padding-left": "2rem",
    "padding-right": "2rem"
}
grid_style2 = {
    "border": f"1px solid rgba(51, 51, 51, 0.5)",
    "textAlign": "center",
    "padding-left": "2rem",
    "padding-right": "2rem",
    "padding-top": "2rem",
    "padding-bottom": "2rem",
}


############ heute ##############

current_power_card = get_current_power_card()
current_soc_card = get_current_soc_card()
current_power_steam_card = get_current_power_steam_card()


grid_kpi = dmc.Grid(
        children=[
            dmc.GridCol(current_power_card, style={   "padding-left": "8rem",
                                                    "padding-right": "0rem",
                                                    "padding-top": "2rem",
                                                    "padding-bottom": "2rem",
                                                     }, span=3),
            dmc.GridCol(current_soc_card, style={   "padding-left": "16rem",
                                                    "padding-right": "0rem",
                                                    "padding-top": "2rem",
                                                    "padding-bottom": "2rem",
                                                     }, span=6),
            dmc.GridCol(current_power_steam_card, style={   "padding-left": "8rem",
                                                    "padding-right": "0rem",
                                                    "padding-top": "2rem",
                                                    "padding-bottom": "2rem",
                                                     }, span=3),
        ],
        style={"padding": "0rem 0rem 0rem 16rem"}
        )


grid_plot = dmc.Grid(
        children=[
            dmc.GridCol(dcc.Graph(id='live-update-graph-bar'), style=grid_style, span=3),
            dmc.GridCol(dcc.Graph(id='live-update-graph-soc'), style=grid_style, span=6),
            dmc.GridCol(dcc.Graph(id='live-update-graph-bar_steam'), style=grid_style, span=3),
        ],
        gutter="xl",
        style={"padding": "0rem 0rem 0rem 16rem"}
        )


# bar plot leistung
@app.callback(
    Output('live-update-graph-bar', 'figure'),
    Output("current-power", "children"),
    [Input('interval-component', 'n_intervals')]
)
def update_power(n_intervals):
    bar_fig, current_power_text = update_power_heute(n_intervals)
    return bar_fig, current_power_text

# plot soc
@app.callback(
    Output('live-update-graph-soc', 'figure'),
    Output("current-soc", "children"),
    [Input('interval-component', 'n_intervals')]
)
def update_soc(n_intervals):
    soc_fig, current_soc_text = update_soc_heute(n_intervals)
    return soc_fig, current_soc_text

# bar plot leistung steam
@app.callback(
    Output('live-update-graph-bar_steam', 'figure'),
    Output("current-power_steam", "children"),
    [Input('interval-component2', 'n_intervals')]
)
def update_steam_power(n_intervals):
    bar_fig, current_power_steam_text = update_steam_power_heute(n_intervals)
    return bar_fig, current_power_steam_text



############ gestern ############

min_soc_gestern_card = get_min_soc_gestern_card()
max_soc_gestern_card = get_max_soc_gestern_card()

grid_kpi_gestern = dmc.Grid(
        children=[
            dmc.GridCol(min_soc_gestern_card, style={   "padding-left": "16rem",
                                                    "padding-right": "0rem",
                                                    "padding-top": "2rem",
                                                    "padding-bottom": "2rem",
                                                     }, span=6),
            dmc.GridCol(max_soc_gestern_card, style={   "padding-left": "16rem",
                                                    "padding-right": "0rem",
                                                    "padding-top": "2rem",
                                                    "padding-bottom": "2rem",
                                                     }, span=6),
        ],
        style={"padding": "0rem 0rem 0rem 16rem"}
        )

@app.callback(
    Output('gestern-graph-soc', 'figure'),
    Output('soc-min', 'children'),
    Output('soc-max', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def get_soc(n_intervals):
    soc_gestern_fig, min_soc_text, max_soc_text = get_soc_gestern()
    return soc_gestern_fig, min_soc_text, max_soc_text

grid_plot_gestern = dmc.Grid(
        children=[
            dmc.GridCol(dcc.Graph(id='gestern-graph-soc'), style=grid_style, span=12),
        ],
        gutter="xl",
        style={"padding": "0rem 0rem 0rem 16em"}
        )


############ Woche ############

min_soc_woche_card = get_min_soc_woche_card()
max_soc_woche_card = get_max_soc_woche_card()

grid_kpi_woche = dmc.Grid(
        children=[
            dmc.GridCol(min_soc_woche_card, style={   "padding-left": "16rem",
                                                    "padding-right": "0rem",
                                                    "padding-top": "2rem",
                                                    "padding-bottom": "2rem",
                                                     }, span=6),
            dmc.GridCol(max_soc_woche_card, style={   "padding-left": "16rem",
                                                    "padding-right": "0rem",
                                                    "padding-top": "2rem",
                                                    "padding-bottom": "2rem",
                                                     }, span=6),
        ],
        style={"padding": "0rem 0rem 0rem 16rem"}
        )

@app.callback(
    Output('woche-graph-soc', 'figure'),
    Output('soc-min-woche', 'children'),
    Output('soc-max-woche', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def get_socw(n_intervals):
    soc_woche_fig, min_soc_text, max_soc_text = get_soc_woche()
    return soc_woche_fig, min_soc_text, max_soc_text

grid_plot_woche = dmc.Grid(
        children=[
            dmc.GridCol(dcc.Graph(id='woche-graph-soc'), style=grid_style, span=12),
        ],
        gutter="xl",
        style={"padding": "0rem 0rem 0rem 16em"}
        )



# Define a callback to update the layout based on the selected URL
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page_content(pathname):
    if pathname in ["/", ""]:
        return [dmc.BackgroundImage(src="assets/background_black_red_wide.png", children=([grid_kpi])), grid_plot]
    elif pathname == "/Gestern":
        return [dmc.BackgroundImage(src="assets/background_black_red_wide.png", children=([grid_kpi_gestern])), grid_plot_gestern]
    elif pathname == "/Woche":
        return [dmc.BackgroundImage(src="assets/background_black_red_wide.png", children=([grid_kpi_woche])), grid_plot_woche]
    elif pathname == "/Gesamt":
        return [grid_kpi]
    elif pathname == "/Einstellungen":
        return
    elif pathname == "/Hilfe":
        return
    else:
        return html.Div("404 Page Not Found")



# Set app layout
app.layout = dmc.MantineProvider(
     forceColorScheme="light",
     theme={
         "primaryColor": "indigo",
         "fontFamily": "'Inter', sans-serif",
         "components": {
             "Button": {"defaultProps": {"fw": 400}},
             "Alert": {"styles": {"title": {"fontWeight": 500}}},
             "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
             "Badge": {"styles": {"root": {"fontWeight": 500}}},
             "Progress": {"styles": {"label": {"fontWeight": 500}}},
             "RingProgress": {"styles": {"label": {"fontWeight": 500}}},
             "CodeHighlightTabs": {"styles": {"file": {"padding": 12}}},
             "Table": {
                 "defaultProps": {
                     "highlightOnHover": True,
                     "withTableBorder": True,
                     "verticalSpacing": "sm",
                     "horizontalSpacing": "md",
                 }
             },
         },
     },
     children=[
         dcc.Location(id='url', refresh=False),
         sidebar,
         html.Div(id="page-content"),
         interval,
         interval2,
     ],
 )


# callbacks
@app.callback(Output("link_heute", "active"),
              Output("link_gestern", "active"),
              Output("link_woche", "active"),
              Output("link_gesamt", "active"),
              Output("link_einstellungen", "active"),
              Output("link_hilfe", "active"),
              [Input("url", "pathname")])
def render_page_content1(pathname):
    if (pathname=="/") or (pathname==""):
        return True, False, False, False, False, False
    if pathname=="/Gestern":
        return False, True, False, False, False, False
    if pathname=="/Woche":
        return False, False, True, False, False, False
    if pathname=="/Gesamt":
        return False, False, False, True, False, False
    if pathname=="/Einstellungen":
        return False, False, False, False, True, False
    if pathname=="/Hilfe":
        return False, False, False, False, False, True
    else:
        return False, False, False, False, False, False



# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
