from dash import dcc
import dash_bootstrap_components as dbc
import dash_ag_grid as dag

# Shared modal + store to be included in page layouts
shared_modal = [
    dcc.Store(id="modal-clicked-chart"),

    dbc.Modal(
        [
            dbc.ModalHeader("Details"),
            dbc.ModalBody(
                dag.AgGrid(
                    id="generic-modal-table",
                    columnDefs=[],
                    rowData=[],
                    pagination=True,
                    paginationPageSize=15,
                    style={"height": "400px", "width": "100%"},
                )
            ),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-generic-modal", className="ms-auto")
            ),
        ],
        id="generic-modal",
        is_open=False,
        size="xl",
    ),
]