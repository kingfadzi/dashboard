from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

def register_dropdown_callbacks(app):
    @callback(
        Output("activity-status-filter", "value"),
        Output("tc-filter", "value"),
        Output("classification-filter", "value"),
        Output("app-id-filter", "value"),
        Output("host-name-filter", "value"),
        Input("url", "pathname"),
        State("default-filter-store", "data"),
        prevent_initial_call="initial_duplicate"
    )
    def initialize_other_filters(pathname, store_data):
        valid_prefixes = (
            "/table-", "/code-insights", "/build-info", "/dependencies", "/overview"
        )
        if not any(pathname.startswith(p) for p in valid_prefixes):
            raise PreventUpdate

        store_data = store_data or {}
        return (
            store_data.get("activity_status"),
            store_data.get("transaction_cycle"),
            store_data.get("classification_label"),
            store_data.get("app_id"),
            store_data.get("host_name"),
        )

    # ✅ Separate callback for language filter only
    @callback(
        Output("language-filter", "value"),
        Output("language-filter-real", "value"),
        Input("url", "pathname"),
        State("default-filter-store", "data"),
        allow_duplicate=True,
        prevent_initial_call="initial_duplicate"
    )
    def init_language_filter(pathname, store_data):
        valid_prefixes = (
            "/table-", "/code-insights", "/build-info", "/dependencies", "/overview"
        )
        if not any(pathname.startswith(p) for p in valid_prefixes):
            raise PreventUpdate

        store_data = store_data or {}
        lang_val = store_data.get("main_language")
        return lang_val, lang_val

    @app.callback(
        Output("default-filter-store", "data"),
        [
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
            Input("host-name-filter", "value"),
            Input("language-filter", "value")
        ],
        prevent_initial_call=True
    )
    def update_filter_store(activity, tc, classification, app_id, host, lang):
        return {
            "activity_status": activity,
            "transaction_cycle": tc,
            "classification_label": classification,
            "app_id": app_id,
            "host_name": host,
            "main_language": lang
        }