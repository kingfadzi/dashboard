import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions

@cache.memoize()
def fetch_markup_language_usage(filters=None):
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT gea.language, COUNT(DISTINCT gea.repo_id) AS repo_count
            FROM go_enry_analysis gea
            JOIN languages l ON gea.language = l.name
            JOIN harvested_repositories hr ON gea.repo_id = hr.repo_id
            WHERE gea.percent_usage > 0 AND l.type IN ('markup', 'data')
            {where_clause}
            GROUP BY gea.language
            ORDER BY repo_count DESC
            LIMIT 10
        """
        where_clause = f"AND {condition_string}" if condition_string else ""
        sql = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)
