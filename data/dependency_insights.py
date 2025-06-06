import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from utils.sql_filter_utils import build_repo_filter_conditions
from data.cache_instance import cache
from sqlalchemy import text
import pandas as pd
import numpy as np
from data.cache_instance import cache


@cache.memoize()
def fetch_middleware_usage_detailed(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                sd.sub_category,
                sd.framework,
                COUNT(DISTINCT sd.repo_id) AS repo_count,
                hr.main_language
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd.category ILIKE 'middleware'
            {extra_where}
            GROUP BY sd.sub_category, sd.framework, hr.main_language
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_middleware_usage_by_sub_category(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT
                sd.sub_category,
                sd.framework,
                hr.main_language,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd.category ILIKE 'middleware'
              AND sd.framework IS NOT NULL
              {f"AND {condition_string}" if condition_string else ""}
            GROUP BY sd.sub_category, sd.framework, hr.main_language
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_with_deps_by_variant(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            WITH contributor_buckets AS (
              SELECT
                repo_id,
                CASE
                  WHEN number_of_contributors = 0 THEN '0'
                  WHEN number_of_contributors BETWEEN 1 AND 5 THEN '1-5'
                  WHEN number_of_contributors BETWEEN 6 AND 10 THEN '6-10'
                  WHEN number_of_contributors BETWEEN 11 AND 20 THEN '11-20'
                  ELSE '21+'
                END AS contributors_bucket
              FROM repo_metrics
            )

            SELECT
              bcc.variant AS build_tool_variant,
              cb.contributors_bucket,
              COUNT(DISTINCT bcc.repo_id) AS repo_count
            FROM build_config_cache bcc
            JOIN contributor_buckets cb ON bcc.repo_id = cb.repo_id
            JOIN syft_dependencies sd ON bcc.repo_id = sd.repo_id
            JOIN harvested_repositories hr ON bcc.repo_id = hr.repo_id
            {extra_where}
            GROUP BY bcc.variant, cb.contributors_bucket
            ORDER BY bcc.variant,
              CASE cb.contributors_bucket
                WHEN '0' THEN 0
                WHEN '1-5' THEN 1
                WHEN '6-10' THEN 2
                WHEN '11-20' THEN 3
                ELSE 4
              END;
        """
        extra_where = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_avg_deps_per_package_type(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
              sd.package_type,
              COUNT(*) / COUNT(DISTINCT sd.repo_id) AS avg_dependencies_per_repo,
              COUNT(DISTINCT sd.repo_id) AS repo_count,
              COUNT(*) AS total_dependencies
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            {where_clause}
              AND sd.package_type IN ('go-module', 'java-archive', 'npm', 'python', 'dotnet')
            GROUP BY sd.package_type
            ORDER BY avg_dependencies_per_repo DESC
            LIMIT 5;
        """
        where_clause = f"WHERE {condition_string}" if condition_string else "WHERE TRUE"
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_no_dependency_repo_scatter(filters=None):
    def execute_query(condition_string, param_dict):
        sql = f"""
            WITH lang_groups AS (
                SELECT 
                    repo_id,
                    CASE LOWER(main_language)
                        WHEN 'java' THEN 'java'
                        WHEN 'python' THEN 'python'
                        WHEN 'javascript' THEN 'javascript'
                        WHEN 'typescript' THEN 'javascript'
                        WHEN 'c#' THEN 'dotnet'
                        WHEN 'f#' THEN 'dotnet'
                        WHEN 'vb.net' THEN 'dotnet'
                        WHEN 'visual basic' THEN 'dotnet'
                        WHEN 'go' THEN 'go'
                        WHEN 'golang' THEN 'go'
                        WHEN 'no language' THEN 'no_language'
                        ELSE 'other_programming'
                    END AS language_group
                FROM harvested_repositories
            ),
            buildtools AS (
                SELECT 
                    repo_id, 
                    STRING_AGG(
                        DISTINCT
                        CASE
                            WHEN runtime_version IS NOT NULL AND runtime_version != ''
                                THEN CONCAT(variant, ':', runtime_version)
                            ELSE variant
                        END,
                        ', '
                    ) AS build_tools
                FROM build_config_cache
                WHERE variant IS NOT NULL AND variant != ''
                GROUP BY repo_id
            )
            SELECT
                hr.repo_id,
                rm.number_of_contributors AS contributor_count,
                rm.total_commits,
                ROUND((rm.repo_size_bytes / 1048576.0)::numeric, 2) AS repo_size_mb,
                COALESCE(bt.build_tools, 'None') AS build_tools,
                lg.language_group
            FROM harvested_repositories hr
            JOIN repo_metrics rm USING (repo_id)
            JOIN lang_groups lg USING (repo_id)
            LEFT JOIN buildtools bt USING (repo_id)
            WHERE NOT EXISTS (
                SELECT 1 FROM syft_dependencies WHERE repo_id = hr.repo_id
            )
            {f"AND {condition_string}" if condition_string else ""}
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return execute_query(condition_string, param_dict).reset_index(drop=True)


@cache.memoize()
def fetch_no_dependency_buildtool_summary(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            WITH build_tools AS (
                SELECT
                    repo_id,
                    COALESCE(NULLIF(variant, ''), 'no_build_tool') AS variant
                FROM build_config_cache
            ),
            no_deps_repos AS (
                SELECT repo_id
                FROM harvested_repositories hr
                WHERE NOT EXISTS (
                    SELECT 1 FROM syft_dependencies sd WHERE sd.repo_id = hr.repo_id
                )
            )
            SELECT
                COALESCE(bt.variant, 'no_build_tool') AS variant,
                COUNT(DISTINCT nd.repo_id) AS repo_count
            FROM no_deps_repos nd
            LEFT JOIN build_tools bt USING (repo_id)
            {where_clause}
            GROUP BY COALESCE(bt.variant, 'no_build_tool')
            ORDER BY repo_count DESC
        """

        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)
