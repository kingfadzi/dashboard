from dash import Input, Output
from urllib.parse import urlparse, parse_qs

def register_filter_value_callbacks(app):
    @app.callback(
        [
            Output("host-name-filter", "value"),
            Output("activity-status-filter", "value"),
            Output("tc-filter", "value"),
            Output("language-filter", "value"),
            Output("classification-filter", "value"),
        ],
        Input("url", "search"),
    )
    def set_filter_values(search):
        if not search:
            return [None] * 5

        query = parse_qs(urlparse(search).query)
        return [
            query.get("host_name", [None])[0],
            query.get("activity_status", [None])[0],
            query.get("tc", [None])[0],
            query.get("main_language", [None])[0],
            query.get("classification_label", [None])[0],
        ]
