import dash
from dash import html, dcc, Input, Output, callback, clientside_callback
import urllib.parse

dash.register_page(__name__, path="/repo", name="Repository Profile")

layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Button(
        "← Return to Table",
        id="back-button",
        className="btn btn-secondary mb-3",
        n_clicks=0
    ),
    html.Div(id="repo-profile-content"),
    html.Div(id="dummy-output", style={"display": "none"})  # Hidden dummy component
])

clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            window.history.back();
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("dummy-output", "children"),
    Input("back-button", "n_clicks"),
    prevent_initial_call=True
)
