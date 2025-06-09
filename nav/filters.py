import yaml
import dash_mantine_components as dmc
from dash import html, Output, Input, State, MATCH, ctx
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from pathlib import Path

FILTER_YAML_PATH = Path("filters.yaml")

with open(FILTER_YAML_PATH) as f:
    yaml_data = yaml.safe_load(f)

FILTER_IDS = [
    "host-name-filter",
    "activity-status-filter",
    "tc-filter",
    "language-filter",
    "classification-filter",
    "app-id-filter",
]

def filter_layout():
    def make_multiselect(id_, placeholder):
        return dmc.MultiSelect(
            id=id_,
            data=[{"value": v, "label": v} for v in yaml_data.get(id_, [])],
            placeholder=placeholder,
            searchable=True,
            clearable=True,
            maxDropdownHeight=150,
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

    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(make_multiselect("host-name-filter", "Select Host Name(s)"), width=2),
                dbc.Col(make_multiselect("activity-status-filter", "Select Activity Status"), width=2),
                dbc.Col(make_multiselect("tc-filter", "Select TC(s)"), width=2),
                dbc.Col(make_multiselect("language-filter", "Select Language(s)"), width=2),
                dbc.Col(make_multiselect("classification-filter", "Select Classification(s)"), width=2),
                dbc.Col(make_textinput("app-id-filter", "Enter App ID or Repo Slug"), width=2),
            ], className="g-3", align="center"),
            html.Div(id="filter-tags", className="mt-3"),
        ]),
        className="bg-light mb-4",
    )

def register_callbacks(app):
    @app.callback(
        Output("filter-tags", "children"),
        [Input(fid, "value") for fid in FILTER_IDS],
        prevent_initial_call=False,
    )
    def update_tags(*values):
        data = dict(zip(FILTER_IDS, values))
        tags = [
            dmc.Badge(
                label,
                variant="light",
                size="md",
                radius="sm",
                rightSection=dmc.ActionIcon(
                    DashIconify(icon="mdi:close", width=12),
                    size="xs",
                    variant="subtle",
                    color="red",
                    n_clicks=0,
                    id={"type": "remove-tag", "filter_id": fid, "value": label},
                ),
                className="me-2 mb-2",
            )
            for fid, vals in data.items() if isinstance(vals, list)
            for label in vals
        ]
        return dmc.Group(tags, spacing="xs", position="left")

    @app.callback(
        Output(MATCH, "value"),
        Input({"type": "remove-tag", "filter_id": MATCH, "value": MATCH}, "n_clicks"),
        State(MATCH, "value"),
        prevent_initial_call=True,
    )
    def remove_tag(n, current_vals):
        triggered = ctx.triggered_id
        if not triggered:
            return current_vals
        to_remove = triggered["value"]
        return [v for v in current_vals if v != to_remove]