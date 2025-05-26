import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

# 1. Total Cyclomatic Complexity (bucketed)
def fetch_total_ccn_buckets(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT
                CASE
                    WHEN total_ccn < 100 THEN '< 100'
                    WHEN total_ccn < 300 THEN '100-299'
                    WHEN total_ccn < 600 THEN '300-599'
                    ELSE '600+'
                END AS ccn_bucket,
                COUNT(*) AS repo_count
            FROM lizard_summary
            JOIN harvested_repositories hr ON lizard_summary.repo_id = hr.repo_id
            {where_clause}
            GROUP BY ccn_bucket
            ORDER BY ccn_bucket
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        sql = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

# 2. Function Count (bucketed)
def fetch_function_count_buckets(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT
                CASE
                    WHEN function_count < 10 THEN '< 10'
                    WHEN function_count < 50 THEN '10-49'
                    WHEN function_count < 200 THEN '50-199'
                    ELSE '200+'
                END AS function_bucket,
                COUNT(*) AS repo_count
            FROM lizard_summary
            JOIN harvested_repositories hr ON lizard_summary.repo_id = hr.repo_id
            {where_clause}
            GROUP BY function_bucket
            ORDER BY function_bucket
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        sql = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

# 3. Total NLOC (bucketed)
def fetch_total_nloc_buckets(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT
                CASE
                    WHEN total_nloc < 1000 THEN '< 1K'
                    WHEN total_nloc < 5000 THEN '1K–4.9K'
                    WHEN total_nloc < 10000 THEN '5K–9.9K'
                    ELSE '10K+'
                END AS nloc_bucket,
                COUNT(*) AS repo_count
            FROM lizard_summary
            JOIN harvested_repositories hr ON lizard_summary.repo_id = hr.repo_id
            {where_clause}
            GROUP BY nloc_bucket
            ORDER BY nloc_bucket
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        sql = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

# 4. Function Count vs Total CCN (scatter)
def fetch_ccn_vs_function_count(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT
                lizard_summary.repo_id,
                function_count,
                total_ccn
            FROM lizard_summary
            JOIN harvested_repositories hr ON lizard_summary.repo_id = hr.repo_id
            {where_clause}
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        sql = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)
