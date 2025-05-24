from sqlalchemy import text
import pandas as pd
from data.cache_instance import cache
from data.db_connection import engine
from data.sql_filter_utils import build_repo_filter_conditions


def fetch_last_commit_buckets(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
        SELECT * FROM (
            SELECT
                CASE
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '1 month' THEN '< 1 month'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '3 months' THEN '1-3 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '6 months' THEN '3-6 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '9 months' THEN '6-9 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '12 months' THEN '9-12 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '18 months' THEN '12-18 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '24 months' THEN '18-24 months'
                    ELSE '24+ months'
                END AS commit_bucket,
                COUNT(DISTINCT rm.repo_id) AS repo_count
            FROM repo_metrics rm
            INNER JOIN harvested_repositories hr ON rm.repo_id = hr.repo_id
            WHERE 1=1
        """
        if condition_string:
            sql += f" AND {condition_string}"
        sql += """
            GROUP BY 1
        ) subquery
        ORDER BY 
            CASE
                WHEN commit_bucket = '< 1 month' THEN 1
                WHEN commit_bucket = '1-3 months' THEN 2
                WHEN commit_bucket = '3-6 months' THEN 3
                WHEN commit_bucket = '6-9 months' THEN 4
                WHEN commit_bucket = '9-12 months' THEN 5
                WHEN commit_bucket = '12-18 months' THEN 6
                WHEN commit_bucket = '18-24 months' THEN 7
                ELSE 8
            END
        """
        stmt = text(sql)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)
