import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

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

# Header row with compact "Table" button
header_with_button = dbc.Row([
    dbc.Col(html.H2("Code Insights"), width="auto"),
    dbc.Col(
        dbc.Button("Table", id="code-insights-modal-open", color="secondary", size="sm", className="ms-auto"),
        width="auto",
        className="d-flex align-items-center justify-content-end"
    ),
], className="mb-2")

layout = dbc.Container([
    header_with_button,

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

    # Modal at the bottom
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Code Insights Table")),
            dbc.ModalBody([
                dbc.Alert(id="code-insights-total", color="info", className="py-2 px-3", is_open=False),
                dcc.Loading(
                    dash_table.DataTable(
                        id="code-insights-table",
                        columns=[],
                        data=[],
                        page_current=0,
                        page_size=10,
                        page_action="custom",
                        sort_action="custom",
                        sort_mode="single",
                        sort_by=[],
                        style_table={"overflowX": "auto"},
                        style_cell={"textAlign": "left", "padding": "5px"},
                        export_format="csv"
                    )
                )
            ]),
            dbc.ModalFooter(
                dbc.Button("Close", id="code-insights-modal-close", className="ms-auto", n_clicks=0)
            ),
        ],
        id="code-insights-modal",
        size="xl",
        is_open=False,
        scrollable=True
    )
], fluid=True, style={"marginTop": "0px", "paddingTop": "0px"})
