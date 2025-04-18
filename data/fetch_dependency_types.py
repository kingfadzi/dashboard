import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_dependency_types_data(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                COALESCE(sub_category, 'Unclassified') AS sub_category,
                COUNT(DISTINCT repo_id) AS repo_count
            FROM syft_dependencies
            GROUP BY sub_category
            ORDER BY repo_count DESC
            LIMIT 20
        """

        if condition_string:
            base_query = base_query.replace("GROUP BY", f"AND {condition_string} GROUP BY")

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)