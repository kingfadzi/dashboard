import dash
from pages.graphs import layout  # reuse layout from graphs.py

dash.register_page(__name__, path="/")
