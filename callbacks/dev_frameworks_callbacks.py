from dash import Input, Output
from data.fetch_dev_frameworks_data import fetch_dev_frameworks_data
from viz.viz_dev_frameworks_chart import viz_dev_frameworks_chart

def register_dev_frameworks_callbacks(app):
    @app.callback(
        Output("dev-frameworks-bar-chart", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("language-filter", "value"),
        ]
    )
    def update_dev_framework_chart(hosts, activity, langs):
        filters = {
            "host_name": hosts,
            "activity_status": activity,
            "main_language": langs
        }

        print("[DevFrameworks] Incoming filters:", filters)
        df = fetch_dev_frameworks_data(filters)
        print("[DevFrameworks] Rows returned:", len(df))

        return viz_dev_frameworks_chart(df)