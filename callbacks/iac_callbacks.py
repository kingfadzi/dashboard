from dash import Input, Output
from data.fetch_iac_data import fetch_iac_data
from viz.viz_iac_chart import viz_iac_chart

def register_iac_callbacks(app):
    @app.callback(
        [
            Output("iac-card", "style"),         # Show/hide the card
            Output("iac-bar-chart", "figure"),   # Chart output
        ],
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_iac(
        host_name, activity_status, tc, language, classification, app_id
    ):
        filters = {
            "host_name": host_name or None,
            "activity_status": activity_status or None,
            "transaction_cycle": tc or None,
            "main_language": language or None,
            "classification_label": classification or None,
            "app_id": app_id or None,
        }

        df = fetch_iac_data(filters)

        if df.empty:
            return {"display": "none"}, {"data": []}

        fig = viz_iac_chart(df)
        return {"display": "block"}, fig