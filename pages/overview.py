import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from config.config import DEFAULT_FILTERS
from layouts.layout_kpi import kpi_layout
from components.modal_table import modal_table  # Optional if keeping modal fallback

dash.register_page(__name__, path="/overview", name="Overview")

def card(title, graph_id, height=300):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dcc.Loading(dcc.Graph(id=graph_id, config={"displayModeBar": False}, style={"height": height})),
        ],
        className="mb-4",
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

        # KPI cards section
        kpi_layout(),

        dbc.Row(
            [
                dbc.Col(html.Div("Repo Status", className="text-center fw-bold")),
                dbc.Col(html.Div("Repository Sizes", className="text-center fw-bold")),
            ],
        ),

        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="active-inactive-bar", config={"displayModeBar": False}, style={"height": 300}), width=6),
                dbc.Col(dcc.Graph(id="classification-pie", config={"displayModeBar": False}, style={"height": 300}), width=6),
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

        dbc.Row(
            [
                dbc.Col(card("Primary Language in Multilingual Repos", "repos-by-language-bar"), width=6),
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

        dbc.Card(
            [
                dbc.CardHeader(html.B("Infrastructure as Code Usage", className="text-center"), className="bg-light"),
                dcc.Graph(id="iac-bar-chart", config={"displayModeBar": False}, style={"height": 450}),
            ],
            className="mb-4",
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
                dbc.Col(card("Vulnerabilities by Severity (Shallow scan)", "trivy-vulnerabilities-bar-chart"), width=6),
                dbc.Col(card("Standards Issues", "semgrep-findings-bar-chart"), width=6),
            ],
            className="mb-4",
        ),

        dbc.Card(
            [
                dbc.CardHeader(html.B("Application Server Usage", className="text-center"), className="bg-light"),
                dcc.Graph(id="appserver-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
            ],
            id="appserver-card",
            className="mb-4",
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.B("Infrastructure as Code Usage", className="text-center"), className="bg-light"),
                dcc.Graph(id="iac-bar-chart", config={"displayModeBar": False}, style={"height": 450}),
            ],
            id="iac-card",
            className="mb-4",
        ),
        dbc.Card(
            [
                dbc.CardHeader(html.B("Top Developer Frameworks", className="text-center"), className="bg-light"),
                dcc.Graph(id="dev-frameworks-bar-chart", config={"displayModeBar": False}, style={"height": 300}),
            ],
            id="dev-frameworks-card",
            className="mb-4",
        ),

        # optional fallback if modal still needed
        # modal_table(),

        dcc.Store(id="default-filter-store"),
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)

