from dash import Dash, dcc, html, Input, Output, page_container
import dash_bootstrap_components as dbc
from filters import filter_layout, FILTER_IDS

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Location(id="repo-modal-location", refresh=False),
        html.Div(id="repo-modal-container"),
        dcc.Store(id="default-filter-store", storage_type="local"),
        filter_layout(),
        page_container,
    ],
    fluid=True,
)

@app.callback(
    Output("default-filter-store", "data"),
    [Input(fid, "value") for fid in FILTER_IDS],
    prevent_initial_call=True,
)
def persist_filter_values(*values):
    return dict(zip(FILTER_IDS, values))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)