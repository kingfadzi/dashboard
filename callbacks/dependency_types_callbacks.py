from dash import Input, Output
from data.fetch_dependency_types_data import fetch_dependency_types_data
from viz.viz_dependency_types_chart import viz_dependency_types_chart

def register_dependency_types_callbacks(app):
    @app.callback(
        [
            Output("dependency-types-bar-chart", "figure"),
            Output("dependency-types-card-container", "style"),
        ],
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("language-filter", "value"),
        ]
    )
    def update_dependency_types_chart(hosts, activity, langs):
        filters = {
            "host_name": hosts,
            "activity_status": activity,
            "main_language": langs
        }

        print("[DependencyTypes] Filters:", filters)
        df = fetch_dependency_types_data(filters)
        print("[DependencyTypes] Rows returned:", len(df))

        figure = viz_dependency_types_chart(df)
        style = {"display": "block"} if not df.empty else {"display": "none"}

        return figure, style