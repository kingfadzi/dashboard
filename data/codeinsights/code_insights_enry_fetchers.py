import pandas as pd
from data.db_connection import engine
from data.buildtools.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_role_distribution(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT sub.language, sub.language_role, COUNT(DISTINCT sub.repo_id) AS repo_count
            FROM (
                SELECT
                    a.repo_id,
                    a.language,
                    CASE WHEN a.language = b.primary_language THEN 'primary' ELSE 'secondary' END AS language_role
                FROM go_enry_analysis a
                JOIN (
                    SELECT DISTINCT ON (repo_id) repo_id, language AS primary_language
                    FROM go_enry_analysis
                    ORDER BY repo_id, percent_usage DESC
                ) b ON a.repo_id = b.repo_id
                JOIN harvested_repositories hr ON a.repo_id = hr.repo_id
                JOIN languages l ON a.language = l.name
                WHERE l.type = 'programming'
                {f'AND {condition_string}' if condition_string else ''}
            ) sub
            GROUP BY sub.language, sub.language_role
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(
        filters, alias="hr", field_alias_map={"repo_slug": "hr"}
    )
    return query_data(condition_string, param_dict)

from sqlalchemy import text

def fetch_language_bubble_chart_data(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            WITH language_metrics AS (
                SELECT
                    ga.language,
                    ROUND(AVG(ga.percent_usage)::numeric, 2) AS avg_percent_usage,
                    COUNT(DISTINCT ga.repo_id) AS repo_count,
                    SUM(CASE WHEN ga.percent_usage = primary_langs.max_usage THEN 1 ELSE 0 END) AS primary_language_count,
                    ROUND(AVG(c.code / NULLIF(c.files, 0))::numeric, 1) AS avg_code_per_file
                FROM go_enry_analysis ga
                JOIN harvested_repositories hr ON ga.repo_id = hr.repo_id
                JOIN languages l ON ga.language = l.name
                JOIN cloc_metrics c ON ga.repo_id = c.repo_id AND ga.language = c.language
                JOIN (
                    SELECT repo_id, MAX(percent_usage) AS max_usage
                    FROM go_enry_analysis
                    GROUP BY repo_id
                ) primary_langs ON ga.repo_id = primary_langs.repo_id
                WHERE l.type = 'programming'
                  AND ga.percent_usage > 0
                  AND ga.percent_usage <> 'NaN'
                  {f'AND {condition_string}' if condition_string else ''}
                GROUP BY ga.language
                HAVING COUNT(DISTINCT ga.repo_id) > 5
            )
            SELECT 
                ROW_NUMBER() OVER (ORDER BY (repo_count * avg_percent_usage) DESC, avg_code_per_file DESC) AS row_num,
                *
            FROM language_metrics
            ORDER BY row_num
            LIMIT 10
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(
        filters, alias="hr", field_alias_map={"repo_slug": "hr"}
    )
    return query_data(condition_string, param_dict)


