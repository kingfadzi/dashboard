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
# Enhanced Navbar with icons, hover effects, and modern styling
navbar = dbc.Navbar(
    dbc.Container(
        [
            # Brand with icon
            dbc.NavbarBrand(
                html.Span(
                    [
                        html.I(className="bi bi-speedometer2 me-2"),  # Dashboard icon
                        "Tech Debt Dashboard",
                    ],
                    className="d-flex align-items-center"
                ),
                href="/",
                className="fs-4 fw-bold text-white pe-5"
            ),
            
            # Navigation items with icons and pills
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-eye me-2"),  # Icon
                            "Overview"
                        ],
                        href="/",
                        active="exact",
                        className="rounded-pill px-3 mx-1 transition-all"
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-bar-chart-line me-2"),
                            "Code Insights"
                        ],
                        href="/code-insights",
                        active="exact",
                        className="rounded-pill px-3 mx-1 transition-all"
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-gear-wide-connected me-2"),
                            "Build Info"
                        ],
                        href="/build-info",
                        active="exact",
                        className="rounded-pill px-3 mx-1 transition-all"
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-diagram-3 me-2"),
                            "Dependencies"
                        ],
                        href="/dependencies",
                        active="exact",
                        className="rounded-pill px-3 mx-1 transition-all"
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-shield-exclamation me-2"),
                            "Vulnerabilities"
                        ],
                        href="/vulnerabilities",
                        active="exact",
                        className="rounded-pill px-3 mx-1 transition-all"
                    ),
                ],
                navbar=True,
                className="mx-auto"  # Center align nav items
            ),
            
            # Settings button aligned to right
            dbc.Button(
                html.I(className="bi bi-funnel"),
                color="light",
                className="rounded-pill px-3",
                id="filter-button",
            )
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
    sticky="top",
    className="shadow gradient-bg",
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