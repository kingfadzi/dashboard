from dash import dash_table
import dash_bootstrap_components as dbc
from dash import html

def table_layout(data, total_count, page_current, page_size):
    return dbc.Card(
        [
            dbc.CardHeader(html.H5("Repository Overview Table")),
            dbc.CardBody(
                dash_table.DataTable(
                    id="overview-table",
                    columns=[
                        {"name": "Repo Name", "id": "repo_id", "type": "text", "presentation": "markdown"},
                        {"name": "TC", "id": "tc", "type": "numeric"},
                        {"name": "App ID", "id": "app_id", "type": "text"},
                        {"name": "Status", "id": "activity_status", "type": "text"},
                        {"name": "Size", "id": "classification_label", "type": "text"},
                        {"name": "Age", "id": "repo_age_days", "type": "text"},
                        {"name": "Language", "id": "all_languages", "type": "text"},
                        {"name": "Scope", "id": "scope", "type": "text"},
                        {"name": "Commits", "id": "total_commits", "type": "numeric"},
                        {"name": "Contributors", "id": "number_of_contributors", "type": "numeric"},
                        {"name": "Last Commit", "id": "last_commit_date", "type": "datetime"},
                    ],
                    data=data,
                    page_current=page_current,
                    page_size=page_size,
                    page_action="custom",
                    markdown_options={"html": True},
                    tooltip_data=[
                        {
                            k: {"value": str(v), "type": "text"} if k in ["tc", "app_id"] else {"value": "", "type": "text"}
                            for k, v in row.items()
                        }
                        for row in data
                    ],
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
            )
        ],
        className="mb-4 shadow-sm"
    )