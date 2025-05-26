import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from layouts.layout_filters import filter_layout

dash.register_page(__name__, path="/build-info", name="Build Info")

layout = dbc.Container([
    html.H2("Build Info"),
    filter_layout(),

    # First row
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="detection-coverage-chart")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="module-count-chart")), width=6),
    ]),

    # Shared tool selector
    dbc.Row([
        dbc.Col([
            html.Label("Select Language Tool", className="fw-bold"),
            dcc.Dropdown(
                id="tool-selector",
                options=[],
                placeholder="Select a tool",
                clearable=True,
            )
        ], width=3),
        dbc.Col([], width=9),
    ], className="mb-2"),

    # Runtime chart full width (now grouped by variant)
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="runtime-versions-chart")), width=12),
    ]),

    # Next row
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="runtime-fragmentation-chart")), width=6),
        dbc.Col(dcc.Loading(dcc.Graph(id="status-by-tool-chart")), width=6),
    ]),

    # Final row
    dbc.Row([
        dbc.Col(dcc.Loading(dcc.Graph(id="confidence-distribution-chart")), width=6),
    ]),
], fluid=True)
