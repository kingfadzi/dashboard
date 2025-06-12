from dash.dependencies import Input, Output
from data.fetch_overview_kpis import fetch_overview_kpis  # updated fetcher
from shared.utils import extract_filter_dict_from_inputs  # assumes similar to extract_filter_dict_from_store

def register_kpi_callbacks(app):
    @app.callback(
        [
            Output("kpi-total-repos", "children"),
            Output("kpi-total-repos-subtext", "children"),
            Output("kpi-avg-commits", "children"),
            Output("kpi-avg-commits-subtext", "children"),
            Output("kpi-avg-contributors", "children"),
            Output("kpi-avg-contributors-subtext", "children"),
            Output("kpi-avg-loc", "children"),
            Output("kpi-avg-loc-subtext", "children"),
            Output("kpi-avg-ccn", "children"),
            Output("kpi-ccn-subtext", "children"),
            Output("kpi-avg-repo-size", "children"),
            Output("kpi-avg-repo-size-subtext", "children"),
            Output("kpi-branches", "children"),
            Output("kpi-branches-subtext", "children"),
            Output("kpi-repo-age", "children"),
            Output("kpi-repo-age-subtext", "children"),
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
    def update_kpi_values(*args):
        filter_keys = [
            "host_name",
            "activity_status",
            "transaction_cycle",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        kpi = fetch_overview_kpis(filters)

        return (
            kpi["total_repos"], f"Active: {kpi['active']} · Inactive: {kpi['inactive']}",
            kpi["recently_updated"], f"New: {kpi['new_repos']} · Last 30d",
            kpi["build_tool_detected"], f"Modules: {kpi['modules']} · Unknown: {kpi['without_tool']}",
            f"{kpi['loc']:,}", f"Files: {kpi['source_files']} · Repos: {kpi['total_repos']}",
            kpi["runtime_detected"], f"Langs: {kpi['languages']}",
            "-", "-",  # Placeholder for repo size
            kpi["branch_sprawl"], f">10 branches · Total Repos: {kpi['total_repos']}",
            "-", "-",  # Placeholder for repo age
        )