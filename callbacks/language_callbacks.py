# language_callbacks.py
from dash import Input, Output
from data.fetch_language_data import fetch_language_data
from callbacks.viz_main_language import viz_main_language

def register_language_callbacks(app):
    @app.callback(
        Output("repos-by-language-bar", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_language(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "tc",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        data = fetch_language_data(filters)
        return viz_main_language(data)