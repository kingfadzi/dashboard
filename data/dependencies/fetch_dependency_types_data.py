import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.buildtools.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_package_type_distribution(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                sd.package_type,
                COUNT(*) AS package_count
            FROM syft_dependencies sd
            JOIN harvested_repositories crm ON crm.repo_id = sd.repo_id
        """

        if condition_string:
            base_query += f" WHERE {condition_string}"

        base_query += " GROUP BY sd.package_type ORDER BY package_count DESC"

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)