from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

def chart_layout():
    return dbc.Col(
        [
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.B("Repository Data Table", className="text-center"),
                        className="bg-light",
                    ),
                    dash_table.DataTable(
                        id="temp-table",
                        columns=[
                            {"name": "Repo Name", "id": "repo_name"},
                            {"name": "Language", "id": "language"},
                            {"name": "Commits", "id": "commits"},
                            {"name": "Contributors", "id": "contributors"},
                            {"name": "Last Commit", "id": "last_commit"},
                        ],
                        data=[],
                        page_size=10,
                        style_table={"overflowX": "auto"},
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
                                    html.B("Num of Languages Used per Repo", className="text-center"),
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
                        html.B("Infrastructure as Code Usage", className="text-center"),
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
                                    html.B("Vulnerabilities by Severity (Shallow Scan)", className="text-center"),
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

            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.B("Java Versions", className="text-center"),
                            className="bg-light",
                        ),
                        dcc.Graph(
                            id="label-tech-bar-chart-java-version",
                            config={"displayModeBar": False},
                            style={"height": 300},
                        ),
                    ], className="mb-4"),
                    width=6
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardHeader(
                            html.B("Build Tools", className="text-center"),
                            className="bg-light",
                        ),
                        dcc.Graph(
                            id="label-tech-bar-chart-build-tool",
                            config={"displayModeBar": False},
                            style={"height": 300},
                        ),
                    ], className="mb-4"),
                    width=6
                ),
            ], className="mb-4"),
        ]
    )