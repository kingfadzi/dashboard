import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from layouts.layout_kpi import kpi_layout
from components.modal_table import modal_table  # Optional if keeping modal fallback

dash.register_page(__name__, path="/overview", name="Overview")

def card(title, graph_id, height=300):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dcc.Loading(dcc.Graph(id=graph_id, config={"displayModeBar": False}, style={"height": height})),
        ],
        className="mb-4 h-100",
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

        # Repo status and sizes
        dbc.Row(
            [
                dbc.Col(card("Repo Status", "active-inactive-bar"), width=6),
                dbc.Col(card("Repository Sizes", "classification-pie"), width=6),
            ],
            className="mb-4",
        ),

        # LOC + Heatmap side by side (50:50)
        dbc.Row(
            [
                dbc.Col(card("Total Lines of Code (Top 10)", "cloc-bar-chart", height=400), width=6),
                dbc.Col(card("Code Contribution by Language", "language-contributors-heatmap", height=400), width=6),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(card("Code Contribution Activity", "scatter-plot")),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(card("Primary Language in Multilingual Repos (Top 10)", "repos-by-language-bar"), width=6),
                dbc.Col(card("Package Type Distribution", "package-type-bar-chart"), width=6),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(card("Num of Languages Used per Repo", "language-usage-buckets-bar"), width=6),
                dbc.Col(card("Last Commit Date", "last-commit-buckets-bar"), width=6),
            ],
            className="mb-4",
        ),

        dbc.Row([dbc.Col(card("Framework Distribution", "framework-distribution-chart"), width=12)], className="mb-4"),

        # IAC + App Servers side by side
        dbc.Row(
            [
                dbc.Col(card("Infrastructure as Code Usage", "iac-bar-chart", height=450), width=6),
                dbc.Col(card("Application Server Usage", "appserver-bar-chart", height=450), width=6),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(card("Vulnerabilities by Severity (Shallow scan)", "trivy-vulnerabilities-bar-chart"), width=6),
                dbc.Col(card("Standards Issues", "semgrep-findings-bar-chart"), width=6),
            ],
            className="mb-4",
        ),

        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)