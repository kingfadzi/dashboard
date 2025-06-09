import yaml
import dash_mantine_components as dmc
from dash import html
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

# Shared style for scrollable MultiSelect fields
SELECT_STYLE = {
    "width": "100%",
    "maxHeight": "72px",      # limit vertical growth
    "overflowY": "auto",      # enable scroll
    "flexWrap": "wrap",
    "display": "flex"
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
            style=SELECT_STYLE,
            persistence=True,
        )

    def make_textinput(id_, placeholder):
        return dmc.TextInput(
            id=id_,
            placeholder=placeholder,
            style={"width": "100%"},
            persistence=True,
        )

    return html.Div([
        html.Div(make_multiselect("host-name-filter", "Select Host Name(s)"),
                 style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),
        html.Div(make_multiselect("activity-status-filter", "Select Activity Status"),
                 style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),
        html.Div(make_multiselect("tc-filter", "Select TC(s)"),
                 style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),
        html.Div(make_multiselect("language-filter", "Select Language(s)"),
                 style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),
        html.Div(make_multiselect("classification-filter", "Select Classification(s)"),
                 style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),
        html.Div(make_textinput("app-id-filter", "Enter App ID or Repo Slug"),
                 style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),
    ])