import yaml
from pathlib import Path
import dash_mantine_components as dmc
from dash import html, Output, Input, MATCH, ALL, ctx, callback

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
        dmc.Grid(
            [
                dmc.Col(make_multiselect("host-name-filter", "Select Host Name(s)"), span=2),
                dmc.Col(make_multiselect("activity-status-filter", "Select Activity Status"), span=2),
                dmc.Col(make_multiselect("tc-filter", "Select TC(s)"), span=2),
                dmc.Col(make_multiselect("language-filter", "Select Language(s)"), span=2),
                dmc.Col(make_multiselect("classification-filter", "Select Classification(s)"), span=2),
                dmc.Col(make_textinput("app-id-filter", "Enter App ID or Repo Slug"), span=2),
            ],
            gutter="xs"
        ),
        html.Div(id="filter-tags", className="mt-2"),
    ])

def register_callbacks(app):
    @app.callback(
        Output("filter-tags", "children"),
        [Input(fid, "value") for fid in FILTER_IDS]
    )
    def update_tags(*values):
        tags = []
        for fid, val in zip(FILTER_IDS, values):
            if isinstance(val, list):
                for v in val:
                    tags.append(dmc.Badge(
                        v,
                        rightSection=dmc.ActionIcon("x", size="xs"),
                        color="blue",
                        variant="light",
                        radius="sm",
                        className="me-1 mb-1"
                    ))
            elif isinstance(val, str) and val:
                tags.append(dmc.Badge(
                    val,
                    rightSection=dmc.ActionIcon("x", size="xs"),
                    color="gray",
                    variant="light",
                    radius="sm",
                    className="me-1 mb-1"
                ))
        return tags