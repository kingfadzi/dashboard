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
                    dbc.CardBody(
                        dash_table.DataTable(
                            id="temp-table",
                            columns=[
                                {"name": "Repo Name", "id": "repo_id", "type": "text", "presentation": "markdown"},
                                {"name": "Language", "id": "language", "type": "text"},
                                {"name": "Commits", "id": "commits", "type": "numeric", "format": {"specifier": ",d"}},
                                {"name": "Contributors", "id": "contributors", "type": "numeric", "format": {"specifier": ",d"}},
                                {"name": "Last Commit", "id": "last_commit", "type": "text"},
                            ],
                            data=[],
                            page_size=10,
                            style_table={"overflowX": "auto"},
                            style_cell={"textAlign": "left"},
                            sort_action="native",
                            filter_action="native",
                        ),
                        className="p-0 flex-fill",
                    ),
                ],
                className="mb-4 h-100 d-flex flex-column",
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
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="active-inactive-bar",
                                        config={"displayModeBar": False, "responsive": True},
                                        style={"width": "100%", "height": "100%"},
                                    ),
                                    className="p-0 flex-fill",
                                ),
                            ],
                            className="mb-4 h-100 d-flex flex-column",
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
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="classification-pie",
                                        config={"displayModeBar": False, "responsive": True},
                                        style={"width": "100%", "height": "100%"},
                                    ),
                                    className="p-0 flex-fill",
                                ),
                            ],
                            className="mb-4 h-100 d-flex flex-column",
                        ),
                        width=6,
                    ),
                ],
                className="mb-4",
                style={"height": "400px"},
            ),

            # Code Contribution Scatter
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.B("Code Contribution Activity", className="text-center"),
                        className="bg-light",
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="scatter-plot",
                            config={"displayModeBar": False, "responsive": True},
                            style={"width": "100%", "height": "100%"},
                        ),
                        className="p-0 flex-fill",
                    ),
                ],
                className="mb-4 h-100 d-flex flex-column",
                style={"height": "300px"},
            ),

            # Primary Language Bar
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.B("Primary Language in Multilingual Repos", className="text-center"),
                        className="bg-light",
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="repos-by-language-bar",
                            config={"displayModeBar": False, "responsive": True},
                            style={"width": "100%", "height": "100%"},
                        ),
                        className="p-0 flex-fill",
                    ),
                ],
                className="mb-4 h-100 d-flex flex-column",
                style={"height": "300px"},
            ),

            # Row: Language Usage Buckets & Last Commit Date
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.B("Num of Languages Used per Repo", className="text-center"),
                                    className="bg-light",
                                ),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="language-usage-buckets-bar",
                                        config={"displayModeBar": False, "responsive": True},
                                        style={"width": "100%", "height": "100%"},
                                    ),
                                    className="p-0 flex-fill",
                                ),
                            ],
                            className="mb-4 h-100 d-flex flex-column",
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
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="last-commit-buckets-bar",
                                        config={"displayModeBar": False, "responsive": True},
                                        style={"width": "100%", "height": "100%"},
                                    ),
                                    className="p-0 flex-fill",
                                ),
                            ],
                            className="mb-4 h-100 d-flex flex-column",
                        ),
                        width=6,
                    ),
                ],
                className="mb-4",
                style={"height": "400px"},
            ),

            # CLOC Metrics Card
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.B("Total Lines of Code", className="text-center"),
                        className="bg-light",
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="cloc-bar-chart",
                            config={"displayModeBar": False, "responsive": True},
                            style={"width": "100%", "height": "100%"},
                        ),
                        className="p-0 flex-fill",
                    ),
                ],
                className="mb-4 h-100 d-flex flex-column",
                style={"height": "300px"},
            ),

            # IaC Usage Card
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.B("Infrastructure as Code Usage", className="text-center"),
                        className="bg-light",
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="iac-bar-chart",
                            config={"displayModeBar": False, "responsive": True},
                            style={"width": "100%", "height": "100%"},
                        ),
                        className="p-0 flex-fill",
                    ),
                ],
                className="mb-4 h-100 d-flex flex-column",
                style={"height": "300px"},
            ),

            # Heatmap Card
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.B("Code Contribution by Language", className="text-center"),
                        className="bg-light",
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="language-contributors-heatmap",
                            config={"displayModeBar": False, "responsive": True},
                            style={"width": "100%", "height": "100%"},
                        ),
                        className="p-0 flex-fill",
                    ),
                ],
                className="mb-4 h-100 d-flex flex-column",
                style={"height": "400px"},
            ),

            # Row: Vulnerabilities & Standards
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.B("Vulnerabilities by Severity (Shallow scan)", className="text-center"),
                                    className="bg-light",
                                ),
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="trivy-vulnerabilities-bar-chart",
                                        config={"displayModeBar": False, "responsive": True},
                                        style={"width": "100%", "height": "100%"},
                                    ),
                                    className="p-0 flex-fill",
                                ),
                            ],
                            className="mb-4 h-100 d-flex flex-column",
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
                                dbc.CardBody(
                                    dcc.Graph(
                                        id="semgrep-findings-bar-chart",
                                        config={"displayModeBar": False, "responsive": True},
                                        style={"width": "100%", "height": "100%"},
                                    ),
                                    className="p-0 flex-fill",
                                ),
                            ],
                            className="mb-4 h-100 d-flex flex-column",
                        ),
                        width=6,
                    ),
                ],
                className="mb-4",
                style={"height": "400px"},
            ),

            # Label-Tech & Package-Type sections unchanged…
            html.Div(id="label-tech-layout"),
            html.Div(
                id="package-type-card-container",
                children=[
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                html.B("Package Type Distribution", className="text-center"),
                                className="bg-light",
                            ),
                            dbc.CardBody(
                                dcc.Graph(
                                    id="package-type-bar-chart",
                                    config={"displayModeBar": False, "responsive": True},
                                    style={"width": "100%", "height": "100%"},
                                ),
                                className="p-0 flex-fill",
                            ),
                        ],
                        className="mb-4 h-100 d-flex flex-column",
                    )
                ],
            ),
        ],
        className="h-100",
    )
