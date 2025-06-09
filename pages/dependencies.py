import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/dependencies", name="Dependencies")


def card(title, graph_id, height=400):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dbc.CardBody(
                dcc.Loading(
                    dcc.Graph(
                        id=graph_id,
                        config={"staticPlot": True},
                        style={"height": f"{height}px"},
                    )
                ),
                className="p-0",
            ),
        ],
        className="mb-4",
    )


header_with_button = dbc.Row(
    [
        dbc.Col(html.H2("Dependencies"), width="auto"),
        dbc.Col(
            html.Div(
                dbc.Button("Table", id="dependencies-table-btn", color="secondary", size="sm"),
                id="dependencies-table-link-container",
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

        # Row 1
        dbc.Row(
            [
                dbc.Col(card("Dependency Detection Coverage", "dep-detection-chart"), width=4),
                dbc.Col(card("Package Type Distribution", "package-type-distribution-chart"), width=4),
                dbc.Col(card("Average Dependencies / Repo", "avg-deps-per-package-type-chart"), width=4),
            ]
        ),

        html.Hr(),

        # Row 2
        dbc.Row([dbc.Col(card("Repos With Dependencies", "with-deps-by-variant-heatmap"), width=12)]),

        # Row 3
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.B("No Dependencies: Size vs Commits", className="text-center"), className="bg-light"),
                            dcc.Loading(
                                dcc.Graph(
                                    id="no-deps-scatter-chart",
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
                    width=6,
                ),
                dbc.Col(card("Repos Without Dependencies", "no-deps-heatmap"), width=6),
            ],
            className="mb-4",
        ),

        # Row 4
        dbc.Row(
            [
                dbc.Col(card("EE API Usage (Jakarta vs Javax)", "ee-usage-chart"), width=4),
                dbc.Col(card("Spring Framework Version Usage", "spring-core-version-chart"), width=4),
                dbc.Col(card("Spring Boot Core Version Usage", "spring-boot-version-chart"), width=4),
            ],
            className="mb-4",
        ),

        # Row 5
        dbc.Row([dbc.Col(card("Framework Distribution", "framework-distribution-chart"), width=12)], className="mb-4"),

        # Row 6: Middleware + App Servers
        dbc.Row(
            [
                dbc.Col(card("Application Servers / Orchestration Frameworks", "iac-server-orchestration-chart"), width=6),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                dbc.Row(
                                    [
                                        dbc.Col(html.B("Middleware Usage"), className="text-start"),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="middleware-subcategory-dropdown",
                                                placeholder="Select Middleware Category",
                                                clearable=True,
                                                value=None,
                                                style={"width": "250px", "fontSize": "14px"},
                                            ),
                                            width="auto",
                                        ),
                                    ],
                                    className="align-items-center justify-content-between",
                                ),
                                className="bg-light",
                            ),
                            dbc.CardBody(
                                dcc.Loading(
                                    dcc.Graph(
                                        id="middleware-subcategory-chart",
                                        config={"staticPlot": True},
                                        style={"height": "400px"},
                                    )
                                ),
                                className="p-0",
                            ),
                        ],
                        className="mb-4",
                    ),
                    width=6,
                ),
            ],
            className="mb-4",
        ),

        # Row 7: IaC Detection + Dependency Volume
        dbc.Row(
            [
                dbc.Col(card("IaC Detection Coverage", "iac-detection-chart"), width=6),
                dbc.Col(card("Dependency Volume", "dependency-volume-chart"), width=6),
            ],
            className="mb-4",
        ),

        # Row 8: All EOL Charts
        dbc.Row(
            [
                dbc.Col(card("EOL Detection Coverage", "xeol-detection-chart"), width=4),
                dbc.Col(card("EOL Top Dependencies", "xeol-top-products-chart"), width=4),
                dbc.Col(card("Top Expired Dependencies", "top-expired-xeol-products-chart"), width=4),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(card("Repos by Resource Type & Severity", "trivy-resource-type-chart"), width=4),
                dbc.Col(card("Top Vulnerable Packages", "trivy-packages-chart"), width=4),
                dbc.Col(card("Fix Availability by Severity", "trivy-fix-status-chart"), width=4),
            ],
            className="mb-4",
        ),


        # Row 9: IaC Category Summary + Adoption
        dbc.Row(
            [
                dbc.Col(card("IaC Category Summary", "iac-category-summary-chart"), width=6),
                dbc.Col(card("IaC Adoption", "iac-adoption-chart"), width=6),
            ],
            className="mb-4",
        ),

        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)