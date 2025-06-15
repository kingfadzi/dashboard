import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions
from data.shared_kpi_query import fetch_kpi_totals


def fetch_dependencies_kpis(filters=None):
    @cache.memoize()
    def _query(condition_string, param_dict):
        # 1) Pull shared repo/language KPIs (includes total_repos, code_repos, etc.)
        shared = fetch_kpi_totals(condition_string, param_dict)
        total_repos = int(shared.get("total_repos", 0))

        # 2) Pull dependency counts, scoped to exactly the same base filter
        dep_sql = f"""
            SELECT
                COUNT(DISTINCT sd.repo_id) AS repos_with_deps,
                COUNT(*) AS total_deps
            FROM harvested_repositories hr
            LEFT JOIN syft_dependencies sd ON hr.repo_id = sd.repo_id
            {f"WHERE {condition_string}" if condition_string else ""}
        """
        dep_row = pd.read_sql(text(dep_sql), engine, params=param_dict).iloc[0]
        repos_with_deps = int(dep_row["repos_with_deps"] or 0)
        total_deps      = int(dep_row["total_deps"]      or 0)

        return {
            "total_deps": total_deps,
            "repos_with_deps": repos_with_deps,
            "repos_without_deps": max(total_repos - repos_with_deps, 0),
            "code_repos": int(shared.get("code_repos", 0)),
            "no_language_repos": int(shared.get("no_language_repos", 0)),
            "markup_data_repos": int(shared.get("markup_data_repos", 0)),
        }

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return _query(condition_string, param_dict)
