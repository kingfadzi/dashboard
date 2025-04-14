import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_table_data(filters=None, page_current=0, page_size=10):
    @cache.memoize()
    def query_data(condition_string, param_dict, page_current, page_size):
        base_query = """
            SELECT
                repo_id,
                web_url,
                tc,
                app_id,
                main_language,
                total_commits,
                number_of_contributors,
                last_commit_date
            FROM combined_repo_metrics
        """

        count_query = "SELECT COUNT(*) FROM combined_repo_metrics"

        if condition_string:
            base_query += f" WHERE {condition_string}"
            count_query += f" WHERE {condition_string}"

        base_query += """
            ORDER BY 
                last_commit_date DESC NULLS LAST,
                number_of_contributors DESC
            LIMIT :limit
            OFFSET :offset
        """

        param_dict = param_dict.copy()
        param_dict.update({
            "limit": page_size,
            "offset": page_current * page_size
        })

        # Execute paginated data query
        stmt = text(base_query)
        df = pd.read_sql(stmt, engine, params=param_dict)

        # Execute count query
        count_stmt = text(count_query)
        total_count = pd.read_sql(count_stmt, engine, params=param_dict).iloc[0, 0]

        numeric_columns = ["total_commits", "number_of_contributors"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        if "last_commit_date" in df.columns:
            df["last_commit_date"] = pd.to_datetime(df["last_commit_date"], errors="coerce").dt.strftime("%Y-%m-%dT%H:%M:%S")

        if "repo_id" in df.columns:
            df["repo_id"] = df["repo_id"].apply(
                lambda repo_id: f"<a href='/repo?repo_id={repo_id}' style='text-decoration: none; color: #007bff;'>{repo_id}</a>"
            )

        return df, total_count

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict, page_current, page_size)
