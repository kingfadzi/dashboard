import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_semgrep_findings(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                COALESCE(s.category, 'Uncategorized') AS category,
                COUNT(DISTINCT s.repo_id) AS repo_count
            FROM semgrep_results s
            JOIN harvested_repositories hr ON s.repo_id = hr.repo_id
            WHERE s.category IS NOT NULL
        """

        if condition_string:
            base_query += f" AND {condition_string}"

        base_query += " GROUP BY s.category"

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)
