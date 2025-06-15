import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions


def fetch_dependencies_kpis(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT
                COUNT(DISTINCT hr.repo_id) AS total_repos,
                COUNT(DISTINCT sd.id) AS total_deps,
                COUNT(DISTINCT sd.repo_id) AS repos_with_deps
            FROM harvested_repositories hr
            LEFT JOIN syft_dependencies sd ON hr.repo_id = sd.repo_id
            {f'WHERE {condition_string}' if condition_string else ''}
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df = query_data(condition_string, param_dict)

    total_repos = int(df["total_repos"].iloc[0] or 0)
    repos_with_deps = int(df["repos_with_deps"].iloc[0] or 0)

    return {
        "total_repos": total_repos,
        "total_deps": int(df["total_deps"].iloc[0] or 0),
        "repos_with_deps": repos_with_deps,
        "repos_without_deps": max(total_repos - repos_with_deps, 0)
    }
