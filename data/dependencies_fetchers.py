import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache
from data.sql_filter_utils import build_repo_filter_conditions


# 1. Syft Dependency Coverage
def fetch_dependency_detection_coverage(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
            SELECT status, COUNT(*) AS repo_count
            FROM (
                SELECT
                    hr.repo_id,
                    CASE WHEN sd.repo_id IS NULL THEN 'No Dependencies Detected'
                         ELSE 'Dependencies Detected'
                    END AS status
                FROM harvested_repositories hr
                LEFT JOIN syft_dependencies sd ON hr.repo_id = sd.repo_id  
                {where_clause}
                GROUP BY hr.repo_id, sd.repo_id
            ) sub
            GROUP BY status
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)


# 2. IaC Component Coverage
def fetch_iac_detection_coverage(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
            SELECT status, COUNT(*) AS repo_count
            FROM (
                SELECT
                    hr.repo_id,
                    CASE WHEN ic.repo_id IS NULL THEN 'No IaC Detected'
                         ELSE 'IaC Detected'
                    END AS status
                FROM harvested_repositories hr
                LEFT JOIN iac_components ic ON hr.repo_id = ic.repo_id
                LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
                {where_clause}
                GROUP BY hr.repo_id, ic.repo_id
            ) sub
            GROUP BY status
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)


# 3. Xeol EOL Coverage
def fetch_xeol_detection_coverage(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
            SELECT status, COUNT(*) AS repo_count
            FROM (
                SELECT
                    hr.repo_id,
                    CASE WHEN x.repo_id IS NULL THEN 'No EOL Detected'
                         ELSE 'EOL Artifacts Detected'
                    END AS status
                FROM harvested_repositories hr
                LEFT JOIN xeol_results x ON hr.repo_id = x.repo_id
                {where_clause}
                GROUP BY hr.repo_id, x.repo_id
            ) sub
            GROUP BY status
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_package_type_distribution(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT sd.package_type, COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            {where_clause}
            GROUP BY sd.package_type
            ORDER BY repo_count DESC
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_top_packages(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT sd.package_name, COUNT(*) AS count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            {where_clause}
            GROUP BY sd.package_name
            ORDER BY count DESC
            LIMIT 20
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_framework_distribution(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT sd.framework, COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd.framework IS NOT NULL AND sd.framework <> ''
            {extra_where}
            GROUP BY sd.framework
            ORDER BY repo_count DESC
            LIMIT 15
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_dependency_volume_buckets(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT dep_bucket, COUNT(*) AS repo_count
            FROM (
                SELECT
                    hr.repo_id,
                    CASE
                        WHEN COUNT(sd.id) = 0 THEN '0'
                        WHEN COUNT(sd.id) BETWEEN 1 AND 10 THEN '1–10'
                        WHEN COUNT(sd.id) BETWEEN 11 AND 50 THEN '11–50'
                        WHEN COUNT(sd.id) BETWEEN 51 AND 100 THEN '51–100'
                        ELSE '100+'
                    END AS dep_bucket
                FROM harvested_repositories hr
                LEFT JOIN syft_dependencies sd ON hr.repo_id = sd.repo_id
                {where_clause}
                GROUP BY hr.repo_id
            ) sub
            GROUP BY dep_bucket
            ORDER BY
                CASE dep_bucket
                    WHEN '0' THEN 1
                    WHEN '1–10' THEN 2
                    WHEN '11–50' THEN 3
                    WHEN '51–100' THEN 4
                    WHEN '100+' THEN 5
                END
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_xeol_top_products(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT x.product_name, COUNT(DISTINCT x.repo_id) AS repo_count
            FROM xeol_results x
            JOIN harvested_repositories hr ON x.repo_id = hr.repo_id
            WHERE x.product_name IS NOT NULL
            {extra_where}
            GROUP BY x.product_name
            ORDER BY repo_count DESC
            LIMIT 15
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)
    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_xeol_exposure_by_bucket_and_artifact_type(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT bucket, artifact_type, COUNT(*) AS repo_count
            FROM (
                SELECT
                    hr.repo_id,
                    COALESCE(x.artifact_type, 'unknown') AS artifact_type,
                    COUNT(x.id) AS eol_count,
                    CASE
                        WHEN COUNT(x.id) = 0 THEN '0'
                        WHEN COUNT(x.id) BETWEEN 1 AND 5 THEN '1–5'
                        WHEN COUNT(x.id) BETWEEN 6 AND 20 THEN '6–20'
                        ELSE '20+'
                    END AS bucket
                FROM harvested_repositories hr
                LEFT JOIN xeol_results x ON hr.repo_id = x.repo_id
                {where_clause}
                GROUP BY hr.repo_id, artifact_type
            ) sub
            WHERE bucket <> '0'
            GROUP BY bucket, artifact_type
            ORDER BY
                CASE bucket
                    WHEN '1–5' THEN 1
                    WHEN '6–20' THEN 2
                    ELSE 3
                END,
                artifact_type
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)
    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_iac_framework_usage(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT ic.framework, COUNT(DISTINCT ic.repo_id) AS repo_count
            FROM iac_components ic
            JOIN harvested_repositories hr ON ic.repo_id = hr.repo_id
            {where_clause}
            GROUP BY ic.framework
            ORDER BY repo_count DESC
            LIMIT 15
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)
    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_iac_adoption_by_framework_count(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT framework_bucket, COUNT(*) AS repo_count
            FROM (
                SELECT
                    hr.repo_id,
                    COUNT(DISTINCT ic.framework) AS framework_count,
                    CASE
                        WHEN COUNT(DISTINCT ic.framework) = 0 THEN '0 (none)'
                        WHEN COUNT(DISTINCT ic.framework) = 1 THEN '1'
                        WHEN COUNT(DISTINCT ic.framework) = 2 THEN '2'
                        WHEN COUNT(DISTINCT ic.framework) BETWEEN 3 AND 4 THEN '3–4'
                        ELSE '5+'
                    END AS framework_bucket
                FROM harvested_repositories hr
                LEFT JOIN iac_components ic ON hr.repo_id = ic.repo_id           
                {where_clause}
                GROUP BY hr.repo_id
            ) sub
            GROUP BY framework_bucket
            ORDER BY
                CASE framework_bucket
                    WHEN '0 (none)' THEN 1
                    WHEN '1' THEN 2
                    WHEN '2' THEN 3
                    WHEN '3–4' THEN 4
                    ELSE 5
                END
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)




