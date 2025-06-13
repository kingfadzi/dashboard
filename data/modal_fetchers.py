import pandas as pd
from sqlalchemy import text
from app.db import engine  # Or however your engine is initialized

def fetch_modal_rows(chart_id: str, value: str, filters: dict) -> pd.DataFrame:
    if chart_id == "spring-core-version-chart":
        return query_spring_core_by_version(value, filters)
    elif chart_id == "spring-boot-version-chart":
        return query_spring_boot_by_version(value, filters)
    return pd.DataFrame()

def query_spring_core_by_version(version: str, filters: dict) -> pd.DataFrame:
    sql = """
        SELECT hr.repo_id, hr.repo_name, hr.web_url, sd.package_name, sd.normalized_version
        FROM syft_dependencies sd
        JOIN harvested_repositories hr ON hr.repo_id = sd.repo_id
        WHERE sd.group_id = 'org.springframework'
          AND sd.normalized_version = :version
          {extra}
    """
    return run_filtered_query(sql, version, filters)

def query_spring_boot_by_version(version: str, filters: dict) -> pd.DataFrame:
    sql = """
        SELECT hr.repo_id, hr.repo_name, hr.web_url, sd.package_name, sd.normalized_version
        FROM syft_dependencies sd
        JOIN harvested_repositories hr ON hr.repo_id = sd.repo_id
        WHERE sd.group_id = 'org.springframework.boot'
          AND sd.normalized_version = :version
          {extra}
    """
    return run_filtered_query(sql, version, filters)

def run_filtered_query(base_sql: str, version: str, filters: dict) -> pd.DataFrame:
    conditions = []
    params = {"version": version}

    if filters.get("main_language"):
        conditions.append("hr.main_language = :main_language")
        params["main_language"] = filters["main_language"]

    if filters.get("host_name"):
        conditions.append("hr.host_name ILIKE :host_name")
        params["host_name"] = f"%{filters['host_name']}%"

    extra = f" AND {' AND '.join(conditions)}" if conditions else ""
    final_sql = base_sql.format(extra=extra)

    return pd.read_sql(text(final_sql), engine, params=params)