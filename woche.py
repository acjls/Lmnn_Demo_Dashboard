from dash import Dash, dcc, html, Input, Output, callback
import dash_mantine_components as dmc

from datetime import datetime as dt
import pytz
import plotly.graph_objs as go
import numpy as np
import pandas as pd


############## cards ##############
def get_min_soc_woche_card():
    min_soc_woche_card = dmc.Card(
        [
            html.Div("Min. Ladestand", style={"font-size": "18px", "color": "#ffffff", "text-align": "center", "margin-bottom": "10px"}),
            html.Div(id="soc-min-woche", style={"font-size": "32px", "color": "#ffffff", "text-align": "center"})
        ],
        style={"background-color": "#333333", "width": "70%", "border": "2px solid #ffffff"},
        shadow="1px 1px 5px #b8b6b6",# Set the background color to grey and add left margin
    )
    return min_soc_woche_card


def get_max_soc_woche_card():
    max_soc_woche_card = dmc.Card(
        [
            html.Div("Max. Ladestand", style={"font-size": "18px", "color": "#ffffff", "text-align": "center", "margin-bottom": "10px"}),
            html.Div(id="soc-max-woche", style={"font-size": "32px", "color": "#ffffff", "text-align": "center"})
        ],
        style={"background-color": "#333333", "width": "70%", "border": "2px solid #ffffff"},
        shadow="1px 1px 5px #b8b6b6",# Set the background color to grey and add left margin
    )
    return max_soc_woche_card

############## plots ##############

# plot soc
def get_soc_woche():
    CAPACITY = 20000  # kWh

    # read excel
    df_soc = pd.read_excel("soc_woche.xlsx")
    df_soc["State_of_Charge"] = df_soc["State_of_Charge"].interpolate(method="quadratic")
    df_soc['State_of_Charge'] = df_soc['State_of_Charge'] * 100
    df_soc.loc[df_soc.State_of_Charge > 100, 'State_of_Charge'] = 100
    df_soc.loc[df_soc.State_of_Charge < 3, 'State_of_Charge'] = 3

    time_data = df_soc['Time'][:]
    soc_data = df_soc['State_of_Charge'][:]

    # Create figure for time series plot
    soc_fig = go.Figure()
    soc_fig.add_trace(go.Scatter(x=time_data, y=soc_data, fill='tozeroy', mode='none', line=dict(color='rgba(0,100,0,0.5)', width=1), showlegend=False, fillgradient=dict(
        type='vertical',
        colorscale=['rgba(0, 0, 192, 1)', 'rgba(192, 0, 0, 1)',  'rgba(192, 0, 0, 1)', 'rgba(192, 0, 0, 1)']
    )))
    soc_fig.update_layout(
        title=dict(
            text="Ladestand des Lumenion Wärmespeichers (Woche)",
            x=0.5,  # Set x to 0.5 to center the title
            font=dict(
                size=28  # Set the font size to 24
            )
        ),
        paper_bgcolor="white",
        xaxis=dict(
            title="Uhrzeit",
            tickmode="array",
            tickvals=np.arange(720, 10081, 720),  # Tick every hour
            ticktext=[str(dt(2022, 1, 1, hour // 60 % 24, hour % 60).strftime('%H:%M')) for hour in
                      np.arange(720, 10081, 720)],  # Format tick text as HH:MM
            range=[0, 10080],  # Set x-axis range from start to end of the day
            tickfont=dict(size=16)
        ),
        yaxis=dict(title="Ladestand (%)",
                   range=[0, 100],
                   gridcolor='rgba(51, 51, 51, 0.25)',  # Set y-axis range
                   ),
        margin=dict(l=60, r=60, t=60, b=50),
        plot_bgcolor='rgba(0, 0, 0, 0)'
    )
    soc_fig.update_yaxes(title_font=dict(size=16),
                         tickfont=dict(size=18))
    soc_fig.update_xaxes(showline=True, linewidth=3, linecolor='rgba(51, 51, 51, 0.15)')


    #
    min_soc = df_soc['State_of_Charge'].min()
    max_soc = df_soc['State_of_Charge'].max()

    min_soc_text = f"{round(min_soc)} %"
    max_soc_text = f"{round(max_soc)} %"

    return soc_fig, min_soc_text, max_soc_text
