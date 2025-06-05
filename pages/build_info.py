import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.modal_table import modal_table
from layouts.layout_filters import filter_layout

dash.register_page(__name__, path="/build-info", name="Build Info")

def card(title, graph_id, height=400):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dcc.Loading(
                dcc.Graph(
                    id=graph_id,
                    config={"staticPlot": True},
                    style={"height": f"{height}px"},
                )
            ),
        ],
        className="mb-4",
    )

header_with_button = dbc.Row(
    [
        dbc.Col(html.H2("Build Info"), width="auto"),
        dbc.Col(
            html.Div(
                dbc.Button(
                    "Table",
                    id="build-info-table-btn",
                    color="secondary",
                    size="sm",
                    n_clicks=0
                ),
                id="build-info-table-link-container",
                className="d-flex justify-content-end",
            ),
            width="auto",
        ),
    ],
    className="mb-2 align-items-center",
)

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        header_with_button,

        dbc.Row(
            [
                dbc.Col(card("Detection Status", "build-runtime-coverage-chart"), width=8),  # Renamed
                dbc.Col(card("Runtime Fragmentation", "runtime-fragmentation-chart"), width=4),  # Swapped
            ],
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(html.B("No Build Tool: Size vs Commits", className="text-center"), className="bg-light"),
                        dcc.Loading(
                            dcc.Graph(
                                id="no-buildtool-scatter",
                                config={
                                    "staticPlot": False,
                                    "displayModeBar": False,
                                    "scrollZoom": False,
                                },
                                style={"height": "400px"},
                            )
                        ),
                    ],
                    className="mb-4",
                ),
                width=12,
            ),
            className="mb-4",
        ),

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
            [
                dbc.Col(card("Runtime Versions", "runtime-versions-chart"), width=12),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(card("Build Tools", "build-tool-variant-chart"), width=12),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(card("Confidence Distribution", "confidence-distribution-chart"), width=4),
                dbc.Col(card("Detection Status", "status-by-tool-chart"), width=4),
                dbc.Col(card("Module Count Per Repo", "module-count-chart"), width=4),
            ],
            className="mb-4",
        ),

        # Detection Coverage moved to bottom
        dbc.Row(
            [
                dbc.Col(card("Detection Coverage", "detection-coverage-chart"), width=12),
            ],
            className="mb-4",
        ),

        modal_table(),
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
