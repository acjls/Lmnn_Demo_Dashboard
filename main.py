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
app.title = 'Lumenion Demo Dashboard'
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

current_power_card = dmc.Card(
    [
        #html.Div("Ladeleistung", style={"font-size": "18px", "color": "white", "text-align": "center", "margin-bottom": "10px"}),
        html.Div(id="current-power", style={"font-size": "32px", "color": "white", "text-align": "center"})
    ],
    style={"background-color": "#333", "width": "60%", "border": "1px solid white"}  # Set the background color to grey and add left margin
)

current_soc_card = dmc.Card(
    [
        #html.Div("Ladestand", style={"font-size": "18px", "color": "white", "text-align": "center", "margin-bottom": "10px"}),
        html.Div(id="current-soc", style={"font-size": "32px", "color": "white", "text-align": "center"})
    ],
    style={"background-color": "#333", "width": "50%", "border": "1px solid white"}  # Set the background color to grey and add left margin
)

current_power_steam_card = dmc.Card(
    [
        #html.Div("Dampfleistung", style={"font-size": "18px", "color": "white", "text-align": "center", "margin-bottom": "10px"}),
        html.Div(id="current-power_steam", style={"font-size": "32px", "color": "white", "text-align": "center"})
    ],
    style={"background-color": "#333", "width": "60%", "border": "1px solid white"}  # Set the background color to grey and add left margin
)

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
def update_graph_live(n_intervals):
    CAPACITY = 20000  # kWh

    # read excel
    df_soc = pd.read_excel("your_file.xlsx")
    df_soc["State_of_Charge"] = df_soc["State_of_Charge"].interpolate(method="quadratic")
    df_soc['State_of_Charge'] = df_soc['State_of_Charge'] * 100
    df_soc.loc[df_soc.State_of_Charge > 100, 'State_of_Charge'] = 100
    df_soc.loc[df_soc.State_of_Charge < 3, 'State_of_Charge'] = 3

    # calc current power
    current_minute = dt.now(pytz.timezone('Europe/Berlin')).hour * 60 + dt.now(pytz.timezone('Europe/Berlin')).minute
    power_cur = (df_soc.loc[current_minute, "State_of_Charge"] - df_soc.loc[current_minute-1, "State_of_Charge"])/100*CAPACITY*60
    power_cur = power_cur + np.random.randint(-50, 50)
    if power_cur < 0:
        power_cur = 0

    # Create a Plotly bar plot
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=[""], y=[power_cur], marker_color='rgba(212, 0, 0, 0.7)', width=0.5))

    bar_fig.update_layout(
        title=dict(
            text="Ladeleistung",
            x=0.5,  # Set x to 0.5 to center the title
            font=dict(
                size=28  # Set the font size
            )
        ),
        margin=dict(l=60, r=60, t=60, b=0),
        paper_bgcolor="white",
        height=400,  # Set the height of the bar plot
        yaxis=dict(range=[0, max(3000, power_cur*1.1)],
                   tickfont=dict(size=18)),  # Set y-axis range
        yaxis_title="Leistung [kW]",  # Set y-axis title
        plot_bgcolor='rgba(51, 51, 51, 0.15)'
    )
    bar_fig.update_yaxes(title_font=dict(size=16))

    current_power_text = f"{round(power_cur)} kW"

    return bar_fig, current_power_text


# bar plot leistung
@app.callback(
    Output('live-update-graph-soc', 'figure'),
    Output("current-soc", "children"),
    [Input('interval-component', 'n_intervals')]
)
def update_graph_live(n_intervals):
    CAPACITY = 20000  # kWh

    # read excel
    df_soc = pd.read_excel("your_file.xlsx")
    df_soc["State_of_Charge"] = df_soc["State_of_Charge"].interpolate(method="quadratic")
    df_soc['State_of_Charge'] = df_soc['State_of_Charge'] * 100
    df_soc.loc[df_soc.State_of_Charge > 100, 'State_of_Charge'] = 100
    df_soc.loc[df_soc.State_of_Charge < 3, 'State_of_Charge'] = 3

    current_minute = dt.now(pytz.timezone('Europe/Berlin')).hour * 60 + dt.now(pytz.timezone('Europe/Berlin')).minute
    time_data = df_soc['Time'][:current_minute]
    soc_data = df_soc['State_of_Charge'][:current_minute]

    # Create figure for time series plot
    soc_fig = go.Figure()
    soc_fig.add_trace(go.Scatter(x=time_data, y=soc_data, fill='tozeroy', mode='none', line=dict(color='rgba(0,100,0,0.5)', width=1), showlegend=False, fillgradient=dict(
        type='vertical',
        colorscale=['rgba(0, 0, 212, 0.5)', 'rgba(212, 0, 0, 0.7)',  'rgba(212, 0, 0, 0.7)', 'rgba(212, 0, 0, 0.7)']
    )))
    soc_fig.update_layout(
        title=dict(
            text="Ladestand des Lumenion Wärmespeichers",
            x=0.5,  # Set x to 0.5 to center the title
            font=dict(
                size=28  # Set the font size to 24
            )
        ),
        paper_bgcolor="white",
        xaxis=dict(
            title="Uhrzeit",
            tickmode="array",
            tickvals=np.arange(120, 1441, 120),  # Tick every hour
            ticktext=[str(dt(2022, 1, 1, hour // 60 % 24, hour % 60).strftime('%H:%M')) for hour in
                      np.arange(120, 1441, 120)],  # Format tick text as HH:MM
            range=[0, 1440],  # Set x-axis range from start to end of the day
            tickfont=dict(size=16)
        ),
        yaxis=dict(title="Ladestand (%)",
                   range=[0, 100],
                   ),
        margin=dict(l=60, r=60, t=60, b=50),
        plot_bgcolor='rgba(51, 51, 51, 0.15)'
    )
    soc_fig.update_yaxes(title_font=dict(size=16),
                         tickfont=dict(size=18))

    current_soc = df_soc.loc[current_minute, 'State_of_Charge']
    current_soc_text = f"{round(current_soc)} %"

    return soc_fig, current_soc_text


# bar plot leistung
@app.callback(
    Output('live-update-graph-bar_steam', 'figure'),
    Output("current-power_steam", "children"),
    [Input('interval-component2', 'n_intervals')]
)
def update_graph_live(n_intervals):
    power_cur = np.random.randint(35, 38)/10

    # Create a Plotly bar plot
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=[""], y=[power_cur], marker_color='rgba(212, 0, 0, 0.7)', width=0.5))

    bar_fig.update_layout(
        title=dict(
            text="Dampfleistung",
            x=0.5,  # Set x to 0.5 to center the title
            font=dict(
                size=28  # Set the font size
            )
        ),
        margin=dict(l=60, r=60, t=60, b=0),
        paper_bgcolor="white",
        height=400,  # Set the height of the bar plot
        yaxis=dict(range=[0, 5],
                   tickfont=dict(size=18)),  # Set y-axis range
        yaxis_title="Leistung [t/h]",  # Set y-axis title
        plot_bgcolor='rgba(51, 51, 51, 0.15)'
    )
    bar_fig.update_yaxes(title_font=dict(size=16))

    current_power_steam_text = f"{round(power_cur,1)} t/h"

    return bar_fig, current_power_steam_text



# Define different layouts for each URL
layout_home = html.Div("Home Page Content")
layout_gestern = html.Div("Gestern Page Content")
layout_woche = html.Div("Woche Page Content")
layout_gesamt = html.Div("Gesamt Page Content")
layout_einstellungen = html.Div("Einstellungen Page Content")
layout_hilfe = html.Div("Hilfe Page Content")

# Define a callback to update the layout based on the selected URL
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page_content(pathname):
    if pathname in ["/", ""]:
        return [dmc.BackgroundImage(
        src="assets/background_black_red_wide.png", children=([grid_kpi])), grid_plot]
    elif pathname == "/Gestern":
        return [grid_kpi]
    elif pathname == "/Woche":
        return [grid_kpi]
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
