import yaml
import json
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc

# Load filter config from YAML
with open("filters.yaml") as f:
    FILTERS = yaml.safe_load(f)["filters"]

# All component IDs
FILTER_IDS = list(FILTERS.keys()) + ["app-id-filter"]

def filter_layout():
    return html.Div([
        dbc.Card(
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Dropdown(
                                id=fid,
                                options=conf.get("options", []),
                                placeholder=conf.get("placeholder", ""),
                                multi=True,
                                clearable=True,
                                value=[],  # <- Ensures options show
                                style={
                                    "fontSize": "14px",
                                    "whiteSpace": "nowrap",
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                },
                            ),
                            width=2
                        )
                        for fid, conf in FILTERS.items()
                    ] + [
                        dbc.Col(
                            dcc.Input(
                                id="app-id-filter",
                                type="text",
                                placeholder="Enter App ID or Repo Slug",
                                debounce=True,
                                className="form-control",
                                style={"fontSize": "14px"},
                                value=""  # <- Ensures it shows empty
                            ),
                            width=2
                        )
                    ],
                    align="center",
                    className="g-3",
                )
            ),
            className="bg-light mb-4",
        ),
        html.Div(id="filter-debug", style={'border': '1px solid gray', 'padding': '10px'})
    ])

# Debug output
@callback(
    Output("filter-debug", "children"),
    Input("default-filter-store", "data"),
)
def debug_filter_store(data):
    return html.Pre(json.dumps(data or {}, indent=2))