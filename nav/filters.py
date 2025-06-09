import yaml
import json
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc

# Load from filters.yaml
with open("filters.yaml") as f:
    FILTERS = yaml.safe_load(f)["filters"]

# List of input field IDs
FILTER_IDS = list(FILTERS.keys()) + ["app-id-filter"]

# Safe dropdown styling: fixed width/height, no wrapping
DROPDOWN_STYLE = {
    "fontSize": "14px",
    "minWidth": "180px",
    "maxHeight": "38px",
    "whiteSpace": "nowrap",
}

def filter_layout():
    return html.Div([
        dbc.Card(
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id="host-name-filter",
                            options=FILTERS["host-name-filter"]["options"],
                            placeholder=FILTERS["host-name-filter"]["placeholder"],
                            multi=True,
                            clearable=True,
                            value=[],
                            style=DROPDOWN_STYLE,
                            persistence=True,
                            persistence_type="local",
                        ), width=2
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="activity-status-filter",
                            options=FILTERS["activity-status-filter"]["options"],
                            placeholder=FILTERS["activity-status-filter"]["placeholder"],
                            multi=True,
                            clearable=True,
                            value=[],
                            style=DROPDOWN_STYLE,
                            persistence=True,
                            persistence_type="local",
                        ), width=2
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="tc-filter",
                            options=FILTERS["tc-filter"]["options"],
                            placeholder=FILTERS["tc-filter"]["placeholder"],
                            multi=True,
                            clearable=True,
                            value=[],
                            style=DROPDOWN_STYLE,
                            persistence=True,
                            persistence_type="local",
                        ), width=2
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="language-filter",
                            options=FILTERS["language-filter"]["options"],
                            placeholder=FILTERS["language-filter"]["placeholder"],
                            multi=True,
                            clearable=True,
                            value=[],
                            style=DROPDOWN_STYLE,
                            persistence=True,
                            persistence_type="local",
                        ), width=2
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="classification-filter",
                            options=FILTERS["classification-filter"]["options"],
                            placeholder=FILTERS["classification-filter"]["placeholder"],
                            multi=True,
                            clearable=True,
                            value=[],
                            style=DROPDOWN_STYLE,
                            persistence=True,
                            persistence_type="local",
                        ), width=2
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="app-id-filter",
                            type="text",
                            placeholder="Enter App ID or Repo Slug",
                            debounce=True,
                            value="",
                            className="form-control",
                            style={"fontSize": "14px", "height": "38px"},
                            persistence=True,
                            persistence_type="local",
                        ), width=2
                    ),
                ],
                align="center",
                className="g-3")
            ),
            className="bg-light mb-4",
        ),
        html.Div(id="filter-debug", style={"border": "1px solid gray", "padding": "10px"})
    ])

@callback(
    Output("filter-debug", "children"),
    Input("default-filter-store", "data"),
)
def debug_filter_store(data):
    return html.Pre(json.dumps(data or {}, indent=2))