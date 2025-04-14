from dash import dcc, html
import dash_bootstrap_components as dbc

def filter_layout():
    dropdown_style = {
        "fontSize": "14px",
        "whiteSpace": "nowrap",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "width": "100%",
    }

    return dbc.Card(
        dbc.CardBody(
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            id="host-name-filter",
                            options=[],
                            multi=True,
                            placeholder="Select Host Name(s)",
                            clearable=True,
                            maxHeight=600,
                            optionHeight=50,
                            style=dropdown_style,
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="activity-status-filter",
                            options=[],
                            multi=True,
                            placeholder="Select Activity Status",
                            clearable=True,
                            maxHeight=600,
                            optionHeight=50,
                            style=dropdown_style,
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="tc-filter",
                            options=[],
                            multi=True,
                            placeholder="Select TC(s)",
                            clearable=True,
                            maxHeight=600,
                            optionHeight=50,
                            style=dropdown_style,
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="language-filter",
                            options=[],
                            multi=True,
                            placeholder="Select Language(s)",
                            clearable=True,
                            maxHeight=600,
                            optionHeight=50,
                            style=dropdown_style,
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="classification-filter",
                            options=[],
                            multi=True,
                            placeholder="Select Classification(s)",
                            clearable=True,
                            maxHeight=600,
                            optionHeight=50,
                            style=dropdown_style,
                        ),
                        width=2,
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="app-id-filter",
                            type="text",
                            placeholder="Enter App ID or Repo Slug",
                            debounce=True,
                            className="form-control",
                            style={"fontSize": "14px", "width": "100%"},
                        ),
                        width=2,
                    ),
                ],
                align="center",
                className="g-3",
            )
        ),
        className="bg-light mb-4",
    )
