from dash import Input, Output
from data.fetch_appserver_data import fetch_appserver_data
from viz.viz_appserver_chart import viz_appserver_chart

def register_appserver_callbacks(app):
    @app.callback(
        Output("appserver-bar-chart", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tech-filter", "value"),
            Input("language-filter", "value"),
        ]
    )
    def update_appserver_chart(hosts, activity, techs, langs):
        filters = {
            "host_name": hosts,
            "activity_status": activity,
            "tech": techs,
            "main_language": langs
        }

        df = fetch_appserver_data(filters)
        return viz_appserver_chart(df)