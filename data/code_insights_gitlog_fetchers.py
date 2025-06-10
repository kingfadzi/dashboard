import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.build_filter_conditions import build_filter_conditions
from utils.sql_filter_utils import LANGUAGE_GROUP_CASE_SQL


# 1. Average File Size (code size / file count)
def fetch_avg_file_size_buckets(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT 
                CASE 
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 500 THEN '< 500B'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 1000 THEN '500B - 1KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 5000 THEN '1KB - 5KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 20000 THEN '5KB - 20KB'
                    ELSE '20KB+' 
                END AS size_bucket,

                {LANGUAGE_GROUP_CASE_SQL} AS language_group,

                COUNT(*) AS repo_count

            FROM repo_metrics
            JOIN harvested_repositories hr ON repo_metrics.repo_id = hr.repo_id
            LEFT JOIN languages l ON hr.main_language = l.name
            {f'WHERE {condition_string}' if condition_string else ''}
            GROUP BY size_bucket, language_group
            ORDER BY size_bucket, repo_count DESC
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


# 2. Contributor Dominance (top contributor commits / total)
def fetch_contributor_dominance(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT 
                CASE 
                    WHEN total_commits = 0 THEN 'No Commits'
                    WHEN top_contributor_commits::float / total_commits >= 0.9 THEN '90%+'
                    WHEN top_contributor_commits::float / total_commits >= 0.75 THEN '75%-89%'
                    WHEN top_contributor_commits::float / total_commits >= 0.5 THEN '50%-74%'
                    ELSE '< 50%'
                END AS dominance_bucket,

                {LANGUAGE_GROUP_CASE_SQL} AS language_group,

                COUNT(*) AS repo_count
            FROM repo_metrics
            JOIN harvested_repositories hr ON repo_metrics.repo_id = hr.repo_id
            LEFT JOIN languages l ON hr.main_language = l.name
            {f'WHERE {condition_string}' if condition_string else ''}
            GROUP BY dominance_bucket, language_group
            ORDER BY dominance_bucket, repo_count DESC
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


# 3. Branch Sprawl (active branch count)
def fetch_branch_sprawl(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT 
                CASE 
                    WHEN active_branch_count = 0 THEN '0'
                    WHEN active_branch_count <= 5 THEN '1-5'
                    WHEN active_branch_count <= 15 THEN '6-15'
                    WHEN active_branch_count <= 30 THEN '16-30'
                    ELSE '30+'
                END AS branch_bucket,
                COUNT(*) AS repo_count
            FROM repo_metrics
            JOIN harvested_repositories hr ON repo_metrics.repo_id = hr.repo_id
            {f'WHERE {condition_string}' if condition_string else ''}
            GROUP BY branch_bucket
            ORDER BY repo_count DESC
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

# 4. Repo Age Buckets (in days)
def fetch_repo_age_buckets(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT 
                CASE 
                    WHEN repo_age_days < 365 THEN '< 1 year'
                    WHEN repo_age_days < 1095 THEN '1 - 3 years'
                    WHEN repo_age_days < 1825 THEN '3 - 5 years'
                    ELSE '5+ years'
                END AS age_bucket,
                COUNT(*) AS repo_count
            FROM repo_metrics
            JOIN harvested_repositories hr ON repo_metrics.repo_id = hr.repo_id
            {f'WHERE {condition_string}' if condition_string else ''}
            GROUP BY age_bucket
            ORDER BY repo_count DESC
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)
