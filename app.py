import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.io as pio


from data.cache_instance import cache
from layouts.layout_filters import filter_layout
from callbacks.register_all_callbacks import register_all_callbacks
from callbacks.table_callbacks import register_table_callbacks
import callbacks.repo_profile_callback
from dash.dependencies import Input, Output
import callbacks.code_insights_modal
from config.config import DEFAULT_FILTERS
from callbacks.register_filter_callbacks import register_filter_callbacks

# Initialize Dash app
app = Dash(__name__, use_pages=True,  suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set Plotly theme
pio.templates.default = "plotly_white"

# Initialize caching
cache.init_app(server)

# Navbar setup
navbar = dbc.Navbar(
    dbc.Container([
        dcc.Link("Dashboard", href="/", className="navbar-brand text-white fw-bold"),

        dbc.Nav([
            dbc.NavItem(
                dcc.Link("Overview", href="/", className="nav-link", id="nav-link-overview")
            ),
            dbc.NavItem(
                dcc.Link("Code Insights", href="/code-insights", className="nav-link", id="nav-link-code-insights")
            ),
            dbc.NavItem(
                dcc.Link("Build Info", href="/build-info", className="nav-link", id="nav-link-build-info")
            ),
            dbc.NavItem(
                dcc.Link("Dependencies", href="/dependencies", className="nav-link", id="nav-link-dependencies")
            ),
            dbc.NavItem(
                dcc.Link("Vulnerabilities", href="/vulnerabilities", className="nav-link", id="nav-link-vulnerabilities")
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
        # use the dict we exported
        dcc.Store(id="default-filter-store", data=DEFAULT_FILTERS),
        filter_layout(),
        dash.page_container,
    ],
    fluid=True,
)

# Callback for navbar active tab highlighting
@app.callback(
    Output("nav-link-overview", "className"),
    Output("nav-link-code-insights", "className"),
    Output("nav-link-build-info", "className"),
    Output("nav-link-dependencies", "className"),
    Output("nav-link-vulnerabilities", "className"),

    Input("url", "pathname"),
)
def highlight_active_tab(pathname):
    return (
        "nav-link active" if pathname == "/" else "nav-link",
        "nav-link active" if pathname == "/code-insights" else "nav-link",
        "nav-link active" if pathname == "/build-info" else "nav-link",
        "nav-link active" if pathname == "/dependencies" else "nav-link",
        "nav-link active" if pathname == "/vulnerabilities" else "nav-link",

    )

# Register callbacks

register_all_callbacks(app)
register_table_callbacks(app)


# Run server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
