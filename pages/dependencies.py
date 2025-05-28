import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import DEFAULT_FILTERS
from components.modal_table import modal_table
# from layouts.layout_filters import filter_layout   # uncomment if you want filters here

dash.register_page(__name__, path="/dependencies", name="Dependencies")

def card(title, graph_id, height=400):
    return dbc.Card(
        [
            dbc.CardHeader(html.B(title, className="text-center"), className="bg-light"),
            dbc.CardBody(
                dcc.Loading(
                    dcc.Graph(
                        id=graph_id,
                        config={"staticPlot": True},
                        style={"height": f"{height}px"},
                    )
                ),
                className="p-0",
            ),
        ],
        className="mb-4",
    )

header_with_button = dbc.Row(
    [
        dbc.Col(html.H2("Dependencies"), width="auto"),
        dbc.Col(
            dbc.Button(
                "Table",
                id="modal-open",
                color="secondary",
                size="sm",
                className="ms-auto",
            ),
            width="auto",
            className="d-flex align-items-center justify-content-end",
        ),
    ],
    className="mb-2 align-items-center",
)

layout = dbc.Container(
    [

        header_with_button,

        # Detection coverage cards
        dbc.Row(
            [
                dbc.Col(card("Dependency Detection Coverage", "dep-detection-chart"), width=4),
                dbc.Col(card("IaC Detection Coverage",        "iac-detection-chart"), width=4),
                dbc.Col(card("EOL Detection Coverage",        "xeol-detection-chart"), width=4),
            ],
            className="mb-4",
        ),

        html.Hr(),

        # Syft dependency insights
        dbc.Row(
            [
                dbc.Col(card("Package Type Distribution",    "package-type-distribution-chart"), width=6),
                dbc.Col(card("Framework Distribution",        "framework-distribution-chart"),     width=6),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [dbc.Col(card("Top Packages", "top-packages-chart"), width=12)],
            className="mb-4",
        ),

        # 🔽 Spring framework version insights
        dbc.Row(
            [
                dbc.Col(card("Spring Core Version Usage", "spring-core-version-chart"), width=6),
                dbc.Col(card("Spring Boot Core Version Usage", "spring-boot-version-chart"), width=6),
            ],
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
                dbc.Col(card("EOL Exposure",      "xeol-exposure-chart", height=450), width=6),
            ],
            className="mb-4",
        ),

        # IaC insights
        dbc.Row(
            [
                dbc.Col(card("IaC Framework Usage", "iac-framework-usage-chart"), width=6),
                dbc.Col(card("IaC Adoption",         "iac-adoption-chart"),         width=6),
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(card("Application Servers / Orchestration Frameworks", "iac-server-orchestration-chart"), width=12),
            ],
            className="mb-4",
        ),

        # Shared modal + table
        modal_table,

        # Shared stores (filters + trigger)
        dcc.Store(id="default-filter-store", data=DEFAULT_FILTERS),
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)