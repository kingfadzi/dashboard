import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.layout_filters import filter_layout

# Register page
dash.register_page(__name__, path="/code-insights", name="Code Insights")

layout = dbc.Container([
    html.H2("Code Insights"),
    filter_layout(),

    # Language Insights
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="role-distribution-chart")), width=12),
    ]),
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="normalized-weight-chart")), width=12),
    ]),

    # Gitlog Insights
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="avg-file-size-chart")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="contributor-dominance-chart")), width=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="branch-sprawl-chart")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="repo-age-chart")), width=6),
    ]),

    # Cloc Insights
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="code-volume-chart")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="file-count-chart")), width=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="code-composition-chart")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="code-file-scatter-chart")), width=6),
    ]),

    # Lizard Insights
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="total-ccn-chart")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="function-count-chart")), width=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="total-nloc-chart")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="ccn-vs-function-count-chart")), width=6),
    ]),


], fluid=True)
