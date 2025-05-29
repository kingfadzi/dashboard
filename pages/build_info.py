import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import DEFAULT_FILTERS

dash.register_page(__name__, path="/build-info", name="Build Info")


def card(title, graph_id, height=400):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dbc.CardBody(
                dcc.Loading(
                    dcc.Graph(
                        id=graph_id,
                        config={"staticPlot": True},
                        style={"height": f"{height}px"},
                    )
                ),
                className="p-0",
            ),
        ],
        className="mb-4",
    )


# Simple header with table link
header_with_button = dbc.Row(
    [
        dbc.Col(html.H2("Build Info"), width="auto"),
        dbc.Col(
            html.Div(
                dbc.Button("Table", id="build-info-table-btn", color="secondary", size="sm"),
                id="build-info-table-link-container",
                className="d-flex justify-content-end",
            ),
            width="auto",
        )

    ],
    className="mb-2 align-items-center",
)


layout = dbc.Container(
    [

        dcc.Location(id="url", refresh=False),

        header_with_button,

        dbc.Row(
            [
                dbc.Col(card("Detection Coverage", "detection-coverage-chart"), width=6),
                dbc.Col(card("Module Count", "module-count-chart"), width=6),
            ],
            className="mb-4",
        ),

        # Tool selector
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select Language Tool", className="fw-bold"),
                        dcc.Dropdown(
                            id="tool-selector",
                            options=[],
                            placeholder="Select a tool",
                            clearable=True,
                        ),
                    ],
                    width=3,
                ),
                dbc.Col([], width=9),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [dbc.Col(card("Runtime Versions", "runtime-versions-chart"), width=12)],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(card("Runtime Fragmentation", "runtime-fragmentation-chart"), width=6),
                dbc.Col(card("Status by Tool", "status-by-tool-chart"), width=6),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [dbc.Col(card("Confidence Distribution", "confidence-distribution-chart"), width=6)],
            className="mb-4",
        ),

        # Shared Stores
        dcc.Store(id="default-filter-store"),
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
