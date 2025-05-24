from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.io as pio
from data.cache_instance import cache
from layouts.layout_filters import filter_layout
import dash
from callbacks.register_all_callbacks import register_all_callbacks
from callbacks.table_callbacks import register_table_callbacks
import callbacks.repo_profile_callback  # ensure side-effect callbacks load

# Initialize Dash app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set Plotly theme
pio.templates.default = "plotly_white"

# Initialize caching
cache.init_app(server)

# Navbar using clean Bootstrap tabs
navbar = dbc.NavbarSimple(
    brand="Tech Debt Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4 shadow-sm",
    children=[
        dbc.NavItem(dbc.NavLink("Overview", href="/", active="exact")),
        dbc.NavItem(dbc.NavLink("Code Insights", href="/code-insights", active="exact")),
        dbc.NavItem(dbc.NavLink("Build Info", href="/build-info", active="exact")),
        dbc.NavItem(dbc.NavLink("Dependencies", href="/dependencies", active="exact")),
        dbc.NavItem(dbc.NavLink("Vulnerabilities", href="/vulnerabilities", active="exact")),
    ]
)

# Layout
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
        html.Div(dash.page_container, className="px-4 pb-4"),
    ],
    fluid=True,
)

# Register callbacks
register_all_callbacks(app)
register_table_callbacks(app)

# Run server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")