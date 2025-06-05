import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache
from utils.sql_filter_utils import normalize_version_sql, build_repo_filter_conditions


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
                    WHEN LOWER(hr.main_language) IN ('go', 'golang') THEN 'go'
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


@cache.memoize()
def fetch_no_buildtool_repo_scatter(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            WITH dominant_language AS (
                SELECT
                    repo_id,
                    language,
                    SUM(files) AS file_count,
                    RANK() OVER (PARTITION BY repo_id ORDER BY SUM(files) DESC) AS lang_rank
                FROM cloc_metrics
                GROUP BY repo_id, language
            ),
            lang_types AS (
                SELECT
                    name,
                    type
                FROM languages
            )
            SELECT
                hr.repo_id,
                dom.file_count AS dominant_file_count,
                ROUND((rm.repo_size_bytes / 1024.0 / 1024.0)::numeric, 2) AS repo_size_mb,
                COALESCE(lt.type, 'unknown') AS dominant_language_type,
                rm.total_commits,
                rm.number_of_contributors AS contributor_count
            FROM harvested_repositories hr
            JOIN repo_metrics rm USING (repo_id)
            LEFT JOIN build_config_cache bcc USING (repo_id)
            JOIN dominant_language dom ON hr.repo_id = dom.repo_id AND dom.lang_rank = 1
            LEFT JOIN lang_types lt ON LOWER(dom.language) = LOWER(lt.name)
            WHERE bcc.tool IS NULL AND bcc.runtime_version IS NULL
            {f"AND {condition_string}" if condition_string else ""}
        """
        stmt = text(sql)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_no_buildtool_language_type_distribution(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            WITH dominant_language_grouped AS (
                SELECT
                    hr.repo_id,
                    hr.classification_label,
                    CASE
                        WHEN LOWER(cloc.language) = 'java' THEN 'java'
                        WHEN LOWER(cloc.language) = 'python' THEN 'python'
                        WHEN LOWER(cloc.language) IN ('javascript', 'typescript') THEN 'javascript'
                        WHEN LOWER(cloc.language) IN ('c#', 'f#', 'vb.net', 'visual basic') THEN 'dotnet'
                        WHEN LOWER(cloc.language) IN ('go', 'golang') THEN 'go'
                        WHEN LOWER(cloc.language) = 'no language' OR cloc.language IS NULL THEN 'no_language'
                        WHEN LOWER(l.type) IN ('markup', 'data') THEN 'markup_or_data'
                        WHEN LOWER(l.type) = 'programming' THEN 'other_programming'
                        ELSE 'unknown'
                    END AS dominant_language,
                    cloc.files,
                    ROW_NUMBER() OVER (
                        PARTITION BY hr.repo_id
                        ORDER BY cloc.files DESC
                    ) AS rn
                FROM harvested_repositories hr
                JOIN cloc_metrics cloc USING (repo_id)
                JOIN languages l ON LOWER(cloc.language) = LOWER(l.name)
                LEFT JOIN build_config_cache bcc USING (repo_id)
                WHERE bcc.tool IS NULL AND bcc.runtime_version IS NULL
                {f"AND {condition_string}" if condition_string else ""}
            )

            SELECT
                COALESCE(dominant_language, 'unknown') AS dominant_language,
                COALESCE(classification_label, 'unknown') AS classification_label,
                COUNT(DISTINCT repo_id) AS repo_count
            FROM dominant_language_grouped
            WHERE rn = 1
            GROUP BY dominant_language, classification_label
            ORDER BY dominant_language, classification_label
        """
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_dotnet_support_status_summary(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                CASE
                    WHEN b.runtime_version IN ('.NET 8', '.NET 9', '.NET Framework 4.8.1') THEN 'Active Support'
                    WHEN b.runtime_version = '.NET Framework 4.8' THEN 'Maintenance Mode'
                    WHEN b.runtime_version IN (
                        '.NET 5', '.NET 6', '.NET 7',
                        '.NET Core 1.0', '.NET Core 1.1',
                        '.NET Core 2.0', '.NET Core 2.1',
                        '.NET Core 3.0', '.NET Core 3.1',
                        '.NET Framework 1.1', '.NET Framework 2.0',
                        '.NET Framework 3.0', '.NET Framework 3.5',
                        '.NET Framework 4.0', '.NET Framework 4.5', '.NET Framework 4.5.1',
                        '.NET Framework 4.5.2', '.NET Framework 4.6', '.NET Framework 4.6.1',
                        '.NET Framework 4.6.2', '.NET Framework 4.7', '.NET Framework 4.7.1',
                        '.NET Framework 4.7.2'
                    ) THEN 'Out of Support'
                    WHEN b.runtime_version IN (
                        '.NET Standard 1.0', '.NET Standard 1.1', '.NET Standard 1.2',
                        '.NET Standard 1.3', '.NET Standard 1.4', '.NET Standard 1.5',
                        '.NET Standard 1.6', '.NET Standard 2.0', '.NET Standard 2.1'
                    ) THEN 'Deprecated'
                    ELSE 'Unknown'
                END AS support_status,
                hr.classification_label,
                COUNT(DISTINCT b.repo_id) AS repo_count
            FROM build_config_cache b
            JOIN harvested_repositories hr ON b.repo_id = hr.repo_id
            WHERE b.runtime_version IS NOT NULL
              AND b.tool = 'dotnet'
              {extra_where}
            GROUP BY support_status, hr.classification_label
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_java_support_status_summary(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                CASE
                    WHEN runtime_version IN ('jdk-17', 'jdk-21') THEN 'Active Support'
                    WHEN runtime_version = 'jdk-11' THEN 'Maintenance Mode'
                    WHEN runtime_version = 'jdk-8' THEN 'Out of Support'
                    WHEN runtime_version ~ '^jdk-[0-9]+$' AND substring(runtime_version from 5)::int < 8 THEN 'Deprecated'
                    ELSE 'Unknown'
                END AS support_status,
                hr.classification_label,
                COUNT(DISTINCT b.repo_id) AS repo_count
            FROM build_config_cache b
            JOIN harvested_repositories hr ON b.repo_id = hr.repo_id
            WHERE b.runtime_version IS NOT NULL
              AND b.tool IN ('maven', 'gradle')
              {extra_where}
            GROUP BY support_status, hr.classification_label
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_python_support_status_summary(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                CASE
                    WHEN regexp_replace(runtime_version, '[^0-9\\.]', '', 'g') IN ('3.11', '3.12') THEN 'Active Support'
                    WHEN regexp_replace(runtime_version, '[^0-9\\.]', '', 'g') = '3.10' THEN 'Maintenance Mode'
                    WHEN regexp_replace(runtime_version, '[^0-9\\.]', '', 'g') = '3.9' THEN 'Out of Support'
                    WHEN regexp_replace(runtime_version, '[^0-9\\.]', '', 'g') ~ '^3\\.[0-8]$' THEN 'Deprecated'
                    ELSE 'Unknown'
                END AS support_status,
                hr.classification_label,
                COUNT(DISTINCT b.repo_id) AS repo_count
            FROM build_config_cache b
            JOIN harvested_repositories hr ON b.repo_id = hr.repo_id
            WHERE b.runtime_version IS NOT NULL
              AND b.runtime_version <> ''
              AND b.tool = 'python'
              {extra_where}
            GROUP BY support_status, hr.classification_label
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_js_support_status_summary(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                CASE
                    WHEN regexp_replace(runtime_version, '[^0-9]', '', 'g') ~ '^[0-9]+$' AND regexp_replace(runtime_version, '[^0-9]', '', 'g')::int >= 18 THEN 'Active Support'
                    WHEN regexp_replace(runtime_version, '[^0-9]', '', 'g') = '16' THEN 'Maintenance Mode'
                    WHEN regexp_replace(runtime_version, '[^0-9]', '', 'g') = '14' THEN 'Out of Support'
                    WHEN regexp_replace(runtime_version, '[^0-9]', '', 'g') ~ '^[0-9]+$' AND regexp_replace(runtime_version, '[^0-9]', '', 'g')::int < 14 THEN 'Deprecated'
                    ELSE 'Unknown'
                END AS support_status,
                hr.classification_label,
                COUNT(DISTINCT b.repo_id) AS repo_count
            FROM build_config_cache b
            JOIN harvested_repositories hr ON b.repo_id = hr.repo_id
            WHERE b.runtime_version IS NOT NULL
              AND b.runtime_version <> ''
              AND regexp_replace(runtime_version, '[^0-9]', '', 'g') <> ''
              AND b.tool = 'javascript'
              {extra_where}
            GROUP BY support_status, hr.classification_label
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_go_support_status_summary(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                CASE
                    WHEN NULLIF(regexp_replace(runtime_version, '[^0-9.]', '', 'g'), '') IS NULL THEN 'Unknown'
                    WHEN split_part(runtime_version, '.', 1)::int >= 1 THEN
                        CASE
                            WHEN split_part(runtime_version, '.', 2)::int >= 20 THEN 'Active Support'
                            WHEN split_part(runtime_version, '.', 2)::int = 19 THEN 'Maintenance Mode'
                            WHEN split_part(runtime_version, '.', 2)::int = 18 THEN 'Out of Support'
                            WHEN split_part(runtime_version, '.', 2)::int < 18 THEN 'Deprecated'
                            ELSE 'Unknown'
                        END
                    ELSE 'Unknown'
                END AS support_status,
                hr.classification_label,
                COUNT(DISTINCT b.repo_id) AS repo_count
            FROM build_config_cache b
            JOIN harvested_repositories hr ON b.repo_id = hr.repo_id
            WHERE b.runtime_version IS NOT NULL
              AND b.tool = 'golang'
              {extra_where}
            GROUP BY support_status, hr.classification_label
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)

