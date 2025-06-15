import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions


def fetch_build_tools_kpis(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT
                COUNT(DISTINCT hr.repo_id) AS total_repos,
                COUNT(DISTINCT CASE WHEN b.variant IS NOT NULL THEN b.variant END) AS total_variants,
                COUNT(DISTINCT CASE WHEN b.runtime_version IS NOT NULL THEN b.runtime_version END) AS total_runtimes,
                COUNT(DISTINCT CASE WHEN b.repo_id IS NULL OR b.tool IS NULL THEN hr.repo_id END) AS no_tool
            FROM harvested_repositories hr
            LEFT JOIN build_config_cache b ON hr.repo_id = b.repo_id
            {f'WHERE {condition_string}' if condition_string else ''}
        """
        df = pd.read_sql(text(sql), engine, params=param_dict)
        return df

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df = query_data(condition_string, param_dict)

    return {
        "repos": int(df["total_repos"].iloc[0] or 0),
        "variants": int(df["total_variants"].iloc[0] or 0),
        "runtimes": int(df["total_runtimes"].iloc[0] or 0),
        "no_tool": int(df["no_tool"].iloc[0] or 0),
    }
