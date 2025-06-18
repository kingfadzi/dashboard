import os

import yaml
import dash
from pathlib import Path
import dash_mantine_components as dmc
from dash import html, Output, Input, State, callback_context, ALL, dcc
import dash_bootstrap_components as dbc

FILTER_IDS = [
    "host_name",
    "activity_status",
    "transaction_cycle",
    "main_language",
    "classification_label",
    "app_id",
]

MULTISELECT_IDS = FILTER_IDS[:-1]
#FILTER_YAML_PATH = Path("filters/.layout_filters.yaml")
FILTER_YAML_PATH = Path(os.environ["FILTER_YAML_PATH"])

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
        dcc.Store(
            id="default-filter-store",
            data={fid: [] for fid in MULTISELECT_IDS},
            storage_type="local"
        ),
        dbc.Card(
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(make_multiselect("transaction_cycle", "Select TC(s)"), width=2),
                    dbc.Col(make_multiselect("main_language", "Select Language(s)"), width=2),
                    dbc.Col(make_multiselect("host_name", "Select Host Name(s)"), width=2),
                    dbc.Col(make_multiselect("activity_status", "Select Activity Status"), width=2),
                    dbc.Col(make_multiselect("classification_label", "Select Classification(s)"), width=2),
                    #dbc.Col(make_textinput("app_id", "Enter App ID or Repo Slug"), width=2),
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

def register_filter_tags_callbacks(app):
    # Show selected values as tags
    @app.callback(
        Output("filter-tags", "children"),
        Input("default-filter-store", "data"),
    )
    def display_tags(data):
        return render_tags(data)

    # Update default-filter-store store and clear dropdown value
    for fid in MULTISELECT_IDS:
        @app.callback(
            Output("default-filter-store", "data", allow_duplicate=True),
            Output(fid, "value"),
            Input(fid, "value"),
            State("default-filter-store", "data"),
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
        Output("default-filter-store", "data"),
        Input({"type": "remove-tag", "filter": ALL, "value": ALL}, "n_clicks"),
        State("default-filter-store", "data"),
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

    # Refresh options for each dropdown based on default-filter-store
    def make_refresh_callback(fid):
        @app.callback(
            Output(fid, "data"),
            Input("default-filter-store", "data"),
            prevent_initial_call=True,
        )
        def refresh_options(data):
            selected = data.get(fid, [])
            original = yaml_data.get(fid, [])
            return [{"value": v, "label": v} for v in original if v not in selected]

    for fid in MULTISELECT_IDS:
        make_refresh_callback(fid)
