import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from pages.layout_kpi import kpi_layout

dash.register_page(__name__, path="/overview", name="Overview")


def card(title, graph_id, height=300):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dcc.Loading(
                dcc.Graph(
                    id=graph_id,
                    config={"displayModeBar": False},
                    style={"height": height}
                )
            ),
        ],
        className="mb-2",  # reduced bottom margin
    )


header_with_button = dbc.Row(
    [
        dbc.Col(html.H2("Overview"), width="auto"),
        dbc.Col(
            html.Div(
                dbc.Button("Table", id="overview-table-btn", color="secondary", size="sm"),
                id="overview-table-link-container",
                className="d-flex justify-content-end"
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

        # KPI cards
        kpi_layout(),

        # Repo Status & Sizes
        dbc.Row(
            [
                dbc.Col(card("Repo Status", "active-inactive-bar"), width=6),
                dbc.Col(card("Repository Sizes", "classification-pie"), width=6),
            ],
            className="mb-2",  # reduced space between rows
        ),

        # LOC & Heatmap
        dbc.Row(
            [
                dbc.Col(card("Total Lines of Code (Top 10)", "cloc-bar-chart"), width=6),
                dbc.Col(card("Code Contribution by Language", "language-contributors-heatmap"), width=6),
            ],
            className="mb-2",
        ),

        # Scatter full width
        dbc.Row(
            [
                dbc.Col(card("Code Contribution Activity", "scatter-plot"), width=12),
            ],
            className="mb-2",
        ),

        # Primary Language & Package Type
        dbc.Row(
            [
                dbc.Col(card("Primary Language in Multilingual Repos (Top 10)", "repos-by-language-bar"), width=6),
                dbc.Col(card("Package Type Distribution", "package-type-bar-chart"), width=6),
            ],
            className="mb-2",
        ),

        # Language Usage & Last Commit
        dbc.Row(
            [
                dbc.Col(card("Num of Languages Used per Repo", "language-usage-buckets-bar"), width=6),
                dbc.Col(card("Last Commit Date", "last-commit-buckets-bar"), width=6),
            ],
            className="mb-2",
        ),

        # Framework Distribution full width
        dbc.Row(
            [
                dbc.Col(card("Framework Distribution", "framework-distribution-chart"), width=12),
            ],
            className="mb-2",
        ),

        # IaC & App Servers
        dbc.Row(
            [
                dbc.Col(card("Infrastructure as Code Usage", "iac-bar-chart"), width=6),
                dbc.Col(card("Application Server Usage", "appserver-bar-chart"), width=6),
            ],
            className="mb-2",
        ),

        # Vulnerabilities & Standards
        dbc.Row(
            [
                dbc.Col(card("Vulnerabilities by Severity (Shallow scan)", "trivy-vulnerabilities-bar-chart"), width=6),
                dbc.Col(card("Standards Issues", "semgrep-findings-bar-chart"), width=6),
            ],
            className="mb-2",
        ),

        # store for filter-triggering callbacks
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
