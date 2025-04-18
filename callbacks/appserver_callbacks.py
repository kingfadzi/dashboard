from dash import Input, Output
from data.fetch_appserver_data import fetch_appserver_data
from viz.viz_appserver_chart import viz_appserver_chart

def register_appserver_callbacks(app):
    @app.callback(
        [
            Output("appserver-bar-chart", "figure"),
            Output("appserver-card", "style")
        ],
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("language-filter", "value"),
        ]
    )
    def update_appserver_chart(hosts, activity, langs):
        filters = {
            "host_name": hosts,
            "activity_status": activity,
            "main_language": langs
        }

        print("[AppServer] Filters:", filters)
        df = fetch_appserver_data(filters)
        print("[AppServer] Rows:", len(df))

        figure = viz_appserver_chart(df)
        card_style = {} if not df.empty else {"display": "none"}

        return figure, card_style