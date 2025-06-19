import json
import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache

@cache.memoize()
def fetch_repo_profile(repo_id: str) -> dict:
    sql = text("""
        SELECT profile_json
        FROM repo_profile_cache
        WHERE repo_id = :repo_id
    """)
    df = pd.read_sql(sql, engine, params={"repo_id": repo_id})
    if df.empty:
        raise ValueError(f"No cached profile found for repo_id={repo_id}")

    return json.loads(df["profile_json"].iloc[0])

@cache.memoize()
def fetch_harvested_repo(repo_id: str) -> dict:
    sql = text("""
        SELECT *
        FROM harvested_repositories
        WHERE repo_id = :repo_id
    """)
    df = pd.read_sql(sql, engine, params={"repo_id": repo_id})
    if df.empty:
        raise ValueError(f"No harvested repository found for repo_id={repo_id}")

    return df.iloc[0].to_dict()


@cache.memoize()
def classify_language_from_db(language: str) -> str:

    sql = text("""
        SELECT
            CASE
                WHEN LOWER(:language) = 'java' THEN 'java'
                WHEN LOWER(:language) = 'python' THEN 'python'
                WHEN LOWER(:language) IN ('javascript', 'typescript', 'tsx') THEN 'javascript'
                WHEN LOWER(:language) IN ('c#', 'f#', 'vb.net', 'visual basic','visual basic.net') THEN 'dotnet'
                WHEN LOWER(:language) IN ('go', 'golang') THEN 'go'
                WHEN LOWER(:language) = 'no language' THEN 'no_language'
                WHEN LOWER(l.type) IN ('markup', 'data') THEN 'markup_or_data'
                WHEN LOWER(l.type) = 'programming' THEN 'other_programming'
                ELSE 'unknown'
            END AS language_group
        FROM languages l
        WHERE LOWER(l.name) = LOWER(:language)
        LIMIT 1
    """)
    df = pd.read_sql(sql, engine, params={"language": language})
    return df["language_group"].iloc[0] if not df.empty else "unknown"

def fetch_last_analysis_log(repo_id: str) -> pd.DataFrame:

    @cache.memoize()
    def query_data(repo_id: str) -> pd.DataFrame:
        base_query = """
            SELECT
                method_name,
                stage,
                run_id,
                status,
                message,
                execution_time,
                duration
            FROM analysis_execution_log
            WHERE repo_id = :repo_id
              AND run_id = (
                  SELECT run_id
                  FROM analysis_execution_log
                  WHERE repo_id = :repo_id
                  ORDER BY execution_time DESC
                  LIMIT 1
              )
            ORDER BY execution_time 
        """
        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params={"repo_id": repo_id})

    return query_data(repo_id)