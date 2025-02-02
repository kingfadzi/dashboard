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

# Sidebar toggle (takes minimal space)
filter_toggle = html.Div(
    [
        html.Span("◀", id="filter-toggle-btn", style={"cursor": "pointer", "padding": "5px", "fontSize": "20px"}),
    ],
    style={"position": "absolute", "left": "5px", "top": "10px", "zIndex": "1000"},
)

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

        # Sidebar & Main Content Row
        dbc.Row(
            [
                # Collapsible Left Sidebar (Filters)
                dbc.Col(
                    dbc.Offcanvas(
                        filter_layout(),
                        id="filter-panel",
                        title="Filters",
                        is_open=True,  # Default: Expanded
                        placement="start",  # Collapse to the left
                        backdrop=False,  # Keep it functional while collapsed
                    ),
                    id="filter-col",
                    md=3,
                ),

                # Sidebar Toggle (Minimal Space)
                filter_toggle,

                # Main Content Expands When Filters Collapse
                dbc.Col(dash.page_container, id="content-col", md=9),
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