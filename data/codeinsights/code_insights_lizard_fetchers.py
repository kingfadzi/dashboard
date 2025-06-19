import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.buildtools.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache
from utils.sql_filter_utils import LANGUAGE_GROUP_CASE_SQL


# 1. Total Cyclomatic Complexity (bucketed)
def fetch_total_ccn_buckets(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT
                CASE
                    WHEN total_ccn < 100 THEN '< 100'
                    WHEN total_ccn < 300 THEN '100-299'
                    WHEN total_ccn < 600 THEN '300-599'
                    ELSE '600+'
                END AS ccn_bucket,

                {LANGUAGE_GROUP_CASE_SQL} AS language_group,

                COUNT(*) AS repo_count
            FROM lizard_summary
            JOIN harvested_repositories hr ON lizard_summary.repo_id = hr.repo_id
            LEFT JOIN languages l ON hr.main_language = l.name
            {{where_clause}}
            GROUP BY ccn_bucket, language_group
            HAVING {LANGUAGE_GROUP_CASE_SQL} NOT IN ('markup_or_data', 'no_language')
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
        base_query = f"""
            SELECT
                CASE
                    WHEN function_count < 21 THEN '1–20'
                    WHEN function_count < 51 THEN '21–50'
                    WHEN function_count < 101 THEN '51–100'
                    WHEN function_count < 201 THEN '101–200'
                    WHEN function_count < 401 THEN '201–400'
                    WHEN function_count < 801 THEN '401–800'
                    WHEN function_count < 1201 THEN '801–1200'
                    WHEN function_count < 1601 THEN '1201–1600'
                    WHEN function_count < 2001 THEN '1601–2000'
                    ELSE '2000+'
                END AS function_bucket,

                {LANGUAGE_GROUP_CASE_SQL} AS language_group,

                COUNT(*) AS repo_count
            FROM lizard_summary
            JOIN harvested_repositories hr ON lizard_summary.repo_id = hr.repo_id
            LEFT JOIN languages l ON hr.main_language = l.name
            {{where_clause}}
            GROUP BY function_bucket, {LANGUAGE_GROUP_CASE_SQL}
            HAVING {LANGUAGE_GROUP_CASE_SQL} NOT IN ('markup_or_data', 'no_language')
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
        base_query = f"""
            SELECT
                CASE
                    WHEN total_nloc < 1000 THEN '< 1K'
                    WHEN total_nloc < 5000 THEN '1K–4.9K'
                    WHEN total_nloc < 10000 THEN '5K–9.9K'
                    ELSE '10K+'
                END AS nloc_bucket,

                {LANGUAGE_GROUP_CASE_SQL} AS language_group,

                COUNT(*) AS repo_count
            FROM lizard_summary
            JOIN harvested_repositories hr ON lizard_summary.repo_id = hr.repo_id
            LEFT JOIN languages l ON hr.main_language = l.name
            {{where_clause}}
            GROUP BY nloc_bucket, {LANGUAGE_GROUP_CASE_SQL}
            HAVING {LANGUAGE_GROUP_CASE_SQL} NOT IN ('markup_or_data', 'no_language')
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
                lz.repo_id,
                hr.repo_name,
                hr.classification_label,
                lz.function_count,
                lz.total_ccn,
                ROUND(lz.total_ccn::numeric / NULLIF(lz.function_count, 0), 2) AS avg_ccn,
                rm.code_size_bytes
            FROM lizard_summary lz
            JOIN harvested_repositories hr ON lz.repo_id = hr.repo_id
            JOIN repo_metrics rm ON lz.repo_id = rm.repo_id
            {where_clause}
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        sql = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


