# app.py

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash
from data.cache_instance import cache
from app_callbacks import register_callbacks, register_dropdown_callbacks
from layouts.layout_filters import filter_layout

# Create Dash app with multi-page support
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Configure caching
server.config["CACHE_TYPE"] = "simple"
server.config["CACHE_DEFAULT_TIMEOUT"] = 3600
cache.init_app(server)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link("Graphs", href="/", className="nav-link")),
        dbc.NavItem(dcc.Link("Table", href="/table", className="nav-link")),
    ],
    brand="Dashboard",
    color="primary",
    dark=True,
)

app.layout = dbc.Container(
    [
        # Needed so we can use url as a callback Input
        dcc.Location(id="url", refresh=False),

        navbar,
        dbc.Row(
            [
                dbc.Col(filter_layout(), md=3),      # Left: Filter layout
                dbc.Col(dash.page_container, md=9),  # Right: Page content
            ],
            className="mt-3",
        ),
    ],
    fluid=True,
)

register_callbacks(app)
register_dropdown_callbacks(app)

if __name__ == "__main__":
    # Listen on 0.0.0.0 so it's accessible externally
    app.run_server(debug=True, host="0.0.0.0")