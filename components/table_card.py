import dash_ag_grid as dag
from dash import html, dcc
import dash_bootstrap_components as dbc


def render_table_card(grid_id: str, title: str = "Repositories Overview"):
    return dbc.Card(
        [
            dbc.CardHeader(html.H5(title, className="mb-0")),
            dbc.CardBody(
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
                            "cellRenderer": "HtmlRenderer",
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
                            "minHeight": "400px",
                        },
                    )
                )
            ),
        ],
        className="shadow-sm rounded mb-4",
        style={"border": "1px solid #dee2e6", "overflow": "hidden"},
    )