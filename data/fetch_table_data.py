import pandas as pd
from sqlalchemy import text

from components.table_column_map import RC_COLUMNS_BY_TABLE_ID
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache


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


def fetch_table_data(filters=None, page_current=0, page_size=10, table_id=None):
    @cache.memoize()
    def query_data(condition_string, param_dict, page_current, page_size):
        # Build the SELECT list
        rc_fields = RC_COLUMNS_BY_TABLE_ID.get(table_id, [])
        select_fields = [
                            "hr.repo_id",
                            "hr.browse_url",
                            "hr.transaction_cycle",
                            "hr.app_id",
                            "hr.scope",
                            "hr.all_languages",
                            "hr.classification_label",
                            "rm.total_commits",
                            "rm.activity_status",
                            "rm.repo_age_days",
                            "rm.number_of_contributors",
                            "rm.last_commit_date",
                        ] + rc_fields

        base_query = f"""
            SELECT
                {', '.join(select_fields)}
            FROM harvested_repositories hr
            LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
            LEFT JOIN repo_catalog rc ON hr.repo_id = rc.repo_id
        """

        # Filters only on hr for now
        field_alias_map = {
            "activity_status": "hr",
            "transaction_cycle": "hr",
            "app_id": "hr",
            "all_languages": "hr",
            "classification_label": "hr",
            "name": "hr",
            "scope": "hr",
            "repo_slug": "hr",
        }
        condition_string, param_dict = build_filter_conditions(filters, field_alias_map=field_alias_map)

        # Apply WHERE
        if condition_string:
            base_query += f" WHERE {condition_string}"
            count_where = f" WHERE {condition_string}"
        else:
            count_where = ""

        # Count query (no joins)
        count_query = "SELECT COUNT(*) FROM harvested_repositories hr" + count_where

        # Add ORDER and pagination
        base_query += """
            ORDER BY
                rm.last_commit_date DESC NULLS LAST,
                rm.number_of_contributors DESC
            LIMIT :limit
            OFFSET :offset
        """
        param_dict = param_dict.copy()
        param_dict.update({"limit": page_size, "offset": page_current * page_size})

        # Execute
        df = pd.read_sql(text(base_query), engine, params=param_dict)
        total_count = pd.read_sql(text(count_query), engine, params=param_dict).iloc[0, 0]

        # ===== Convert and rename rm.* columns to unprefixed ====
        metrics_map = {
            "rm.total_commits": ("total_commits", int),
            "rm.number_of_contributors": ("number_of_contributors", int),
            "rm.repo_age_days": ("repo_age_days", None),
            "rm.last_commit_date": ("last_commit_date", "date"),
        }

        for rm_col, (out_col, dtype) in metrics_map.items():
            if rm_col in df.columns:
                series = df[rm_col]
                if dtype is int:
                    try:
                        df[out_col] = pd.to_numeric(series, errors="coerce").fillna(0).astype(int)
                    except Exception:
                        pass
                elif dtype == "date":
                    try:
                        df[out_col] = pd.to_datetime(series, errors="coerce").dt.strftime("%Y-%m-%dT%H:%M:%S")
                    except Exception:
                        pass
                elif dtype is None:
                    try:
                        df[out_col] = series.apply(format_repo_age)
                    except Exception:
                        pass

        return df, total_count

    # Prime the cache with the filter conditions
    condition_string, param_dict = build_filter_conditions(
        filters or {},
        field_alias_map={
            "activity_status": "hr",
            "transaction_cycle": "hr",
            "app_id": "hr",
            "all_languages": "hr",
            "classification_label": "hr",
            "name": "hr",
            "scope": "hr",
            "repo_slug": "hr",
        }
    )
    return query_data(condition_string, param_dict, page_current, page_size)
