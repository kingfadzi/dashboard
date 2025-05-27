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
                            columns=[],
                            data=[],

                            # native pagination & sorting
                            page_action="native",
                            page_size=10,
                            sort_action="native",
                            sort_mode="single",

                            # CSV export & tooltips
                            export_format="csv",
                            markdown_options={"html": True},
                            tooltip_duration=None,
                            tooltip_data=[],

                            # styling
                            style_table={"overflowX": "auto"},
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
                                "maxWidth": "180px",
                                "overflow": "hidden",
                                "textOverflow": "ellipsis",
                                "whiteSpace": "nowrap",
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
                ]
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="modal-close", className="ms-auto")
            ),
        ],
        id="modal",
        size="xl",
        is_open=False,
        scrollable=True,
    )
