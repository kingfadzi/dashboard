from dash import Input, Output, State, ctx, no_update
import dash

def register_filter_value_callbacks(app):
    @app.callback(
        [
            Output("host-name-filter", "value"),
            Output("activity-status-filter", "value"),
            Output("tc-filter", "value"),
            Output("language-filter", "value"),
            Output("classification-filter", "value"),
            Output("app-id-filter", "value"),
            Output("default-filter-store", "data"),
        ],
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),

            Input("host-name-filter", "options"),
            Input("activity-status-filter", "options"),
            Input("tc-filter", "options"),
            Input("language-filter", "options"),
            Input("classification-filter", "options"),
        ],
        State("default-filter-store", "data"),
        prevent_initial_call=True,
        allow_duplicate=True
    )
    def sync_filter(
        hosts_val, activity_val, tc_val, lang_val, classif_val, app_id_val,
        host_opts, activity_opts, tc_opts, lang_opts, classif_opts,
        store_data
    ):
        triggered = ctx.triggered_id

        is_user_change = triggered and triggered.endswith(".value")
        is_restore_trigger = triggered and triggered.endswith(".options")

        # ✅ User is changing a filter
        if is_user_change:
            return [
                no_update, no_update, no_update, no_update, no_update, no_update,
                {
                    "host-name-filter": hosts_val,
                    "activity-status-filter": activity_val,
                    "tc-filter": tc_val,
                    "language-filter": lang_val,
                    "classification-filter": classif_val,
                    "app-id-filter": app_id_val,
                }
            ]

        # ✅ Restore from store when options are ready
        if is_restore_trigger and store_data:
            if not all([host_opts, activity_opts, tc_opts, lang_opts, classif_opts]):
                return [no_update] * 7

            return [
                store_data.get("host-name-filter"),
                store_data.get("activity-status-filter"),
                store_data.get("tc-filter"),
                store_data.get("language-filter"),
                store_data.get("classification-filter"),
                store_data.get("app-id-filter"),
                store_data  # ✅ triggers chart callbacks
            ]

        return [no_update] * 7