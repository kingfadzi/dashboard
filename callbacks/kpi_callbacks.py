from dash.dependencies import Input, Output
from data.fetch_kpi_data import fetch_kpi_data
from dash.dependencies import Input, Output
from data.fetch_kpi_data import fetch_kpi_data

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
            "tc",
            "main_language",
            "classification_label",
            "app_id",
        ]
        filters = {key: (arg if arg else None) for key, arg in zip(filter_keys, args)}
        kpi_data = fetch_kpi_data(filters)

        # Total Repos
        total_repos = kpi_data.get("total_repos", "0")
        total_repos_subtext = f"Total={total_repos}"

        # Commits
        commits_data = kpi_data.get("commits", {})
        avg_commits = commits_data.get("median", "0")
        avg_commits_subtext = f"IQR={commits_data.get('iqr', '0')} | Outliers={commits_data.get('outlier_count', 0)}"

        # Contributors
        contributors_data = kpi_data.get("contributors", {})
        avg_contributors = contributors_data.get("median", "0")
        avg_contributors_subtext = f"IQR={contributors_data.get('iqr', '0')} | Outliers={contributors_data.get('outlier_count', 0)}"

        # LOC
        loc_data = kpi_data.get("loc", {})
        avg_loc = loc_data.get("median", "0")
        avg_loc_subtext = f"IQR={loc_data.get('iqr', '0')} | Outliers={loc_data.get('outlier_count', 0)}"

        # CCN
        ccn_data = kpi_data.get("avg_ccn", {})
        avg_ccn = ccn_data.get("median", "0")
        formatted_function_count = ccn_data.get("function_count", "0")
        formatted_total_ccn = ccn_data.get("total_cyclomatic_complexity", "0")
        avg_ccn_subtext = f"Fn={formatted_function_count} | Total CCN={formatted_total_ccn}"

        # Repo Size
        size_data = kpi_data.get("repo_size", {})
        avg_repo_size = size_data.get("median", "0")
        avg_repo_size_subtext = f"IQR={size_data.get('iqr', '0')} | Outliers={size_data.get('outlier_count', 0)}"

        # Branches
        branches_data = kpi_data.get("branches", {})
        branches = branches_data.get("median", "0")
        branches_subtext = f"IQR={branches_data.get('iqr', '0')} | Outliers={branches_data.get('outlier_count', 0)}"

        # Repo Age
        age_data = kpi_data.get("repo_age_days", {})
        repo_age = age_data.get("median", "0")
        repo_age_subtext = f"IQR={age_data.get('iqr', '0')} | Outliers={age_data.get('outlier_count', 0)}"

        return (
            total_repos, total_repos_subtext,
            avg_commits, avg_commits_subtext,
            avg_contributors, avg_contributors_subtext,
            avg_loc, avg_loc_subtext,
            avg_ccn, avg_ccn_subtext,
            avg_repo_size, avg_repo_size_subtext,
            branches, branches_subtext,
            repo_age, repo_age_subtext
        )
