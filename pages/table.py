import dash
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from layouts.layout_filters import filter_layout

dash.register_page(__name__, path="/table")

layout = dbc.Container(
    [
        filter_layout(),

        dbc.Card(
            [
                dbc.CardHeader(
                    html.H5("Repositories Overview", className="mb-0")
                ),
                dbc.CardBody(
                    dash_table.DataTable(
                        id="temp-table",
                        columns=[
                            {"name": "Repo Name", "id": "repo_id", "type": "text", "presentation": "markdown"},
                            {"name": "TC", "id": "tc", "type": "numeric", "format": {"specifier": ",d"}},
                            {"name": "App ID", "id": "app_id", "type": "text"},
                            {"name": "Language", "id": "main_language", "type": "text"},
                            {"name": "Commits", "id": "total_commits", "type": "numeric", "format": {"specifier": ",d"}},
                            {"name": "Contributors", "id": "number_of_contributors", "type": "numeric", "format": {"specifier": ",d"}},
                            {"name": "Last Commit", "id": "last_commit_date", "type": "text"},
                        ],
                        data=[],  # Will be populated by callback
                        page_size=10,
                        markdown_options={"html": True},
                        style_table={
                            "overflowX": "auto",
                        },
                        style_header={
                            "backgroundColor": "#e9ecef",
                            "fontWeight": "bold",
                            "borderBottom": "2px solid #dee2e6",
                            "textAlign": "left",
                        },
                        style_cell={
                            "textAlign": "left",
                            "padding": "10px",
                            "borderBottom": "1px solid #dee2e6",
                            "maxWidth": "180px",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                            "whiteSpace": "nowrap",
                            "fontFamily": "system-ui, sans-serif",
                            "fontSize": "14px",
                        },
                        style_data_conditional=[
                            {"if": {"row_index": "odd"}, "backgroundColor": "#f8f9fa"},
                            {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"},
                            {"if": {"state": "active"}, "backgroundColor": "#e2e6ea", "border": "1px solid #adb5bd"},
                        ],
                        tooltip_duration=None,
                        tooltip_data=[],  # populated dynamically
                        sort_action="native",
                        filter_action="native",
                        filter_options={"case": "insensitive"},
                        column_selectable="single",
                    )
                ),
            ],
            className="shadow-sm rounded mb-4",
            style={"border": "1px solid #dee2e6", "overflow": "hidden"},
        ),

        dbc.Row(
            dbc.Col(
                [
                    dbc.Button(
                        "Re-Scan Current Filtered Repositories",
                        id="rescan-button",
                        color="primary",
                        size="lg",
                        className="mt-3",
                    ),
                    dcc.Loading(
                        id="loading-rescan",
                        type="circle",
                        children=html.Div(id="rescan-status", className="mt-3 text-success"),
                    ),
                ],
                className="text-center",
            )
        ),
    ],
    fluid=True,
)