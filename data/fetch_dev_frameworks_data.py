import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_dev_frameworks_data(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                COALESCE(sd.framework, 'Unclassified') AS framework,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN combined_repo_metrics crm ON crm.repo_id = sd.repo_id
            WHERE (
                sd.sub_category IS NULL
                OR TRIM(sd.sub_category) NOT ILIKE ANY (ARRAY[
                    '%utility%',
                    '%utilities%',
                    '%general%',
                    '%general purpose%',
                    '%helper%',
                    '%misc%'
                ])
            )
        """

        if condition_string:
            base_query += f" AND {condition_string}"

        base_query += " GROUP BY framework ORDER BY repo_count DESC LIMIT 20"

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)