import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.layout_filters import filter_layout

dash.register_page(__name__, path="/dependencies", name="Dependencies")

layout = dbc.Container([
    html.H2("Dependencies"),
    filter_layout(),

    # Detection coverage
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="dep-detection-chart")), width=4),
        dbc.Col(dcc.Loading(dcc.Graph(id="iac-detection-chart")), width=4),
        dbc.Col(dcc.Loading(dcc.Graph(id="xeol-detection-chart")), width=4),
    ]),

    html.Hr(),

    # New Syft dependency insights
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="package-type-distribution-chart")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="framework-distribution-chart")), width=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="top-packages-chart")), width=12),
    ]),

    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="dependency-volume-chart")), width=12),
    ]),
    # Xeol Charts

    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="xeol-top-products-chart")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="xeol-exposure-chart")), width=6),
    ]),
    # IaC Insights
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="iac-framework-usage-chart")), width=6),

    ]),
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="iac-adoption-chart")), width=12),
    ]),

], fluid=True)
