import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_role_distribution(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT Language, Role, COUNT(DISTINCT "Repo ID") AS "Repo Count"
            FROM (
                SELECT
                    a."Repo ID",
                    a."Language",
                    CASE WHEN a."Language" = b."Primary Language" THEN 'Primary' ELSE 'Secondary' END AS Role
                FROM go_enry_analysis a
                JOIN (
                    SELECT DISTINCT ON ("Repo ID") "Repo ID", "Language" AS "Primary Language"
                    FROM go_enry_analysis
                    ORDER BY "Repo ID", "Percent Usage" DESC
                ) b ON a."Repo ID" = b."Repo ID"
                {where_clause}
            ) sub
            GROUP BY Language, Role
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        sql = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)

def fetch_normalized_weight(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT Language, ROUND(AVG("Percent Usage"), 2) AS "Avg Percent Usage"
            FROM go_enry_analysis
            {where_clause}
            GROUP BY Language
            ORDER BY "Avg Percent Usage" DESC
            LIMIT 20
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        sql = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(sql, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)
