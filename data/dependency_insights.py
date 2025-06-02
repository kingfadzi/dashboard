import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.build_filter_conditions import build_filter_conditions

@cache.memoize()
def fetch_version_drift(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT "Package Name", COUNT(DISTINCT "Normalized Version") AS version_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            {f"WHERE {condition_string}" if condition_string else ""}
            GROUP BY "Package Name"
            ORDER BY version_count DESC
            LIMIT 20;
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_legacy_version_exposure(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT 
                sd."Framework",
                CASE 
                    WHEN sd."Normalized Version" ~ '^\\d+\\.\\d+' 
                    THEN SPLIT_PART(sd."Normalized Version", '.', 1) || '.' || SPLIT_PART(sd."Normalized Version", '.', 2)
                    ELSE 'not detected'
                END AS version,
                COUNT(*) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            {f"WHERE {condition_string}" if condition_string else ""}
            GROUP BY sd."Framework", version
            ORDER BY repo_count DESC;
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_testing_framework_versions(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT sd."Framework", sd."Normalized Version", COUNT(*) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE (LOWER(sd."Framework") LIKE '%junit%' OR LOWER(sd."Framework") LIKE '%pytest%' OR LOWER(sd."Framework") LIKE '%mocha%')
            {f"AND {condition_string}" if condition_string else ""}
            GROUP BY sd."Framework", sd."Normalized Version"
            ORDER BY repo_count DESC;
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_dependency_volume_distribution(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            WITH dep_counts AS (
                SELECT sd."Repo ID", COUNT(*) AS dep_count
                FROM syft_dependencies sd
                JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
                {f"WHERE {condition_string}" if condition_string else ""}
                GROUP BY sd."Repo ID"
            )
            SELECT
                CASE
                    WHEN dep_count <= 10 THEN '0–10'
                    WHEN dep_count <= 25 THEN '11–25'
                    WHEN dep_count <= 50 THEN '26–50'
                    WHEN dep_count <= 100 THEN '51–100'
                    ELSE '100+'
                END AS bucket,
                COUNT(*) AS repo_count
            FROM dep_counts
            GROUP BY bucket
            ORDER BY bucket;
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_framework_diversity_distribution(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            WITH fw_count AS (
                SELECT sd."Repo ID", COUNT(DISTINCT sd."Framework") AS fw_count
                FROM syft_dependencies sd
                JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
                WHERE sd."Framework" IS NOT NULL AND sd."Framework" <> ''
                {f"AND {condition_string}" if condition_string else ""}
                GROUP BY sd."Repo ID"
            )
            SELECT fw_count, COUNT(*) AS repo_count
            FROM fw_count
            GROUP BY fw_count
            ORDER BY fw_count;
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_category_coverage(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT sd."Category", COUNT(DISTINCT sd."Repo ID") AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd."Category" IS NOT NULL AND sd."Category" <> ''
            {f"AND {condition_string}" if condition_string else ""}
            GROUP BY sd."Category"
            ORDER BY repo_count DESC;
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_category_standardization(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT sd."Category", sd."Framework", COUNT(DISTINCT sd."Repo ID") AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd."Category" IS NOT NULL AND sd."Framework" IS NOT NULL
            {f"AND {condition_string}" if condition_string else ""}
            GROUP BY sd."Category", sd."Framework"
            ORDER BY repo_count DESC;
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_uncategorized_packages(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT COUNT(*) AS uncategorized_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE (sd."Category" IS NULL OR sd."Category" = '')
            {f"AND {condition_string}" if condition_string else ""};
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_framework_overlap(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT sd."Repo ID", sd."Category", COUNT(DISTINCT sd."Framework") AS framework_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd."Category" IS NOT NULL AND sd."Framework" IS NOT NULL
            {f"AND {condition_string}" if condition_string else ""}
            GROUP BY sd."Repo ID", sd."Category"
            HAVING COUNT(DISTINCT sd."Framework") > 1
            ORDER BY framework_count DESC;
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)
