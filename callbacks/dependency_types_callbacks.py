from dash import Input, Output
from data.fetch_dependency_types_data import fetch_package_type_distribution
from viz.viz_dependency_types_chart import viz_package_type_distribution_chart

def register_dependency_types_callbacks(app):
    @app.callback(
        Output("package-type-bar-chart", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ]
    )
    def update_package_type_chart(hosts, activity, tc, langs, classification, app_id):
        filters = {
            "host_name": hosts,
            "activity_status": activity,
            "transaction_cycle": tc,
            "main_language": langs,
            "classification_label": classification,
            "app_id": app_id,
        }

        print("[PackageType] Filters:", filters)
        df = fetch_package_type_distribution(filters)
        print("[PackageType] Rows returned:", len(df))

        figure = viz_package_type_distribution_chart(df)
        return figure
