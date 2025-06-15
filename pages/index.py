import dash
from pages.overview.overview import layout  # reuse layout from overview.py

dash.register_page(__name__, path="/")
