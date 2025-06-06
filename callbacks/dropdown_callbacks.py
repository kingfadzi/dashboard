from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate


def register_dropdown_callbacks(app):
    # Update store when any input changes
    @app.callback(
        Output("default-filter-store", "data"),
        [
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),  # <-- only sync from visible
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
            Input("host-name-filter", "value"),
        ],
        prevent_initial_call=True,
    )
    def update_filter_store(activity, tc, lang, classification, app_id, host):
        return {
            "activity_status": activity,
            "transaction_cycle": tc,
            "main_language": lang,
            "classification_label": classification,
            "app_id": app_id,
            "host_name": host,
        }

    # Restore all dropdowns except language
    @callback(
        Output("activity-status-filter", "value"),
        Output("tc-filter", "value"),
        Output("classification-filter", "value"),
        Output("app-id-filter", "value"),
        Output("host-name-filter", "value"),
        Input("url", "pathname"),
        State("default-filter-store", "data"),
        prevent_initial_call="initial_duplicate",
    )
    def initialize_other_dropdowns(pathname, store_data):
        valid_prefixes = ("/table-", "/overview", "/build-info", "/code-insights", "/dependencies")
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

    # Restore language filter separately
    @callback(
        Output("language-filter", "value"),
        Output("language-filter-real", "value"),
        Input("url", "pathname"),
        State("default-filter-store", "data"),
        prevent_initial_call="initial_duplicate",
        allow_duplicate=True
    )
    def initialize_language_dropdown(pathname, store_data):
        valid_prefixes = ("/table-", "/overview", "/build-info", "/code-insights", "/dependencies")
        if not any(pathname.startswith(p) for p in valid_prefixes):
            raise PreventUpdate

        store_data = store_data or {}
        val = store_data.get("main_language")
        return val, val

    # Sync hidden real input → visible summary input
    @callback(
        Output("language-filter", "value"),
        Input("language-filter-real", "value"),
        allow_duplicate=True
    )
    def sync_real_to_display(value):
        return value