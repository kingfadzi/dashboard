import logging
import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

logger = logging.getLogger(__name__)

def fetch_table_data(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT
                repo_id,
                web_url,
                main_language AS language,
                total_commits AS commits,
                number_of_contributors AS contributors,
                last_commit_date AS last_commit
            FROM combined_repo_metrics
        """
        if condition_string:
            base_query += f" WHERE {condition_string}"

        logger.debug("Executing Table Query:")
        logger.debug(base_query)
        logger.debug("With parameters:")
        logger.debug(param_dict)

        stmt = text(base_query)
        df = pd.read_sql(stmt, engine, params=param_dict)

        if df.empty:
            return df

        df["web_url"] = df["web_url"].fillna("#")

        # Handle NaN values before converting to int
        for col in ["commits", "contributors"]:
            if col in df.columns:
                df[col] = df[col].fillna(0).astype(int)

        if "last_commit" in df.columns:
            df["last_commit"] = pd.to_datetime(df["last_commit"], errors="coerce").dt.strftime("%Y-%m-%d")

        return df

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)