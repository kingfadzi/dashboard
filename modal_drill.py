import pandas as pd
import dash
from dash import html, dcc, Input, Output, State
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px
import uuid
from datetime import datetime

# Sample data
df = pd.DataFrame({
    "version": ["5.3.1", "5.3.2", "5.3.1", "6.0.0", "6.0.0", "6.0.1", "4.0.0", "4.0.0"],
    "host_name": ["alpha", "beta", "alpha", "beta", "gamma", "gamma", "delta", "alpha"]
})
df["repo_count"] = 1
df["version_bucket"] = df["version"].str.extract(r"^(\d+\.\d+)")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dcc.Store(id='click-store', data={'version': '__init__', 'uuid': str(uuid.uuid4())}),
    html.Div(id='debug-output', style={'display': 'none'}),
    html.H4("Spring Versions"),
    dcc.Graph(
        id="spring-chart",
        figure=px.bar(
            df.groupby(["version_bucket", "host_name"], as_index=False)["repo_count"].sum(),
            x="version_bucket",
            y="repo_count",
            color="host_name",
            barmode="stack"
        ),
        config={'doubleClick': 'reset'}
    ),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Repositories by Version")),
            dbc.ModalBody(
                dag.AgGrid(
                    id="spring-version-table",
                    columnDefs=[],
                    rowData=[],
                    dashGridOptions={"pagination": True}
                )
            ),
            dbc.ModalFooter(dbc.Button("Close", id="close-modal")),
        ],
        id="modal",
        is_open=False,
        size="xl"
    )
])

def log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {message}")

# 1. Handle chart clicks
@app.callback(
    Output('click-store', 'data'),
    Output('debug-output', 'children'),
    Input('spring-chart', 'clickData'),
    State('click-store', 'data'),
    prevent_initial_call=True
)
def store_click(clickData, current_data):
    log("[store_click] callback triggered")
    log(f"[store_click] incoming clickData = {clickData}")
    if not clickData or not clickData.get("points"):
        raise dash.exceptions.PreventUpdate

    version = clickData["points"][0]["x"]
    prev_version = current_data.get("version")
    new_uuid = str(uuid.uuid4())

    if version == prev_version:
        log("[store_click] same version clicked again; forcing new uuid")
    else:
        log("[store_click] new version selected")

    payload = {"version": version, "uuid": new_uuid}
    log(f"[store_click] stored: {payload}")
    return payload, f"Click stored at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}"

# 2. Open modal
@app.callback(
    Output("modal", "is_open"),
    Output("spring-version-table", "columnDefs"),
    Output("spring-version-table", "rowData"),
    Input('click-store', 'data'),
    prevent_initial_call=True
)
def open_modal(click_data):
    log(f"[open_modal] called — data={click_data}")
    version = click_data.get("version")
    if not version or version == '__cleared__':
        log("[open_modal] No valid version selected")
        raise dash.exceptions.PreventUpdate

    filtered = df[df["version"].str.startswith(version)]
    log(f"[open_modal] version_bucket={version}")
    log(f"[open_modal] filtered rows={len(filtered)}")

    return (
        True,
        [{"field": col} for col in filtered.columns],
        filtered.to_dict("records")
    )

# 3. Close modal and reset store
@app.callback(
    Output("modal", "is_open", allow_duplicate=True),
    Output('click-store', 'data', allow_duplicate=True),
    Input("close-modal", "n_clicks"),
    prevent_initial_call=True
)
def close_modal(n_clicks):
    log("[close_modal] clicked")
    return False, {"version": "__cleared__", "uuid": str(uuid.uuid4())}

if __name__ == "__main__":
    log("App started")
    app.run(debug=True)
