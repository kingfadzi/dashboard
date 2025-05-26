import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.layout_filters import filter_layout

# Register page
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

layout = dbc.Container([
    html.H2("Code Insights"),

    # Language Insights
    card("Language Role Distribution", "role-distribution-chart"),
    card("Normalized Language Weight (Top 20)", "normalized-weight-chart"),

    # Gitlog Insights
    dbc.Row([
        dbc.Col(card("Average File Size (code_size / file_count)", "avg-file-size-chart"), width=6),
        dbc.Col(card("Contributor Dominance (Top Contributor % of Commits)", "contributor-dominance-chart"), width=6),
    ]),
    dbc.Row([
        dbc.Col(card("Branch Sprawl (Active Branch Count)", "branch-sprawl-chart"), width=6),
        dbc.Col(card("Repository Age Buckets", "repo-age-chart"), width=6),
    ]),

    # Cloc Insights
    dbc.Row([
        dbc.Col(card("Code Volume", "code-volume-chart"), width=6),
        dbc.Col(card("File Count", "file-count-chart"), width=6),
    ]),
    dbc.Row([
        dbc.Col(card("Code Composition", "code-composition-chart"), width=6),
        dbc.Col(card("File Size Scatter", "code-file-scatter-chart"), width=6),
    ]),

    # Lizard Insights
    dbc.Row([
        dbc.Col(card("Total Cyclomatic Complexity (Architectural Risk)", "total-ccn-chart"), width=6),
        dbc.Col(card("Function Count (Modularity vs Monoliths)", "function-count-chart"), width=6),
    ]),
    dbc.Row([
        dbc.Col(card("Total Logical Lines of Code", "total-nloc-chart"), width=6),
        dbc.Col(card("Complexity vs Function Count", "ccn-vs-function-count-chart"), width=6),
    ]),
], fluid=True, style={"marginTop": "0px", "paddingTop": "0px"})
