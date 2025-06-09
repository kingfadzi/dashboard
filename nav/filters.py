import yaml
import dash_mantine_components as dmc
from dash import html
from pathlib import Path

FILTER_YAML_PATH = Path("filters.yaml")

# Load from YAML
with open(FILTER_YAML_PATH) as f:
    yaml_data = yaml.safe_load(f)

# Define IDs
FILTER_IDS = [
    "host-name-filter",
    "activity-status-filter",
    "tc-filter",
    "language-filter",
    "classification-filter",
    "app-id-filter",
]

# Create component map
def filter_layout():
    return html.Div([
        html.Div([
            dmc.MultiSelect(
                id="host-name-filter",
                data=[{"value": opt, "label": opt} for opt in yaml_data.get("host-name-filter", [])],
                placeholder="Select Host Name(s)",
                searchable=True,
                maxDropdownHeight=100,
                style={"width": "100%"},
                persistence=True,
                clearable=True,
            ),
        ], style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),

        html.Div([
            dmc.MultiSelect(
                id="activity-status-filter",
                data=[{"value": opt, "label": opt} for opt in yaml_data.get("activity-status-filter", [])],
                placeholder="Select Activity Status",
                searchable=True,
                maxDropdownHeight=100,
                style={"width": "100%"},
                persistence=True,
                clearable=True,
            ),
        ], style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),

        html.Div([
            dmc.MultiSelect(
                id="tc-filter",
                data=[{"value": opt, "label": opt} for opt in yaml_data.get("tc-filter", [])],
                placeholder="Select TC(s)",
                searchable=True,
                maxDropdownHeight=100,
                style={"width": "100%"},
                persistence=True,
                clearable=True,
            ),
        ], style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),

        html.Div([
            dmc.MultiSelect(
                id="language-filter",
                data=[{"value": opt, "label": opt} for opt in yaml_data.get("language-filter", [])],
                placeholder="Select Language(s)",
                searchable=True,
                maxDropdownHeight=100,
                style={"width": "100%"},
                persistence=True,
                clearable=True,
            ),
        ], style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),

        html.Div([
            dmc.MultiSelect(
                id="classification-filter",
                data=[{"value": opt, "label": opt} for opt in yaml_data.get("classification-filter", [])],
                placeholder="Select Classification(s)",
                searchable=True,
                maxDropdownHeight=100,
                style={"width": "100%"},
                persistence=True,
                clearable=True,
            ),
        ], style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),

        html.Div([
            dmc.TextInput(
                id="app-id-filter",
                placeholder="Enter App ID or Repo Slug",
                style={"width": "100%"},
                persistence=True,
            ),
        ], style={"width": "16.66%", "display": "inline-block", "padding": "4px"}),
    ])