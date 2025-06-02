import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.sql_filter_utils import build_repo_filter_conditions
from data.cache_instance import cache
from data.build_filter_conditions import build_filter_conditions

@cache.memoize()
def fetch_outdated_library_usage(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                sd.package_name,
                COUNT(DISTINCT sd.normalized_version) AS version_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            {where_clause}
            GROUP BY sd.package_name
            ORDER BY version_count DESC
            LIMIT 10
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)
    
    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_legacy_version_usage(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                CONCAT(split_part(sd.normalized_version, '.', 1), '.', split_part(sd.normalized_version, '.', 2)) AS major_minor,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE (sd.package_name ILIKE 'spring%%' OR sd.package_name ILIKE '%%boot%%')
            {extra_where}
            GROUP BY major_minor
            ORDER BY major_minor
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_junit_version_usage(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                sd.normalized_version,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE (sd.group_id ILIKE 'junit%%' OR sd.package_name ILIKE '%%junit%%')
            {extra_where}
            GROUP BY sd.normalized_version
            ORDER BY sd.normalized_version
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_dependency_count_per_repo(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                hr.repo_id,
                COUNT(sd.id) AS dep_count
            FROM harvested_repositories hr
            LEFT JOIN syft_dependencies sd ON hr.repo_id = sd.repo_id
            {where_clause}
            GROUP BY hr.repo_id
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_frameworks_per_repo(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                hr.repo_id,
                COUNT(DISTINCT sd.framework) AS framework_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            {where_clause}
            GROUP BY hr.repo_id
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)