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
                            {"name": "Status", "id": "activity_status", "type": "text"},
                            {"name": "Size", "id": "classification_label", "type": "text"},
                            {"name": "Age", "id": "repo_age_days", "type": "text"},
                            {"name": "Language", "id": "all_languages", "type": "text"},
                            {"name": "Scope", "id": "scope", "type": "text"},
                            {"name": "Commits", "id": "total_commits", "type": "numeric", "format": {"specifier": ",d"}},
                            {"name": "Contributors", "id": "number_of_contributors", "type": "numeric", "format": {"specifier": ",d"}},
                            {"name": "Last Commit", "id": "last_commit_date", "type": "datetime"},
                        ],
                        data=[],
                        markdown_options={"html": True},
                        page_action="custom",
                        page_current=0,
                        page_size=10,
                        #sort_action="native",
                        #filter_action="custom",
                        tooltip_duration=None,
                        tooltip_data=[],
                        style_table={"overflowX": "auto"},
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
                    )
                ),
            ],
            className="shadow-sm rounded mb-4",
            style={"border": "1px solid #dee2e6", "overflow": "hidden"},
        ),
    ],
    fluid=True,
)
