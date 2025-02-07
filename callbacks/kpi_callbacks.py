from dash.dependencies import Input, Output
from data.fetch_kpi_data import fetch_kpi_data

def register_kpi_callbacks(app):
    @app.callback(
        [
            Output("kpi-total-repos", "children"),
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
        filter_keys = ["host_name", "activity_status", "tc", "main_language", "classification_label", "app_id"]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        
        kpi_data = fetch_kpi_data(filters)
        
        total_repos = kpi_data.get("total_repos", "0")
        
        avg_commits_data = kpi_data.get("avg_commits", {})
        avg_commits = avg_commits_data.get("value", "0")
        avg_commits_subtext = f"Min={avg_commits_data.get('min', '0')} | Max={avg_commits_data.get('max', '0')}"
        
        avg_contributors_data = kpi_data.get("avg_contributors", {})
        avg_contributors = avg_contributors_data.get("value", "0")
        avg_contributors_subtext = f"Min={avg_contributors_data.get('min', '0')} | Max={avg_contributors_data.get('max', '0')}"
        
        avg_loc_data = kpi_data.get("avg_loc", {})
        avg_loc = avg_loc_data.get("value", "0")
        avg_loc_subtext = f"Min={avg_loc_data.get('min', '0')} | Max={avg_loc_data.get('max', '0')}"
        
        avg_ccn_data = kpi_data.get("avg_ccn", {})
        avg_ccn = avg_ccn_data.get("value", "0")
        avg_ccn_subtext = (
            f"Tokens={avg_ccn_data.get('total_token_count', '0')} | "
            f"Fn={avg_ccn_data.get('function_count', '0')} | "
            f"Total CCN={avg_ccn_data.get('total_cyclomatic_complexity', '0')}"
        )
        
        avg_repo_size_data = kpi_data.get("avg_repo_size", {})
        avg_repo_size = avg_repo_size_data.get("value", "0")
        avg_repo_size_subtext = f"Min={avg_repo_size_data.get('min', '0')} | Max={avg_repo_size_data.get('max', '0')}"
        
        return (
            total_repos,
            avg_commits,
            avg_commits_subtext,
            avg_contributors,
            avg_contributors_subtext,
            avg_loc,
            avg_loc_subtext,
            avg_ccn,
            avg_ccn_subtext,
            avg_repo_size,
            avg_repo_size_subtext,
        )