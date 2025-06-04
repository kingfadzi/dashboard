from dash import Input, Output, State

def register_filter_value_callbacks(app):
    # 1. Save user input
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

    # 2. Restore values and trigger chart refresh
    @app.callback(
        [
            Output("host-name-filter", "value"),
            Output("activity-status-filter", "value"),
            Output("tc-filter", "value"),
            Output("language-filter", "value"),
            Output("classification-filter", "value"),
            Output("app-id-filter", "value"),
            Output("default-filter-store", "data"),  # this re-fires chart callbacks
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
    def load_filter_values(_, __, ___, ____, _____, data):
        if not data:
            return [None] * 6 + [dash.no_update]
        return [
            data.get("host-name-filter"),
            data.get("activity-status-filter"),
            data.get("tc-filter"),
            data.get("language-filter"),
            data.get("classification-filter"),
            data.get("app-id-filter"),
            data,  # re-write the same data to trigger chart updates
        ]