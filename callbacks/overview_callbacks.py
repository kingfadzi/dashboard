from dash import Input, Output
from callbacks.redirect_callbacks import generate_redirect_callbacks
from utils.filter_utils import extract_filter_dict_from_store

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from data.fetch_overview_metrics import (
    fetch_repo_status,
    fetch_repo_sizes,
    fetch_cloc,
    fetch_contribution_activity,
    fetch_language_distribution,
    fetch_package_types,
    fetch_multilang_usage,
    fetch_commit_buckets,
    fetch_iac_usage,
    fetch_code_contributors,
    fetch_vulnerabilities,
    fetch_standards_issues,
    fetch_appserver_usage,
    fetch_dev_frameworks,
)

from viz.viz_overview_charts import (
    render_repo_status_chart,
    render_repo_size_chart,
    render_cloc_chart,
    render_contribution_scatter,
    render_primary_language_chart,
    render_package_type_chart,
    render_multilang_chart,
    render_commit_buckets_chart,
    render_iac_chart,
    render_language_contributors_heatmap,
    render_vulnerabilities_chart,
    render_standards_issues_chart,
    render_appserver_chart,
    render_dev_frameworks_chart,
)


def register_overview_callbacks(app):

    @app.callback(Output("active-inactive-bar", "figure"), Input("default-filter-store", "data"))
    def update_repo_status(store_data):
        filters = extract_filter_dict_from_store(store_data)
        logger.info(f"[Repo Status] Filters: {filters}")
        return render_repo_status_chart(fetch_repo_status(filters))

    @app.callback(Output("classification-pie", "figure"), Input("default-filter-store", "data"))
    def update_repo_size(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_repo_size_chart(fetch_repo_sizes(filters))

    @app.callback(Output("cloc-bar-chart", "figure"), Input("default-filter-store", "data"))
    def update_cloc_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_cloc_chart(fetch_cloc(filters))

    @app.callback(Output("scatter-plot", "figure"), Input("default-filter-store", "data"))
    def update_contribution_scatter(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_contribution_scatter(fetch_contribution_activity(filters))

    @app.callback(Output("repos-by-language-bar", "figure"), Input("default-filter-store", "data"))
    def update_primary_language(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_primary_language_chart(fetch_language_distribution(filters))

    @app.callback(Output("package-type-bar-chart", "figure"), Input("default-filter-store", "data"))
    def update_package_type(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_package_type_chart(fetch_package_types(filters))

    @app.callback(Output("language-usage-buckets-bar", "figure"), Input("default-filter-store", "data"))
    def update_multilang_usage(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_multilang_chart(fetch_multilang_usage(filters))

    @app.callback(Output("last-commit-buckets-bar", "figure"), Input("default-filter-store", "data"))
    def update_commit_buckets(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_commit_buckets_chart(fetch_commit_buckets(filters))

    @app.callback(Output("iac-bar-chart", "figure"), Input("default-filter-store", "data"))
    def update_iac_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_iac_chart(fetch_iac_usage(filters))

    @app.callback(Output("language-contributors-heatmap", "figure"), Input("default-filter-store", "data"))
    def update_contributors_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_language_contributors_heatmap(fetch_code_contributors(filters))

    @app.callback(Output("trivy-vulnerabilities-bar-chart", "figure"), Input("default-filter-store", "data"))
    def update_vulnerabilities_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_vulnerabilities_chart(fetch_vulnerabilities(filters))

    @app.callback(Output("semgrep-findings-bar-chart", "figure"), Input("default-filter-store", "data"))
    def update_standards_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_standards_issues_chart(fetch_standards_issues(filters))

    @app.callback(Output("appserver-bar-chart", "figure"), Input("default-filter-store", "data"))
    def update_appserver_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_appserver_chart(fetch_appserver_usage(filters))

    @app.callback(Output("dev-frameworks-bar-chart", "figure"), Input("default-filter-store", "data"))
    def update_dev_frameworks_chart(store_data):
        filters = extract_filter_dict_from_store(store_data)
        return render_dev_frameworks_chart(fetch_dev_frameworks(filters))

    generate_redirect_callbacks(
        app,
        target_href="/table-overview",
        button_id="overview-table-btn",
        output_container_id="overview-table-link-container",
        reverse_href="/overview",
        reverse_button_id="back-to-charts-btn-overview",
    )
