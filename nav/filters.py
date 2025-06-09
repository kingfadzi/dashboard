import yaml
from pathlib import Path
import dash_mantine_components as dmc
from dash import html, Output, Input, State, callback_context, ALL
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
        classNames={"values": "scrollable-tags"},
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
    ])

def render_tags(data):
    tags = []
    for fid in FILTER_IDS:
        values = data.get(fid)
        if not values:
            continue
        # Accept both string (for text field) and list (for dropdowns)
        if isinstance(values, str):
            if values.strip():
                tags.append(
                    dmc.Badge(
                        values,
                        rightSection=dmc.ActionIcon(
                            "x", 
                            size="xs",
                            id={"type": "remove-tag", "filter": fid, "value": values}
                        ),
                        variant="light",
                        className="me-1 mb-1"
                    )
                )
        else:
            for v in values:
                tags.append(
                    dmc.Badge(
                        v,
                        rightSection=dmc.ActionIcon(
                            "x",
                            size="xs",
                            id={"type": "remove-tag", "filter": fid, "value": v}
                        ),
                        variant="light",
                        className="me-1 mb-1"
                    )
                )
    return tags

def register_callbacks(app):
    @app.callback(
        Output("filter-tags", "children"),
        [Input(fid, "value") for fid in FILTER_IDS]
    )
    def update_tags(*values):
        data = dict(zip(FILTER_IDS, values))
        return render_tags(data)

    @app.callback(
        [Output(fid, "value") for fid in FILTER_IDS],
        Input({"type": "remove-tag", "filter": ALL, "value": ALL}, "n_clicks"),
        [State(fid, "value") for fid in FILTER_IDS],
        prevent_initial_call=True
    )
    def clear_tag(n_clicks, *states):
        ctx = callback_context
        if not ctx.triggered or not any(n_clicks):
            raise dash.exceptions.PreventUpdate
        triggered = ctx.triggered_id
        outputs = []
        for fid, state in zip(FILTER_IDS, states):
            if triggered and fid == triggered["filter"]:
                if isinstance(state, list):
                    outputs.append([v for v in state if v != triggered["value"]])
                elif isinstance(state, str) and state == triggered["value"]:
                    outputs.append("")
                else:
                    outputs.append(state)
            else:
                outputs.append(state)
        return outputs