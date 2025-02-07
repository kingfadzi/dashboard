# iac_callbacks.py
from dash import Input, Output
from data.fetch_iac_data import fetch_iac_data
from callbacks.viz_iac_chart import viz_iac_chart

def register_iac_callbacks(app):
    @app.callback(
        Output("iac-bar-chart", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_iac(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "tc",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        data = fetch_iac_data(filters)
        return viz_iac_chart(data)