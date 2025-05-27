# pages/overview.py

import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from layouts.layout_kpi import kpi_layout
from layouts.layout_filters import filter_layout
from config.config import DEFAULT_FILTERS

# Register this page
dash.register_page(__name__, path="/overview", name="Overview")

layout = dbc.Container(
    [

        dcc.Location(id="url", refresh=False),

        # Header row with H2 and matching Table button
        dbc.Row(
            [
                dbc.Col(html.H2("Overview"), width="auto"),
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
        ),

        # Filter layout placeholder (uncomment to enable)
        html.Div(
            # filter_layout(),
            style={"marginTop": "0px", "paddingTop": "0px"},
        ),

        # KPI Cards
        kpi_layout(),

        # First row of charts
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.B("Repo Status", className="text-center"), className="bg-light"),
                            dcc.Graph(id="active-inactive-bar", config={"displayModeBar": False}, style={"height": 300}),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.B("Repository Sizes", className="text-center"), className="bg-light"),
                            dcc.Graph(id="classification-pie", config={"displayModeBar": False}, style={"height": 300}),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Total Lines of Code card
        dbc.Card(
            [
                dbc.CardHeader(html.B("Total Lines of Code", className="text-center"), className="bg-light"),
                dcc.Graph(id="cloc-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
            ],
            className="mb-4",
        ),

        # Code Contribution Activity card
        dbc.Card(
            [
                dbc.CardHeader(html.B("Code Contribution Activity", className="text-center"), className="bg-light"),
                dcc.Graph(id="scatter-plot", config={"displayModeBar": False}, style={"height": 300}),
            ],
            className="mb-4",
        ),

        # Primary Language in Multilingual Repos card

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.B("Primary Language in Multilingual Repos", className="text-center"), className="bg-light"),
                            dcc.Graph(id="repos-by-language-bar", config={"displayModeBar": False}, style={"height": 300}),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.B("Package Type Distribution", className="text-center"), className="bg-light"),
                            dcc.Graph(id="package-type-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Second row of charts
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.B("Num of Languages Used per Repo", className="text-center"), className="bg-light"),
                            dcc.Graph(id="language-usage-buckets-bar", config={"displayModeBar": False}, style={"height": 300}),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.B("Last Commit Date", className="text-center"), className="bg-light"),
                            dcc.Graph(id="last-commit-buckets-bar", config={"displayModeBar": False}, style={"height": 300}),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Infrastructure as Code Usage card
        dbc.Card(
            [
                dbc.CardHeader(html.B("Infrastructure as Code Usage", className="text-center"), className="bg-light"),
                dcc.Graph(id="iac-bar-chart", config={"displayModeBar": False}, style={"height": 450}),
            ],
            className="mb-4",
            id="iac-card",
        ),

        # Code Contribution by Language card
        dbc.Card(
            [
                dbc.CardHeader(html.B("Code Contribution by Language", className="text-center"), className="bg-light"),
                dcc.Graph(id="language-contributors-heatmap", config={"displayModeBar": False}, style={"height": 600}),
            ],
            className="mb-4",
        ),

        # Third row of charts
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.B("Vulnerabilities by Severity (Shallow scan)", className="text-center"), className="bg-light"),
                            dcc.Graph(id="trivy-vulnerabilities-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.B("Standards Issues", className="text-center"), className="bg-light"),
                            dcc.Graph(id="semgrep-findings-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Application Server Usage card
        dbc.Card(
            [
                dbc.CardHeader(html.B("Application Server Usage", className="text-center"), className="bg-light"),
                dcc.Graph(id="appserver-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
            ],
            className="mb-4",
            id="appserver-card",
        ),

        # Top Developer Frameworks card
        dbc.Card(
            [
                dbc.CardHeader(html.B("Top Developer Frameworks", className="text-center"), className="bg-light"),
                dcc.Graph(id="dev-frameworks-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
            ],
            className="mb-4",
            id="dev-frameworks-card",
        ),


    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)

# Shared Table Modal (reuses code_insights_modal callbacks)
layout.children.append(
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
                dbc.Button("Close", id="code-insights-modal-close", className="ms-auto", n_clicks=0)
            ),
        ],
        id="code-insights-modal",
        size="xl",
        is_open=False,
        scrollable=True,
    )
)

# Shared filter stores
layout.children.append(dcc.Store(id="default-filter-store", data=DEFAULT_FILTERS))
layout.children.append(dcc.Store(id="filters-applied-trigger", data=None))
