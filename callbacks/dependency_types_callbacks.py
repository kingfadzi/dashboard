 from dash import Input, Output
from data.fetch_package_type_distribution import fetch_package_type_distribution
from viz.viz_package_type_distribution_chart import viz_package_type_distribution_chart

def register_package_type_callbacks(app):
    @app.callback(
        [
            Output("package-type-pie-chart", "figure"),
            Output("package-type-card-container", "style"),
        ],
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("language-filter", "value"),
        ]
    )
    def update_package_type_chart(hosts, activity, langs):
        filters = {
            "host_name": hosts,
            "activity_status": activity,
            "main_language": langs
        }

        print("[PackageType] Filters:", filters)
        df = fetch_package_type_distribution(filters)
        print("[PackageType] Rows returned:", len(df))

        figure = viz_package_type_distribution_chart(df)
        style = {"display": "block"} if not df.empty else {"display": "none"}

        return figure, style