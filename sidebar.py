import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_mantine_components as dmc

from datetime import datetime as dt
import pytz


def get_sidebar():
    # Define styles for sidebar and content
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#333",  # Darker background color
        "color": "#fff",  # White text color
        'border-right': '1px solid #c2c2c2',
    }


    # Create sidebar layout
    sidebar = html.Div(
        [
            html.Img(src="https://lumenion.com/wp-content/uploads/2022/08/logo.svg", height="60px"),
            html.Div(style={'margin-bottom': '40px'}),  # Add some margin-bottom for space
            html.Hr(style={'background-color': 'white'}),
            html.P("Demo Dashboard", className="lead", style={"color": "#fff", "font-size": "24px", "text-align": "center"}),  # White text color
            html.Hr(style={'background-color': 'white'}),
            html.Div(style={'margin-bottom': '20px'}),  # Add some margin-bottom for space
            dcc.DatePickerSingle(
                id='date-picker',
                display_format='DD/MM/YYYY',
                min_date_allowed=dt(2022, 1, 1),
                max_date_allowed=dt(2024, 12, 31),
                initial_visible_month=dt.now(pytz.timezone('Europe/Berlin')),
                date=dt.now(pytz.timezone('Europe/Berlin'))
            ),
            html.Div(style={'margin-bottom': '20px'}),  # Add some margin-bottom for space
            html.Div(
                [
                    dmc.NavLink(id="link_heute", label="Heute", href="/"),
                    dmc.NavLink(id="link_gestern", label="Gestern", href="/Gestern"),
                    dmc.NavLink(id="link_woche", label="Letzte Woche", href="/Woche"),
                ],
            ),
            html.Hr(style={'background-color': 'white'}),  # Optional: Add a horizontal line for separation
            html.Div(
                [
                    dmc.NavLink(id="link_einstellungen", label="Einstellungen", href="/Einstellungen"),
                    dmc.NavLink(id="link_hilfe", label="Hilfe", href="/Hilfe"),
                ],
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    return sidebar

