import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.layout_filters import filter_layout

# Register page
 dash.register_page(__name__, path="/code-insights")

layout = dbc.Container([
    html.H2("Code Insights"),
    filter_layout(),
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="role-distribution-chart")), width=12),
    ]),
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="normalized-weight-chart")), width=12),
    ]),
], fluid=True)
