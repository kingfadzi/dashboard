# contributors_callbacks.py
from dash import Input, Output
from data.fetch_contributors_commits_size import fetch_contributors_commits_size
from viz.viz_contributors_commits_size import viz_contributors_commits_size

def register_contributors_callbacks(app):
    @app.callback(
        Output("scatter-plot", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_contributors(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "tc",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        data = fetch_contributors_commits_size(filters)
        return viz_contributors_commits_size(data)
