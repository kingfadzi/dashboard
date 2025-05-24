import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/repo",
    name="Repository Profile",
    title="Repository Profile"
)

layout = html.Div([
    dcc.Location(id='repo-url', refresh=False),
    html.Div(id='repo-profile-content')
])
