import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.modal_table import modal_table

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

# Header + Table button + KPI Cards
header_with_button = dbc.Row(
    [
        dbc.Col(html.H2("Code Insights"), width="auto", className="d-flex align-items-center"),
        dbc.Col(
            html.Div(
                dbc.Button("Table", id="code-insights-table-btn", color="secondary", size="sm"),
                id="code-insights-table-link-container",
                className="d-flex justify-content-end align-items-center"
            ),
            width="auto",
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader("Files", className="text-center bg-light", style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                    dbc.CardBody([
                        html.H5("0", id="kpi-total-files", className="text-center"),
                        html.Small("LOC: 0", id="kpi-total-files-subtext", className="text-center text-muted d-block", style={"fontSize": "0.7rem"}),
                    ])
                ],
                className="mb-2",
            ),
            width=2,
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader("Functions", className="text-center bg-light", style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                    dbc.CardBody([
                        html.H5("0", id="kpi-total-functions", className="text-center"),
                        html.Small("Avg CCN: 0", id="kpi-total-functions-subtext", className="text-center text-muted d-block", style={"fontSize": "0.7rem"}),
                    ])
                ],
                className="mb-2",
            ),
            width=2,
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader("Complexity", className="text-center bg-light", style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                    dbc.CardBody([
                        html.H5("0", id="kpi-total-ccn", className="text-center"),
                        html.Small("per 1000 LOC", id="kpi-total-ccn-subtext", className="text-center text-muted d-block", style={"fontSize": "0.7rem"}),
                    ])
                ],
                className="mb-2",
            ),
            width=2,
        ),
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader("Repos", className="text-center bg-light", style={"fontSize": "0.8rem", "whiteSpace": "nowrap"}),
                    dbc.CardBody([
                        html.H5("0", id="kpi-total-repos", className="text-center"),
                        html.Small("w/ Lizard Data", id="kpi-total-repos-subtext", className="text-center text-muted d-block", style={"fontSize": "0.7rem"}),
                    ])
                ],
                className="mb-2",
            ),
            width=2,
        ),
    ],
    className="mb-3 align-items-center g-2",
    justify="start"
)

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),

        header_with_button,

        # Charts
        card("Language Role Distribution", "role-distribution-chart"),

        # Normalized + Markup side by side (50:50)
        dbc.Row([
            dbc.Col(card("Language Usage vs. Code Density", "language-bubble-chart"), width=6),
            dbc.Col(card("Markup/Data Language Usage", "markup-language-usage-chart"), width=6),
        ], className="mb-4"),

        # Gitlog charts
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

        # Lizard charts
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