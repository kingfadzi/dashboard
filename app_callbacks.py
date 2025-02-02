# app_callbacks.py

from dash import Input, Output, State
from data.fetch_dropdown_options import fetch_dropdown_options
from data.fetch_contributors_commits_size import fetch_contributors_commits_size
from data.fetch_iac_data import fetch_iac_data
from data.fetch_active_inactive_data import fetch_active_inactive_data
from data.fetch_classification_data import fetch_classification_data
from data.fetch_language_data import fetch_language_data
from data.fetch_language_contributors_heatmap import fetch_language_contributors_heatmap
from callbacks.viz_contributors_commits_size import viz_contributors_commits_size
from callbacks.viz_iac_chart import viz_iac_chart
from callbacks.viz_active_inactive import viz_active_inactive
from callbacks.viz_classification import viz_classification
from callbacks.viz_main_language import viz_main_language
from data.fetch_cloc_by_language import fetch_cloc_by_language
from callbacks.viz_cloc_by_language import viz_cloc_by_language
from callbacks.viz_language_contributors_heatmap import viz_language_contributors_heatmap
from data.fetch_trivy_vulnerabilities import fetch_trivy_vulnerabilities
from callbacks.viz_trivy_vulnerabilities import viz_trivy_vulnerabilities
from data.fetch_semgrep_findings import fetch_semgrep_findings
from callbacks.viz_semgrep_findings import viz_semgrep_findings
from data.fetch_multi_language_usage import fetch_multi_language_usage
from callbacks.viz_multi_language_usage import viz_multi_language_usage
from data.fetch_last_commit_buckets import fetch_last_commit_buckets
from callbacks.viz_last_commit_buckets import viz_last_commit_buckets
from data.fetch_label_tech_data import fetch_label_tech_data
from callbacks.viz_label_tech import viz_label_tech
from data.fetch_kpi_data import fetch_kpi_data

from data.fetch_table_data import fetch_table_data
from callbacks.viz_table_data import viz_table_data


### **Dropdown Filters Callback (Triggers on Page Load)**
def register_dropdown_callbacks(app):
    @app.callback(
        [
            Output("host-name-filter", "options"),
            Output("activity-status-filter", "options"),
            Output("tc-filter", "options"),
            Output("language-filter", "options"),
            Output("classification-filter", "options"),
        ],
        [Input("url", "pathname")]  # Fire once on page load or URL change
    )
    def populate_dropdown_options(_):
        """Populates dropdown filter options when the app loads or URL changes."""
        options = fetch_dropdown_options()
        return (
            [{"label": name, "value": name} for name in options["host_names"]],
            [{"label": status, "value": status} for status in options["activity_statuses"]],
            [{"label": tc, "value": tc} for tc in options["tcs"]],
            [{"label": lang, "value": lang} for lang in options["languages"]],
            [{"label": label, "value": label} for label in options["classification_labels"]],
        )


### **Graphs & KPI Callback (Includes All Tech Label Charts)**
def register_callbacks(app):
    @app.callback(
        [
            Output("active-inactive-bar", "figure"),
            Output("classification-pie", "figure"),
            Output("scatter-plot", "figure"),
            Output("repos-by-language-bar", "figure"),
            Output("cloc-bar-chart", "figure"),
            Output("iac-bar-chart", "figure"),
            Output("language-contributors-heatmap", "figure"),
            Output("trivy-vulnerabilities-bar-chart", "figure"),
            Output("semgrep-findings-bar-chart", "figure"),
            Output("language-usage-buckets-bar", "figure"),
            Output("last-commit-buckets-bar", "figure"),
            Output("label-tech-bar-chart-java-version", "figure"),
            Output("label-tech-bar-chart-build-tool", "figure"),
            Output("label-tech-bar-chart-appserver", "figure"),
            Output("label-tech-bar-chart-database", "figure"),
            Output("label-tech-bar-chart-spring-framework-version", "figure"),
            Output("label-tech-bar-chart-spring-boot-version", "figure"),
            Output("label-tech-bar-chart-middleware", "figure"),
            Output("label-tech-bar-chart-logging", "figure"),
            Output("kpi-total-repos", "children"),
            Output("kpi-avg-commits", "children"),
            Output("kpi-avg-contributors", "children"),
            Output("kpi-avg-loc", "children"),
            Output("kpi-avg-ccn", "children"),
            Output("kpi-avg-repo-size", "children"),
        ],
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_charts(*args):
        """Fetches all chart data & KPIs when filter values change (no table data here)."""
        filter_keys = [
            "host_name", "activity_status", "tc", "main_language",
            "classification_label", "app_id"
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}

        return (
            viz_active_inactive(fetch_active_inactive_data(filters)),
            viz_classification(fetch_classification_data(filters)),
            viz_contributors_commits_size(fetch_contributors_commits_size(filters)),
            viz_main_language(fetch_language_data(filters)),
            viz_cloc_by_language(fetch_cloc_by_language(filters)),
            viz_iac_chart(fetch_iac_data(filters)),
            viz_language_contributors_heatmap(fetch_language_contributors_heatmap(filters)),
            viz_trivy_vulnerabilities(fetch_trivy_vulnerabilities(filters)),
            viz_semgrep_findings(fetch_semgrep_findings(filters)),
            viz_multi_language_usage(fetch_multi_language_usage(filters)),
            viz_last_commit_buckets(fetch_last_commit_buckets(filters)),
            viz_label_tech(fetch_label_tech_data(filters, "cto.io/java-version")),
            viz_label_tech(fetch_label_tech_data(filters, "cto.io/build-tool")),
            viz_label_tech(fetch_label_tech_data(filters, "cto.io/appserver")),
            viz_label_tech(fetch_label_tech_data(filters, "cto.io/database")),
            viz_label_tech(fetch_label_tech_data(filters, "cto.io/spring-framework-version")),
            viz_label_tech(fetch_label_tech_data(filters, "cto.io/spring-boot-version")),
            viz_label_tech(fetch_label_tech_data(filters, "cto.io/middleware")),
            viz_label_tech(fetch_label_tech_data(filters, "cto.io/logging")),
            fetch_kpi_data(filters)["total_repos"],
            fetch_kpi_data(filters)["avg_commits"],
            fetch_kpi_data(filters)["avg_contributors"],
            fetch_kpi_data(filters)["avg_loc"],
            fetch_kpi_data(filters)["avg_ccn"],
            fetch_kpi_data(filters)["avg_repo_size"],
        )

    # **Table Callback (Uses Only `fetch_table_data()`, No Tech Labels)**
    @app.callback(
        Output("temp-table", "data"),
        [
            Input("host-name-filter", "value"),
            Input("activity-status-filter", "value"),
            Input("tc-filter", "value"),
            Input("language-filter", "value"),
            Input("classification-filter", "value"),
            Input("app-id-filter", "value"),
        ],
    )
    def update_table(*args):
        """Fetches table data using `fetch_table_data()` with correct filters."""
        filter_keys = [
            "host_name", "activity_status", "tc", "main_language",
            "classification_label", "app_id"
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}

        table_raw_df = fetch_table_data(filters)
        return viz_table_data(table_raw_df)
        
        
        # **Sidebar Toggle Callback (Fixes Hamburger Toggle)**
    @app.callback(
        Output("filter-panel", "is_open"),
        Input("filter-toggle-btn", "n_clicks"),
        State("filter-panel", "is_open"),
        prevent_initial_call=True,
    )
    def toggle_filters(n_clicks, is_open):
        """Toggles the filter sidebar sliding in and out."""
        return not is_open
        
    
    
    
      @app.callback(
        Output("rescan-status", "children"),
        Input("rescan-button", "n_clicks"),
        State("temp-table", "selected_rows"),
        State("temp-table", "data"),
        prevent_initial_call=True,
    )
    def trigger_rescan(n_clicks, selected_rows, table_data):
        """Dummy function for triggering a repo re-scan based on selected rows."""
    
        if not selected_rows:
            return "No repositories selected for re-scan."
    
        # Extract repo IDs of selected rows
        selected_repos = [table_data[i]["repo_id"] for i in selected_rows]
    
        # Show confirmation message
        return f"Re-Scan triggered for {len(selected_repos)} repositories!"