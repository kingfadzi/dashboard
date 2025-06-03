import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.sql_filter_utils import build_repo_filter_conditions
from data.cache_instance import cache


@cache.memoize()
def fetch_middleware_usage_detailed(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                sd.sub_category,
                sd.framework,
                COUNT(DISTINCT sd.repo_id) AS repo_count,
                hr.main_language
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd.category ILIKE 'middleware'
            {extra_where}
            GROUP BY sd.sub_category, sd.framework, hr.main_language
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_middleware_usage_by_sub_category(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT
                sd.sub_category,
                sd.framework,
                hr.main_language,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd.category ILIKE 'middleware'
              AND sd.framework IS NOT NULL
              {f"AND {condition_string}" if condition_string else ""}
            GROUP BY sd.sub_category, sd.framework, hr.main_language
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)
