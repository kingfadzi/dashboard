# components/modal_table.py

import dash_bootstrap_components as dbc
from dash import dcc, dash_table, html

def modal_table():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Details Table")),
            dbc.ModalBody(
                [
                    dbc.Alert(id="modal-total", color="info", is_open=False),
                    dcc.Loading(
                        dash_table.DataTable(
                            id="modal-table",
                            columns=[
                                {
                                    "name": "Repo ID",
                                    "id": "repo_id",
                                    "presentation": "markdown",
                                },
                                {
                                    "name": "App ID",
                                    "id": "app_id",
                                    "presentation": "markdown",
                                },
                                # add any additional columns here…
                            ],
                            data=[],  # to be populated in your callback

                            # Pagination & sorting
                            page_action="native",
                            page_size=10,
                            sort_action="native",
                            sort_mode="single",

                            # Disable built-in export
                            export_format="none",
                            markdown_options={"html": True},
                            tooltip_duration=None,
                            tooltip_data=[],

                            # Styling: fill modal width
                            style_table={
                                "overflowX": "auto",
                                "width": "100%",
                                "minWidth": "100%",
                            },
                            style_header={
                                "backgroundColor": "#e9ecef",
                                "fontWeight": "bold",
                                "borderBottom": "2px solid #dee2e6",
                                "textAlign": "left",
                            },
                            style_cell={
                                "textAlign": "left",
                                "padding": "10px",
                                "borderBottom": "1px solid #dee2e6",
                                "minWidth": "120px",
                                "whiteSpace": "nowrap",
                                "overflow": "hidden",
                                "textOverflow": "ellipsis",
                                "fontFamily": "system-ui, sans-serif",
                                "fontSize": "14px",
                            },
                            style_data_conditional=[
                                {"if": {"row_index": "odd"},  "backgroundColor": "#f8f9fa"},
                                {"if": {"row_index": "even"}, "backgroundColor": "#ffffff"},
                                {
                                    "if": {"state": "active"},
                                    "backgroundColor": "#e2e6ea",
                                    "border": "1px solid #adb5bd",
                                },
                            ],
                        )
                    ),
                    html.Div(
                        dbc.Button(
                            "Downloadx CSV (up to 500)",
                            id="download-all-btn",
                            color="link"
                        ),
                        className="mt-2"
                    ),
                    dcc.Download(id="download-all"),
                ]
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="modal-close", className="ms-auto")
            ),
        ],
        id="modal",
        fullscreen=True,    # span full viewport width
        is_open=False,
        scrollable=True,
    )
