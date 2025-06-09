import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_trivy_vulnerabilities(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                v.severity,
                COUNT(DISTINCT v.repo_id) AS repo_count
            FROM trivy_vulnerability v
            JOIN harvested_repositories hr ON v.repo_id = hr.repo_id
            WHERE v.severity IS NOT NULL
        """

        if condition_string:
            base_query += f" AND {condition_string}"

        base_query += " GROUP BY v.severity"

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_repo_count_by_trivy_severity(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT 
                severity,
                COUNT(DISTINCT repo_id) AS repo_count
            FROM trivy_vulnerability tv
            JOIN harvested_repositories hr USING (repo_id)
            WHERE {condition_string}
            GROUP BY severity
        """
        stmt = text(sql.format(condition_string=condition_string or "TRUE"))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_repo_count_by_trivy_resource_type_and_severity(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            WITH resource_totals AS (
                SELECT 
                    resource_type,
                    COUNT(DISTINCT repo_id) AS total_repo_count
                FROM trivy_vulnerability tv
                JOIN harvested_repositories hr USING (repo_id)
                WHERE resource_type IS NOT NULL AND {condition_string}
                GROUP BY resource_type
                ORDER BY total_repo_count DESC
                LIMIT 10
            )
            SELECT 
                tv.resource_type,
                tv.severity,
                COUNT(DISTINCT tv.repo_id) AS repo_count
            FROM trivy_vulnerability tv
            JOIN harvested_repositories hr USING (repo_id)
            JOIN resource_totals rt ON tv.resource_type = rt.resource_type
            WHERE {condition_string}
            GROUP BY tv.resource_type, tv.severity
        """
        stmt = text(sql.format(condition_string=condition_string or "TRUE"))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_repo_count_by_fix_status_and_severity(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT 
                severity,
                CASE 
                    WHEN fixed_version IS NOT NULL AND fixed_version <> '' THEN 'Fix Available'
                    ELSE 'No Fix'
                END AS fix_status,
                COUNT(DISTINCT repo_id) AS repo_count
            FROM trivy_vulnerability tv
            JOIN harvested_repositories hr USING (repo_id)
            WHERE {condition_string}
            GROUP BY severity, fix_status
        """
        stmt = text(sql.format(condition_string=condition_string or "TRUE"))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_top_expired_trivy_products(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                CASE
                    WHEN tv.resource_type = 'pom' THEN SPLIT_PART(tv.pkg_name, ':', 1)
                    ELSE tv.pkg_name
                END AS product_name,
                tv.resource_type,
                tv.severity,
                COUNT(DISTINCT tv.repo_id) AS repo_count
            FROM trivy_vulnerability tv
            JOIN harvested_repositories hr USING (repo_id)
            WHERE tv.pkg_name IS NOT NULL
              {extra_where}
            GROUP BY
                CASE
                    WHEN tv.resource_type = 'pom' THEN SPLIT_PART(tv.pkg_name, ':', 1)
                    ELSE tv.pkg_name
                END,
                tv.resource_type,
                tv.severity
            ORDER BY repo_count DESC
            LIMIT 10
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)
