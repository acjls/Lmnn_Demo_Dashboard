from dash import Dash, dcc, html, Input, Output, callback
import dash_mantine_components as dmc

from datetime import datetime as dt
import pytz
import plotly.graph_objs as go
import numpy as np
import pandas as pd


############## cards ##############
def get_current_power_card():
    current_power_card = dmc.Card(
        [
            #html.Div("Ladeleistung", style={"font-size": "18px", "color": "white", "text-align": "center", "margin-bottom": "10px"}),
            html.Div(id="current-power", style={"font-size": "32px", "color": "#ffffff", "text-align": "center"})
        ],
        style={"background-color": "#333333", "width": "70%", "border": "2px solid #ffffff"},
        shadow="1px 1px 5px #b8b6b6",# Set the background color to grey and add left margin
    )
    return current_power_card


def get_current_soc_card():
    current_soc_card = dmc.Card(
        [
            # html.Div("Ladestand", style={"font-size": "18px", "color": "white", "text-align": "center", "margin-bottom": "10px"}),
            html.Div(id="current-soc", style={"font-size": "32px", "color": "#ffffff", "text-align": "center"})
        ],
        style={"background-color": "#333333", "width": "70%", "border": "2px solid #ffffff"},
        shadow="1px 1px 5px #b8b6b6",# Set the background color to grey and add left margin
    )
    return current_soc_card


def get_current_power_steam_card():
    current_power_steam_card = dmc.Card(
        [
            # html.Div("Dampfleistung", style={"font-size": "18px", "color": "white", "text-align": "center", "margin-bottom": "10px"}),
            html.Div(id="current-power_steam", style={"font-size": "32px", "color": "#ffffff", "text-align": "center"})
        ],
        style={"background-color": "#333333", "width": "70%", "border": "2px solid #ffffff"},
        shadow="1px 1px 5px #b8b6b6",# Set the background color to grey and add left margin
    )
    return current_power_steam_card



############## plots ################

# bar plot power
def update_power_heute(n_intervals):
    CAPACITY = 20000  # kWh

    # read excel
    df_soc = pd.read_excel("soc_heute.xlsx")
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
    bar_fig.add_trace(go.Bar(x=[""], y=[power_cur], marker_color='rgba(192, 0, 0, 1)', width=0.5))

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
        height=550,  # Set the height of the bar plot
        yaxis=dict(range=[0, max(3000, power_cur*1.1)],
                   tickfont=dict(size=18),
                   gridcolor='rgba(51, 51, 51, 0.25)'),  # Set y-axis range
        yaxis_title="Leistung [kW]",  # Set y-axis title
        plot_bgcolor='rgba(0, 0, 0, 0)'
    )
    bar_fig.update_yaxes(title_font=dict(size=16))
    bar_fig.update_xaxes(showline=True, linewidth=3, linecolor='rgba(51, 51, 51, 0.15)')

    current_power_text = f"{round(power_cur)} kW"

    return bar_fig, current_power_text


# plot soc
def update_soc_heute(n_intervals):
    CAPACITY = 20000  # kWh

    # read excel
    df_soc = pd.read_excel("soc_heute.xlsx")
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
        colorscale=['rgba(0, 0, 192, 1)', 'rgba(192, 0, 0, 1)',  'rgba(192, 0, 0, 1)', 'rgba(192, 0, 0, 1)']
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
        height=595,
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
                   gridcolor='rgba(51, 51, 51, 0.25)',  # Set y-axis range
                   ),
        margin=dict(l=60, r=60, t=60, b=50),
        plot_bgcolor='rgba(0, 0, 0, 0)'
    )
    soc_fig.update_yaxes(title_font=dict(size=16),
                         tickfont=dict(size=18))
    soc_fig.update_xaxes(showline=True, linewidth=3, linecolor='rgba(51, 51, 51, 0.15)')

    current_soc = df_soc.loc[current_minute, 'State_of_Charge']
    current_soc_text = f"{round(current_soc)} %"

    return soc_fig, current_soc_text


# bar plot steam power
def update_steam_power_heute(n_intervals):
    power_cur = np.random.randint(35, 38)/10

    # Create a Plotly bar plot
    a = go.Bar(x=[""], y=[power_cur], marker_color='rgba(192, 0, 0, 1)', width=0.5)
    bar_fig = go.Figure(a)

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
        height=550,  # Set the height of the bar plot
        yaxis=dict(range=[0, 5],
                   tickfont=dict(size=18),
                   gridcolor='rgba(51, 51, 51, 0.25)'),  # Set y-axis range
        yaxis_title="Leistung [t/h]",  # Set y-axis title
        plot_bgcolor='rgba(0, 0, 0, 0)'
    )
    bar_fig.update_yaxes(title_font=dict(size=16))
    bar_fig.update_xaxes(showline=True, linewidth=3, linecolor='rgba(51, 51, 51, 0.15)')

    current_power_steam_text = f"{round(power_cur,1)} t/h"

    return bar_fig, current_power_steam_text


def random_energiefluss_values(n_intervals):
    power_ee = np.random.randint(500, 700)
    power_bhkw = np.random.randint(8000, 9000)
    power_netz = np.random.randint(-200, 300)

    power_input_total = power_ee + power_bhkw + power_netz

    power_strom = int(power_input_total * 0.6)
    power_waerme = int(power_input_total * 0.4 * 0.95)

    power_ee_str = str(power_ee) + " kW"
    power_bhkw_str = str(power_bhkw) + " kW"
    power_netz_str = str(power_netz) + " kW"
    power_strom_str = str(power_strom) + " kW"
    power_waerme_str = str(power_waerme) + " kW"

    return power_ee_str, power_bhkw_str, power_netz_str, power_strom_str, power_waerme_str