from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.io as pio
from data.cache_instance import cache  # No need for CACHE_AVAILABLE
from layouts.layout_filters import filter_layout
import dash
from callbacks.register_all_callbacks import register_all_callbacks
from callbacks.table_callbacks import register_table_callbacks
import callbacks.repo_profile_callback

# Initialize Dash app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set Plotly theme
pio.templates.default = "plotly_white"

# Initialize caching (handled inside cache_instance.py)
cache.init_app(server)

# Navbar setup
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link("Graphs", href="/", className="nav-link")),
        dbc.NavItem(dcc.Link("Table", href="/table", className="nav-link")),
        html.Span(
            "☰", 
            id="filter-toggle-btn", 
            style={"cursor": "pointer", "fontSize": "24px", "marginLeft": "10px"}
        ),
    ],
    brand=dcc.Link("Dashboard", href="/", className="navbar-brand"),
    color="primary",
    dark=True,
)

# Define app layout
app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Offcanvas(
            filter_layout(),
            id="filter-panel",
            title="Filters",
            is_open=False,
            placement="start",
            backdrop=True,
        ),
        dash.page_container,
    ],
    fluid=True,
)

# Register all callbacks
register_all_callbacks(app)
register_table_callbacks(app)

# Run server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")