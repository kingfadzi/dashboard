# pages/graphs.py

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.layout_kpi import kpi_layout
from layouts.layout_filters import filter_layout

# Register this page at the root URL ("/")
dash.register_page(__name__, path="/")

layout = dbc.Container(
    [
        filter_layout(),
        # KPI Cards layout
        kpi_layout(),

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

        # Total Lines of Code moved here (fourth row)
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

        dbc.Card(
            [
                dbc.CardHeader(
                    html.B("Primary Language in Multilingual Repos", className="text-center"),
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

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.B("Num of Languages Use per repod", className="text-center"),
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

        dbc.Card(
            [
               dbc.CardHeader(
                     html.B("infrastructure as Code Usage", className="text-center"),
                     className="bg-light",
                      ),
                      dcc.Graph(
                          id="iac-bar-chart",
                          config={"displayModeBar": False},
                          style={"height": 300},
                      ),
                  ],
                  className="mb-4",
                  id="iac-card"   # added ID for conditional styling
              ),
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

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.B("Vulnerabilities by Severity (Shallow scan)", className="text-center"),
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
            id="appserver-card"
        ),

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
    id="dev-frameworks-card"  # <- this ID is already correct
),
      
      
    html.Div(
    id="package-type-card-container",
    children=[
        dbc.Card(
            [
                dbc.CardHeader(
                    html.B("Package Type Distribution", className="text-center"),
                    className="bg-light",
                ),
                dcc.Graph(
                    id="package-type-pie-chart",
                    config={"displayModeBar": False},
                    style={"height": 300},
                ),
            ],
            className="mb-4",
            id="package-type-card"
        )
    ]
),  
    
    ],
    fluid=True,
)