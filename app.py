from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.io as pio
from data.cache_instance import cache  # No need for CACHE_AVAILABLE
from layouts.layout_filters import filter_layout
import dash
from callbacks.register_all_callbacks import register_all_callbacks
from callbacks.table_callbacks import register_table_callbacks
import callbacks.repo_profile_callback
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


# Initialize Dash app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set Plotly theme
pio.templates.default = "plotly_white"

# Initialize caching (handled inside cache_instance.py)
cache.init_app(server)

# Navbar setup

navbar = dbc.Navbar(
    dbc.Container([
        dcc.Link("Dashboard", href="/", className="navbar-brand text-white fw-bold"),

        dbc.Nav([
            dbc.NavItem(
                dcc.Link("Graphs", href="/", className="nav-link", id="nav-link-graphs")
            ),
            dbc.NavItem(
                dcc.Link("Table", href="/table", className="nav-link", id="nav-link-table")
            ),
        ], className="ms-auto", pills=True),
    ]),
    color="primary",
    dark=True,
    className="mb-4 shadow-sm"
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

@app.callback(
    Output("nav-link-graphs", "className"),
    Output("nav-link-table", "className"),
    Input("url", "pathname"),
)
def highlight_active_tab(pathname):
    return (
        "nav-link active" if pathname == "/" else "nav-link",
        "nav-link active" if pathname == "/table" else "nav-link",
    )


# Register all callbacks
register_all_callbacks(app)
register_table_callbacks(app)

# Run server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")