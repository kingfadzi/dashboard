from dash import html, dcc
import dash_bootstrap_components as dbc

def chart_layout(filters=None):
    return dbc.Container(
        [
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
                ]
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
                                dbc.CardHeader(html.B("Num of Languages Used", className="text-center"), className="bg-light"),
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
                ]
            ),

            dbc.Card(
                [
                    dbc.CardHeader(html.B("IaC Usage", className="text-center"), className="bg-light"),
                    dcc.Graph(id="iac-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                ],
                className="mb-4",
            ),

            dbc.Card(
                [
                    dbc.CardHeader(html.B("Language vs Contributors", className="text-center"), className="bg-light"),
                    dcc.Graph(id="language-contributors-heatmap", config={"displayModeBar": False}, style={"height": 600}),
                ],
                className="mb-4",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.B("Vulnerabilities (Trivy)", className="text-center"), className="bg-light"),
                                dcc.Graph(id="trivy-vulnerabilities-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                            ],
                            className="mb-4",
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.B("Standards Issues (Semgrep)", className="text-center"), className="bg-light"),
                                dcc.Graph(id="semgrep-findings-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                            ],
                            className="mb-4",
                        ),
                        width=6,
                    ),
                ]
            ),

            dbc.Card(
                [
                    dbc.CardHeader(html.B("App Server Usage", className="text-center"), className="bg-light"),
                    dcc.Graph(id="appserver-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                ],
                className="mb-4",
            ),

            dbc.Card(
                [
                    dbc.CardHeader(html.B("Top Developer Frameworks", className="text-center"), className="bg-light"),
                    dcc.Graph(id="dev-frameworks-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                ],
                className="mb-4",
            ),

            dbc.Card(
                [
                    dbc.CardHeader(html.B("Package Type Distribution", className="text-center"), className="bg-light"),
                    dcc.Graph(id="package-type-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
                ],
                className="mb-4",
            ),
        ],
        fluid=True,
        className="px-2"
    )