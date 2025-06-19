import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.buildtools.build_filter_conditions import build_filter_conditions


def fetch_modal_rows(chart_id: str, click_data: dict, filters: dict | None = None):
    print(f"[FETCHER] chart_id = {chart_id}")
    print(f"[FETCHER] click_data = {click_data}")
    print(f"[FETCHER] filters = {filters}")

    if chart_id in {"spring-core-version-chart", "spring-boot-version-chart"}:
        version = click_data.get("version_bucket", "").lstrip("v")
        return _fetch_spring_modal_rows(version, filters)

    elif chart_id == "ee-usage-chart":
        return _fetch_ee_usage_modal_rows(click_data, filters)

    print(f"[FETCHER] No handler for chart_id = {chart_id}")
    return [], []



# --- Handlers ---

def _handle_spring(chart_id: str, click_data: dict, filters: dict | None):
    version = click_data.get("version_bucket", "")
    if not version:
        print("[_handle_spring] No version provided.")
        return [], []

    if version.startswith("v"):
        version = version[1:]
        print(f"[_handle_spring] stripped version = {version}")

    return _fetch_spring_modal_rows(version, filters)


def _handle_ee_usage(chart_id: str, click_data: dict, filters: dict | None):
    ee_usage = click_data.get("prefix", "").strip().lower()
    if not ee_usage:
        print("[_handle_ee_usage] No EE prefix provided.")
        return [], []

    return _fetch_ee_usage_modal_rows(ee_usage, filters)


# --- Query Runners ---

def _fetch_spring_modal_rows(version_prefix: str, filters: dict | None):
    condition_string, param_dict = build_filter_conditions(
        filters, alias="hr", field_alias_map={"repo_slug": "hr"}
    )
    param_dict["version_prefix"] = version_prefix

    sql = text(f"""
        SELECT DISTINCT
            hr.repo_id,
            hr.transaction_cycle,
            hr.app_id,
            sd.normalized_version AS version,
            hr.host_name    
        FROM syft_dependencies sd
        JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
        WHERE sd.normalized_version LIKE :version_prefix || '%'
          AND sd.group_id IN (
              'org.springframework', 'org.springframework.boot'
          )
          {f"AND {condition_string}" if condition_string else ""}
    """)

    df = pd.read_sql(sql, engine, params=param_dict)
    print(f"[_fetch_spring_modal_rows] matched rows = {len(df)}")
    if not df.empty:
        print(df.head())

    return (
        [{"field": col} for col in df.columns],
        df.to_dict("records")
    )


def _fetch_ee_usage_modal_rows(click_data: dict, filters: dict | None = None):
    ee_usage_prefix = click_data.get("ee_usage")
    print(f"[_fetch_ee_usage_modal_rows] incoming ee_usage_prefix = {ee_usage_prefix}")

    if not ee_usage_prefix:
        print("[_fetch_ee_usage_modal_rows] No prefix provided")
        return [], []

    condition_string, param_dict = build_filter_conditions(
        filters, alias="hr", field_alias_map={"repo_slug": "hr"}
    )

    # Build WHERE clause
    if ee_usage_prefix == "mixed":
        prefix_condition = "(sd.package_name ILIKE 'javax%' OR sd.package_name ILIKE 'jakarta%')"
    else:
        param_dict["prefix"] = ee_usage_prefix
        prefix_condition = "sd.package_name ILIKE :prefix || '%'"

    sql = text(f"""
        SELECT DISTINCT
            hr.repo_id,
            hr.transaction_cycle,
            hr.app_id,
            sd.package_name AS dependency,
            sd.normalized_version AS version,
          hr.host_name
        FROM syft_dependencies sd
        JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
        WHERE {prefix_condition}
        {f"AND {condition_string}" if condition_string else ""}
    """)

    df = pd.read_sql(sql, engine, params=param_dict)
    print(f"[_fetch_ee_usage_modal_rows] matched rows = {len(df)}")
    if not df.empty:
        print(df.head())

    return (
        [{"field": col} for col in df.columns],
        df.to_dict("records")
    )
