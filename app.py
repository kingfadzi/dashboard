from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.io as pio
from data.cache_instance import cache
from layouts.layout_filters import filter_layout
import dash
from callbacks.register_all_callbacks import register_all_callbacks  # Imported from the callbacks package
from callbacks.table_callbacks import register_table_callbacks

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

pio.templates.default = "plotly_white"

server.config["CACHE_TYPE"] = "simple"
server.config["CACHE_DEFAULT_TIMEOUT"] = 3600
cache.init_app(server)

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

# Register all callbacks from the callbacks package
register_all_callbacks(app)
# Register table callbacks as before
register_table_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")