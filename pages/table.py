import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/table")

layout = dbc.Container(
    [
        html.H1("Repository Data Table", className="text-center mb-4"),
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
                        {"name": "Language", "id": "language", "type": "text"},
                        {
                            "name": "Commits",
                            "id": "commits",
                            "type": "numeric",
                            "format": {"specifier": ",d"},
                        },
                        {
                            "name": "Contributors",
                            "id": "contributors",
                            "type": "numeric",
                            "format": {"specifier": ",d"},
                        },
                        {
                            "name": "Last Commit",
                            "id": "last_commit",
                            "type": "text",
                        },
                    ],
                    data=[],
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left"},
                    sort_action="native",
                    filter_action="native",
                ),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)