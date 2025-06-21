from dash import dcc, html
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

def render_table_card(grid_id: str, title: str = "Repositories Overview"):
    download_btn_id = grid_id.replace("-table", "-download-csv")
    download_target_id = f"{download_btn_id}-target"

    return dbc.Card(
        [
            dbc.CardHeader(html.H5(title, className="mb-0")),
            dbc.CardBody(
                [
                    dbc.Button(
                        "Download CSV",
                        id=download_btn_id,
                        color="primary",
                        className="mb-3"
                    ),
                    dcc.Download(id=download_target_id),
                    dcc.Loading(
                        dag.AgGrid(
                            id=grid_id,
                            columnDefs=[],  # to be set by callback
                            rowData=[],     # to be set by callback
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
                                "onPaginationChanged": {
                                    "function": "function(e) { return { currentPage: e.api.paginationGetCurrentPage() }; }"
                                },
                            },
                            eventData={"paginationChanged": ["currentPage"]},
                            columnSize="sizeToFit",
                            style={
                                "width": "100%",
                                "height": "100%",
                                "minHeight": "400px",
                            },
                        )
                    )
                ]
            ),
        ],
        className="shadow-sm rounded mb-4",
        style={"border": "1px solid #dee2e6", "overflow": "hidden"},
    )