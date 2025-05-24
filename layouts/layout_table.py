from dash import html, dash_table
import dash_bootstrap_components as dbc

def table_layout(data, total_count, page_current, page_size):
    return dbc.Card(
        [
            dbc.CardHeader(html.H5("Repositories Overview", className="mb-0")),
            dbc.CardBody(
                dash_table.DataTable(
                    id="overview-table",
                    columns=[
                        {"name": "Repo", "id": "repo_id", "presentation": "markdown"},
                        {"name": "TC", "id": "tc"},
                        {"name": "App ID", "id": "app_id"},
                        {"name": "Status", "id": "activity_status"},
                        {"name": "Size", "id": "classification_label"},
                        {"name": "Age", "id": "repo_age_days"},
                        {"name": "Lang", "id": "all_languages"},
                        {"name": "Scope", "id": "scope"},
                        {"name": "Commits", "id": "total_commits", "type": "numeric"},
                        {"name": "Contributors", "id": "number_of_contributors", "type": "numeric"},
                        {"name": "Last Commit", "id": "last_commit_date"},
                    ],
                    data=data,
                    markdown_options={"html": True},
                    page_current=page_current,
                    page_size=page_size,
                    page_action="custom",
                    style_table={"overflowX": "auto"},
                    style_header={"fontWeight": "bold"},
                )
            )
        ],
        className="shadow-sm rounded"
    )