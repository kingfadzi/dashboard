import dash
from pages.overview.overview_page import layout  # reuse layout from overview_page.py

dash.register_page(__name__, path="/")
