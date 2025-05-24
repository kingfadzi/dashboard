# pages/graphs.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.layout_kpi import kpi_layout
from layouts.layout_filters import filter_layout

# Register this page at /graphs
dash.register_page(__name__, path="/graphs")

layout = dbc.Container(
    [

        dcc.Location(id="url", refresh=False),

        # Compact filter row with inline 'Switch to Table View' link
        dbc.Row(
            [
                dbc.Col(
                    html.Div("Filters", className="text-muted small fw-bold mb-0"),
                    width="auto",
                ),
                dbc.Col(
                    html.A(
                        id="switch-to-table-link",
                        children="Switch to Table View",
                        href="/table",  # Will be overridden by callback
                        className="text-primary small fw-normal text-decoration-none",
                        target="_self",
                    ),
                    width="auto",
                    className="text-end",
                ),
            ],
            justify="between",
            className="align-items-center g-0",
            style={"margin": "0px", "padding": "0px"},
        ),

        # Filter layout, stripped of margin/padding
        html.Div(
            filter_layout(),
            style={"marginTop": "0px", "paddingTop": "0px"},
        ),

        # KPI Cards
        kpi_layout(),

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

        dbc.Card(
            [
                dbc.CardHeader(html.B("Total Lines of Code", className="text-center"), className="bg-light"),
                dcc.Graph(id="cloc-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
            ],
            className="mb-4",
        ),

        dbc.Card(
            [
                dbc.CardHeader(html.B("Code Contribution Activity", className="text-center"), className="bg-light"),
                dcc.Graph(id="scatter-plot", config={"displayModeBar": False}, style={"height": 300}),
            ],
            className="mb-4",
        ),

        dbc.Card(
            [
                dbc.CardHeader(html.B("Primary Language in Multilingual Repos", className="text-center"), className="bg-light"),
                dcc.Graph(id="repos-by-language-bar", config={"displayModeBar": False}, style={"height": 300}),
            ],
            className="mb-4",
        ),

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

        dbc.Card(
            [
                dbc.CardHeader(html.B("Infrastructure as Code Usage", className="text-center"), className="bg-light"),
                dcc.Graph(id="iac-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
            ],
            className="mb-4",
            id="iac-card",
        ),

        dbc.Card(
            [
                dbc.CardHeader(html.B("Code Contribution by Language", className="text-center"), className="bg-light"),
                dcc.Graph(id="language-contributors-heatmap", config={"displayModeBar": False}, style={"height": 600}),
            ],
            className="mb-4",
        ),

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

        dbc.Card(
            [
                dbc.CardHeader(html.B("Application Server Usage", className="text-center"), className="bg-light"),
                dcc.Graph(id="appserver-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
            ],
            className="mb-4",
            id="appserver-card",
        ),

        dbc.Card(
            [
                dbc.CardHeader(html.B("Top Developer Frameworks", className="text-center"), className="bg-light"),
                dcc.Graph(id="dev-frameworks-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
            ],
            className="mb-4",
            id="dev-frameworks-card",
        ),

        html.Div(
            id="dependency-types-card-container",
            children=[
                dbc.Card(
                    [
                        dbc.CardHeader(html.B("Top Dependency Types", className="text-center"), className="bg-light"),
                        dcc.Graph(id="dependency-types-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                    ],
                    className="mb-4",
                    id="dependency-types-card",
                )
            ],
        ),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
