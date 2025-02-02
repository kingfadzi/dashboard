# app.py

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.io as pio
from data.cache_instance import cache
from app_callbacks import register_callbacks, register_dropdown_callbacks
from layouts.layout_filters import filter_layout
import dash

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Force all graphs to use a white background globally
pio.templates.default = "plotly_white"

server.config["CACHE_TYPE"] = "simple"
server.config["CACHE_DEFAULT_TIMEOUT"] = 3600
cache.init_app(server)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link("Graphs", href="/", className="nav-link")),
        dbc.NavItem(dcc.Link("Table", href="/table", className="nav-link")),
        html.Span("☰", id="filter-toggle-btn", style={"cursor": "pointer", "fontSize": "24px", "marginLeft": "10px"}),
    ],
    brand="Dashboard",
    color="primary",
    dark=True,
)

app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        navbar,

        # Offcanvas Filter Panel (Slides Over Content)
        dbc.Offcanvas(
            filter_layout(),
            id="filter-panel",
            title="Filters",
            is_open=False,  # Default is closed
            placement="start",  # Slides in from the left
            backdrop=True,  # Click outside to close
        ),

        # Main Content Always Uses Full Width
        dash.page_container,
    ],
    fluid=True,
)

register_callbacks(app)
register_dropdown_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")