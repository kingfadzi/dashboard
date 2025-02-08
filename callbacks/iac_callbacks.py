# iac_callbacks.py
from dash import Input, Output
from data.fetch_iac_data import fetch_iac_data
from viz.viz_iac_chart import viz_iac_chart

def register_iac_callbacks(app):
    @app.callback(
        [
            Output("iac-card", "style"),      # Output to update the card's visibility
            Output("iac-bar-chart", "figure"),  # Output for the chart's figure
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
        fig = viz_iac_chart(data)
        
        # Determine whether the figure has any data.
        if not fig:
            # No figure returned at all
            return {"display": "none"}, {"data": []}
        
        # Check for data in the figure:
        if isinstance(fig, dict):
            chart_data = fig.get("data", [])
        else:
            chart_data = fig.data
        
        # If there's no data, hide the card.
        if not chart_data:
            return {"display": "none"}, {"data": []}
        
        # Otherwise, show the card with the chart.
        return {"display": "block"}, fig