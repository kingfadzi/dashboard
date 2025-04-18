import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_iac_data(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                ic.framework AS iac_type,
                COUNT(DISTINCT ic.repo_id) AS repo_count
            FROM iac_components ic
            JOIN combined_repo_metrics crm ON crm.repo_id = ic.repo_id
        """

        if condition_string:
            base_query += f" WHERE {condition_string}"

        base_query += " GROUP BY ic.framework ORDER BY repo_count DESC LIMIT 20"

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)