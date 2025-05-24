from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

def chart_layout():
    return dbc.Col(
        [
            # Repository Data Table
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.B("Repository Data Table", className="text-center"),
                        className="bg-light",
                    ),
                    dash_table.DataTable(
                        id="temp-table",
                        columns=[
                            {
                                "name": "Repo Name",
                                "id": "repo_id",
                                "type": "text",
                                "presentation": "markdown",
                            },
                            {"name": "Language", "id": "language", "type": "text"},
                            {
                                "name": "Commits",
                                "id": "commits",
                                "type": "numeric",
                                "format": {"specifier": ",d"},
                            },
                            {
                                "name": "Contributors",
                                "id": "contributors",
                                "type": "numeric",
                                "format": {"specifier": ",d"},
                            },
                            {
                                "name": "Last Commit",
                                "id": "last_commit",
                                "type": "text",
                            },
                        ],
                        data=[],
                        page_size=10,
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left"},
                        sort_action="native",
                        filter_action="native",
                    ),
                ],
                className="mb-4",
            ),

            # Row: Activity Status & Repository Classification
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

            # Contributors vs Commits Scatter Plot
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

            # Repositories by Main Language
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

            # Row: Language Usage Buckets & Repository Activity by Last Commit Date
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

            # CLOC Metrics by Language
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

            # Repositories by IaC Type
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
            ),

            # Programming Languages vs Contributor Buckets Heatmap
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

            # Row: Vulnerabilities by Severity & Standards Issues
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

            # Label Tech Charts (conditionally rendered by callback)
            html.Div(id="label-tech-layout"),
        ]
    )