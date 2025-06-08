import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache
from components.table_column_map import RC_COLUMNS_BY_TABLE_ID


def format_repo_age(days: int) -> str:
    if pd.isna(days):
        return "Unknown"
    days = int(days)
    if days < 30:
        return f"{days} days"
    elif days < 365:
        weeks = days // 7
        return f"{weeks} weeks"
    else:
        years = days / 365
        return f"{years:.1f} years"


def get_field_alias_map(table_id: str) -> dict:
    alias_map = {
        "activity_status": "hr",
        "transaction_cycle": "hr",
        "app_id": "hr",
        "all_languages": "hr",
        "classification_label": "hr",
        "scope": "hr",
        "repo_slug": "hr",
        "host_name": "hr",
    }

    rc_columns = RC_COLUMNS_BY_TABLE_ID.get(table_id, [])
    for col in rc_columns:
        if col.startswith("rm."):
            alias_map[col.replace("rm.", "")] = "rm"
        # ignore rc.* since they're enriched, not joined

    return alias_map


def build_count_query(base_table: str, joins: dict, filters: dict, field_alias_map: dict) -> str:
    query = f"SELECT COUNT(*) FROM {base_table}"
    required_joins = {
        alias: join_sql for alias, join_sql in joins.items()
        if any(field_alias_map.get(f) == alias for f in filters or {})
    }
    for join_sql in required_joins.values():
        query += f" {join_sql}"
    return query


def fetch_table_data(filters=None, page_current=0, page_size=10, table_id="overview"):
    @cache.memoize()
    def query_data(condition_string, param_dict, page_current, page_size):
        rc_columns = RC_COLUMNS_BY_TABLE_ID.get(table_id, [])
        rc_select_fields = [col.replace("rc.", "") for col in rc_columns if col.startswith("rc.")]
        rm_select_fields = [col.replace("rm.", "rm.") + f" AS rm_{col.replace('rm.', '')}" for col in rc_columns if col.startswith("rm.")]

        base_query = f"""
            SELECT
                hr.repo_id,
                hr.browse_url,
                hr.transaction_cycle,
                hr.app_id,
                hr.scope,
                hr.all_languages,
                hr.classification_label,
                hr.activity_status,
                hr.repo_slug,
                {", ".join(rm_select_fields) if rm_select_fields else ''}
            FROM harvested_repositories hr
            LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
        """

        field_alias_map = get_field_alias_map(table_id)

        count_query = build_count_query(
            base_table="harvested_repositories hr",
            joins={"rm": "LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id"},
            filters=filters,
            field_alias_map=field_alias_map
        )

        condition_string, param_dict = build_filter_conditions(filters, field_alias_map=field_alias_map)

        if condition_string:
            base_query += f" WHERE {condition_string}"
            count_query += f" WHERE {condition_string}"

        base_query += """
            ORDER BY 
                rm.last_commit_date DESC NULLS LAST,
                rm.number_of_contributors DESC
            LIMIT :limit
            OFFSET :offset
        """

        param_dict = param_dict.copy()
        param_dict.update({
            "limit": page_size,
            "offset": page_current * page_size
        })

        stmt = text(base_query)
        df = pd.read_sql(stmt, engine, params=param_dict)

        count_stmt = text(count_query)
        total_count = pd.read_sql(count_stmt, engine, params=param_dict).iloc[0, 0]

        numeric_columns = ["rm_total_commits", "rm_number_of_contributors"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        if "rm_last_commit_date" in df.columns:
            df["rm_last_commit_date"] = pd.to_datetime(df["rm_last_commit_date"], errors="coerce").dt.strftime("%Y-%m-%dT%H:%M:%S")

        if "rm_repo_age_days" in df.columns:
            df["rm_repo_age_days"] = df["rm_repo_age_days"].apply(format_repo_age)

        return df, total_count

    return query_data(*build_filter_conditions(filters or {}, field_alias_map=get_field_alias_map(table_id)),
                      page_current=page_current, page_size=page_size)