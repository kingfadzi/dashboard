import dash
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.io as pio
from dash.dependencies import Input, Output, State

from data.cache_instance import cache
from layouts.layout_filters import filter_layout  # Original name preserved
from callbacks.register_all_callbacks import register_all_callbacks

# Initialize Dash app
app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server

# Set Plotly theme
pio.templates.default = "plotly_white"

# Initialize caching
cache.init_app(server)

# Navbar setup
navbar = dbc.Navbar(
    dbc.Container([
        dcc.Link("Dashboard", href="/", className="navbar-brand text-white fw-bold"),
        dbc.Nav(
            [
                dbc.NavItem(dcc.Link("Overview", href="/", className="nav-link", id="nav-link-overview")),
                dbc.NavItem(dcc.Link("Code Insights", href="/code-insights", className="nav-link", id="nav-link-code-insights")),
                dbc.NavItem(dcc.Link("Build Info", href="/build-info", className="nav-link", id="nav-link-build-info")),
                dbc.NavItem(dcc.Link("Dependencies", href="/dependencies", className="nav-link", id="nav-link-dependencies")),
                dbc.NavItem(dcc.Link("Vulnerabilities", href="/vulnerabilities", className="nav-link", id="nav-link-vulnerabilities")),
                # Filters button as the last item
                dbc.NavItem(
                    dbc.Button(
                        "☰ Filters",
                        id="toggle-filters-btn",
                        color="secondary",
                        size="sm",
                        className="ms-2",
                        style={"padding": "0.25rem 0.5rem", "fontSize": "0.8rem"}
                    )
                ),
            ],
            className="ms-auto",  # Pushes all nav items to the right
            pills=True
        ),
    ]),
    color="primary",
    dark=True,
    className="mb-4 shadow-sm"
)


# App layout

app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Location(id="repo-modal-location", refresh=False),  # ← ADD HERE
        html.Div(id="repo-modal-container"),                    # ← AND HERE
        navbar,
        dcc.Store(id="default-filter-store", storage_type="local"),
        dbc.Collapse(filter_layout(), id="filter-collapse", is_open=True),
        dash.page_container,
    ],
    fluid=True,
)

# Highlight active tab in navbar
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

# Toggle filter visibility
@app.callback(
    Output("filter-collapse", "is_open"),
    Input("url", "pathname"),
    Input("toggle-filters-btn", "n_clicks"),
    State("filter-collapse", "is_open"),
)
def toggle_filter_visibility(pathname, n_clicks, is_open):
    # Pages that should not show the filter
    pages_without_filter = ["/repo"]

    if pathname in pages_without_filter:
        return False  # Force collapse

    # Allow toggle only on pages that support filters
    if n_clicks:
        return not is_open
    return is_open


# Register app callbacks
register_all_callbacks(app)


# Run app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
