from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.io as pio
from data.cache_instance import cache
from layouts.layout_filters import filter_layout
import dash
from callbacks.register_all_callbacks import register_all_callbacks
from callbacks.table_callbacks import register_table_callbacks
import callbacks.repo_profile_callback
from dash.dependencies import Input, Output

# Initialize Dash app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Set Plotly theme
pio.templates.default = "plotly_white"

# Initialize caching
cache.init_app(server)

# Updated Navbar
navbar = dbc.Navbar(
    dbc.Container([
        dcc.Link("Tech Debt Dashboard", href="/", className="navbar-brand text-white fw-bold"),

        dbc.Nav([
            dbc.NavItem(dcc.Link("Overview", href="/", className="nav-link", id="nav-link-overview")),
            dbc.NavItem(dcc.Link("Code Insights", href="/code-insights", className="nav-link", id="nav-link-code")),
            dbc.NavItem(dcc.Link("Build Info", href="/build-info", className="nav-link", id="nav-link-build")),
            dbc.NavItem(dcc.Link("Dependencies", href="/dependencies", className="nav-link", id="nav-link-deps")),
            dbc.NavItem(dcc.Link("Vulnerabilities", href="/vulnerabilities", className="nav-link", id="nav-link-vuln")),
        ], className="ms-auto", pills=True),
    ]),
    color="primary",
    dark=True,
    className="mb-4 shadow-sm"
)

# App layout
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

# Active tab highlighting
@app.callback(
    Output("nav-link-overview", "className"),
    Output("nav-link-code", "className"),
    Output("nav-link-build", "className"),
    Output("nav-link-deps", "className"),
    Output("nav-link-vuln", "className"),
    Input("url", "pathname"),
)
def highlight_active_tab(pathname):
    def active(link): return "nav-link active" if pathname == link else "nav-link"
    return (
        active("/"),
        active("/code-insights"),
        active("/build-info"),
        active("/dependencies"),
        active("/vulnerabilities"),
    )

# Register callbacks
register_all_callbacks(app)
register_table_callbacks(app)

# Run server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")