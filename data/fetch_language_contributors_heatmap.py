import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.sql_filter_utils import build_repo_filter_conditions


def fetch_language_contributors_heatmap(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            WITH top_languages AS (
                SELECT 
                    hr.main_language,
                    COUNT(DISTINCT hr.repo_id) AS total_repos
                FROM harvested_repositories hr
                WHERE hr.main_language != 'SUM'
                GROUP BY hr.main_language
                ORDER BY total_repos DESC
                LIMIT 20
            )
            SELECT 
                hr.main_language AS language,
                CASE
                    WHEN rm.number_of_contributors BETWEEN 0 AND 1 THEN '0-1'
                    WHEN rm.number_of_contributors BETWEEN 2 AND 5 THEN '2-5'
                    WHEN rm.number_of_contributors BETWEEN 6 AND 10 THEN '6-10'
                    WHEN rm.number_of_contributors BETWEEN 11 AND 20 THEN '11-20'
                    WHEN rm.number_of_contributors BETWEEN 21 AND 50 THEN '21-50'
                    WHEN rm.number_of_contributors BETWEEN 51 AND 100 THEN '51-100'
                    WHEN rm.number_of_contributors BETWEEN 101 AND 500 THEN '101-500'
                    ELSE '500+'
                END AS contributor_bucket,
                COUNT(DISTINCT hr.repo_id) AS repo_count
            FROM harvested_repositories hr
            LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
            INNER JOIN top_languages tl ON hr.main_language = tl.main_language
            WHERE 1=1
        """


        if condition_string:
            base_query += f" AND {condition_string}"

        base_query += """
            GROUP BY hr.main_language, contributor_bucket
        """

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)
