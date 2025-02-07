# last_commit_callbacks.py
from dash import Input, Output
from data.fetch_last_commit_buckets import fetch_last_commit_buckets
from callbacks.viz_last_commit_buckets import viz_last_commit_buckets

def register_last_commit_callbacks(app):
    @app.callback(
        Output("last-commit-buckets-bar", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_last_commit(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "tc",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        data = fetch_last_commit_buckets(filters)
        return viz_last_commit_buckets(data)