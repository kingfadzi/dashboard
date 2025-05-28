from dash_ag_grid import AgGrid

modal_table = AgGrid(
    id="modal-table",
    className="ag-theme-balham",
    columnSize="sizeToFit",
    style={"height": "600px", "width": "100%"},
    defaultColDef={
        "sortable": True,
        "filter": True,
        "resizable": True,
        "wrapText": True,
        "autoHeight": True
    },
    enableEnterpriseModules=False,
    dashGridOptions={
        "pagination": True,
        "paginationPageSize": 25,
        "suppressCellFocus": True,
    },
)