from dash import Dash, dcc, html, Input, Output, page_container, clientside_callback
import dash_bootstrap_components as dbc
from filters import filter_layout, FILTER_IDS

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Location(id="repo-modal-location", refresh=False),
        html.Div(id="repo-modal-container"),
        dcc.Store(id="default-filter-store", storage_type="local"),
        dbc.Collapse(filter_layout(), id="filter-collapse", is_open=True),
        html.Div(id="dropdown-scroll-trigger"),  # Dummy output for JS callback
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

# ✅ Client-side callback to enable scroll inside multiselects
clientside_callback(
    """
    function() {
        setTimeout(() => {
            document.querySelectorAll('.Select--multi .Select-value-container').forEach(container => {
                container.style.maxHeight = '72px';
                container.style.overflowY = 'auto';
                container.style.display = 'flex';
                container.style.flexWrap = 'wrap';
                container.style.alignItems = 'flex-start';
            });
        }, 100);
        return window.dash_clientside.no_update;
    }
    """,
    Output("dropdown-scroll-trigger", "children"),
    [Input(fid, "value") for fid in FILTER_IDS]
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)