import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.build_filter_conditions import build_filter_conditions

def fetch_modal_rows(chart_id: str, value: str, filters: dict) -> pd.DataFrame:
    if chart_id == "spring-core-version-chart":
        return query_spring_core_by_version(value, filters)
    elif chart_id == "spring-boot-version-chart":
        return query_spring_boot_by_version(value, filters)
    return pd.DataFrame()

@cache.memoize()
def query_spring_core_by_version(version: str, filters: dict):
    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    param_dict["version"] = version

    sql = text(f"""
        SELECT hr.repo_id,
               hr.repo_name,
               hr.web_url,
               sd.package_name,
               sd.normalized_version
        FROM syft_dependencies sd
        JOIN harvested_repositories hr ON hr.repo_id = sd.repo_id
        WHERE sd.group_id = 'org.springframework'
          AND sd.normalized_version = :version
          {f'AND {condition_string}' if condition_string else ''}
    """)
    return pd.read_sql(sql, engine, params=param_dict)

@cache.memoize()
def query_spring_boot_by_version(version: str, filters: dict):
    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    param_dict["version"] = version

    sql = text(f"""
        SELECT hr.repo_id,
               hr.repo_name,
               hr.web_url,
               sd.package_name,
               sd.normalized_version
        FROM syft_dependencies sd
        JOIN harvested_repositories hr ON hr.repo_id = sd.repo_id
        WHERE sd.group_id = 'org.springframework.boot'
          AND sd.normalized_version = :version
          {f'AND {condition_string}' if condition_string else ''}
    """)
    return pd.read_sql(sql, engine, params=param_dict)