import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_table_data(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
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

        if condition_string:
            base_query += f" WHERE {condition_string}"

        stmt = text(base_query)
        df = pd.read_sql(stmt, engine, params=param_dict)

        numeric_columns = ["total_commits", "number_of_contributors"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        if "last_commit_date" in df.columns:
            df["last_commit_date"] = pd.to_datetime(df["last_commit_date"], errors="coerce").dt.strftime("%Y-%m-%d")

        # ⭐ Real HTML link instead of markdown
        if "repo_id" in df.columns:
            df["repo_id"] = df["repo_id"].apply(
                lambda repo_id: f"<a href='/repo?repo_id={repo_id}' style='text-decoration: none; color: #007bff;'>{repo_id}</a>"
            )

        return df

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)
