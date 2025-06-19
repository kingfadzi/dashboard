import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions
from utils.sql_filter_utils import LANGUAGE_GROUP_CASE_SQL


# 1. Average File Size (code size / file count)
def fetch_avg_file_size_buckets(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT 
                CASE 
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 1024 THEN '0–1KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 2048 THEN '1–2KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 4096 THEN '2–4KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 6144 THEN '4–6KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 8192 THEN '6–8KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 10240 THEN '8–10KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 12288 THEN '10–12KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 14336 THEN '12–14KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 16384 THEN '14–16KB'
                    WHEN code_size_bytes / NULLIF(file_count, 0) < 20480 THEN '16–20KB'
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
                    WHEN ratio < 0.1 THEN '0–10%'
                    WHEN ratio < 0.2 THEN '10–20%'
                    WHEN ratio < 0.3 THEN '20–30%'
                    WHEN ratio < 0.4 THEN '30–40%'
                    WHEN ratio < 0.5 THEN '40–50%'
                    WHEN ratio < 0.6 THEN '50–60%'
                    WHEN ratio < 0.7 THEN '60–70%'
                    WHEN ratio < 0.8 THEN '70–80%'
                    WHEN ratio < 0.9 THEN '80–90%'
                    ELSE '90–100%'
                END AS dominance_bucket,

                {LANGUAGE_GROUP_CASE_SQL} AS language_group,

                COUNT(*) AS repo_count

            FROM (
                SELECT *,
                       CASE WHEN total_commits > 0 THEN top_contributor_commits::float / total_commits ELSE NULL END AS ratio
                FROM repo_metrics
            ) rm
            JOIN harvested_repositories hr ON rm.repo_id = hr.repo_id
            LEFT JOIN languages l ON hr.main_language = l.name
            {f'WHERE {condition_string}' if condition_string else ''}
            GROUP BY dominance_bucket, language_group
            HAVING {LANGUAGE_GROUP_CASE_SQL} NOT IN ('markup_or_data', 'no_language')
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
            WITH bucketed AS (
                SELECT 
                    CASE 
                        WHEN active_branch_count = 1 THEN '1'
                        WHEN active_branch_count BETWEEN 2 AND 5 THEN '2-5'
                        WHEN active_branch_count BETWEEN 6 AND 8 THEN '6-8'
                        WHEN active_branch_count BETWEEN 9 AND 15 THEN '9-15'
                        WHEN active_branch_count BETWEEN 16 AND 20 THEN '16-20'
                        WHEN active_branch_count BETWEEN 21 AND 30 THEN '21-30'
                        WHEN active_branch_count BETWEEN 31 AND 40 THEN '31-40'
                        WHEN active_branch_count BETWEEN 41 AND 60 THEN '41-60'
                        WHEN active_branch_count BETWEEN 61 AND 80 THEN '61-80'
                        ELSE '80+'
                    END AS branch_bucket,

                    {LANGUAGE_GROUP_CASE_SQL} AS language_group,

                    COUNT(*) AS repo_count

                FROM repo_metrics
                JOIN harvested_repositories hr ON repo_metrics.repo_id = hr.repo_id
                LEFT JOIN languages l ON hr.main_language = l.name
                {f'WHERE {condition_string}' if condition_string else ''}
                GROUP BY branch_bucket, language_group
                HAVING {LANGUAGE_GROUP_CASE_SQL} NOT IN ('markup_or_data', 'no_language')
            )

            SELECT * FROM bucketed
            ORDER BY branch_bucket, repo_count DESC
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
                    WHEN repo_age_days < 30 THEN '<1 month'
                    WHEN repo_age_days < 90 THEN '1-3 months'
                    WHEN repo_age_days < 180 THEN '3-6 months'
                    WHEN repo_age_days < 365 THEN '6-12 months'
                    WHEN repo_age_days < 730 THEN '1-2 years'
                    WHEN repo_age_days < 1095 THEN '2-3 years'
                    WHEN repo_age_days < 1460 THEN '3-4 years'
                    WHEN repo_age_days < 1825 THEN '4-5 years'
                    WHEN repo_age_days < 2555 THEN '5-7 years'
                    ELSE '7+ years'
                END AS age_bucket,
                hr.classification_label,
                COUNT(*) AS repo_count
            FROM repo_metrics
            JOIN harvested_repositories hr ON repo_metrics.repo_id = hr.repo_id
            {f'WHERE {condition_string}' if condition_string else ''}
            GROUP BY age_bucket, hr.classification_label
            ORDER BY age_bucket, repo_count DESC
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


