from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from data.cache_instance import cache
from app_callbacks import register_callbacks, register_dropdown_callbacks
from layouts.layout_filters import filter_layout
import dash

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

server.config["CACHE_TYPE"] = "simple"
server.config["CACHE_DEFAULT_TIMEOUT"] = 3600
cache.init_app(server)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link("Graphs", href="/", className="nav-link")),
        dbc.NavItem(dcc.Link("Table", href="/table", className="nav-link")),
    ],
    brand="Dashboard",
    color="primary",
    dark=True,
)

app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),

        navbar,

        dbc.Row(
            [
                # Left: Filter with Collapsible Functionality
                dbc.Col(
                    [
                        dbc.Button(
                            "Toggle Filters",
                            id="filter-toggle-btn",
                            color="primary",
                            className="mb-2",
                        ),
                        dbc.Collapse(
                            filter_layout(),  # Existing filter layout
                            id="filter-panel",
                            is_open=True,  # Default: Expanded
                        ),
                    ],
                    md=3,
                ),

                # Right: Page Content
                dbc.Col(dash.page_container, md=9),
            ],
            className="mt-3",
        ),
    ],
    fluid=True,
)

register_callbacks(app)
register_dropdown_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0")