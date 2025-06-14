from dash import Input, Output, State, ctx, callback
from data.modal_fetchers import fetch_modal_rows
import pandas as pd
import dash

def register_shared_modal_callbacks(app, chart_ids: list, filter_store_id: str = "default-filter-store"):
    # Callback: save chart click + filters to store
    @app.callback(
        Output("modal-clicked-chart", "data"),
        [Input(chart_id, "clickData") for chart_id in chart_ids],
        State(filter_store_id, "data"),
        prevent_initial_call=True
    )
    def capture_chart_click(*clicks_and_filters):
        click_datas = clicks_and_filters[:-1]
        filters = clicks_and_filters[-1] or {}

        triggered_chart = ctx.triggered_id
        clicked_data = ctx.triggered[0]["value"]

        if not triggered_chart or not clicked_data:
            return dash.no_update

        clicked_value = clicked_data["points"][0]["x"]

        return {
            "chart_id": triggered_chart,
            "value": clicked_value,
            "filters": filters
        }

    # Callback: open modal + load filtered data
    @app.callback(
        Output("generic-modal", "is_open"),
        Output("generic-modal-table", "columnDefs"),
        Output("generic-modal-table", "rowData"),
        Input("modal-clicked-chart", "data"),
        Input("close-generic-modal", "n_clicks"),
        State("generic-modal", "is_open"),
    )
    def show_modal_with_table(chart_click_data, close_click, is_open):
        if ctx.triggered_id == "close-generic-modal":
            return False, dash.no_update, dash.no_update

        if ctx.triggered_id == "modal-clicked-chart" and chart_click_data:
            chart_id = chart_click_data["chart_id"]
            value = chart_click_data["value"]
            filters = chart_click_data.get("filters", {})

            df = fetch_modal_rows(chart_id, value, filters)
            if df.empty:
                return False, dash.no_update, dash.no_update

            columns = [{"field": col} for col in df.columns]
            return True, columns, df.to_dict("records")

        return is_open, dash.no_update, dash.no_update