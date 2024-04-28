import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
from datetime import datetime as dt
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from dash_bootstrap_components import Card, CardHeader
from dash.dependencies import ClientsideFunction


# Initialize Dash app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

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
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Create sidebar layout
sidebar = html.Div(
    [
        html.Img(src="https://lumenion.com/wp-content/uploads/2022/08/logo.svg", height="50px"),
        html.Hr(style={'background-color': 'white'}),
        html.P("Demo Dashboard", className="lead", style={"color": "#fff"}),  # White text color
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=dt(2022, 1, 1),
            max_date_allowed=dt(2024, 12, 31),
            initial_visible_month=dt.now(),
            date=dt.now()
        ),
        html.Div(style={'margin-bottom': '20px'}),  # Add some margin-bottom for space
        dbc.Nav(
            [
                dbc.NavLink("Heute", href="/", active="exact", style={"color": "white"}),
                dbc.NavLink("Gestern", href="/page-1", active="exact", style={"color": "white"}),
                dbc.NavLink("Letzte Woche", href="/page-2", active="exact", style={"color": "white"}),
                dbc.NavLink("Letzter Monat", href="/page-3", active="exact", style={"color": "white"}),
                dbc.NavLink("Gesamter Zeitraum", href="/page-4", active="exact", style={"color": "white"}),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(style={'background-color': 'white'}),  # Optional: Add a horizontal line for separation
        dbc.Nav(
            [
                dbc.NavLink("Einstellungen", href="/settings", active="exact", style={"color": "white"}),
                dbc.NavLink("Hilfe", href="/help", active="exact", style={"color": "white"}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# Create content layout
content = html.Div(id="page-content", style=CONTENT_STYLE)

# Create callback to render page content
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

# Create time array from 0 to 1440 minutes (24 hours)
# Read data from Excel file
df = pd.read_excel('your_file.xlsx')  # Replace 'your_file.xlsx' with the path to your Excel file
df["State_of_Charge"] = df["State_of_Charge"].interpolate(method="quadratic")
# Assuming your Excel file has 'Time' and 'State_of_Charge' columns
time = df['Time']
df['State_of_Charge'] = df['State_of_Charge'] * 100 + 20
df.loc[df.State_of_Charge>100, 'State_of_Charge'] = 100
state_of_charge = df['State_of_Charge']

# Get current minute of the day
current_minute = dt.now().hour * 60 + dt.now().minute

# Create figure
fig = go.Figure()

# Add area plot
fig.add_trace(go.Scatter(x=time[:current_minute], y=state_of_charge[:current_minute], fill='tozeroy', mode='none', line=dict(color='rgba(0,100,0,0.5)', width=1), showlegend=False, fillgradient=dict(
        type='vertical',
        colorscale=['rgba(204, 0, 0, 0.5)', 'rgba(0, 102, 0, 0.5)', 'rgba(0, 102, 0, 0.5)']
    )))

# Update layout
fig.update_layout(
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
        tickvals=np.arange(0, 1441, 60),  # Tick every hour
        ticktext=[str(dt(2022, 1, 1, hour // 60 % 24, hour % 60).strftime('%H:%M')) for hour in np.arange(0, 1441, 60)],  # Format tick text as HH:MM
        range=[0, 1440]  # Set x-axis range from start to end of the day
    ),
    yaxis=dict(title="Ladestand (%)",
               range=[0, 101],
               ),
    margin=dict(l=20, r=20, t=40, b=20),
)

# Render the plot
plotly_figure = dcc.Graph(id='state-of-charge-plot', figure=fig)



category = ""
value = -2700

# Create bar plot
bar_fig = go.Figure(go.Bar(x=[category], y=[value], marker_color='rgb(55, 83, 109)', width=0.5))  # Adjust width of the bar

# Update bar plot layout
bar_fig.update_layout(
    title=dict(
        text="Leistung",
        x=0.6,  # Set x to 0.5 to center the title
        font=dict(
            size=28  # Set the font size
        )
    ),
    margin=dict(l=20, r=20, t=40, b=20),
    paper_bgcolor="white",
    height=400,  # Set the height of the bar plot
    yaxis=dict(range=[-5000, 5000]),  # Set y-axis range
    yaxis_title="Leistung [kW]"  # Set y-axis title
)

# Render the bar plot
bar_plot = dcc.Graph(id='bar-plot', figure=bar_fig)

# Wrap the html.Div inside a dbc.Card component
current_power_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div("Aktuelle Leistung", style={"font-size": "18px", "color": "white", "text-align": "center", "margin-bottom": "10px"}),
                html.Div(id="current-power", style={"font-size": "32px", "color": "white", "text-align": "center"})
            ]
        )
    ],
    style={"background-color": "#333", "width": "15%"}  # Set the background color to grey
)

# Create a new card for State of Charge (SoC)
current_soc_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div("Ladestand", style={"font-size": "18px", "color": "white", "text-align": "center", "margin-bottom": "10px"}),
                html.Div(id="current-soc", style={"font-size": "32px", "color": "white", "text-align": "center"})
            ]
        )
    ],
    style={"background-color": "#333", "width": "15%", "margin-left": "100px"}  # Set the background color to grey and add left margin
)

def get_current_time():
    return dt.now().strftime("%H:%M")

current_time_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div("Uhrzeit", style={"font-size": "18px", "color": "white", "text-align": "center", "margin-bottom": "10px"}),
                html.Div(id="current-time", children=get_current_time(), style={"font-size": "32px", "color": "white", "text-align": "center"})
            ]
        )
    ],
    style={"background-color": "#333", "width": "15%", "position": "absolute", "top": "2rem", "right": "2rem"}  # Set the background color to grey and position the card
)

# Combine both cards in a single row
card_row = html.Div(
    [
        current_power_card,
        current_soc_card,
        current_time_card
    ],
    style={'display': 'flex', 'justify-content': 'start', 'margin-bottom': '20px'}  # Use flexbox to align cards horizontally with space between
)

# Adjust the width of the time series plot
time_series_width = "90%"  # Set width to 100% of the remaining space
bar_plot_width = "15%"  # Set width to 25% of the content area

# Combine content with plots
content = html.Div(
    [
        card_row,  # Include the row of cards
        html.Hr(style={'margin': '20px 30px 20px 0px'}),  # Add a horizontal line separator
        html.Div(
            [
                html.Div(
                    [
                        html.Div(bar_plot, style={'width': bar_plot_width}),
                        html.Div(plotly_figure, style={'flex': '1', 'width': time_series_width, 'margin-left': '30px'})
                    ],
                    style={'display': 'flex', 'flexDirection': 'row'}
                )
            ],
            #style={'display': 'flex'}
        ),
        html.Hr(style={'margin': '20px 30px 20px 0px'}),  # Add a horizontal line separator
    ],
    style={'margin-left': '20rem', 'margin-top': '2rem'}  # Adjust margin-left to match the width of the sidebar
)
# Create an interval component to update the current power every 2 seconds
interval_component = dcc.Interval(
    id='interval-component',
    interval=2000,  # in milliseconds
    n_intervals=0
)

# Set app layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content, interval_component, current_time_card])

# Callback to update the current time every second
@app.callback(
    Output("current-time", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_time(n):
    return get_current_time()

# Create a callback to update the current power and the bar plot every 2 seconds
# Modify the callback function to include the loading of the DataFrame and extraction of the last value
@app.callback(
    [Output("current-power", "children"),
     Output("bar-plot", "figure"),
     Output("current-soc", "children"),
     Output("state-of-charge-plot", "figure")],  # Add Output for time series plot
    [Input("interval-component", "n_intervals")]
)
def update_power_and_plot(n):
    global last_generated_value  # Declare last_generated_value as global

    # Initialize last_generated_value if it's not defined yet
    if 'last_generated_value' not in globals():
        last_generated_value = None

    # Generate a random power value within a range of 50 from the last generated value
    if last_generated_value is None:
        power = np.random.randint(-5000, 5000)  # If no last value, generate any random value
    else:
        min_value = max(-5000, last_generated_value - 50)  # Ensure minimum value is 1
        max_value = min(5000, last_generated_value + 50)  # Ensure maximum value is 100
        power = np.random.randint(min_value, max_value + 1)

    # Update the last generated value
    last_generated_value = power

    # Load the DataFrame from the Excel file
    df = pd.read_excel('your_file.xlsx')
    df["State_of_Charge"] = df["State_of_Charge"].interpolate(method="quadratic")
    # Assuming your Excel file has 'Time' and 'State_of_Charge' columns
    df['State_of_Charge'] = df['State_of_Charge'] * 100 + 20
    df.loc[df.State_of_Charge > 100, 'State_of_Charge'] = 100

    # Get the last value of 'State_of_Charge' from the DataFrame
    current_soc = df['State_of_Charge'][dt.now().hour * 60 + dt.now().minute]

    # Determine marker color based on power value
    marker_color = 'rgba(0, 102, 0, 0.5)' if power >= 0 else 'rgba(204, 0, 0, 0.5)'

    # Create bar plot
    bar_fig = go.Figure(go.Bar(x=[category], y=[power], marker_color=marker_color, width=0.5))  # Adjust width of the bar

    # Update bar plot layout
    bar_fig.update_layout(
        title=dict(
            text="Leistung",
            x=0.6,  # Set x to 0.5 to center the title
            font=dict(
                size=28  # Set the font size
            )
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        height=400,  # Set the height of the bar plot
        yaxis=dict(range=[-5000, 5000]),  # Set y-axis range
        yaxis_title="Leistung [kW]"  # Set y-axis title
    )

    # Update the displayed value for "Aktueller Ladestand"
    current_soc_text = f"{round(current_soc)} %"

    # Update time series plot data
    current_minute = dt.now().hour * 60 + dt.now().minute
    time_data = df['Time'][:current_minute]
    soc_data = df['State_of_Charge'][:current_minute]

    # Create figure for time series plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_data, y=soc_data, fill='tozeroy', mode='none', line=dict(color='rgba(0,100,0,0.5)', width=1), showlegend=False, fillgradient=dict(
        type='vertical',
        colorscale=['rgba(204, 0, 0, 0.5)', 'rgba(0, 102, 0, 0.5)', 'rgba(0, 102, 0, 0.5)']
    )))
    fig.update_layout(
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
            tickvals=np.arange(0, 1441, 60),  # Tick every hour
            ticktext=[str(dt(2022, 1, 1, hour // 60 % 24, hour % 60).strftime('%H:%M')) for hour in
                      np.arange(0, 1441, 60)],  # Format tick text as HH:MM
            range=[0, 1440]  # Set x-axis range from start to end of the day
        ),
        yaxis=dict(title="Ladestand (%)",
                   range=[0, 101],
                   ),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return f"{power} kW", bar_fig, current_soc_text, fig  # Return current power, bar plot, current SOC, and time series plot


# Run the app
if __name__ == "__main__":
    app.run_server(debug=False)
