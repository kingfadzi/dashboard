from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate

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
            Input("_pages_location",           "pathname"),
            Input("activity-status-filter",  "options"),
            Input("tc-filter",               "options"),
            Input("language-filter",         "options"),
            Input("classification-filter",   "options"),
            Input("host-name-filter",        "options"),
        ],
        State("default-filter-store",      "data"),
        prevent_initial_call=False
    )
    def set_filter_defaults(pathname,
                            activity_opts,
                            tc_opts,
                            lang_opts,
                            class_opts,
                            host_opts,
                            default_filters):
        if default_filters is None:
            raise PreventUpdate

        def validate(key, options):
            vals = default_filters.get(key) or []
            valid = {o["value"] for o in options}
            return [v for v in vals if v in valid]

        return [
            validate("activity_status",   activity_opts),
            validate("transaction_cycle", tc_opts),
            validate("main_language",     lang_opts),
            validate("classification_label", class_opts),
            default_filters.get("app_id", ""),
            validate("host_name",         host_opts),
        ]
