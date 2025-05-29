import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.table_card import render_table_card

dash.register_page(__name__, path="/table-code-insights", name="Code Insights – Table View")

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="default-filter-store"),

        dbc.Row(
            [
                dbc.Col(html.H2("Code Insights – Table View"), width="auto"),
                dbc.Col(
                    html.Div(
                        dbc.Button("Charts", id="back-to-charts-btn-code-insights", color="primary", size="sm"),
                        id="code-insights-table-link-container",
                        className="d-flex justify-content-end"
                    ),
                    width="auto",
                ),
            ],
            className="mb-2 align-items-center",
        ),

        render_table_card("code-insights-table"),
    ],
    fluid=True,
    style={"marginTop": "0", "paddingTop": "0"},
)
