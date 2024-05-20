from dash import Dash, dcc, html, Input, Output, callback
import dash_mantine_components as dmc

from datetime import datetime as dt
import pytz
import plotly.graph_objs as go
import numpy as np
import pandas as pd


############## cards ##############
def get_EE_card():
    EE_card = dmc.Card(
        [
            html.Div("Erneuerbare Energieversorgung (heute)", style={"font-size": "18px", "color": "#ffffff", "text-align": "center", "margin-bottom": "10px", "font-family": "'Nunito Sans', sans-serif"}),
            html.Div("98 %", style={"font-size": "32px", "color": "#ffffff", "text-align": "center", "font-family": "'Nunito Sans', sans-serif"})
        ],
        style={"background-color": "#333333", "width": "70%", "border": "2px solid #ffffff"},
        shadow="1px 1px 5px #b8b6b6",# Set the background color to grey and add left margin
    )
    return EE_card


def get_lebensmittel_card():
    lebensmittel_card = dmc.Card(
        [
            html.Div("Erneuerbar produzierte Lebensmittel (heute)", style={"font-size": "18px", "color": "#ffffff", "text-align": "center", "margin-bottom": "10px"}),
            html.Div(id="value_production", style={"font-size": "32px", "color": "#ffffff", "text-align": "center"})
        ],
        style={"background-color": "#333333", "width": "70%", "border": "2px solid #ffffff"},
        shadow="1px 1px 5px #b8b6b6",# Set the background color to grey and add left margin
    )
    return lebensmittel_card
