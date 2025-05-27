# layouts/layout_filters.py

from dash import dcc
import dash_bootstrap_components as dbc
from config.config import DEFAULT_FILTERS

def filter_layout():
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            id="host-name-filter",
                            options=[],
                            value=DEFAULT_FILTERS["host_name"],
                            multi=True,
                            placeholder="Select Host Name(s)",
                            clearable=True,
                            style={"fontSize": "14px"},
                        ), width=2
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="activity-status-filter",
                            options=[],
                            value=DEFAULT_FILTERS["activity_status"],
                            multi=True,
                            placeholder="Select Activity Status",
                            clearable=True,
                            style={"fontSize": "14px"},
                        ), width=2
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="tc-filter",
                            options=[],
                            value=DEFAULT_FILTERS["transaction_cycle"],
                            multi=True,
                            placeholder="Select TC(s)",
                            clearable=True,
                            style={"fontSize": "14px"},
                        ), width=2
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="language-filter",
                            options=[],
                            value=DEFAULT_FILTERS["main_language"],
                            multi=True,
                            placeholder="Select Language(s)",
                            clearable=True,
                            style={"fontSize": "14px"},
                        ), width=2
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="classification-filter",
                            options=[],
                            value=DEFAULT_FILTERS["classification_label"],
                            multi=True,
                            placeholder="Select Classification(s)",
                            clearable=True,
                            style={"fontSize": "14px"},
                        ), width=2
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="app-id-filter",
                            type="text",
                            value=DEFAULT_FILTERS["app_id"],
                            placeholder="Enter App ID or Repo Slug",
                            debounce=True,
                            className="form-control",
                            style={"fontSize": "14px"},
                        ), width=2
                    ),
                ],
                align="center",
                className="g-3",
            )
        ),
        className="bg-light mb-4",
    )
