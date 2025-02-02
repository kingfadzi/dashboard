from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
#import dash.pages  # 

import dash
from dash_labs.plugins.pages 

import plotly.io as pio
from data.cache_instance import cache
from app_callbacks import register_callbacks, register_dropdown_callbacks

# Initialize Dash app with multi-page support
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Flask server

# Configure Flask-Caching
server.config["CACHE_TYPE"] = "simple"
server.config["CACHE_DEFAULT_TIMEOUT"] = 3600
cache.init_app(server)

pio.templates.default = "plotly_white"

# Define the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link("Graphs", href="/", className="nav-link")),
        dbc.NavItem(dcc.Link("Table", href="/table", className="nav-link")),
    ],
    brand="Dashboard",
    color="primary",
    dark=True,
)

# Define the app layout
app.layout = dbc.Container(
    [
        navbar,
        dash.page_container,  # Renders the correct page dynamically
    ],
    fluid=True,
)

# Register callbacks
register_callbacks(app)
register_dropdown_callbacks(app)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)