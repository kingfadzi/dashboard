import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.table_card import render_table_card

dash.register_page(__name__, path="/table-dependencies", name="Dependencies")

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),

        dbc.Row(
            [
                dbc.Col(html.H2("Dependencies"), width="auto"),
                dbc.Col(
                    html.Div(
                        dbc.Button("Charts", id="back-to-charts-btn-dependencies", color="primary", size="sm"),
                        id="dependencies-table-link-container",
                        className="d-flex justify-content-end"
                    ),
                    width="auto",
                ),
            ],
            className="mb-2 align-items-center",
        ),

        render_table_card("dependencies-table"),
    ],
    fluid=True,
    style={"marginTop": "0", "paddingTop": "0"},
)
