from dash import Input, Output, State, callback, ctx
from dash.exceptions import PreventUpdate
from urllib.parse import parse_qs

def register_filter_value_callbacks(app):
    @callback(
        [
            Output("activity-status-filter",   "value"),
            Output("tc-filter",                "value"),
            Output("language-filter",          "value"),
            Output("classification-filter",    "value"),
            Output("app-id-filter",            "value"),
            Output("host-name-filter",         "value"),
        ],
        [
            Input("_pages_location", "pathname"),
            Input("url", "search"),
            Input("activity-status-filter", "options"),
            Input("tc-filter", "options"),
            Input("language-filter", "options"),
            Input("classification-filter", "options"),
            Input("host-name-filter", "options"),
        ],
        State("default-filter-store", "data"),
        prevent_initial_call=True,
        allow_duplicate=True,
    )
    def unified_filter_loader(pathname, search,
                              activity_opts, tc_opts, lang_opts, class_opts, host_opts,
                              default_filters):
        print("[unified_filter_loader] Triggered by:", ctx.triggered_id)

        if ctx.triggered_id == "url" and search:
            print(f"[unified_filter_loader] Populating from URL query: {search}")
            parsed = parse_qs(search.lstrip("?"))
            filters = {
                "host_name": parsed.get("host_name", []),
                "activity_status": parsed.get("activity_status", []),
                "transaction_cycle": parsed.get("transaction_cycle", []),
                "main_language": parsed.get("main_language", []),
                "classification_label": parsed.get("classification_label", []),
                "app_id": parsed.get("app_id", [""])[0],
            }
        elif default_filters:
            print(f"[unified_filter_loader] Populating from default filter store: {default_filters}")
            filters = {
                "host_name": default_filters.get("host_name", []),
                "activity_status": default_filters.get("activity_status", []),
                "transaction_cycle": default_filters.get("transaction_cycle", []),
                "main_language": default_filters.get("main_language", []),
                "classification_label": default_filters.get("classification_label", []),
                "app_id": default_filters.get("app_id", ""),
            }
        else:
            raise PreventUpdate

        def validate(vals, options):
            valid = {o["value"] for o in options}
            return [v for v in vals if v in valid]

        return [
            validate(filters["activity_status"], activity_opts),
            validate(filters["transaction_cycle"], tc_opts),
            validate(filters["main_language"], lang_opts),
            validate(filters["classification_label"], class_opts),
            filters["app_id"],
            validate(filters["host_name"], host_opts),
        ]
