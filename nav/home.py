import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div("Hello, this is the home page.")