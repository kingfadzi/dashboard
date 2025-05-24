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

# Navbar with full horizontal & vertical centering
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row([
                # Brand column
                dbc.Col(
                    dbc.NavbarBrand(
                        html.Span(
                            [
                                html.I(className="bi bi-speedometer2 me-2"),
                                "Tech Debt Dashboard",
                            ],
                            className="d-flex align-items-center justify-content-center"
                        ),
                        href="/",
                        className="fs-4 fw-bold text-white text-center"
                    ),
                    width="auto",
                    className="d-flex align-items-center"
                ),

                # Centered navigation items
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.NavLink(
                                [html.I(className="bi bi-eye me-2"), "Overview"],
                                href="/",
                                active="exact",
                                className="rounded-pill px-3 mx-1 text-center"
                            ),
                            dbc.NavLink(
                                [html.I(className="bi bi-bar-chart-line me-2"), "Code Insights"],
                                href="/code-insights",
                                active="exact",
                                className="rounded-pill px-3 mx-1 text-center"
                            ),
                            dbc.NavLink(
                                [html.I(className="bi bi-gear-wide-connected me-2"), "Build Info"],
                                href="/build-info",
                                active="exact",
                                className="rounded-pill px-3 mx-1 text-center"
                            ),
                            dbc.NavLink(
                                [html.I(className="bi bi-diagram-3 me-2"), "Dependencies"],
                                href="/dependencies",
                                active="exact",
                                className="rounded-pill px-3 mx-1 text-center"
                            ),
                            dbc.NavLink(
                                [html.I(className="bi bi-shield-exclamation me-2"), "Vulnerabilities"],
                                href="/vulnerabilities",
                                active="exact",
                                className="rounded-pill px-3 mx-1 text-center"
                            ),
                        ],
                        pills=True,
                        className="justify-content-center w-100"
                    ),
                    className="d-flex align-items-center justify-content-center",
                ),

                # Filter button column
                dbc.Col(
                    dbc.Button(
                        html.I(className="bi bi-funnel"),
                        color="light",
                        className="rounded-pill px-3",
                        id="filter-button",
                    ),
                    width="auto",
                    className="d-flex align-items-center justify-content-end"
                ),
            ], align="center", className="w-100"),
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
    sticky="top",
    className="shadow",
    style={"background": "linear-gradient(145deg, #0d6efd, #0b5ed7)"}
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