import uuid
from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from data.fetch_modal_rows import fetch_modal_rows
from utils.filter_utils import extract_filter_dict_from_store
from utils.modal_store import build_modal_store_payload


def register_modal_callbacks(app):
    @app.callback(
        Output("shared-modal-store", "data", allow_duplicate=True),
        Input("spring-core-version-chart", "clickData"),
        Input("spring-boot-version-chart", "clickData"),
        Input("ee-usage-chart", "clickData"),
        prevent_initial_call=True,
    )
    def update_store(click_data_core, click_data_boot, click_data_ee):
        triggered = ctx.triggered_id

        mapping = {
            "spring-core-version-chart": ("version_bucket", click_data_core),
            "spring-boot-version-chart": ("version_bucket", click_data_boot),
            "ee-usage-chart": ("ee_usage", click_data_ee),
        }

        if triggered in mapping:
            field, click_data = mapping[triggered]
            if click_data and click_data.get("points"):
                payload = build_modal_store_payload(triggered, field, click_data)
                if payload:
                    print(f"[MODAL STORE] Triggered by {triggered}, payload={payload}")
                    return payload

        raise PreventUpdate

    @app.callback(
        Output("shared-modal", "is_open"),
        Output("shared-modal-table", "columnDefs"),
        Output("shared-modal-table", "rowData"),
        Input("shared-modal-store", "data"),
        Input("shared-modal-close", "n_clicks"),
        State("default-filter-store", "data"),
        prevent_initial_call=True,
    )
    def control_modal(store_data, close_clicks, store_filters):
        triggered = ctx.triggered_id

        if triggered == "shared-modal-close":
            print("[MODAL CLOSE] User clicked close")
            return False, [], []

        if triggered == "shared-modal-store" and store_data:
            chart_id = store_data.get("chart_id")
            click_data = store_data.get("click_data")
            filters = extract_filter_dict_from_store(store_filters)

            if chart_id and click_data:
                columnDefs, rowData = fetch_modal_rows(chart_id, click_data, filters)
                print(f"[MODAL OPEN] chart={chart_id}, rows={len(rowData)}")
                return True, columnDefs, rowData

        raise PreventUpdate
