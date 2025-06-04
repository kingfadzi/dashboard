from dash import Input, Output, State, callback, no_update
import dash

def register_filter_value_callbacks(app):
    # ✅ 1. Save user input to the store
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
    def update_filter_store(hosts, activity, tc, lang, classif, app_id):
        return {
            "host-name-filter": hosts,
            "activity-status-filter": activity,
            "tc-filter": tc,
            "language-filter": lang,
            "classification-filter": classif,
            "app-id-filter": app_id,
        }

    # ✅ 2. Restore values AND re-trigger charts by re-writing store
    @app.callback(
        [
            Output("host-name-filter", "value"),
            Output("activity-status-filter", "value"),
            Output("tc-filter", "value"),
            Output("language-filter", "value"),
            Output("classification-filter", "value"),
            Output("app-id-filter", "value"),
            Output("default-filter-store", "data"),  # used to trigger chart updates
        ],
        [
            Input("host-name-filter", "options"),
            Input("activity-status-filter", "options"),
            Input("tc-filter", "options"),
            Input("language-filter", "options"),
            Input("classification-filter", "options"),
        ],
        State("default-filter-store", "data"),
        prevent_initial_call=True,
        allow_duplicate=True  # ✅ Required to reuse the same Output
    )
    def restore_filter_values(*args):
        data = args[-1]
        if not data:
            return [None] * 6 + [no_update]
        return [
            data.get("host-name-filter"),
            data.get("activity-status-filter"),
            data.get("tc-filter"),
            data.get("language-filter"),
            data.get("classification-filter"),
            data.get("app-id-filter"),
            data,  # ✅ Write same data back to trigger chart callbacks
        ]