import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.modal_table import modal_table

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

def interactive_card(title, graph_id, height=400):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dcc.Loading(
                dcc.Graph(
                    id=graph_id,
                    config={
                        "staticPlot": False,
                        "displayModeBar": False,
                        "scrollZoom": False
                    },
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

        # First row
        dbc.Row(
            [
                dbc.Col(card("Build Tool/Runtime Detection Coverage", "build-runtime-coverage-chart"), width=4),
                dbc.Col(card("Build Tool Detection Status", "status-by-tool-chart"), width=4),
                dbc.Col(card("Runtime Fragmentation", "runtime-fragmentation-chart"), width=4),
            ],
            className="mb-4",
        ),

        # Second row
        dbc.Row(
            [
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
                    width=8,
                ),
                dbc.Col(card("No Build Tool: Language Type Breakdown", "no-buildtool-language-distribution", height=400), width=4),
            ],
            className="mb-4",
        ),

        # Third row
        dbc.Row(
            [
                dbc.Col(card("Build Tools", "build-tool-variant-chart"), width=8),
                dbc.Col(card("Module Count Per Repo", "module-count-chart"), width=4),
            ],
            className="mb-4",
        ),

        # Fourth row: Dropdown inside the card
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                dbc.Row(
                                    [
                                        dbc.Col(html.B("Runtime Versions"), className="text-start"),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="tool-selector",
                                                placeholder="Select Language Tool",
                                                options=[],
                                                clearable=True,
                                                value=None,
                                                style={"width": "250px", "fontSize": "14px"},
                                            ),
                                            width="auto",
                                        ),
                                    ],
                                    className="align-items-center justify-content-between",
                                ),
                                className="bg-light",
                            ),
                            dbc.CardBody(
                                dcc.Loading(
                                    dcc.Graph(
                                        id="runtime-versions-chart",
                                        config={"staticPlot": True},
                                        style={"height": "400px"},
                                    )
                                ),
                                className="p-0",
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=12,
                ),
            ],
            className="mb-4",
        ),

        # Fifth row
        dbc.Row(
            [
                dbc.Col(interactive_card("Support Status (.NET)", "dotnet-support-status-chart"), width=4),
                dbc.Col(interactive_card("Support Status (Java)", "java-support-status-chart"), width=4),
                dbc.Col(interactive_card("Support Status (Go)", "go-support-status-chart"), width=4),
            ],
            className="mb-4",
        ),

        # Sixth row
        dbc.Row(
            [
                dbc.Col(interactive_card("Support Status (Python)", "python-support-status-chart"), width=6),
                dbc.Col(interactive_card("Support Status (JavaScript)", "js-support-status-chart"), width=6),
            ],
            className="mb-4",
        ),

        # dbc.Row(
        #     [
        #         dbc.Col(card("Detection Coverage", "detection-coverage-chart"), width=12),
        #     ],
        #     className="mb-4",
        # ),
        #
        # dbc.Row(
        #     [
        #         dbc.Col(card("Confidence Distribution", "confidence-distribution-chart"), width=6),
        #     ],
        #     className="mb-4",
        # ),

        modal_table(),
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
