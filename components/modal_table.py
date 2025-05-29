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
                    html.Div(
                        dbc.Button(
                            "Download CSV (up to 1000)",
                            id="download-all-btn",
                            color="link",
                            size="sm",
                        ),
                        className="d-flex justify-content-end mb-2",
                    ),
                    dcc.Loading(
                        dag.AgGrid(
                            id="modal-table",
                            columnDefs=[],  # Will be set in callback
                            rowData=[],     # Will be set in callback
                            defaultColDef={
                                "sortable": True,
                                "filter": True,
                                "resizable": True,
                                "flex": 1,
                                "minWidth": 100,
                                "cellStyle": {
                                    "textAlign": "left",
                                    "padding": "4px",
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
                                "animateRows": True,
                                "enableCellTextSelection": True,
                                "suppressMultiSort": False,
                                "sortingOrder": ["asc", "desc", None],
                            },
                            columnSize="sizeToFit",
                            style={
                                "width": "100%",
                                "height": "100%",
                                "minHeight": "300px",
                            },
                        )
                    ),
                    dcc.Download(id="download-all"),
                ],
                style={
                    "overflowX": "auto",
                    "width": "100%",
                    "padding": "0.5rem",
                    "margin": "0",
                },
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="modal-close", className="ms-auto")
            ),
        ],
        id="modal",
        is_open=False,
        scrollable=False,
        size="xl",
        centered=True,
        backdrop="static",
        style={
            "maxWidth": "80vw",
            "width": "80vw",
            "height": "84vh",
            "maxHeight": "84vh",
            "overflow": "hidden",
        },
    )