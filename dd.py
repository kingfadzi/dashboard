import dash
from dash import dcc, html, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Sample DataFrame
df = px.data.gapminder().query("year == 2007")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dcc.Graph(id="example-chart", figure=px.bar(df, x="continent", y="pop", color="continent")),
        
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Drilldown View")),
                dbc.ModalBody(id="modal-content"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
                ),
            ],
            id="modal",
            is_open=False,
            size="lg",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("modal", "is_open"),
    Output("modal-content", "children"),
    Input("example-chart", "clickData"),
    Input("close-modal", "n_clicks"),
    State("modal", "is_open"),
)
def toggle_modal(click_data, close_clicks, is_open):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    trigger = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger == "example-chart" and click_data:
        continent = click_data["points"][0]["x"]
        filtered = df[df["continent"] == continent]
        table = dbc.Table.from_dataframe(filtered[["country", "lifeExp", "gdpPercap"]], striped=True, bordered=True, hover=True)
        return True, table

    elif trigger == "close-modal":
        return False, dash.no_update

    return is_open, dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)