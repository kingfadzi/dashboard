# pages/overview.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from config.config import DEFAULT_FILTERS
from layouts.layout_kpi import kpi_layout
from components.modal_table import modal_table

dash.register_page(__name__, path="/overview", name="Overview")

# Header with page title and Table button
header_with_button = dbc.Row(
    [
        dbc.Col(html.H2("Overview"), width="auto"),
        dbc.Col(
            dbc.Button("Table", id="modal-open", color="secondary", size="sm"),
            width="auto",
            className="d-flex align-items-center justify-content-end",
        ),
    ],
    className="mb-2 align-items-center",
)

layout = dbc.Container(
    [
        header_with_button,

        # KPI cards section
        kpi_layout(),

        # First row of charts
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.B("Repo Status", className="text-center"),
                                className="bg-light",
                            ),
                            dcc.Graph(
                                id="active-inactive-bar",
                                config={"displayModeBar": False},
                                style={"height": 300},
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.B("Repository Sizes", className="text-center"),
                                className="bg-light",
                            ),
                            dcc.Graph(
                                id="classification-pie",
                                config={"displayModeBar": False},
                                style={"height": 300},
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Total Lines of Code
        dbc.Card(
            [
                dbc.CardHeader(
                    html.B("Total Lines of Code", className="text-center"),
                    className="bg-light",
                ),
                dcc.Graph(
                    id="cloc-bar-chart",
                    config={"displayModeBar": False},
                    style={"height": 300},
                ),
            ],
            className="mb-4",
        ),

        # Code Contribution Activity
        dbc.Card(
            [
                dbc.CardHeader(
                    html.B("Code Contribution Activity", className="text-center"),
                    className="bg-light",
                ),
                dcc.Graph(
                    id="scatter-plot",
                    config={"displayModeBar": False},
                    style={"height": 300},
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
                            dbc.CardHeader(
                                html.B(
                                    "Primary Language in Multilingual Repos",
                                    className="text-center",
                                ),
                                className="bg-light",
                            ),
                            dcc.Graph(
                                id="repos-by-language-bar",
                                config={"displayModeBar": False},
                                style={"height": 300},
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.B("Package Type Distribution", className="text-center"),
                                className="bg-light",
                            ),
                            dcc.Graph(
                                id="package-type-bar-chart",
                                config={"displayModeBar": False},
                                style={"height": 300},
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Third row of charts
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.B(
                                    "Num of Languages Used per Repo",
                                    className="text-center",
                                ),
                                className="bg-light",
                            ),
                            dcc.Graph(
                                id="language-usage-buckets-bar",
                                config={"displayModeBar": False},
                                style={"height": 300},
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.B("Last Commit Date", className="text-center"),
                                className="bg-light",
                            ),
                            dcc.Graph(
                                id="last-commit-buckets-bar",
                                config={"displayModeBar": False},
                                style={"height": 300},
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Infrastructure as Code Usage
        dbc.Card(
            [
                dbc.CardHeader(
                    html.B("Infrastructure as Code Usage", className="text-center"),
                    className="bg-light",
                ),
                dcc.Graph(
                    id="iac-bar-chart",
                    config={"displayModeBar": False},
                    style={"height": 450},
                ),
            ],
            className="mb-4",
            id="iac-card",
        ),

        # Code Contribution by Language
        dbc.Card(
            [
                dbc.CardHeader(
                    html.B("Code Contribution by Language", className="text-center"),
                    className="bg-light",
                ),
                dcc.Graph(
                    id="language-contributors-heatmap",
                    config={"displayModeBar": False},
                    style={"height": 600},
                ),
            ],
            className="mb-4",
        ),

        # Vulnerabilities and Standards
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.B(
                                    "Vulnerabilities by Severity (Shallow scan)",
                                    className="text-center",
                                ),
                                className="bg-light",
                            ),
                            dcc.Graph(
                                id="trivy-vulnerabilities-bar-chart",
                                config={"displayModeBar": False},
                                style={"height": 300},
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.B("Standards Issues", className="text-center"),
                                className="bg-light",
                            ),
                            dcc.Graph(
                                id="semgrep-findings-bar-chart",
                                config={"displayModeBar": False},
                                style={"height": 300},
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Application Server Usage
        dbc.Card(
            [
                dbc.CardHeader(
                    html.B("Application Server Usage", className="text-center"),
                    className="bg-light",
                ),
                dcc.Graph(
                    id="appserver-bar-chart",
                    config={"displayModeBar": False},
                    style={"height": 300},
                ),
            ],
            className="mb-4",
            id="appserver-card",
        ),

        # Top Developer Frameworks
        dbc.Card(
            [
                dbc.CardHeader(
                    html.B("Top Developer Frameworks", className="text-center"),
                    className="bg-light",
                ),
                dcc.Graph(
                    id="dev-frameworks-bar-chart",
                    config={"displayModeBar": False},
                    style={"height": 300},
                ),
            ],
            className="mb-4",
            id="dev-frameworks-card",
        ),

        # Shared modal + table
        modal_table(),

        dcc.Store(id="default-filter-store", data=DEFAULT_FILTERS),
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
