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


def build_count_query(base_table: str, filters: dict, field_alias_map: dict) -> str:
    query = f"SELECT COUNT(*) FROM {base_table}"
    condition_string, _ = build_filter_conditions(filters, field_alias_map=field_alias_map)
    if condition_string:
        query += f" WHERE {condition_string}"
    return query


def fetch_table_data(filters=None, page_current=0, page_size=10, table_id="overview"):
    @cache.memoize()
    def query_data(condition_string, param_dict, page_current, page_size, table_id):
        # Always include these columns from hr
        hr_columns = [
            "hr.repo_id",
            "hr.browse_url",
            "hr.transaction_cycle",
            "hr.app_id",
            "hr.scope",
            "hr.all_languages",
            "hr.classification_label",
            "hr.name",
            "hr.repo_slug",
            "hr.host_name",
            "hr.platform",
            "hr.repo_size_bytes",
            "hr.last_commit_date",
            "hr.number_of_contributors",
        ]

        # Add rc columns based on table_id
        rc_columns = RC_COLUMNS_BY_TABLE_ID.get(table_id, RC_COLUMNS_BY_TABLE_ID["overview"])
        select_cols = hr_columns + rc_columns

        # SELECT query
        base_query = f"""
            SELECT {', '.join(select_cols)}
            FROM harvested_repositories hr
            LEFT JOIN repo_catalog rc ON hr.repo_id = rc.repo_id
        """

        # field alias map for WHERE logic
        field_alias_map = {col.split(".")[-1]: "hr" for col in hr_columns}
        field_alias_map.update({col.split(".")[-1]: "rc" for col in rc_columns})

        # WHERE clause
        condition_string, param_dict = build_filter_conditions(filters, field_alias_map=field_alias_map)
        if condition_string:
            base_query += f" WHERE {condition_string}"

        base_query += """
            ORDER BY hr.last_commit_date DESC NULLS LAST,
                     hr.number_of_contributors DESC
            LIMIT :limit OFFSET :offset
        """

        param_dict = param_dict.copy()
        param_dict.update({
            "limit": page_size,
            "offset": page_current * page_size
        })

        # COUNT query only from hr
        count_query = build_count_query("harvested_repositories hr", filters, field_alias_map={k: "hr" for k in field_alias_map if field_alias_map[k] == "hr"})

        # Execute
        df = pd.read_sql(text(base_query), engine, params=param_dict)
        total_count = pd.read_sql(text(count_query), engine, params=param_dict).iloc[0, 0]

        # Format fields
        if "number_of_contributors" in df.columns:
            df["number_of_contributors"] = pd.to_numeric(df["number_of_contributors"], errors="coerce").fillna(0).astype(int)

        if "total_commits" in df.columns:
            df["total_commits"] = pd.to_numeric(df["total_commits"], errors="coerce").fillna(0).astype(int)

        if "last_commit_date" in df.columns:
            df["last_commit_date"] = pd.to_datetime(df["last_commit_date"], errors="coerce").dt.strftime("%Y-%m-%dT%H:%M:%S")

        if "repo_age_days" in df.columns:
            df["repo_age_days"] = df["repo_age_days"].apply(format_repo_age)

        return df, total_count

    return query_data(*build_filter_conditions(filters or {}, field_alias_map={}),
                      page_current=page_current,
                      page_size=page_size,
                      table_id=table_id)