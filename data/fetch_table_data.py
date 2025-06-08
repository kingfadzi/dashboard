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


def fetch_table_data(filters=None, page_current=0, page_size=10, table_id=None):
    @cache.memoize()
    def query_data(condition_string, param_dict, page_current, page_size):
        rc_fields = RC_COLUMNS_BY_TABLE_ID.get(table_id, [])

        rm_select_fields = [
            f"{col} AS rm_{col.split('.')[-1]}"
            for col in rc_fields
            if col.startswith("rm.")
        ]
        rc_select_fields = [
            f"{col} AS {col.split('.')[-1]}"
            for col in rc_fields
            if col.startswith("rc.")
        ]

        select_fields = [
            "hr.repo_id",
            "hr.browse_url",
            "hr.transaction_cycle",
            "hr.app_id",
            "hr.scope",
            "hr.all_languages",
            "hr.classification_label",
            "hr.activity_status",
            "hr.repo_slug",
        ]
        if rm_select_fields:
            select_fields.extend(rm_select_fields)

        base_query = f"""
            SELECT
                {", ".join(select_fields)}
            FROM harvested_repositories hr
            LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
        """

        if condition_string:
            base_query += f" WHERE {condition_string}"

        base_query += """
            ORDER BY 
                rm.last_commit_date DESC NULLS LAST,
                rm.number_of_contributors DESC
            LIMIT :limit
            OFFSET :offset
        """

        count_query = build_count_query(
            base_table="harvested_repositories hr",
            filters=filters or {},
            field_alias_map={
                "activity_status": "hr",
                "total_commits": "rm",
                "repo_age_days": "rm",
                "number_of_contributors": "rm",
                "last_commit_date": "rm",
                "transaction_cycle": "hr",
                "app_id": "hr",
                "all_languages": "hr",
                "classification_label": "hr",
                "name": "hr",
                "scope": "hr",
                "repo_slug": "hr",
            }
        )

        param_dict = param_dict.copy()
        param_dict.update({
            "limit": page_size,
            "offset": page_current * page_size
        })

        stmt = text(base_query)
        df = pd.read_sql(stmt, engine, params=param_dict)

        if rc_select_fields:
            rc_query = f"""
                SELECT
                    repo_id,
                    {", ".join(rc_select_fields)}
                FROM repo_catalog
                WHERE repo_id = ANY(:repo_ids)
            """
            rc_stmt = text(rc_query)
            rc_df = pd.read_sql(rc_stmt, engine, params={"repo_ids": df["repo_id"].tolist()})
            df = pd.merge(df, rc_df, how="left", on="repo_id")

        count_stmt = text(count_query)
        total_count = pd.read_sql(count_stmt, engine, params=param_dict).iloc[0, 0]

        numeric_columns = [
            "rm_total_commits", "rm_number_of_contributors", "rm_repo_age_days"
        ]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        if "rm_last_commit_date" in df.columns:
            df["rm_last_commit_date"] = pd.to_datetime(df["rm_last_commit_date"], errors="coerce").dt.strftime(
                "%Y-%m-%dT%H:%M:%S"
            )

        if "rm_repo_age_days" in df.columns:
            df["rm_repo_age_days"] = df["rm_repo_age_days"].apply(format_repo_age)

        return df, total_count

    return query_data(*build_filter_conditions(filters or {}, field_alias_map={
        "activity_status": "hr",
        "total_commits": "rm",
        "repo_age_days": "rm",
        "number_of_contributors": "rm",
        "last_commit_date": "rm",
        "transaction_cycle": "hr",
        "app_id": "hr",
        "all_languages": "hr",
        "classification_label": "hr",
        "name": "hr",
        "scope": "hr",
        "repo_slug": "hr",
    }), page_current=page_current, page_size=page_size)