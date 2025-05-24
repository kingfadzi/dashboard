from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.io as pio
from data.cache_instance import cache
from layouts.layout_filters import filter_layout
import dash
from callbacks.register_all_callbacks import register_all_callbacks
from callbacks.table_callbacks import register_table_callbacks
import callbacks.repo_profile_callback
from dash import Dash, dcc, html, Input, Output, State

# Initialize Dash app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set Plotly theme
pio.templates.default = "plotly_white"

# Initialize caching
cache.init_app(server)

# Navbar with graph/table toggle instead of filter button
navbar = dbc.Navbar(
    dbc.Container(
        dbc.Row([
            # Brand
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

            # Tabs
            dbc.Col(
                dbc.Nav(
                    [
                        dbc.NavLink([html.I(className="bi bi-eye me-2"), "Overview"],
                                    href="/", active="exact",
                                    className="rounded-pill px-3 mx-1 text-center"),
                        dbc.NavLink([html.I(className="bi bi-bar-chart-line me-2"), "Code Insights"],
                                    href="/code-insights", active="exact",
                                    className="rounded-pill px-3 mx-1 text-center"),
                        dbc.NavLink([html.I(className="bi bi-gear-wide-connected me-2"), "Build Info"],
                                    href="/build-info", active="exact",
                                    className="rounded-pill px-3 mx-1 text-center"),
                        dbc.NavLink([html.I(className="bi bi-diagram-3 me-2"), "Dependencies"],
                                    href="/dependencies", active="exact",
                                    className="rounded-pill px-3 mx-1 text-center"),
                        dbc.NavLink([html.I(className="bi bi-shield-exclamation me-2"), "Vulnerabilities"],
                                    href="/vulnerabilities", active="exact",
                                    className="rounded-pill px-3 mx-1 text-center"),
                    ],
                    pills=True,
                    className="justify-content-center w-100"
                ),
                className="d-flex align-items-center justify-content-center",
            ),

            # View mode toggle (graph/table)
            dbc.Col(
                dbc.ButtonGroup(
                    [
                        dbc.Button("Graph", id="global-toggle-graph", color="light"),
                        dbc.Button("Table", id="global-toggle-table", color="light"),
                    ],
                    size="sm",
                    className="d-flex"
                ),
                width="auto",
                className="d-flex align-items-center justify-content-end"
            ),
        ], align="center", className="w-100"),
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
        dcc.Store(id="view-mode", data="graph"),  # Global toggle store
        navbar,
        dbc.Offcanvas(
            filter_layout(),
            id="filter-panel",
            title="Filters",
            is_open=True,
            placement="start",
            backdrop=True,
        ),
        html.Div(dash.page_container, className="px-4 pb-4"),
    ],
    fluid=True,
)

# View toggle callback
@app.callback(
    Output("view-mode", "data"),
    Input("global-toggle-graph", "n_clicks"),
    Input("global-toggle-table", "n_clicks"),
    State("view-mode", "data"),
)
def update_view_mode(n_graph, n_table, current):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current
    triggered = ctx.triggered[0]["prop_id"].split(".")[0]
    return "graph" if "graph" in triggered else "table"

# Register callbacks
register_all_callbacks(app)
register_table_callbacks(app)

# Run server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")