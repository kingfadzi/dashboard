import yaml
from pathlib import Path
from dash import html, Output, Input, State, callback_context
import dash_mantine_components as dmc
import dash
import dash_bootstrap_components as dbc

FILTER_IDS = [
    "host-name-filter",
    "activity-status-filter",
    "tc-filter",
    "language-filter",
    "classification-filter",
    "app-id-filter",
]

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
        value=[],  # Start empty; selections tracked separately
        style={"width": "100%"},
        persistence=True,
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
        dmc.LoadingOverlay(
            html.Div(id="dummy-output"),
            overlayOpacity=0,
            visible=False
        )
    ])

def render_tags(data):
    tags = []
    for fid in FILTER_IDS:
        values = data.get(fid)
        if not values:
            continue
        if not isinstance(values, list):
            values = [values]
        for v in values:
            tags.append(
                dmc.Badge(
                    v,
                    rightSection=dmc.CloseButton(size="xs", id={"type": "remove-tag", "filter": fid, "value": v}),
                    variant="light",
                    className="me-1 mb-1"
                )
            )
    return tags

def register_callbacks(app):
    @app.callback(
        Output("default-filter-store", "data", allow_duplicate=True),
        [Input(fid, "value") for fid in FILTER_IDS],
        prevent_initial_call=True
    )
    def persist_filters(*values):
        return dict(zip(FILTER_IDS, values))

    @app.callback(
        Output("filter-tags", "children"),
        Input("default-filter-store", "data")
    )
    def update_tags(data):
        if not data:
            return []
        return render_tags(data)

    @app.callback(
        Output("default-filter-store", "data", allow_duplicate=True),
        Input({"type": "remove-tag", "filter": dash.ALL, "value": dash.ALL}, "n_clicks"),
        State("default-filter-store", "data"),
        prevent_initial_call=True
    )
    def remove_tag(n_clicks_list, data):
        ctx = callback_context
        if not ctx.triggered or not data:
            return data
        triggered = ctx.triggered_id
        if not triggered:
            return data
        fid = triggered["filter"]
        val = triggered["value"]
        updated = data.copy()
        current_values = updated.get(fid, [])
        if isinstance(current_values, list):
            updated[fid] = [v for v in current_values if v != val]
        elif current_values == val:
            updated[fid] = []
        return updated