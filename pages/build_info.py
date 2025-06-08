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
                    config={"staticPlot": True},  # fully static (no hover)
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
                        "staticPlot": False,       # enable hover
                        "displayModeBar": False,   # hide toolbar
                        "scrollZoom": False        # disable scroll-zoom
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

        # First row: Detection Status & Runtime Fragmentation
        dbc.Row(
            [
                dbc.Col(card("Build Tool/Runtime Detection Coverage", "build-runtime-coverage-chart"), width=4),
                dbc.Col(card("Build Tool Detection Status", "status-by-tool-chart"), width=4),
                dbc.Col(card("Runtime Fragmentation", "runtime-fragmentation-chart"), width=4),
            ],
            className="mb-4",
        ),

        # Second row: No Build Tool scatter & language distribution
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



        # Combined row: Build Tools + Module Count
        dbc.Row(
            [
                dbc.Col(card("Build Tools", "build-tool-variant-chart"), width=8),
                dbc.Col(card("Module Count Per Repo", "module-count-chart"), width=4),
            ],
            className="mb-4",
        ),

        # Third row: Tool selector
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


        # Fourth row: Runtime Versions
        dbc.Row(
            [
                dbc.Col(card("Runtime Versions", "runtime-versions-chart"), width=12),
            ],
            className="mb-4",
        ),



        # Fifth row: Support Status (.NET + Java)
        dbc.Row(
            [
                dbc.Col(interactive_card("Support Status (.NET)", "dotnet-support-status-chart"), width=6),
                dbc.Col(interactive_card("Support Status (Java)", "java-support-status-chart"), width=6),
            ],
            className="mb-4",
        ),

        # Sixth row: Support Status (Python + JavaScript + Go)
        dbc.Row(
            [
                dbc.Col(interactive_card("Support Status (Python)", "python-support-status-chart"), width=4),
                dbc.Col(interactive_card("Support Status (JavaScript)", "js-support-status-chart"), width=4),
                dbc.Col(interactive_card("Support Status (Go)", "go-support-status-chart"), width=4),
            ],
            className="mb-4",
        ),



        # Detection Coverage as standalone
        dbc.Row(
            [
                dbc.Col(card("Detection Coverage", "detection-coverage-chart"), width=12),
            ],
            className="mb-4",
        ),

        # Confidence Distribution & Detection Status by Tool
        dbc.Row(
            [
                dbc.Col(card("Confidence Distribution", "confidence-distribution-chart"), width=6),

            ],
            className="mb-4",
        ),

        modal_table(),
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
