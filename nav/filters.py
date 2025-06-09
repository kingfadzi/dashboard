import yaml
import dash_mantine_components as dmc
from dash import html
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

# Used to limit selected tag display height (vertical scroll only)
TAG_STYLE = {
    "maxHeight": 60,
    "overflowY": "auto"
}

def filter_layout():
    def make_multiselect(id_, placeholder):
        return dmc.MultiSelect(
            id=id_,
            data=[{"value": v, "label": v} for v in yaml_data.get(id_, [])],
            placeholder=placeholder,
            searchable=True,
            clearable=True,
            maxDropdownHeight=150,
            value=[],
            style={"width": "100%"},
            classNames={"values": TAG_STYLE},
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
        dbc.CardBody(
            dbc.Row([
                dbc.Col(make_multiselect("host-name-filter", "Select Host Name(s)"), width=2),
                dbc.Col(make_multiselect("activity-status-filter", "Select Activity Status"), width=2),
                dbc.Col(make_multiselect("tc-filter", "Select TC(s)"), width=2),
                dbc.Col(make_multiselect("language-filter", "Select Language(s)"), width=2),
                dbc.Col(make_multiselect("classification-filter", "Select Classification(s)"), width=2),
                dbc.Col(make_textinput("app-id-filter", "Enter App ID or Repo Slug"), width=2),
            ],
            className="g-3",
            align="center")
        ),
        className="bg-light mb-4",
    )