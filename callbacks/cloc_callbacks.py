# cloc_callbacks.py
from dash import Input, Output
from data.fetch_cloc_by_language import fetch_cloc_by_language
from viz.viz_cloc_by_language import viz_cloc_by_language

def register_cloc_callbacks(app):
    @app.callback(
        Output("cloc-bar-chart", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_cloc(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "transaction_cycle",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        data = fetch_cloc_by_language(filters)
        return viz_cloc_by_language(data)
