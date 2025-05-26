# language_contributors_callbacks.py
from dash import Input, Output
from data.fetch_language_contributors_heatmap import fetch_language_contributors_heatmap
from viz.viz_language_contributors_heatmap import viz_language_contributors_heatmap

def register_language_contributors_callbacks(app):
    @app.callback(
        Output("language-contributors-heatmap", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_language_contributors(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "transaction_cycle",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        data = fetch_language_contributors_heatmap(filters)
        return viz_language_contributors_heatmap(data)
