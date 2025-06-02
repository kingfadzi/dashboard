from dash import Input, Output
from data.dependencies_fetchers import (
    fetch_dependency_detection_coverage,
    fetch_iac_detection_coverage,
    fetch_xeol_detection_coverage,
    fetch_package_type_distribution,
    fetch_top_packages,
    fetch_framework_distribution,
    fetch_dependency_volume_buckets,
    fetch_xeol_exposure_by_bucket_and_artifact_type,
    fetch_xeol_top_products,
    fetch_iac_framework_usage,
    fetch_iac_adoption_by_framework_count,
)
from data.fetch_spring_versions import fetch_spring_framework_versions
from data.fetch_iac_data import fetch_iac_server_orchestration_usage

from utils.redirect_callbacks import generate_redirect_callbacks
from utils.filter_utils import extract_filter_dict_from_store

from viz.viz_dependencies import (
    render_dependency_detection_chart,
    render_iac_detection_chart,
    render_xeol_detection_chart,
    render_package_type_distribution_chart,
    render_top_packages_chart,
    render_framework_distribution_chart,
    render_dependency_volume_chart,
    render_xeol_exposure_bucketed_chart,
    render_xeol_top_products_chart,
    render_iac_framework_usage_chart,
    render_iac_adoption_by_framework_count_chart,
)
from viz.viz_spring_versions import render_spring_version_chart
from viz.viz_iac_server_orchestration import render_iac_server_orchestration_chart


def register_dependencies_callbacks(app):

    @app.callback(Output("dep-detection-chart", "figure"), Input("default-filter-store", "data"))
    def update_dep_detection_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_dependency_detection_chart(fetch_dependency_detection_coverage(filters))

    @app.callback(Output("iac-detection-chart", "figure"), Input("default-filter-store", "data"))
    def update_iac_detection_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_iac_detection_chart(fetch_iac_detection_coverage(filters))

    @app.callback(Output("xeol-detection-chart", "figure"), Input("default-filter-store", "data"))
    def update_xeol_detection_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_xeol_detection_chart(fetch_xeol_detection_coverage(filters))

    @app.callback(Output("package-type-distribution-chart", "figure"), Input("default-filter-store", "data"))
    def update_package_type_distribution_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_package_type_distribution_chart(fetch_package_type_distribution(filters))

    @app.callback(Output("top-packages-chart", "figure"), Input("default-filter-store", "data"))
    def update_top_packages_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_top_packages_chart(fetch_top_packages(filters))

    @app.callback(Output("framework-distribution-chart", "figure"), Input("default-filter-store", "data"))
    def update_framework_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_framework_distribution_chart(fetch_framework_distribution(filters))

    @app.callback(Output("dependency-volume-chart", "figure"), Input("default-filter-store", "data"))
    def update_dependency_volume_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_dependency_volume_chart(fetch_dependency_volume_buckets(filters))

    @app.callback(Output("xeol-top-products-chart", "figure"), Input("default-filter-store", "data"))
    def update_xeol_top_products_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_xeol_top_products_chart(fetch_xeol_top_products(filters))

    @app.callback(Output("xeol-exposure-chart", "figure"), Input("default-filter-store", "data"))
    def update_xeol_exposure_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_xeol_exposure_bucketed_chart(fetch_xeol_exposure_by_bucket_and_artifact_type(filters))

    @app.callback(Output("iac-framework-usage-chart", "figure"), Input("default-filter-store", "data"))
    def update_iac_framework_usage(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_iac_framework_usage_chart(fetch_iac_framework_usage(filters))

    @app.callback(Output("iac-adoption-chart", "figure"), Input("default-filter-store", "data"))
    def update_iac_adoption_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_iac_adoption_by_framework_count_chart(fetch_iac_adoption_by_framework_count(filters))

    @app.callback(
        Output("iac-server-orchestration-chart", "figure"),
        Input("default-filter-store", "data"),
    )
    def update_iac_server_orchestration(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_iac_server_orchestration_chart(fetch_iac_server_orchestration_usage(filters))

    

    @app.callback(
        Output("spring-version-chart", "figure"),
        Input("default-filter-store", "data"),
    )
    def update_spring_versions(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_spring_framework_versions(filters)
        return render_spring_version_chart(df, title="Spring & Spring Boot Usage by Version")
    
    generate_redirect_callbacks(
        app,
        target_href="/table-dependencies",
        button_id="dependencies-table-btn",
        output_container_id="dependencies-table-link-container",
        reverse_href="/dependencies",
        reverse_button_id="back-to-charts-btn-dependencies",
    )
