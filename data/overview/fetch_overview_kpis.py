import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions


def fetch_code_insights_kpis(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT
                COUNT(DISTINCT hr.repo_id) FILTER (
                    WHERE lang.type = 'programming'
                ) AS code_repos,

                COUNT(DISTINCT hr.repo_id) FILTER (
                    WHERE LOWER(hr.main_language) = 'no language'
                ) AS no_language_repos,

                COUNT(DISTINCT hr.repo_id) FILTER (
                    WHERE LOWER(lang.type) IN ('markup', 'data')
                ) AS markup_data_repos,

                SUM(CASE 
                        WHEN cm.language != 'SUM' AND lang.type = 'programming' 
                        THEN cm.code 
                        ELSE 0 
                    END) AS total_loc,

                SUM(cm.files) AS total_files,
                SUM(lz.function_count) AS total_functions
            FROM harvested_repositories hr
            LEFT JOIN cloc_metrics cm ON hr.repo_id = cm.repo_id
            LEFT JOIN lizard_summary lz ON hr.repo_id = lz.repo_id
            LEFT JOIN languages lang ON LOWER(hr.main_language) = LOWER(lang.name)
            {f"WHERE {condition_string}" if condition_string else ""}
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df = query_data(condition_string, param_dict)

    return {
        "code_repos": int(df["code_repos"].iloc[0] or 0),
        "no_language_repos": int(df["no_language_repos"].iloc[0] or 0),
        "markup_data_repos": int(df["markup_data_repos"].iloc[0] or 0),
        "loc": int(df["total_loc"].iloc[0] or 0),
        "functions": int(df["total_functions"].iloc[0] or 0),
        "files": int(df["total_files"].iloc[0] or 0),
    }
