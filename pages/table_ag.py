import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

dash.register_page(__name__, path="/table_ag", name="Build Info – Table View")

layout = dbc.Container(
    [

        dcc.Location(id="url", refresh=False),

        dbc.Row(
            [
                dbc.Col(html.H2("X – Table View"), width="auto"),
                dbc.Col(
                    html.Div(id="table-link-container", className="d-flex justify-content-end"),
                    width="auto",
                ),
            ],
            className="mb-2 align-items-center",
        ),

        dbc.Card(
            [
                dbc.CardHeader(html.H5("Repositories Overview", className="mb-0")),
                dbc.CardBody(
                    dcc.Loading(
                        dag.AgGrid(
                            id="temp-table",
                            columnDefs=[], rowData=[],
                            defaultColDef={
                                "sortable": True, "filter": True, "resizable": True,
                                "flex": 1, "minWidth": 100,
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
                            style={"width": "100%", "height": "100%", "minHeight": "400px"},
                        )
                    )
                ),
            ],
            className="shadow-sm rounded mb-4",
            style={"border": "1px solid #dee2e6", "overflow": "hidden"},
        ),
    ],
    fluid=True,
    style={"marginTop": "0", "paddingTop": "0"},
)
