# pages/table.py

import dash
from dash import html, dash_table
import dash_bootstrap_components as dbc

# Register this page at "/table"
dash.register_page(__name__, path="/table")

layout = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardHeader(
                    html.B("Repository Data Table", className="text-center"),
                    className="bg-light text-dark rounded-top",
                ),
                dash_table.DataTable(
                    id="temp-table",
                    columns=[
                        {"name": "Repo Name", "id": "repo_id", "type": "text", "presentation": "markdown"},
                        {"name": "Language", "id": "language", "type": "text"},
                        {"name": "Commits", "id": "commits", "type": "numeric", "format": {"specifier": ",d"}},
                        {"name": "Contributors", "id": "contributors", "type": "numeric", "format": {"specifier": ",d"}},
                        {"name": "Last Commit", "id": "last_commit", "type": "text"},
                    ],
                    data=[],  # Will be populated by callback
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_header={
                        "backgroundColor": "#f8f9fa",  # Light grey background
                        "fontWeight": "bold",
                        "borderBottom": "2px solid #dee2e6",
                        "textAlign": "left",
                    },
                    style_cell={
                        "textAlign": "left",
                        "padding": "10px",
                        "borderBottom": "1px solid #dee2e6",
                    },
                    style_data_conditional=[
                        {"if": {"row_index": "odd"}, "backgroundColor": "#f9f9f9"},  # Zebra striping
                        {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"},
                        {
                            "if": {"state": "active"},  # Highlight on selection
                            "backgroundColor": "#e9ecef",
                            "border": "1px solid #adb5bd",
                        },
                    ],
                ),
            ],
            className="shadow-sm rounded",  # Matches filter styling
            style={"border": "1px solid #dee2e6", "overflow": "hidden"},
        ),
    ],
    fluid=True,
)