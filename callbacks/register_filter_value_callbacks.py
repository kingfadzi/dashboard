from dash import Input, Output, State, no_update

def register_filter_value_callbacks(app):
    # ✅ 1. Save current values to store on user change
    @app.callback(
        Output("default-filter-store", "data"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
        prevent_initial_call=True
    )
    def save_filter_state(hosts, activity, tc, lang, classif, app_id):
        return {
            "host-name-filter": hosts,
            "activity-status-filter": activity,
            "tc-filter": tc,
            "language-filter": lang,
            "classification-filter": classif,
            "app-id-filter": app_id,
        }

    # ✅ 2. Restore dropdown values only after all options are ready
    @app.callback(
        [
            Output("host-name-filter", "value"),
            Output("activity-status-filter", "value"),
            Output("tc-filter", "value"),
            Output("language-filter", "value"),
            Output("classification-filter", "value"),
            Output("app-id-filter", "value"),
        ],
        [
            Input("host-name-filter", "options"),
            Input("activity-status-filter", "options"),
            Input("tc-filter", "options"),
            Input("language-filter", "options"),
            Input("classification-filter", "options"),
        ],
        State("default-filter-store", "data"),
        prevent_initial_call=True
    )
    def restore_filter_values(
        host_opts, activity_opts, tc_opts, lang_opts, classif_opts, store_data
    ):
        if not store_data:
            return [None] * 6

        # Optional strict check: all dropdowns must have options before restoring
        if not all([host_opts, activity_opts, tc_opts, lang_opts, classif_opts]):
            return [no_update] * 6

        return [
            store_data.get("host-name-filter"),
            store_data.get("activity-status-filter"),
            store_data.get("tc-filter"),
            store_data.get("language-filter"),
            store_data.get("classification-filter"),
            store_data.get("app-id-filter"),
        ]