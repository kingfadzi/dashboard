# active_inactive_callbacks.py
from dash import Input, Output
from data.fetch_active_inactive_data import fetch_active_inactive_data
from viz.viz_active_inactive import viz_active_inactive

def register_active_inactive_callbacks(app):
    @app.callback(
        Output("active-inactive-bar", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_active_inactive(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "transaction_cycle",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        data = fetch_active_inactive_data(filters)
        return viz_active_inactive(data)
