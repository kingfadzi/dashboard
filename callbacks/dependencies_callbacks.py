from dash import Input, Output
from data.dependencies_fetchers import (
    fetch_dependency_detection_coverage,
    fetch_iac_detection_coverage,
    fetch_xeol_detection_coverage,
    fetch_package_type_distribution,
    fetch_top_packages,
    fetch_framework_distribution, fetch_dependency_volume_buckets, fetch_xeol_exposure_by_bucket_and_artifact_type,
    fetch_xeol_top_products, fetch_iac_framework_usage,
)
from viz.viz_dependencies import (
    render_dependency_detection_chart,
    render_iac_detection_chart,
    render_xeol_detection_chart,
    render_package_type_distribution_chart,
    render_top_packages_chart,
    render_framework_distribution_chart, render_dependency_volume_chart, render_xeol_exposure_bucketed_chart,
    render_xeol_top_products_chart, render_iac_framework_usage_chart,
)

from data.dependencies_fetchers import fetch_iac_adoption_by_framework_count
from viz.viz_dependencies import render_iac_adoption_by_framework_count_chart

from dash import Input, Output
from data.fetch_spring_versions import fetch_spring_framework_versions
from viz.viz_spring_versions import render_spring_version_chart

from data.fetch_iac_data import fetch_iac_server_orchestration_usage
from viz.viz_iac_server_orchestration import render_iac_server_orchestration_chart


def register_dependencies_callbacks(app):
    filter_inputs = [
        Input("host-name-filter", "value"),
        Input("app-id-filter", "value"),
        Input("tc-filter", "value"),
        Input("language-filter", "value"),
        Input("classification-filter", "value"),
        Input("activity-status-filter", "value"),
    ]
    filter_keys = ["host_name", "app_id", "transaction_cycle", "main_language", "classification_label", "activity_status"]

    @app.callback(Output("dep-detection-chart", "figure"), filter_inputs)
    def update_dep_detection_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_dependency_detection_coverage(filters)
        return render_dependency_detection_chart(df)

    @app.callback(Output("iac-detection-chart", "figure"), filter_inputs)
    def update_iac_detection_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_iac_detection_coverage(filters)
        return render_iac_detection_chart(df)

    @app.callback(Output("xeol-detection-chart", "figure"), filter_inputs)
    def update_xeol_detection_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_xeol_detection_coverage(filters)
        return render_xeol_detection_chart(df)

    @app.callback(Output("package-type-distribution-chart", "figure"), filter_inputs)
    def update_package_type_distribution_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_package_type_distribution(filters)
        return render_package_type_distribution_chart(df)

    @app.callback(Output("top-packages-chart", "figure"), filter_inputs)
    def update_top_packages_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_top_packages(filters)
        return render_top_packages_chart(df)

    @app.callback(Output("framework-distribution-chart", "figure"), filter_inputs)
    def update_framework_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_framework_distribution(filters)
        return render_framework_distribution_chart(df)

    @app.callback(Output("dependency-volume-chart", "figure"), filter_inputs)
    def update_dependency_volume_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_dependency_volume_buckets(filters)
        return render_dependency_volume_chart(df)



    @app.callback(Output("xeol-top-products-chart", "figure"), filter_inputs)
    def update_xeol_top_products_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_xeol_top_products(filters)
        return render_xeol_top_products_chart(df)


    @app.callback(Output("xeol-exposure-chart", "figure"), filter_inputs)
    def update_xeol_exposure_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_xeol_exposure_by_bucket_and_artifact_type(filters)
        return render_xeol_exposure_bucketed_chart(df)


    @app.callback(Output("iac-framework-usage-chart", "figure"), filter_inputs)
    def update_iac_framework_usage(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_iac_framework_usage(filters)
        return render_iac_framework_usage_chart(df)

    @app.callback(Output("iac-adoption-chart", "figure"), filter_inputs)
    def update_iac_adoption_chart(*vals):
        filters = dict(zip(filter_keys, vals))
        df = fetch_iac_adoption_by_framework_count(filters)
        return render_iac_adoption_by_framework_count_chart(df)

    @app.callback(
        [
            Output("spring-core-version-chart", "figure"),
            Output("spring-boot-version-chart", "figure")
        ],
        [
            Input("host-name-filter", "value"),
            Input("app-id-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("activity-status-filter", "value"),
        ]
    )
    def update_spring_versions(hosts, apps, tcs, langs, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "transaction_cycle": tcs,
            "main_language": langs,
            "classification_label": classifications,
            "activity_status": activity
        }
        df_core, df_boot = fetch_spring_framework_versions(filters)
        return (
            render_spring_version_chart(df_core, "Spring Core Versions"),
            render_spring_version_chart(df_boot, "Spring Boot Core Versions")
        )
      

    @app.callback(
        Output("iac-server-orchestration-chart", "figure"),
        [
            Input("host-name-filter", "value"),
            Input("app-id-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("activity-status-filter", "value"),
        ]
    )
    def update_chart(hosts, apps, tcs, langs, classifications, activity):
        filters = {
            "host_name": hosts,
            "app_id": apps,
            "transaction_cycle": tcs,
            "main_language": langs,
            "classification_label": classifications,
            "activity_status": activity,
        }
        df = fetch_iac_server_orchestration_usage(filters)
        return render_iac_server_orchestration_chart(df)