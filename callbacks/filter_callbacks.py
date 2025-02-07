# filter_callbacks.py
from dash import Input, Output, State
from data.fetch_dropdown_options import fetch_dropdown_options

def register_filter_callbacks(app):
    @app.callback(
        [
            Output("host-name-filter", "options"),
            Output("activity-status-filter", "options"),
            Output("tc-filter", "options"),
            Output("language-filter", "options"),
            Output("classification-filter", "options"),
        ],
        [Input("url", "pathname")]
    )
    def populate_dropdown_options(_):
        options = fetch_dropdown_options()
        return (
            [{"label": name, "value": name} for name in options["host_names"]],
            [{"label": status, "value": status} for status in options["activity_statuses"]],
            [{"label": tc, "value": tc} for tc in options["tcs"]],
            [{"label": lang, "value": lang} for lang in options["languages"]],
            [{"label": label, "value": label} for label in options["classification_labels"]],
        )
    
    @app.callback(
        Output("filter-panel", "is_open"),
        Input("filter-toggle-btn", "n_clicks"),
        State("filter-panel", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_filters(n_clicks, is_open):
        return not is_open