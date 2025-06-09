import yaml
import json
import dash
from dash import dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc

# Load filters.yaml
with open("filters.yaml") as f:
    FILTERS = yaml.safe_load(f)["filters"]

FILTER_IDS = list(FILTERS.keys()) + ["app-id-filter"]

def chip_field(filter_id):
    return html.Div([
        dcc.Store(id=f"{filter_id}-store", storage_type="local"),
        html.Div(id=f"{filter_id}-chips", n_clicks=0, style={"cursor": "pointer"}),
        dcc.Dropdown(
            id=filter_id,
            options=FILTERS[filter_id]["options"],
            placeholder=FILTERS[filter_id]["placeholder"],
            multi=True,
            clearable=True,
            value=[],
            style={"display": "none"},
        )
    ])

def filter_layout():
    return html.Div([
        dbc.Card(
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(chip_field("host-name-filter"), width=2),
                    dbc.Col(chip_field("activity-status-filter"), width=2),
                    dbc.Col(chip_field("tc-filter"), width=2),
                    dbc.Col(chip_field("language-filter"), width=2),
                    dbc.Col(chip_field("classification-filter"), width=2),
                    dbc.Col(
                        dcc.Input(
                            id="app-id-filter",
                            type="text",
                            placeholder="Enter App ID or Repo Slug",
                            debounce=True,
                            value="",
                            className="form-control",
                            style={"fontSize": "14px", "height": "38px"},
                        ),
                        width=2
                    ),
                ], align="center", className="g-3")
            ),
            className="bg-light mb-4",
        ),
        html.Div(id="filter-debug", style={"border": "1px solid gray", "padding": "10px"})
    ])

# Show chips with "+N more" summary
def render_chip_callback(filter_id):
    @callback(
        Output(f"{filter_id}-chips", "children"),
        Input(f"{filter_id}-store", "data"),
        State(f"{filter_id}", "options"),
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

# Toggle dropdown open/close
def toggle_dropdown_callback(filter_id):
    @callback(
        Output(filter_id, "style"),
        Output(f"{filter_id}-chips", "style"),
        Input(f"{filter_id}-chips", "n_clicks"),
        Input(filter_id, "value"),
        prevent_initial_call=True
    )
    def toggle_dropdown(chip_clicks, value):
        trigger = dash.callback_context.triggered_id
        if trigger == f"{filter_id}-chips":
            return {"display": "block"}, {"display": "none"}
        else:
            return {"display": "none"}, {"display": "block"}

# Sync dropdown values into store
def sync_selection_store_callback(filter_id):
    @callback(
        Output(f"{filter_id}-store", "data"),
        Input(filter_id, "value"),
    )
    def sync_to_store(value):
        return value

# Register all callbacks for each field
for fid in FILTERS:
    render_chip_callback(fid)
    toggle_dropdown_callback(fid)
    sync_selection_store_callback(fid)

# Show all filter values for debug
@callback(
    Output("filter-debug", "children"),
    [Input(f"{fid}-store", "data") for fid in FILTERS] + [Input("app-id-filter", "value")],
)
def debug_display(*values):
    data = dict(zip(FILTER_IDS, values))
    return html.Pre(json.dumps(data or {}, indent=2))