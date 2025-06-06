from dash import html, dcc
import dash_bootstrap_components as dbc

def render_language_filter():
    return dbc.Col(
        html.Div([
            dcc.Store(id="language-filter-visible", data=False),

            # Hidden actual dropdown
            dcc.Dropdown(
                id="language-filter",
                options=[],
                multi=True,
                placeholder="Select Language(s)",
                style={"display": "none"},
                persistence=True,
                persistence_type="local"
            ),

            # Visible summary display
            html.Div(
                id="language-filter-display",
                className="form-control d-flex align-items-center",
                style={
                    "height": "38px",
                    "overflow": "hidden",
                    "cursor": "pointer",
                    "fontSize": "14px"
                },
                n_clicks=0
            ),

            # Real editable dropdown (shown on click)
            html.Div(
                dcc.Dropdown(
                    id="language-filter-real",
                    options=[],
                    multi=True,
                    placeholder="Select Language(s)",
                    persistence=True,
                    persistence_type="local"
                ),
                id="language-filter-dropdown-container",
                style={"display": "none"},
            )
        ]),
        width=2
    )