from dash import dcc
import dash_bootstrap_components as dbc
from components.react_select_dropdown import render_language_filter

def filter_layout():
    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(dcc.Dropdown(
                        id="host-name-filter",
                        options=[], multi=True,
                        placeholder="Select Host Name(s)",
                        clearable=True,
                        style={"fontSize": "14px"},
                        persistence=True,
                        persistence_type="local"
                    ), width=2),

                    dbc.Col(dcc.Dropdown(
                        id="activity-status-filter",
                        options=[], multi=True,
                        placeholder="Select Activity Status",
                        clearable=True,
                        style={"fontSize": "14px"},
                        persistence=True,
                        persistence_type="local"
                    ), width=2),

                    dbc.Col(dcc.Dropdown(
                        id="tc-filter",
                        options=[], multi=True,
                        placeholder="Select TC(s)",
                        clearable=True,
                        style={"fontSize": "14px"},
                        persistence=True,
                        persistence_type="local"
                    ), width=2),

                    render_language_filter(),  # ← compact language dropdown here

                    dbc.Col(dcc.Dropdown(
                        id="classification-filter",
                        options=[], multi=True,
                        placeholder="Select Classification(s)",
                        clearable=True,
                        style={"fontSize": "14px"},
                        persistence=True,
                        persistence_type="local"
                    ), width=2),

                    dbc.Col(dcc.Input(
                        id="app-id-filter",
                        type="text",
                        placeholder="Enter App ID or Repo Slug",
                        debounce=True,
                        className="form-control",
                        style={"fontSize": "14px"},
                        persistence=True,
                        persistence_type="local"
                    ), width=2)
                ],
                align="center",
                className="g-3"
            )
        ),
        className="bg-light mb-4"
    )