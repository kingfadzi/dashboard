import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.layout_filters import filter_layout

dash.register_page(__name__, path="/code-insights")

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),

        # Filter header and switch link
        dbc.Row(
            [
                dbc.Col(html.Div("Filters", className="text-muted small fw-bold mb-0"), width="auto"),
                dbc.Col(
                    html.A(
                        id="switch-to-table-link",  # Optional: create a callback if you want dynamic URL
                        children="Switch to Table View",
                        href="/table",
                        className="text-primary small fw-normal text-decoration-none",
                        target="_self",
                    ),
                    width="auto",
                    className="text-end",
                ),
            ],
            justify="between",
            className="align-items-center g-0",
            style={"margin": "0px", "padding": "0px"},
        ),

        html.Div(filter_layout(), style={"marginTop": "0px", "paddingTop": "0px"}),

        # Placeholder for Code Insights content
        dbc.Card(
            [
                dbc.CardHeader(html.B("Code Insights Coming Soon", className="text-center"), className="bg-light"),
                dbc.CardBody(html.P("This section will display insights like Semgrep, Lizard, and static analysis results.")),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
