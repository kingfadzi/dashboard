import yaml
import dash
from pathlib import Path
import dash_mantine_components as dmc
from dash import html, Output, Input, State, callback_context, ALL, dcc
import dash_bootstrap_components as dbc

FILTER_IDS = [
    "host-name-filter",
    "activity-status-filter",
    "tc-filter",
    "language-filter",
    "classification-filter",
    "app-id-filter",
]

MULTISELECT_IDS = FILTER_IDS[:-1]
FILTER_YAML_PATH = Path("filters.yaml")

with open(FILTER_YAML_PATH) as f:
    yaml_data = yaml.safe_load(f)

def make_multiselect(id_, placeholder):
    return dmc.MultiSelect(
        id=id_,
        data=[{"value": v, "label": v} for v in yaml_data.get(id_, [])],
        placeholder=placeholder,
        searchable=True,
        clearable=True,
        maxDropdownHeight=150,
        classNames={"values": "scrollable-tags"},
        style={"width": "100%"},
        persistence=True,
        hidePickedOptions=True,
    )

def make_textinput(id_, placeholder):
    return dmc.TextInput(
        id=id_,
        placeholder=placeholder,
        style={"width": "100%"},
        persistence=True,
    )

def filter_layout():
    return html.Div([
        dcc.Store(id="selected-tags", data={fid: [] for fid in MULTISELECT_IDS}),
        dbc.Card(
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(make_multiselect("host-name-filter", "Select Host Name(s)"), width=2),
                    dbc.Col(make_multiselect("activity-status-filter", "Select Activity Status"), width=2),
                    dbc.Col(make_multiselect("tc-filter", "Select TC(s)"), width=2),
                    dbc.Col(make_multiselect("language-filter", "Select Language(s)"), width=2),
                    dbc.Col(make_multiselect("classification-filter", "Select Classification(s)"), width=2),
                    dbc.Col(make_textinput("app-id-filter", "Enter App ID or Repo Slug"), width=2),
                ], className="g-3", align="center")
            ),
            className="bg-light mb-3"
        ),
        html.Div(id="filter-tags", className="mb-4"),
    ])

def render_tags(data):
    tags = []
    for fid, values in data.items():
        if not values:
            continue
        for val in values:
            tags.append(
                dmc.Badge(
                    val,
                    rightSection=dmc.ActionIcon(
                        "x",
                        size="xs",
                        id={"type": "remove-tag", "filter": fid, "value": val}
                    ),
                    variant="light",
                    className="me-1 mb-1"
                )
            )
    return tags

def register_callbacks(app):
    # Show selected values as tags
    @app.callback(
        Output("filter-tags", "children"),
        Input("selected-tags", "data"),
    )
    def display_tags(data):
        return render_tags(data)

    # Update selected-tags store and clear dropdown value
    for fid in MULTISELECT_IDS:
        @app.callback(
            Output("selected-tags", "data", allow_duplicate=True),
            Output(fid, "value"),
            Input(fid, "value"),
            State("selected-tags", "data"),
            prevent_initial_call=True,
        )
        def add_tag(value, data, fid=fid):
            if not value:
                raise dash.exceptions.PreventUpdate
            updated = data.copy()
            updated[fid] = list(set(updated.get(fid, []) + value))
            return updated, []

    # Remove tag and put it back into dropdown
    @app.callback(
        Output("selected-tags", "data"),
        Input({"type": "remove-tag", "filter": ALL, "value": ALL}, "n_clicks"),
        State("selected-tags", "data"),
        prevent_initial_call=True,
    )
    def remove_tag(n_clicks, data):
        ctx = callback_context
        if not ctx.triggered_id or not any(n_clicks):
            raise dash.exceptions.PreventUpdate
        fid = ctx.triggered_id["filter"]
        val = ctx.triggered_id["value"]
        if fid in data:
            data[fid] = [v for v in data[fid] if v != val]
        return data

    # Refresh options for each dropdown based on selected-tags
    def make_refresh_callback(fid):
        @app.callback(
            Output(fid, "data"),
            Input("selected-tags", "data"),
            prevent_initial_call=True,
        )
        def refresh_options(data):
            selected = data.get(fid, [])
            original = yaml_data.get(fid, [])
            return [{"value": v, "label": v} for v in original if v not in selected]

    for fid in MULTISELECT_IDS:
        make_refresh_callback(fid)
