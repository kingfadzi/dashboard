import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from layouts.layout_filters import filter_layout
from config.config import DEFAULT_FILTERS

dash.register_page(__name__, path="/dependencies", name="Dependencies")

# Reusable card helper with fixed height
def card(title, graph_id, height=400):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dbc.CardBody(
                dcc.Loading(
                    dcc.Graph(
                        id=graph_id,
                        config={"staticPlot": True},
                        style={"height": f"{height}px"}
                    )
                ),
                className="p-0"
            ),
        ],
        className="mb-4",
    )

# Header with title and Table button
header_with_button = dbc.Row(
    [
        dbc.Col(html.H2("Dependencies"), width="auto"),
        dbc.Col(
            dbc.Button(
                "Table",
                id="code-insights-modal-open",
                color="secondary",
                size="sm",
                className="ms-auto",
            ),
            width="auto",
            className="d-flex align-items-center justify-content-end",
        ),
    ],
    className="mb-2",
)

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        header_with_button,

        # Optional filters
        html.Div(
            # filter_layout(),
            style={"marginTop": "0px", "paddingTop": "0px"},
        ),

        # Detection coverage cards
        dbc.Row(
            [
                dbc.Col(card("Dependency Detection Coverage", "dep-detection-chart"), width=4),
                dbc.Col(card("IaC Detection Coverage", "iac-detection-chart"), width=4),
                dbc.Col(card("EOL Detection Coverage", "xeol-detection-chart"), width=4),
            ],
            className="mb-4",
        ),

        html.Hr(),

        # Syft dependency insights
        dbc.Row(
            [
                dbc.Col(card("Package Type Distribution", "package-type-distribution-chart"), width=6),
                dbc.Col(card("Framework Distribution", "framework-distribution-chart"), width=6),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [dbc.Col(card("Top Packages", "top-packages-chart"), width=12)],
            className="mb-4",
        ),

        # Xeol charts
        dbc.Row(
            [dbc.Col(card("EOL Top Products", "xeol-top-products-chart"), width=12)],
            className="mb-4",
        ),

        # Volume & exposure
        dbc.Row(
            [
                dbc.Col(card("Dependency Volume", "dependency-volume-chart"), width=6),
                dbc.Col(card("EOL Exposure", "xeol-exposure-chart", height=450), width=6),
            ],
            className="mb-4",
        ),

        # IaC insights
        dbc.Row(
            [
                dbc.Col(card("IaC Framework Usage", "iac-framework-usage-chart"), width=6),
                dbc.Col(card("IaC Adoption", "iac-adoption-chart"), width=6),
            ],
            className="mb-4",
        ),

        # Shared Table Modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Repository Table")),
                dbc.ModalBody(
                    [
                        dbc.Alert(id="code-insights-total", color="info", is_open=False),
                        dcc.Loading(
                            dash_table.DataTable(
                                id="code-insights-table",
                                columns=[],
                                data=[],
                                page_current=0,
                                page_size=10,
                                page_action="custom",
                                sort_action="custom",
                                sort_mode="single",
                                sort_by=[],
                                export_format="csv",
                                style_table={"overflowX": "auto"},
                                style_cell={"textAlign": "left", "padding": "5px"},
                            )
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="code-insights-modal-close", className="ms-auto")
                ),
            ],
            id="code-insights-modal",
            size="xl",
            is_open=False,
            scrollable=True,
        ),

        # Shared stores
        dcc.Store(id="default-filter-store", data=DEFAULT_FILTERS),
        dcc.Store(id="filters-applied-trigger", data=None),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)
