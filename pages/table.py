# pages/table.py

import dash
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/table")

layout = dbc.Container(
    [
        dbc.Card(
            [
                dash_table.DataTable(
                    id="temp-table",
                    columns=[
                        {
                            "name": "Repo Name",
                            "id": "repo_id",
                            "type": "text",
                            "presentation": "markdown",
                        },
                        {
                            "name": "TC",
                            "id": "tc",
                            "type": "numeric",
                            "format": {"specifier": ",d"},
                        },
                        {
                            "name": "App ID",
                            "id": "app_id",
                            "type": "text",
                        },
                        {
                            "name": "Language",
                            "id": "main_language",
                            "type": "text",
                        },
                        {
                            "name": "Commits",
                            "id": "total_commits",
                            "type": "numeric",
                            "format": {"specifier": ",d"},
                        },
                        {
                            "name": "Contributors",
                            "id": "number_of_contributors",
                            "type": "numeric",
                            "format": {"specifier": ",d"},
                        },
                        {
                            "name": "Last Commit",
                            "id": "last_commit_date",
                            "type": "text",
                        },
                    ],
                    data=[],  # Will be populated by callback
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_header={
                        "backgroundColor": "#f8f9fa",
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
                        {"if": {"row_index": "odd"}, "backgroundColor": "#f9f9f9"},
                        {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"},
                        {
                            "if": {"state": "active"},
                            "backgroundColor": "#e9ecef",
                            "border": "1px solid #adb5bd",
                        },
                    ],
                    sort_action="native",
                    filter_action="native",
                    filter_options={"case": "insensitive"},
                    column_selectable="single",
                ),
            ],
            className="shadow-sm rounded",
            style={"border": "1px solid #dee2e6", "overflow": "hidden"},
        ),

        # Re-Scan Button
        html.Div(
            [
                dbc.Button(
                    "Re-Scan Current Filtered Repositories",
                    id="rescan-button",
                    color="primary",
                    className="mt-3",
                ),
                dcc.Loading(
                    id="loading-rescan",
                    type="circle",
                    children=html.Div(id="rescan-status", className="mt-2 text-success"),
                ),
            ],
            className="text-center",
        ),
    ],
    fluid=True,
)