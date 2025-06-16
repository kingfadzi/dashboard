import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.buildtools.build_filter_conditions import build_filter_conditions
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


def build_count_query(base_table: str, joins: dict, filters: dict, field_alias_map: dict) -> str:
    query = f"SELECT COUNT(*) FROM {base_table}"
    required_joins = {
        alias: join_sql for alias, join_sql in joins.items()
        if any(field_alias_map.get(f) == alias for f in filters or {})
    }
    for join_sql in required_joins.values():
        query += f" {join_sql}"
    return query


def fetch_table_data(filters=None, page_current=0, page_size=10):
    @cache.memoize()
    def query_data(condition_string, param_dict, page_current, page_size):
        base_query = """
            SELECT
                hr.repo_id,
                hr.browse_url,
                COALESCE(NULLIF(hr.transaction_cycle, ''), '-None-') AS transaction_cycle,
                COALESCE(NULLIF(hr.app_id, ''), '-None-') AS app_id,
                hr.scope,
                hr.all_languages,
                hr.main_language,
                hr.classification_label,
                rm.total_commits,
                rm.activity_status,
                rm.repo_age_days,
                rm.number_of_contributors,
                rm.last_commit_date,
                -- Subquery to fetch the latest execution_time for this repo
                (
                  SELECT MAX(ael.execution_time)
                  FROM analysis_execution_log ael
                  WHERE ael.repo_id = hr.repo_id
                ) AS last_analysis_date
            FROM harvested_repositories hr
            LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
        """

        # Use helper to conditionally build count query
        field_alias_map = {
            "activity_status": "rm",
            "total_commits": "rm",
            "repo_age_days": "rm",
            "number_of_contributors": "rm",
            "last_commit_date": "rm",
            "transaction_cycle": "hr",
            "app_id": "hr",
            "all_languages": "hr",
            "main_language": "hr",
            "classification_label": "hr",
            "name": "hr",
            "scope": "hr",
            "repo_slug": "hr"
        }

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

        # bind paging params
        params = param_dict.copy()
        params.update({
            "limit":  page_size,
            "offset": page_current * page_size
        })

        # read data
        df = pd.read_sql(text(base_query), engine, params=params)

        # get total count
        total_count = pd.read_sql(text(count_query), engine, params=params).iloc[0, 0]

        # normalize numeric cols
        for col in ("total_commits", "number_of_contributors"):
            if col in df:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        # format existing date cols
        if "last_commit_date" in df:
            df["last_commit_date"] = pd.to_datetime(df["last_commit_date"], errors="coerce") \
                .dt.strftime("%Y-%m-%dT%H:%M:%S")

        # format repo_age_days
        if "repo_age_days" in df:
            df["repo_age_days"] = df["repo_age_days"].apply(format_repo_age)

        # format our new last_analysis_date
        if "last_analysis_date" in df:
            df["last_analysis_date"] = pd.to_datetime(df["last_analysis_date"], errors="coerce") \
                .dt.strftime("%B %d, %Y %I:%M %p")

        return df, total_count

    return query_data(*build_filter_conditions(filters, field_alias_map={
        "activity_status": "rm",
        "total_commits": "rm",
        "repo_age_days": "rm",
        "number_of_contributors": "rm",
        "last_commit_date": "rm",
        "transaction_cycle": "hr",
        "app_id": "hr",
        "all_languages": "hr",
        "main_language": "hr",
        "classification_label": "hr",
        "name": "hr",
        "repo_slug": "hr"
    }), page_current=page_current, page_size=page_size)