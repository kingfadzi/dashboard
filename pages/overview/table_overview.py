import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.table_card import render_table_card

dash.register_page(__name__, path="/table-overview", name="Overview")

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Row(
            [
                dbc.Col(html.H2("Overview – Table View"), width="auto"),
                dbc.Col(
                    html.Div(
                        dbc.Button("Charts", id="back-to-charts-btn-overview", color="primary", size="sm"),
                        id="overview-table-link-container",
                        className="d-flex justify-content-end"
                    ),
                    width="auto",
                ),
            ],
            className="mb-2 align-items-center",
        ),
        render_table_card("overview-table"),
    ],
    fluid=True,
    style={"marginTop": "0", "paddingTop": "0"},
)
