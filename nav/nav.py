from dash import Dash, dcc, html, page_container
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from filters import filter_layout, register_callbacks

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dmc.MantineProvider([
    dcc.Location(id="url", refresh=False),
    filter_layout(),
    page_container,
])

register_callbacks(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)