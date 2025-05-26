import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.build_filter_conditions import build_filter_conditions

# 1. Code Volume by Language
def fetch_code_volume_by_language(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT language, SUM(code) AS code_lines
            FROM cloc_metrics
            JOIN harvested_repositories hr ON cloc_metrics.repo_id = hr.repo_id
            {f'WHERE {condition_string}' if condition_string else ''}
            GROUP BY language
            ORDER BY code_lines DESC
            LIMIT 20
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

# 2. Total File Count by Language
def fetch_file_count_by_language(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT language, SUM(files) AS total_files
            FROM cloc_metrics
            JOIN harvested_repositories hr ON cloc_metrics.repo_id = hr.repo_id
            {f'WHERE {condition_string}' if condition_string else ''}
            GROUP BY language
            ORDER BY total_files DESC
            LIMIT 20
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

# 3. Code vs. Comment Composition
def fetch_code_composition_by_language(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT cloc_metrics.language,
               SUM(cloc_metrics.code) AS code,
               SUM(cloc_metrics.comment) AS comment,
               SUM(cloc_metrics.blank) AS blank
            FROM cloc_metrics
            JOIN harvested_repositories hr ON cloc_metrics.repo_id = hr.repo_id
            {f'WHERE {condition_string}' if condition_string else ''}
            GROUP BY language
            ORDER BY code DESC
            LIMIT 20
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

# 4. Code vs. File Scatter (Unbalanced Usage)
def fetch_code_file_scatter(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT language, SUM(code) AS code, SUM(files) AS files
            FROM cloc_metrics
            JOIN harvested_repositories hr ON cloc_metrics.repo_id = hr.repo_id
            {f'WHERE {condition_string}' if condition_string else ''}
            GROUP BY language
            HAVING SUM(code) > 0 AND SUM(files) > 0
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)
