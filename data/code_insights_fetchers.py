import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
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

def fetch_normalized_weight(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT ga.language, ROUND(AVG(ga.percent_usage)::numeric, 2) AS avg_percent_usage
            FROM go_enry_analysis ga
            JOIN harvested_repositories hr ON ga.repo_id = hr.repo_id
            JOIN languages l ON ga.language = l.name
            WHERE l.type = 'programming' and ga.percent_usage > 0
            {f'AND {condition_string}' if condition_string else ''}
            GROUP BY ga.language
            ORDER BY avg_percent_usage DESC
            LIMIT 20
        """
        sql = text(base_query)
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(
        filters, alias="hr", field_alias_map={"repo_slug": "hr"}
    )
    return query_data(condition_string, param_dict)
