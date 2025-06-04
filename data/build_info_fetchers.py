import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache
from data.sql_filter_utils import normalize_version_sql


# 1. Detection Coverage by Tool
def fetch_detection_coverage_by_tool(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT
                COALESCE(tool_group.tool, 'unknown') AS tool,
                COALESCE(tool_group.detection_status, 'No Modules Detected') AS detection_status,
                COUNT(DISTINCT hr.repo_id) AS repo_count
            FROM harvested_repositories hr
            LEFT JOIN (
                SELECT
                    repo_id,
                    MAX(tool) AS tool,
                    CASE
                        WHEN COUNT(*) = 0 THEN 'No Modules Detected'
                        WHEN MAX(CASE WHEN tool_version IS NOT NULL THEN 1 ELSE 0 END) = 1
                             AND MAX(CASE WHEN runtime_version IS NOT NULL THEN 1 ELSE 0 END) = 1 THEN 'Both'
                        WHEN MAX(CASE WHEN tool_version IS NOT NULL THEN 1 ELSE 0 END) = 1 THEN 'Only Tool'
                        WHEN MAX(CASE WHEN runtime_version IS NOT NULL THEN 1 ELSE 0 END) = 1 THEN 'Only Runtime'
                        ELSE 'Neither'
                    END AS detection_status
                FROM build_config_cache
                GROUP BY repo_id
            ) tool_group ON hr.repo_id = tool_group.repo_id
            {where_clause}
            GROUP BY COALESCE(tool_group.tool, 'unknown'), COALESCE(tool_group.detection_status, 'No Modules Detected')
            ORDER BY tool, detection_status
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


def fetch_module_counts_per_repo(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT
                CASE
                    WHEN module_count = 1 THEN '1'
                    WHEN module_count BETWEEN 2 AND 5 THEN '2–5'
                    WHEN module_count BETWEEN 6 AND 10 THEN '6–10'
                    ELSE '10+'
                END AS module_bucket,
                classification_label,
                COUNT(*) AS repo_count
            FROM (
                SELECT
                    build_config_cache.repo_id,
                    COUNT(*) AS module_count,
                    hr.classification_label
                FROM build_config_cache
                JOIN harvested_repositories hr ON build_config_cache.repo_id = hr.repo_id
                {where_clause}
                GROUP BY build_config_cache.repo_id, hr.classification_label
            ) sub
            GROUP BY module_bucket, classification_label
            ORDER BY module_bucket, classification_label
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)



# 3. Runtime Versions by Tool (fixed: includes variant)
@cache.memoize()
def fetch_runtime_versions_by_tool(filters=None):
    def query_data(condition_string, param_dict):
        normalized = normalize_version_sql("bcc.runtime_version")

        base_query = f"""
            SELECT
                bcc.tool,
                {normalized} AS runtime_version,
                bcc.variant,
                COUNT(DISTINCT bcc.repo_id) AS repo_count
            FROM build_config_cache bcc
            JOIN harvested_repositories hr ON bcc.repo_id = hr.repo_id
            WHERE bcc.runtime_version IS NOT NULL
            {{extra_where}}
            GROUP BY bcc.tool, runtime_version, bcc.variant
            ORDER BY bcc.tool, runtime_version, repo_count DESC
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(base_query.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


# 4. Status by Tool
def fetch_status_by_tool(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT build_config_cache.tool,
                   build_config_cache.status,
                   COUNT(DISTINCT build_config_cache.repo_id) AS repo_count
            FROM build_config_cache
            JOIN harvested_repositories hr ON build_config_cache.repo_id = hr.repo_id
            {where_clause}
            GROUP BY build_config_cache.tool, build_config_cache.status
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

# 5. Runtime Fragmentation by Tool
def fetch_runtime_fragmentation_by_tool(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT tool, COUNT(DISTINCT runtime_version) AS version_count
            FROM build_config_cache
            JOIN harvested_repositories hr ON build_config_cache.repo_id = hr.repo_id
            WHERE runtime_version IS NOT NULL
            {extra_where}
            GROUP BY tool
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(base_query.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)

# 6. Confidence Distribution
def fetch_confidence_distribution(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT
                COALESCE(bcc.tool, 'unknown') AS tool,
                bcc.confidence,
                COUNT(DISTINCT bcc.repo_id) AS repo_count
            FROM build_config_cache bcc
            JOIN harvested_repositories hr ON bcc.repo_id = hr.repo_id
            {where_clause}
            GROUP BY COALESCE(bcc.tool, 'unknown'), bcc.confidence
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(base_query.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)




# 7. Runtime Coverage by Tool
def fetch_runtime_build_coverage_by_language(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                CASE
                    WHEN LOWER(hr.main_language) = 'java' THEN 'java'
                    WHEN LOWER(hr.main_language) = 'python' THEN 'python'
                    WHEN LOWER(hr.main_language) IN ('javascript', 'typescript') THEN 'javascript'
                    WHEN LOWER(hr.main_language) IN ('c#', 'f#', 'vb.net', 'visual basic') THEN 'dotnet'
                    WHEN LOWER(hr.main_language) = 'no language' OR hr.main_language IS NULL THEN 'no_language'
                    WHEN LOWER(l.type) IN ('markup', 'data') THEN 'markup_or_data'
                    WHEN LOWER(l.type) = 'programming' THEN 'other_programming'
                    ELSE 'unknown'
                END AS language_group,

                CASE
                    WHEN bcc.tool IS NOT NULL AND bcc.runtime_version IS NOT NULL THEN 'Both Detected'
                    WHEN bcc.tool IS NOT NULL THEN 'Only Build Tool'
                    WHEN bcc.runtime_version IS NOT NULL THEN 'Only Runtime'
                    ELSE 'None Detected'
                END AS detection_status,

                COUNT(DISTINCT hr.repo_id) AS repo_count

            FROM harvested_repositories hr
            LEFT JOIN build_config_cache bcc ON hr.repo_id = bcc.repo_id
            LEFT JOIN languages l ON LOWER(hr.main_language) = LOWER(l.name)
            {where_clause}
            GROUP BY language_group, detection_status
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_build_tool_variants(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                bcc.variant,
                COUNT(DISTINCT bcc.repo_id) AS repo_count
            FROM build_config_cache bcc
            JOIN harvested_repositories hr ON bcc.repo_id = hr.repo_id
            {where_clause}
            AND bcc.variant IS NOT NULL
            GROUP BY bcc.variant
            ORDER BY repo_count DESC
            LIMIT 20
        """
        where_clause = f"WHERE {condition_string}" if condition_string else "WHERE TRUE"
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)