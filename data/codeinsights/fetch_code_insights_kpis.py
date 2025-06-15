import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions


def fetch_code_insights_kpis(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT
                COUNT(DISTINCT hr.repo_id) AS total_repos,
                SUM(cloc.code) AS total_loc,
                SUM(cloc.files) AS total_files,
                SUM(lizard.function_count) AS total_functions
            FROM harvested_repositories hr
            LEFT JOIN cloc_metrics cloc ON hr.repo_id = cloc.repo_id
            LEFT JOIN lizard_summary lizard ON hr.repo_id = lizard.repo_id
            {f'WHERE {condition_string}' if condition_string else ''}
        """
        sql = text(base_query)
        df = pd.read_sql(sql, engine, params=param_dict)
        return df

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df = query_data(condition_string, param_dict)

    return {
        "repos": int(df["total_repos"].iloc[0] or 0),
        "loc": int(df["total_loc"].iloc[0] or 0),
        "functions": int(df["total_functions"].iloc[0] or 0),
        "files": int(df["total_files"].iloc[0] or 0),
    }
