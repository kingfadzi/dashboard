import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.modal_table import modal_table

dash.register_page(__name__, path="/code-insights", name="Code Insights")

def card(title, graph_id, height=240):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light", style={"fontSize": "0.8rem"}),
            dcc.Loading(
                dcc.Graph(id=graph_id, config={"displayModeBar": False}, style={"height": height})
            ),
        ],
        className="mb-4",
    )

# Compact KPI section + header
header_with_kpis = dbc.Row(
    [
        dbc.Col(html.H2("Code Insights"), width="auto", className="align-self-center"),
        dbc.Col(
            html.Div(
                dbc.Button("Table", id="code-insights-table-btn", color="secondary", size="sm"),
                id="code-insights-table-link-container",
                className="d-flex justify-content-end"
            ),
            width="auto",
        ),
        dbc.Col(
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader("Files", className="text-center bg-light", style={"fontSize": "0.7rem"}),
                    dbc.CardBody([
                        html.H6("0", id="kpi-codeinsights-files", className="text-center", style={"fontSize": "1rem"}),
                        html.Small("per repo", className="text-center text-muted d-block", style={"fontSize": "0.65rem"})
                    ])
                ], className="mb-2"), width="auto"),

                dbc.Col(dbc.Card([
                    dbc.CardHeader("LOC", className="text-center bg-light", style={"fontSize": "0.7rem"}),
                    dbc.CardBody([
                        html.H6("0", id="kpi-codeinsights-loc", className="text-center", style={"fontSize": "1rem"}),
                        html.Small("avg", className="text-center text-muted d-block", style={"fontSize": "0.65rem"})
                    ])
                ], className="mb-2"), width="auto"),

                dbc.Col(dbc.Card([
                    dbc.CardHeader("CCN", className="text-center bg-light", style={"fontSize": "0.7rem"}),
                    dbc.CardBody([
                        html.H6("0", id="kpi-codeinsights-ccn", className="text-center", style={"fontSize": "1rem"}),
                        html.Small("avg", className="text-center text-muted d-block", style={"fontSize": "0.65rem"})
                    ])
                ], className="mb-2"), width="auto"),

                dbc.Col(dbc.Card([
                    dbc.CardHeader("Langs", className="text-center bg-light", style={"fontSize": "0.7rem"}),
                    dbc.CardBody([
                        html.H6("0", id="kpi-codeinsights-langs", className="text-center", style={"fontSize": "1rem"}),
                        html.Small("per repo", className="text-center text-muted d-block", style={"fontSize": "0.65rem"})
                    ])
                ], className="mb-2"), width="auto"),
            ],
            className="gx-2 justify-content-end"),
            width="auto",
        )
    ],
    className="mb-2 align-items-center justify-content-between",
)

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        header_with_kpis,

        # Charts
        card("Language Role Distribution", "role-distribution-chart"),

        dbc.Row([
            dbc.Col(card("Language Usage vs. Code Density", "language-bubble-chart"), width=6),
            dbc.Col(card("Markup/Data Language Usage", "markup-language-usage-chart"), width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(card("Average File Size (code_size / file_count)", "avg-file-size-chart"), width=6),
            dbc.Col(card("Top Contributor Dominance", "contributor-dominance-chart"), width=6),
        ]),
        dbc.Row([
            dbc.Col(card("Branch Sprawl", "branch-sprawl-chart"), width=6),
            dbc.Col(card("Repository Age Buckets", "repo-age-chart"), width=6),
        ]),

        dbc.Row([
            dbc.Col(card("Code Composition", "code-composition-chart"), width=6),
            dbc.Col(card("File Size Scatter", "code-file-scatter-chart"), width=6),
        ]),

        dbc.Row([
            dbc.Col(card("Complexity vs Function Count", "ccn-vs-function-count-chart"), width=6),
            dbc.Col(card("Function Count (Modularity vs Monoliths)", "function-count-chart"), width=6),
        ]),

        modal_table(),

        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)