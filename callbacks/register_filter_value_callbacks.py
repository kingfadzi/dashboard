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
            Input("_pages_location", "pathname"),  # page change
        ],
        State("default-filter-store", "data"),
        prevent_initial_call=True,
        allow_duplicate=True  # needed for re-writing same store data
    )
    def sync_filter_state(
        hosts_val, activity_val, tc_val, lang_val, classif_val, app_id_val,
        hosts_opts, activity_opts, tc_opts, lang_opts, classif_opts,
        pathname,
        store_data
    ):
        trigger = ctx.triggered_id

        if trigger is None:
            return [no_update] * 7

        is_restore_trigger = trigger.endswith(".options")
        is_page_trigger = trigger == "_pages_location"

        # 🟩 Restore filter UI from store
        if is_restore_trigger:
            if not store_data:
                return [None] * 6 + [no_update]
            return [
                store_data.get("host-name-filter"),
                store_data.get("activity-status-filter"),
                store_data.get("tc-filter"),
                store_data.get("language-filter"),
                store_data.get("classification-filter"),
                store_data.get("app-id-filter"),
                store_data,
            ]

        # 🟦 Refresh on page navigation
        if is_page_trigger:
            if not store_data:
                return [no_update] * 7
            return [no_update] * 6 + [store_data]

        # 🟨 User input → update store
        return [
            no_update, no_update, no_update, no_update, no_update, no_update,
            {
                "host-name-filter": hosts_val,
                "activity-status-filter": activity_val,
                "tc-filter": tc_val,
                "language-filter": lang_val,
                "classification-filter": classif_val,
                "app-id-filter": app_id_val,
            },
        ]