from dash import Input, Output, State
from dash.exceptions import PreventUpdate

from data.dependencies.dependencies_fetchers import fetch_no_deps_heatmap_data, fetch_subcategory_distribution
from data.dependencies.dependency_insights import (
    fetch_middleware_usage_detailed, fetch_middleware_usage_by_sub_category, fetch_with_deps_by_variant,
    fetch_avg_deps_per_package_type, fetch_no_dependency_repo_scatter, fetch_no_dependency_buildtool_summary,
    fetch_ee_usage_by_repo,
)
from data.overview.fetch_overview_metrics import fetch_dev_frameworks

from data.codeinsights.fetch_trivy_vulnerabilities import fetch_repo_count_by_trivy_severity, \
    fetch_repo_count_by_trivy_resource_type_and_severity, fetch_repo_count_by_fix_status_and_severity, \
    fetch_top_trivy_products_by_repo_impact
from utils.filter_utils import extract_filter_dict_from_store
from viz.dependencies.viz_dependencies import render_middleware_subcategory_chart, render_subcategory_distribution_chart
from viz.dependencies.viz_dependency_insights import render_no_deps_heatmap, render_with_deps_by_variant, \
    render_avg_deps_per_package_type_chart, render_no_dependency_repo_scatter, \
    render_no_dependency_buildtool_summary_chart, render_ee_usage_chart
from viz.overview.viz_overview_charts import render_dev_frameworks_chart
from viz.codeinsights.viz_trivy_vulnerabilities import render_repo_count_by_trivy_severity_chart, \
    render_repo_count_by_trivy_resource_type_chart, render_repo_count_by_fix_status_chart, \
    render_top_trivy_repo_impact_chart


def register_dependency_insights_callbacks(app):
    @app.callback(
        Output("middleware-subcategory-dropdown", "options"),
        Input("middleware-subcategory-dropdown", "id")  # dummy input
    )
    def populate_subcategory_dropdown(_):
        df = fetch_middleware_usage_detailed()
        options = sorted(df["sub_category"].dropna().unique())
        return [{"label": s, "value": s} for s in options]

    @app.callback(
        Output("middleware-subcategory-chart", "figure"),
        Input("middleware-subcategory-dropdown", "value"),
        State("default-filter-store", "data"),
    )
    def update_middleware_chart(selected_subcategory, filters):
        filters = filters or {}  # ← Ensure it's a dict
        df = fetch_middleware_usage_by_sub_category(filters)

        print("Selected subcategory:", selected_subcategory)
        print("Filters:", filters)
        print("Middleware Data:")
        print(df.head())

        if selected_subcategory:
            df = df[df["sub_category"] == selected_subcategory]

        if df.empty:
            raise PreventUpdate

        return render_middleware_subcategory_chart(df)

    @app.callback(Output("no-deps-heatmap", "figure"), Input("default-filter-store", "data"))
    def update_no_deps_heatmap(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_no_deps_heatmap(fetch_no_deps_heatmap_data(filters))


    @app.callback(Output("with-deps-by-variant-heatmap", "figure"), Input("default-filter-store", "data"))
    def update_with_deps_by_variant(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_with_deps_by_variant(fetch_with_deps_by_variant(filters))

    @app.callback(Output("avg-deps-per-package-type-chart", "figure"), Input("default-filter-store", "data"))
    def update_avg_deps_per_package_type_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_avg_deps_per_package_type_chart(fetch_avg_deps_per_package_type(filters))

    @app.callback(Output("no-deps-scatter-chart", "figure"), Input("default-filter-store", "data"))
    def update_no_dependency_repo_scatter_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_no_dependency_repo_scatter(fetch_no_dependency_repo_scatter(filters))

    @app.callback(
        Output("no-deps-buildtool-summary-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_no_dependency_buildtool_summary_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_no_dependency_buildtool_summary(filters)
        return render_no_dependency_buildtool_summary_chart(df)

    @app.callback(
        Output("ee-usage-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_ee_usage_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_ee_usage_by_repo(filters)
        return render_ee_usage_chart(df)

    @app.callback(
        Output("trivy-severity-repo-count-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_repo_count_by_trivy_severity_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_repo_count_by_trivy_severity(filters)
        fig = render_repo_count_by_trivy_severity_chart(df)
        return fig

    @app.callback(
        Output("trivy-resource-type-repo-count-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_repo_count_by_trivy_resource_type_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_repo_count_by_trivy_resource_type_and_severity(filters)
        fig = render_repo_count_by_trivy_resource_type_chart(df)
        return fig

    @app.callback(
        Output("trivy-fix-status-repo-count-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_repo_count_by_fix_status_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_repo_count_by_fix_status_and_severity(filters)
        fig = render_repo_count_by_fix_status_chart(df)
        return fig

    @app.callback(
        Output("top-expired-trivy-products-chart", "figure"),
        Input("default-filter-store", "data")
    )
    def update_top_expired_trivy_products_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_top_trivy_products_by_repo_impact(filters)
        fig = render_top_trivy_repo_impact_chart(df)
        return fig

    @app.callback(Output("framework-distribution-chart", "figure"), Input("default-filter-store", "data"))
    def update_framework_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_subcategory_distribution_chart(fetch_subcategory_distribution(filters))

    @app.callback(
        Output("dev-frameworks-bar-chart", "figure"),
        Input("default-filter-store", "data"),
        Input("framework-language-dropdown", "value")
    )
    def update_dev_frameworks_chart(store_data, selected_language):
        filters = extract_filter_dict_from_store(store_data)
        df = fetch_dev_frameworks(filters, selected_language)
        return render_dev_frameworks_chart(df)