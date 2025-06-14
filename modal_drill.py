import pandas as pd
import dash
from dash import html, dcc, Input, Output, State, ctx
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import plotly.express as px

# ✅ Correct import
from components.chart_style import stacked_bar_chart_style

# --- Sample data ---
df = pd.DataFrame({
    "version": ["5.3.1", "5.3.2", "5.3.1", "6.0.0", "6.0.0", "6.0.1", "4.0.0", "4.0.0"],
    "host_name": ["alpha", "beta", "alpha", "beta", "gamma", "gamma", "delta", "alpha"]
})
df["repo_count"] = 1
df["version_bucket"] = df["version"].str.extract(r"^(\d+\.\d+)").fillna("Invalid")

# --- Chart render function ---
@stacked_bar_chart_style(x_col="version_bucket", y_col="repo_count")
def render_chart(data: pd.DataFrame):
    grouped = data.groupby(["version_bucket", "host_name"], as_index=False)["repo_count"].sum()
    return px.bar(
        grouped,
        x="version_bucket",
        y="repo_count",
        color="host_name",
        barmode="stack",
        labels={"version_bucket": "Version", "repo_count": "Repo Count"},
    ), grouped

# --- Dash App Setup ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H4("Spring Version Chart (click to open modal)"),
        dcc.Graph(id="spring-chart", figure=render_chart(df)[0], config={"staticPlot": False}),
        dcc.Store(id="clicked-version"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Repositories by Version")),
                dbc.ModalBody(
                    dag.AgGrid(
                        id="spring-version-table",
                        columnDefs=[],
                        rowData=[],
                        dashGridOptions={
                            "pagination": True,
                            "paginationPageSize": 5
                        },
                        defaultColDef={"sortable": True, "filter": True, "resizable": True},
                        style={"height": "400px", "width": "100%"},
                    )
                ),
                dbc.ModalFooter(dbc.Button("Close", id="close-modal", className="ms-auto")),
            ],
            id="modal",
            is_open=False,
            size="xl"
        )
    ],
    fluid=True
)

# --- Store Clicked Version ---
@app.callback(
    Output("clicked-version", "data"),
    Input("spring-chart", "clickData"),
    prevent_initial_call=True,
)
def store_click(clickData):
    if clickData and clickData["points"]:
        return {"version_bucket": clickData["points"][0]["x"]}
    return dash.no_update

# --- Show Modal and Filter Table ---
@app.callback(
    Output("modal", "is_open"),
    Output("spring-version-table", "columnDefs"),
    Output("spring-version-table", "rowData"),
    Input("clicked-version", "data"),
    Input("close-modal", "n_clicks"),
    State("modal", "is_open"),
    prevent_initial_call=True,
)
def toggle_modal(click_data, close_clicks, is_open):
    triggered = ctx.triggered_id
    if triggered == "close-modal":
        return False, dash.no_update, dash.no_update

    if triggered == "clicked-version" and click_data:
        version = click_data["version_bucket"]
        filtered = df[df["version"].str.startswith(version)]
        return (
            True,
            [{"field": col} for col in filtered.columns],
            filtered.to_dict("records"),
        )

    return is_open, dash.no_update, dash.no_update

if __name__ == "__main__":
    app.run(debug=True)
