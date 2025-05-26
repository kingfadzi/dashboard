# classification_callbacks.py
from dash import Input, Output
from data.fetch_classification_data import fetch_classification_data
from viz.viz_classification import viz_classification

def register_classification_callbacks(app):
    @app.callback(
        Output("classification-pie", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_classification(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "transaction_cycle",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        data = fetch_classification_data(filters)
        return viz_classification(data)
