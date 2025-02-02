from dash import dcc, html
import dash_bootstrap_components as dbc

def filter_layout():
    return dbc.Card(
        dbc.CardBody(
            [
                # Toggle switch for view mode selection
                html.Div(
                    [
                        dbc.Switch(
                            id="view-mode-toggle",
                            label="Graphical View",
                            value=True,  # Default to graphical view
                        ),
                    ],
                    className="mb-4",
                ),
                
                # Filters
                html.Div(
                    [
                        dbc.Label("Host Name"),
                        dcc.Dropdown(
                            id="host-name-filter",
                            options=[],  # Options will be populated dynamically
                            multi=True,
                            placeholder="Select Host Name(s)",
                            clearable=True,
                            maxHeight=600,
                            optionHeight=50,
                            style={"fontSize": "14px"}
                        ),
                    ],
                    className="mb-4",
                ),
                html.Div(
                    [
                        dbc.Label("Activity Status"),
                        dcc.Dropdown(
                            id="activity-status-filter",
                            options=[],  # Options will be populated dynamically
                            multi=True,
                            placeholder="Select Activity Status",
                            clearable=True,
                            maxHeight=600,
                            optionHeight=50,
                            style={"fontSize": "14px"}
                        ),
                    ],
                    className="mb-4",
                ),
                html.Div(
                    [
                        dbc.Label("TC"),
                        dcc.Dropdown(
                            id="tc-filter",
                            options=[],  # Options will be populated dynamically
                            multi=True,
                            placeholder="Select TC(s)",
                            clearable=True,
                            maxHeight=600,
                            optionHeight=50,
                            style={"fontSize": "14px"}
                        ),
                    ],
                    className="mb-4",
                ),
                html.Div(
                    [
                        dbc.Label("Repo Main Language"),
                        dcc.Dropdown(
                            id="language-filter",
                            options=[],  # Options will be populated dynamically
                            multi=True,
                            placeholder="Select Language(s)",
                            clearable=True,
                            maxHeight=600,
                            optionHeight=50,
                            style={"fontSize": "14px"}
                        ),
                    ],
                    className="mb-4",
                ),
                html.Div(
                    [
                        dbc.Label(
                            [
                                "Classification",
                                html.Span(
                                    " ?",
                                    id="classification-help-text",
                                    style={"color": "blue", "cursor": "pointer", "fontSize": "12px", "marginLeft": "5px"},
                                ),
                            ]
                        ),
                        dbc.Tooltip(
                            r"""
                            Classification Guide:
                            - Tiny: < 1MB.
                            - Small: < 10MB.
                            - Medium: < 100MB.
                            - Large: < 1GB.
                            - Massive: ≥ 1GB.
                            - Unclassified: Doesn't fit any above criteria.
                            """,
                            target="classification-help-text",
                            placement="left",
                            style={
                                "whiteSpace": "pre-wrap",
                                "maxWidth": "400px",
                                "width": "400px",
                                "fontSize": "12px"
                            },
                        ),
                        dcc.Dropdown(
                            id="classification-filter",
                            options=[],  # Options will be populated dynamically
                            multi=True,
                            placeholder="Select Classification(s)",
                            clearable=True,
                            maxHeight=600,
                            optionHeight=50,
                            style={"fontSize": "14px"}
                        ),
                    ],
                    className="mb-4",
                ),
                html.Div(
                    [
                        dbc.Label("App ID"),
                        dcc.Input(
                            id="app-id-filter",
                            type="text",
                            placeholder="Enter App IDs (comma-separated)...",
                            debounce=True,
                            className="form-control",
                            style={"fontSize": "14px"}
                        ),
                    ],
                    className="mb-4",
                ),
            ]
        ),
        className="bg-light mb-4",
    )