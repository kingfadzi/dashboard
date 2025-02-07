# multi_language_usage_callbacks.py
from dash import Input, Output
from data.fetch_multi_language_usage import fetch_multi_language_usage
from callbacks.viz_multi_language_usage import viz_multi_language_usage

def register_multi_language_usage_callbacks(app):
    @app.callback(
        Output("language-usage-buckets-bar", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_multi_language_usage(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "tc",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        data = fetch_multi_language_usage(filters)
        return viz_multi_language_usage(data)