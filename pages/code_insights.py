import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import DEFAULT_FILTERS
from components.modal_table import modal_table
from layouts.layout_filters import filter_layout

dash.register_page(__name__, path="/code-insights", name="Code Insights")

def card(title, graph_id, height=300):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dcc.Loading(
                dcc.Graph(id=graph_id, config={"displayModeBar": False}, style={"height": height})
            ),
        ],
        className="mb-4",
    )

header_with_button = dbc.Row(
    [
        dbc.Col(html.H2("Code Insights"), width="auto"),
        dbc.Col(
            dbc.Button("Table", id="modal-open", color="secondary", size="sm"),
            width="auto",
            className="d-flex align-items-center justify-content-end",
        ),
    ],
    className="mb-2 align-items-center",
)

layout = dbc.Container(
    [
        header_with_button,

        # Language Insights
        card("Language Role Distribution", "role-distribution-chart"),
        card("Normalized Language Weight (Top 20)", "normalized-weight-chart"),
        dbc.Card(
            [
                dbc.CardHeader(html.B("Markup/Data Language Usage", className="text-center"), className="bg-light"),
                dbc.CardBody(
                    dcc.Loading(id="markup-language-usage-chart", type="default"),
                    className="p-0",
                ),
            ],
            className="mb-4",
        ),

        # Gitlog Insights
        dbc.Row(
            [
                dbc.Col(card("Average File Size (code_size / file_count)", "avg-file-size-chart"), width=6),
                dbc.Col(card("Contributor Dominance", "contributor-dominance-chart"), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(card("Branch Sprawl", "branch-sprawl-chart"), width=6),
                dbc.Col(card("Repository Age Buckets", "repo-age-chart"), width=6),
            ]
        ),

        # Cloc Insights
        dbc.Row(
            [
                dbc.Col(card("Code Volume", "code-volume-chart"), width=6),
                dbc.Col(card("File Count", "file-count-chart"), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(card("Code Composition", "code-composition-chart"), width=6),
                dbc.Col(card("File Size Scatter", "code-file-scatter-chart"), width=6),
            ]
        ),

        # Lizard Insights
        dbc.Row(
            [
                dbc.Col(card("Total Cyclomatic Complexity", "total-ccn-chart"), width=6),
                dbc.Col(card("Function Count (Modularity vs Monoliths)", "function-count-chart"), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(card("Total Logical Lines of Code", "total-nloc-chart"), width=6),
                dbc.Col(card("Complexity vs Function Count", "ccn-vs-function-count-chart"), width=6),
            ]
        ),

        # Shared modal + table
        modal_table,

        # Stores for filters
        dcc.Store(id="default-filter-store", data=DEFAULT_FILTERS),
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
