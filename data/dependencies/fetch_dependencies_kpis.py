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
                COUNT(DISTINCT sd.id) AS total_deps,
                COUNT(DISTINCT sd.repo_id) AS repos_with_deps,
                COUNT(DISTINCT CASE
                    WHEN LOWER(hr.main_language) IN (
                        'java', 'python', 'javascript', 'typescript', 'tsx',
                        'asp.net', 'c#', 'f#', 'visual basic.net', 'visual basic', 'visual basic 6.0',
                        'go', 'golang'
                    ) THEN hr.repo_id
                END) AS code_repos,
                COUNT(DISTINCT CASE
                    WHEN LOWER(hr.main_language) = 'no markup_or_data' OR hr.main_language IS NULL THEN hr.repo_id
                END) AS no_language_repos,
                COUNT(DISTINCT CASE
                    WHEN LOWER(l.type) IN ('markup', 'data') THEN hr.repo_id
                END) AS markup_data_repos,
                COUNT(DISTINCT hr.repo_id) AS total_repos
            FROM harvested_repositories hr
            LEFT JOIN syft_dependencies sd ON hr.repo_id = sd.repo_id
            LEFT JOIN languages l ON hr.main_language = l.name
            {f'WHERE {condition_string}' if condition_string else ''}
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df = query_data(condition_string, param_dict)

    total_repos = int(df["total_repos"].iloc[0] or 0)
    repos_with_deps = int(df["repos_with_deps"].iloc[0] or 0)

    return {
        "total_deps": int(df["total_deps"].iloc[0] or 0),
        "repos_with_deps": repos_with_deps,
        "repos_without_deps": max(total_repos - repos_with_deps, 0),
        "code_repos": int(df["code_repos"].iloc[0] or 0),
        "no_language_repos": int(df["no_language_repos"].iloc[0] or 0),
        "markup_data_repos": int(df["markup_data_repos"].iloc[0] or 0),
    }
