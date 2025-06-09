import yaml
import json
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc

# Load filters.yaml
with open("filters.yaml") as f:
    FILTERS = yaml.safe_load(f)["filters"]

FILTER_IDS = list(FILTERS.keys()) + ["app-id-filter"]

def chip_container(filter_id):
    return html.Div([
        dcc.Dropdown(
            id=filter_id,
            options=FILTERS[filter_id]["options"],
            placeholder=FILTERS[filter_id]["placeholder"],
            multi=True,
            clearable=True,
            value=[],
            style={"display": "none"},
        ),
        html.Div(id=f"{filter_id}-chips", style={"fontSize": "14px"})
    ])

def filter_layout():
    return html.Div([
        dbc.Card(
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(chip_container("host-name-filter"), width=2),
                    dbc.Col(chip_container("activity-status-filter"), width=2),
                    dbc.Col(chip_container("tc-filter"), width=2),
                    dbc.Col(chip_container("language-filter"), width=2),
                    dbc.Col(chip_container("classification-filter"), width=2),
                    dbc.Col(
                        dcc.Input(
                            id="app-id-filter",
                            type="text",
                            placeholder="Enter App ID or Repo Slug",
                            debounce=True,
                            value="",
                            className="form-control",
                            style={"fontSize": "14px"},
                        ), width=2
                    ),
                ],
                align="center",
                className="g-3")
            ),
            className="bg-light mb-4"
        ),
        html.Div(id="filter-debug", style={"border": "1px solid gray", "padding": "10px"})
    ])

# Callback to render chips for a field
def render_chip_callback(filter_id):
    @callback(
        Output(f"{filter_id}-chips", "children"),
        Input(filter_id, "value"),
        State(filter_id, "options"),
    )
    def update_chips(selected, options):
        if not selected:
            return html.Div(FILTERS[filter_id]["placeholder"], style={"color": "#999"})

        limit = 2
        visible = selected[:limit]
        hidden = len(selected) - limit

        chips = [
            dbc.Badge(
                next((o["label"] for o in options if o["value"] == v), v),
                color="primary",
                pill=True,
                className="me-1"
            ) for v in visible
        ]
        if hidden > 0:
            chips.append(html.Span(f"+{hidden} more", style={"color": "#555", "fontSize": "12px"}))

        return html.Div(chips, style={"whiteSpace": "nowrap", "overflow": "hidden", "textOverflow": "ellipsis"})

# Register one callback per field
for fid in FILTERS:
    render_chip_callback(fid)

# Show current filter state
@callback(
    Output("filter-debug", "children"),
    Input("default-filter-store", "data"),
)
def debug_filter_store(data):
    return html.Pre(json.dumps(data or {}, indent=2))