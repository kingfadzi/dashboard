from sqlalchemy import text
import pandas as pd
from data.db_connection import engine


def fetch_kpi_totals(condition_string: str, param_dict: dict) -> dict:
    sql = f"""
        WITH base AS (
            SELECT
                hr.repo_id,
                hr.main_language,
                lang_main.type AS lang_type
            FROM harvested_repositories hr
            LEFT JOIN languages lang_main ON LOWER(hr.main_language) = LOWER(lang_main.name)
            {f"WHERE {condition_string}" if condition_string else ""}
        )

        SELECT
            COUNT(*) AS total_repos,

            COUNT(DISTINCT b.repo_id) FILTER (
                WHERE b.lang_type = 'programming'
            ) AS code_repos,

            COUNT(DISTINCT b.repo_id) FILTER (
                WHERE LOWER(b.main_language) = 'no language'
                   OR b.main_language IS NULL
                   OR TRIM(b.main_language) = ''
            ) AS no_language_repos,

            COUNT(DISTINCT b.repo_id) FILTER (
                WHERE LOWER(b.lang_type) IN ('markup', 'data')
            ) AS markup_data_repos,

            (
                SELECT SUM(cm.code)
                FROM cloc_metrics cm
                JOIN languages lang ON cm.language = lang.name
                WHERE cm.language != 'SUM'
                  AND lang.type = 'programming'
                  AND cm.repo_id IN (SELECT repo_id FROM base)
            ) AS total_loc,

            (
                SELECT SUM(cm.files)
                FROM cloc_metrics cm
                JOIN languages lang ON cm.language = lang.name
                WHERE cm.language != 'SUM'
                  AND lang.type = 'programming'
                  AND cm.repo_id IN (SELECT repo_id FROM base)
            ) AS total_files,

            (
                SELECT SUM(lz.function_count)
                FROM lizard_summary lz
                WHERE lz.repo_id IN (SELECT repo_id FROM base)
            ) AS total_functions

        FROM base b
    """
    return pd.read_sql(text(sql), engine, params=param_dict).iloc[0].to_dict()
