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
            JOIN harvested_repositories crm ON crm.repo_id = sd.repo_id
            WHERE TRIM(sd.sub_category) IN (
                'Caching Libraries',
                'Cloud & DevOps Tools',
                'Cloud SDKs',
                'Database Libraries',
                'Dependency Injection',
                'Frontend Frameworks',
                'Message Brokers & ETL Tools',
                'Messaging Frameworks',
                'Networking',
                'NoSQL & Big Data',
                'Relational Databases',
                'Spring Boot',
                'Spring Framework Core',
                'Web Frameworks'
            )
        """

        if condition_string:
            base_query += f" AND {condition_string}"

        base_query += " GROUP BY framework ORDER BY repo_count DESC LIMIT 20"

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)
