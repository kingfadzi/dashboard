import yaml
import json
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc

# Load YAML filters
with open("filters.yaml") as f:
    FILTERS = yaml.safe_load(f)["filters"]

# List of input IDs for use in callbacks
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
                                value=[],  # ensure options render
                                style={
                                    "fontSize": "14px",
                                    "whiteSpace": "nowrap",
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                },
                                persistence=True,
                                persistence_type="local",
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
                                persistence=True,
                                persistence_type="local",
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

# Optional: Debug callback (if store is global)
@callback(
    Output("filter-debug", "children"),
    Input("default-filter-store", "data"),
)
def debug_filter_store(data):
    return html.Pre(json.dumps(data, indent=2))