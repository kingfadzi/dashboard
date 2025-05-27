# callbacks/register_filter_value_callbacks.py
from dash import Input, Output
from urllib.parse import urlparse, parse_qs
from dash.exceptions import PreventUpdate

def register_filter_value_callbacks(app):
    @app.callback(
        [
            Output("activity-status-filter", "value"),
            Output("tc-filter", "value"),
            Output("language-filter", "value"),
            Output("classification-filter", "value"),
        ],
        [
            Input("url", "search"),
            Input("activity-status-filter", "options"),
            Input("tc-filter", "options"),
            Input("language-filter", "options"),
            Input("classification-filter", "options"),
            Input("default-filter-store", "data"),
        ]
    )
    def set_filter_defaults(search, activity_opts, tc_opts, lang_opts, class_opts, default_filters):
        if default_filters is None:
            raise PreventUpdate

        query = parse_qs(urlparse(search).query) if search else {}

        def get_val(query_key, default_key):
            return query.get(query_key) or default_filters.get(default_key)

        def normalize(val):
            return val if isinstance(val, list) else [val] if val else []

        def validate(value_list, options):
            valid = {opt["value"] for opt in options}
            return [v for v in normalize(value_list) if v in valid]

        return [
            validate(get_val("activity_status", "activity_status"), activity_opts),
            validate(get_val("transaction_cycle", "transaction_cycle"), tc_opts),
            validate(get_val("main_language", "main_language"), lang_opts),
            validate(get_val("classification_label", "classification_label"), class_opts),
        ]