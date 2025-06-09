import yaml
import dash
import dash_mantine_components as dmc
from dash import html, Input, Output, State, ctx, dcc
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


# Each filter's MultiSelect
filter_components = {
    fid: dmc.MultiSelect(
        id=fid,
        data=[{"value": v, "label": v} for v in yaml_data.get(fid, [])],
        placeholder=fid.replace("-", " ").title(),
        searchable=True,
        clearable=True,
        maxDropdownHeight=150,
        classNames={"values": "scrollable-tags"},
        style={"width": "100%"},
        persistence=True,
        value=[],
    )
    for fid in FILTER_IDS if fid != "app-id-filter"
}

filter_components["app-id-filter"] = dmc.TextInput(
    id="app-id-filter",
    placeholder="Enter App ID or Repo Slug",
    style={"width": "100%"},
    persistence=True,
    value="",
)


def filter_layout():
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(filter_components[fid], width=2) for fid in FILTER_IDS
                ],
                className="g-3",
                align="center",
            )
        ),
        className="bg-light mb-4",
    )


def tag_layout():
    return html.Div(id="filter-tags-container", className="mb-3")


def register_callbacks(app):
    @app.callback(
        Output("filter-tags-container", "children"),
        [Input(fid, "value") for fid in FILTER_IDS],
        prevent_initial_call=False
    )
    def update_tags(*values):
        tags = []
        for fid, val in zip(FILTER_IDS, values):
            if isinstance(val, list):
                for v in val:
                    tags.append(
                        dmc.Badge(
                            f"{v}",
                            rightSection=dmc.ActionIcon(
                                dmc.IconX(size=10),
                                size="xs",
                                variant="transparent",
                                id={"type": "remove-tag", "filter_id": fid, "value": v},
                            ),
                            variant="light",
                            className="me-1 mb-1"
                        )
                    )
            elif isinstance(val, str) and val:
                tags.append(
                    dmc.Badge(
                        f"{val}",
                        rightSection=dmc.ActionIcon(
                            dmc.IconX(size=10),
                            size="xs",
                            variant="transparent",
                            id={"type": "remove-tag", "filter_id": fid, "value": val},
                        ),
                        variant="light",
                        className="me-1 mb-1"
                    )
                )
        return tags

    # Dynamically clear value when X is clicked
    for fid in FILTER_IDS:
        @app.callback(
            Output(fid, "value"),
            Input({"type": "remove-tag", "filter_id": fid, "value": dash.dependencies.ALL}, "n_clicks"),
            State(fid, "value"),
            prevent_initial_call=True,
        )
        def clear_value(n_clicks_list, current_values):
            if not ctx.triggered_id or not isinstance(current_values, (list, str)):
                raise dash.exceptions.PreventUpdate

            triggered = ctx.triggered_id
            to_remove = triggered["value"]

            if isinstance(current_values, list):
                return [v for v in current_values if v != to_remove]
            elif isinstance(current_values, str) and current_values == to_remove:
                return ""
            raise dash.exceptions.PreventUpdate