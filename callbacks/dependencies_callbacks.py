from dash import Input, Output
from data.dependencies_fetchers import (
    fetch_dependency_detection_by_language,
    fetch_iac_detection_coverage,
    fetch_xeol_detection_coverage,
    fetch_package_type_distribution,
    fetch_subcategory_distribution,
    fetch_dependency_volume_buckets,
    fetch_iac_adoption_by_framework_count, fetch_top_expired_xeol_products,
)
from data.fetch_spring_versions import fetch_spring_framework_versions
from data.fetch_iac_data import fetch_iac_server_orchestration_usage

from callbacks.redirect_callbacks import generate_redirect_callbacks
from utils.filter_utils import extract_filter_dict_from_store

from viz.viz_dependencies import (
    render_dependency_detection_heatmap,
    render_iac_detection_chart,
    render_xeol_detection_chart,
    render_package_type_distribution_chart,
    render_subcategory_distribution_chart,
    render_dependency_volume_chart,
    render_xeol_top_products_chart,
)
from viz.viz_spring_versions import render_spring_version_chart
from viz.viz_iac_server_orchestration import render_iac_server_orchestration_chart


def register_dependencies_callbacks(app):

    @app.callback(Output("dep-detection-chart", "figure"), Input("default-filter-store", "data"))
    def update_dep_detection_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_dependency_detection_heatmap(fetch_dependency_detection_by_language(filters))

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

    @app.callback(Output("framework-distribution-chart", "figure"), Input("default-filter-store", "data"))
    def update_framework_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_subcategory_distribution_chart(fetch_subcategory_distribution(filters))

    @app.callback(Output("dependency-volume-chart", "figure"), Input("default-filter-store", "data"))
    def update_dependency_volume_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_dependency_volume_chart(fetch_dependency_volume_buckets(filters))

    @app.callback(
        Output("iac-server-orchestration-chart", "figure"),
        Input("default-filter-store", "data"),
    )
    def update_iac_server_orchestration(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_iac_server_orchestration_chart(fetch_iac_server_orchestration_usage(filters))


    @app.callback(
        Output("spring-core-version-chart", "figure"),
        Output("spring-boot-version-chart", "figure"),
        Input("default-filter-store", "data"),
    )
    def update_spring_versions(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df_core, df_boot = fetch_spring_framework_versions(filters)
        return (
            render_spring_version_chart(df_core, "Spring Core Version Usage"),
            render_spring_version_chart(df_boot, "Spring Boot Version Usage")
        )
    
    generate_redirect_callbacks(
        app,
        target_href="/table-dependencies",
        button_id="dependencies-table-btn",
        output_container_id="dependencies-table-link-container",
        reverse_href="/dependencies",
        reverse_button_id="back-to-charts-btn-dependencies",
    )
