import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config.config import DEFAULT_FILTERS
from components.modal_table import modal_table

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
            html.Div(
                dbc.Button("Table", id="dependencies-table-btn", color="secondary", size="sm"),
                id="dependencies-table-link-container",
                className="d-flex justify-content-end",
            ),
            width="auto",
        ),
    ],
    className="mb-2 align-items-center",
)

layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        header_with_button,

        dbc.Row(
            [
                dbc.Col(card("Dependency Detection Coverage", "dep-detection-chart"), width=4),
                dbc.Col(card("IaC Detection Coverage", "iac-detection-chart"), width=4),
                dbc.Col(card("EOL Detection Coverage", "xeol-detection-chart"), width=4),
            ]
        ),

        html.Hr(),

        dbc.Row(
            [
                dbc.Col(card("Package Type Distribution", "package-type-distribution-chart"), width=6),
                dbc.Col(card("Framework Distribution", "framework-distribution-chart"), width=6),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(card("Spring Framework Version Usage", "spring-core-version-chart"), width=6),
                dbc.Col(card("Spring Boot Core Version Usage", "spring-boot-version-chart"), width=6),
            ]
        ),


        dbc.Row(
            [
                dbc.Col(card("IaC Category Summary", "iac-category-summary-chart"), width=12)

            ]
        ),


        dbc.Row(
            [
                dbc.Col(card("EOL Top Dependencies", "xeol-top-products-chart"), width=6),
                dbc.Col(card("Top Expired Dependencies", "top-expired-xeol-products-chart"), width=6),
            ]
        ),
        dbc.Row(
            [

                dbc.Col(card("IaC Adoption", "iac-adoption-chart"), width=6),
                dbc.Col(card("Application Servers / Orchestration Frameworks", "iac-server-orchestration-chart"), width=6)
            ]
        ),

        dbc.Row(
            [
                dbc.Col(card("Dependency Volume", "dependency-volume-chart"), width=6),

            ]
        ),

        dbc.Row(
            [
                dbc.Col(card("Frameworks per Repo", "frameworks-per-repo-chart"), width=6),
                dbc.Col(card("Dependency Count per Repo", "dependency-count-chart"), width=6),
            ]
        ),


        html.Hr(),

        dbc.Row(
            [
                dbc.Col(card("Outdated Libraries", "outdated-library-chart"), width=6),
                dbc.Col(card("Legacy Version Usage", "legacy-version-chart"), width=6),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(card("JUnit Version Usage", "junit-version-chart"), width=6),
                dbc.Col(card("Dependency Count per Repo", "dependency-count-chart"), width=6),
            ]
        ),


        modal_table(),
        dcc.Store(id="default-filter-store"),
        dcc.Store(id="filters-applied-trigger"),
    ],
    fluid=True,
    style={"marginTop": "0px", "paddingTop": "0px"},
)