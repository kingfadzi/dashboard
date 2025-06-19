# File: pages/status/layout.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from pages.layout_filters import filter_layout

def card(title, count_id, color="light"):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className=f"bg-{color}"),
            dbc.CardBody(
                html.H3(id=count_id, className="card-title text-center"),
                className="py-3",
            ),
        ],
        className="mb-3",
    )

def get_status_layout():
    return dbc.Container(
        [
            dcc.Location(id="url", refresh=False),
            html.H2("Analysis Status", className="mt-4 mb-4"),

            # include filter store + tags
            filter_layout(),

            dbc.Row(
                [
                    dbc.Col(card("Waiting",      "status-waiting-count",     "secondary"), width=3),
                    dbc.Col(card("In Progress",  "status-in-progress-count", "info"),      width=3),
                    dbc.Col(card("Completed",    "status-completed-count",   "success"),   width=3),
                    dbc.Col(card("Failed",       "status-failed-count",      "danger"),    width=3),
                ],
                className="gx-2",
            ),
        ],
        fluid=True,
        className="p-4",
    )
