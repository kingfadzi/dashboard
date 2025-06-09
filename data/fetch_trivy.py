import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

@cache.memoize()
def fetch_trivy_repo_severity_by_resource_type(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT 
                tv.resource_type,
                tv.severity,
                COUNT(DISTINCT tv.repo_id) AS repo_count
            FROM trivy_vulnerability tv
            JOIN harvested_repositories hr USING (repo_id)
            WHERE tv.resource_type IS NOT NULL
              AND {condition_string}
            GROUP BY tv.resource_type, tv.severity
        """
        stmt = text(sql.format(condition_string=condition_string or "TRUE"))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_top_trivy_packages_by_severity(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            WITH package_counts AS (
                SELECT 
                    tv.pkg_name,
                    tv.severity,
                    COUNT(*) AS vuln_count
                FROM trivy_vulnerability tv
                JOIN harvested_repositories hr USING (repo_id)
                WHERE tv.pkg_name IS NOT NULL
                  AND {condition_string}
                GROUP BY tv.pkg_name, tv.severity
            ),
            top_packages AS (
                SELECT pkg_name
                FROM package_counts
                GROUP BY pkg_name
                ORDER BY SUM(vuln_count) DESC
                LIMIT 10
            )
            SELECT pc.pkg_name, pc.severity, pc.vuln_count
            FROM package_counts pc
            JOIN top_packages tp ON pc.pkg_name = tp.pkg_name
        """
        stmt = text(sql.format(condition_string=condition_string or "TRUE"))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_trivy_fix_status_by_severity(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT 
                tv.severity,
                CASE 
                    WHEN tv.fixed_version IS NOT NULL AND tv.fixed_version <> '' THEN 'Fix Available'
                    ELSE 'No Fix'
                END AS fix_status,
                COUNT(*) AS vuln_count
            FROM trivy_vulnerability tv
            JOIN harvested_repositories hr USING (repo_id)
            WHERE {condition_string}
            GROUP BY tv.severity, fix_status
        """
        stmt = text(sql.format(condition_string=condition_string or "TRUE"))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)
