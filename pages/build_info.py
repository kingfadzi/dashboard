# pages/build_info.py

import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from layouts.layout_filters import filter_layout
from config.config import DEFAULT_FILTERS

dash.register_page(__name__, path="/build-info", name="Build Info")

# Reusable card helper
def card(title, graph_id, height=300):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dbc.CardBody(
                dcc.Loading(
                    dcc.Graph(
                        id=graph_id,
                        config={"displayModeBar": False},
                        style={"height": f"{height}px"}
                    )
                ),
                className="p-0"
            ),
        ],
        className="mb-4",
    )

# Header with title and Table button
header_with_button = dbc.Row(
    [
        dbc.Col(html.H2("Build Info"), width="auto"),
        dbc.Col(
            dbc.Button(
                "Table",
                id="code-insights-modal-open",
                color="secondary",
                size="sm",
                className="ms-auto",
            ),
            width="auto",
            className="d-flex align-items-center justify-content-end",
        ),
    ],
    className="mb-2",
)

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        header_with_button,

        # Optional filters
        html.Div(
            # filter_layout(),
            style={"marginTop": "0px", "paddingTop": "0px"},
        ),

        # First row of cards
        dbc.Row(
            [
                dbc.Col(card("Detection Coverage", "detection-coverage-chart"), width=6),
                dbc.Col(card("Module Count", "module-count-chart"), width=6),
            ],
            className="mb-4",
        ),

        # Tool selector (not a chart)
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

        # Runtime versions (full width)
        dbc.Row(
            [dbc.Col(card("Runtime Versions", "runtime-versions-chart"), width=12)],
            className="mb-4",
        ),

        # Fragmentation & Status
        dbc.Row(
            [
                dbc.Col(card("Runtime Fragmentation", "runtime-fragmentation-chart"), width=6),
                dbc.Col(card("Status by Tool", "status-by-tool-chart"), width=6),
            ],
            className="mb-4",
        ),

        # Confidence distribution
        dbc.Row(
            [dbc.Col(card("Confidence Distribution", "confidence-distribution-chart"), width=6)],
            className="mb-4",
        ),

        # Shared Table Modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Repository Table")),
                dbc.ModalBody(
                    [
                        dbc.Alert(id="code-insights-total", color="info", is_open=False),
                        dcc.Loading(
                            dash_table.DataTable(
                                id="code-insights-table",
                                columns=[],
                                data=[],
                                page_current=0,
                                page_size=10,
                                page_action="custom",
                                sort_action="custom",
                                sort_mode="single",
                                sort_by=[],
                                export_format="csv",
                                style_table={"overflowX": "auto"},
                                style_cell={"textAlign": "left", "padding": "5px"},
                            )
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="code-insights-modal-close", className="ms-auto")
                ),
            ],
            id="code-insights-modal",
            size="xl",
            is_open=False,
            scrollable=True,
        ),

        # Shared stores
        dcc.Store(id="default-filter-store", data=DEFAULT_FILTERS),
        dcc.Store(id="filters-applied-trigger", data=None),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
