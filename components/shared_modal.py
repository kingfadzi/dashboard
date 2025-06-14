from dash import html, dcc
import dash_bootstrap_components as dbc
from dash_ag_grid import AgGrid

def shared_modal_layout():
    return html.Div([
        dcc.Store(id="shared-modal-store"),
        dcc.Store(id="shared-modal-open-trigger"),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Repositories")),
                dbc.ModalBody(
                    AgGrid(
                        id="shared-modal-table",
                        columnDefs=[],
                        rowData=[],
                        dashGridOptions={"pagination": True, "paginationPageSize": 10},
                        defaultColDef={"sortable": True, "filter": True, "resizable": True},
                        style={"height": "400px", "width": "100%"},
                    )
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="shared-modal-close", className="ms-auto")
                ),
            ],
            id="shared-modal",
            is_open=False,
            size="xl"
        )
    ])
