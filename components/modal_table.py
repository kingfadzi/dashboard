# components/modal_table.py

from dash import dcc, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

def modal_table():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Details Table")),
            dbc.ModalBody(
                [
                    dbc.Alert(id="modal-total", color="info", is_open=False),
                    dcc.Loading(
                        dag.AgGrid(
                            id="modal-table",
                            columnDefs=[],  # set in callback
                            rowData=[],     # populated in callback
                            defaultColDef={
                                "sortable": True,
                                "filter": True,
                                "resizable": True,
                                "minWidth": 120,
                                "wrapText": False,
                                "autoHeight": True,
                                "cellStyle": {
                                    "textAlign": "left",
                                    "padding": "8px",
                                    "fontFamily": "system-ui, sans-serif",
                                    "fontSize": "14px",
                                    "whiteSpace": "nowrap",
                                    "overflow": "hidden",
                                    "textOverflow": "ellipsis",
                                },
                            },
                            dashGridOptions={
                                "pagination": True,
                                "paginationPageSize": 10,
                                "domLayout": "autoHeight",
                            },
                            style={"width": "100%", "minWidth": "100%"},
                        )
                    ),
                    html.Div(
                        dbc.Button(
                            "Download CSV (up to 500)",
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
        fullscreen=True,
        is_open=False,
        scrollable=True,
    )