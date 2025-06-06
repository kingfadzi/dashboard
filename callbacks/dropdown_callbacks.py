@callback(
    Output("activity-status-filter",   "value"),
    Output("tc-filter",                "value"),
    Output("language-filter",          "value"),
    Output("language-filter-real",     "value"),  # ✅ add this
    Output("classification-filter",    "value"),
    Output("app-id-filter",            "value"),
    Output("host-name-filter",         "value"),
    Input("url", "pathname"),
    State("default-filter-store", "data"),
    prevent_initial_call="initial_duplicate",
    allow_duplicate=True
)
def initialize_dropdowns_from_store(pathname, store_data):
    valid_prefixes = (
        "/table-",
        "/code-insights",
        "/build-info",
        "/dependencies",
        "/overview",
    )
    if not any(pathname.startswith(p) for p in valid_prefixes):
        raise PreventUpdate

    store_data = store_data or {}
    value = store_data.get("main_language")

    return (
        store_data.get("activity_status"),
        store_data.get("transaction_cycle"),
        value,
        value,  # sets real dropdown value directly
        store_data.get("classification_label"),
        store_data.get("app_id"),
        store_data.get("host_name"),
    )