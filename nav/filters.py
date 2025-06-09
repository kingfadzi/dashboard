import yaml
import dash_mantine_components as dmc
from dash import html, Input, Output, State, callback, ALL
import dash_bootstrap_components as dbc
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
        return html.Div([
            dmc.MultiSelect(
                id=id_,
                data=[{"value": v, "label": v} for v in yaml_data.get(id_, [])],
                placeholder=placeholder,
                clearable=True,
                searchable=True,
                maxDropdownHeight=150,
                style={"width": "100%"},
                persistence=True,
            ),
            html.Div(id=f"{id_}-tags", className="mt-2")
        ])

    def make_textinput(id_, placeholder):
        return dmc.TextInput(
            id=id_,
            placeholder=placeholder,
            style={"width": "100%"},
            persistence=True,
        )

    return dbc.Card(
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
        className="bg-light mb-4",
    )

# Create callbacks for each MultiSelect to update tags
def register_callbacks(app):
    for fid in FILTER_IDS:
        if fid == "app-id-filter":
            continue
        @app.callback(
            Output(f"{fid}-tags", "children"),
            Input(fid, "value"),
            prevent_initial_call=True,
        )
        def update_tags(selected, fid=fid):
            if not selected:
                return []
            return dmc.Group(
                [
                    dmc.Badge(
                        label,
                        rightSection=dmc.CloseButton(
                            id={"type": "close-tag", "field": fid, "value": label},
                            size="xs",
                            style={"marginLeft": 4}
                        ),
                        variant="light",
                    )
                    for label in selected
                ],
                spacing="xs",
            )

        @app.callback(
            Output(fid, "value"),
            Input({"type": "close-tag", "field": fid, "value": ALL}, "n_clicks"),
            State(fid, "value"),
            prevent_initial_call=True,
        )
        def remove_tag(n_clicks, current_values, fid=fid):
            if not any(n_clicks):
                return current_values
            triggered = [t for t in callback_context.triggered if t["value"]][0]
            tag_value = eval(triggered["prop_id"].split(".")[0])["value"]
            return [v for v in current_values if v != tag_value]