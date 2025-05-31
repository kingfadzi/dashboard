import dash
from dash import html, dcc, Input, Output, callback
import urllib.parse

dash.register_page(__name__, path="/repo", name="Repository Profile")

layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="return-button-container"),
    html.Div(id="repo-profile-content")
])

@callback(
    Output("return-button-container", "children"),
    Input("url", "search"),
)
def render_return_button(search):
    if not search:
        return html.Div()

    params = urllib.parse.parse_qs(search.lstrip("?"))
    return_url_raw = params.get("returnUrl", ["/"])[0]
    return_url = urllib.parse.unquote(return_url_raw)

    return dcc.Link(
        html.Button("← Return to Table", className="btn btn-secondary mb-3"),
        href=return_url
    )
