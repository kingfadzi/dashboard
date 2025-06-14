# fetch_overview_metrics.py

import logging

from data.fetch_contributors_commits_size import human_readable_age
from utils.sql_filter_utils import build_repo_filter_conditions, LANGUAGE_GROUP_CASE_SQL
from utils.formattting import deduplicate_comma_separated_values

logger = logging.getLogger(__name__)

def fetch_repo_status(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
        SELECT
            activity_status,
            host_name,
            COUNT(*) AS repo_count
        FROM harvested_repositories
        """
        if condition_string:
            sql += f" WHERE {condition_string}"
        sql += " GROUP BY activity_status, host_name"

        stmt = text(sql)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)
# fetch_overview_metrics.py


def _clean_classification_label(label):
    if isinstance(label, str):
        return label.split("->", 1)[1].strip() if "->" in label else label.strip()
    return label


def fetch_repo_sizes(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT
                hr.classification_label,
                {LANGUAGE_GROUP_CASE_SQL} AS language_group,
                COUNT(*) AS repo_count
            FROM harvested_repositories hr
            LEFT JOIN languages l ON hr.main_language = l.name
            {"WHERE " + condition_string if condition_string else ""}
            GROUP BY hr.classification_label, {LANGUAGE_GROUP_CASE_SQL}
           
        """

        stmt = text(sql)
        df = pd.read_sql(stmt, engine, params=param_dict)

        df["classification_value"] = df["classification_label"].apply(_clean_classification_label)
        df = df.groupby(["classification_value", "language_group"], as_index=False)["repo_count"].sum()
        df.rename(columns={"classification_value": "classification_label"}, inplace=True)

        return df

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)


def fetch_dev_frameworks(filters=None, selected_language=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                COALESCE(sd.framework, 'Unclassified') AS framework,
                sd.language,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories crm ON crm.repo_id = sd.repo_id
            WHERE TRIM(sd.sub_category) IN (
                'Caching Libraries',
                'Cloud & DevOps Tools',
                'Cloud SDKs',
                'Database Libraries',
                'Dependency Injection',
                'Frontend Frameworks',
                'Message Brokers & ETL Tools',
                'Messaging Frameworks',
                'Networking',
                'NoSQL & Big Data',
                'Relational Databases',
                'Spring Boot',
                'Spring Framework Core',
                'Web Frameworks'
            )
        """

        if condition_string:
            base_query += f" AND {condition_string}"
        if selected_language:
            base_query += " AND sd.language = :selected_language"
            param_dict["selected_language"] = selected_language

        base_query += """
            GROUP BY sd.framework, sd.language
            ORDER BY repo_count DESC
            LIMIT 20
        """

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)


import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache

def fetch_appserver_usage(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                ic.framework AS iac_type,
                COUNT(DISTINCT ic.repo_id) AS repo_count
            FROM iac_components ic
            JOIN harvested_repositories crm ON crm.repo_id = ic.repo_id
            WHERE ic.subcategory = 'Application Servers'
        """

        if condition_string:
            base_query += f" AND {condition_string}"

        base_query += " GROUP BY ic.framework ORDER BY repo_count DESC"

        stmt = text(base_query)
        df = pd.read_sql(stmt, engine, params=param_dict)
        return df if not df.empty else pd.DataFrame(columns=["iac_type", "repo_count"])

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)


def fetch_standards_issues(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT 
                COALESCE(s.category, 'Uncategorized') AS category,
                {LANGUAGE_GROUP_CASE_SQL} AS language_group,
                COUNT(DISTINCT s.repo_id) AS repo_count
            FROM semgrep_results s
            JOIN harvested_repositories hr ON s.repo_id = hr.repo_id
            JOIN repo_metrics rm ON s.repo_id = rm.repo_id
            LEFT JOIN languages l ON hr.main_language = l.name
            WHERE s.category IS NOT NULL AND TRIM(s.category) <> ''
        """

        if condition_string:
            base_query += f" AND {condition_string}"

        base_query += " GROUP BY category, language_group"

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)



def fetch_vulnerabilities(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT 
                v.severity,
                {LANGUAGE_GROUP_CASE_SQL} AS language_group,
                COUNT(DISTINCT v.repo_id) AS repo_count
            FROM trivy_vulnerability v
            JOIN harvested_repositories hr ON v.repo_id = hr.repo_id
            JOIN repo_metrics rm ON rm.repo_id = hr.repo_id
            LEFT JOIN languages l ON hr.main_language = l.name
            WHERE v.severity IS NOT NULL
        """

        if condition_string:
            base_query += f" AND {condition_string}"

        base_query += """
            GROUP BY v.severity, language_group
        """

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


def fetch_iac_usage(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        # CTE to find top 10 IaC frameworks
        base_query = f"""
            WITH top_frameworks AS (
                SELECT 
                    ic.framework AS iac_type
                FROM iac_components ic
                JOIN harvested_repositories hr ON hr.repo_id = ic.repo_id
                JOIN repo_metrics rm ON rm.repo_id = ic.repo_id
                LEFT JOIN languages l ON hr.main_language = l.name
                {f"WHERE {condition_string}" if condition_string else ""}
                GROUP BY ic.framework
                ORDER BY COUNT(DISTINCT ic.repo_id) DESC
                LIMIT 10
            )
            SELECT 
                ic.framework AS iac_type,
                {LANGUAGE_GROUP_CASE_SQL} AS language_group,
                COUNT(DISTINCT ic.repo_id) AS repo_count
            FROM iac_components ic
            JOIN harvested_repositories hr ON hr.repo_id = ic.repo_id
            JOIN repo_metrics rm ON rm.repo_id = ic.repo_id
            LEFT JOIN languages l ON hr.main_language = l.name
            JOIN top_frameworks tf ON tf.iac_type = ic.framework
            {f"WHERE {condition_string}" if condition_string else ""}
            GROUP BY ic.framework, language_group
        """

        logger.debug("Executing IaC framework usage query (top 10):")
        logger.debug(base_query)
        logger.debug("With parameters:")
        logger.debug(param_dict)

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)


def fetch_commit_buckets(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = f"""
        SELECT *
        FROM (
            SELECT
                CASE
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '1 month'   THEN '< 1 month'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '3 months'  THEN '1-3 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '6 months'  THEN '3-6 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '9 months'  THEN '6-9 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '12 months' THEN '9-12 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '15 months' THEN '12-15 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '18 months' THEN '15-18 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '21 months' THEN '18-21 months'
                    WHEN rm.last_commit_date >= NOW() - INTERVAL '24 months' THEN '21-24 months'
                    ELSE                                                       '24+ months'
                END AS commit_bucket,
                {LANGUAGE_GROUP_CASE_SQL} AS language_group,
                COUNT(DISTINCT rm.repo_id) AS repo_count
            FROM repo_metrics rm
            INNER JOIN harvested_repositories hr
              ON rm.repo_id = hr.repo_id
            LEFT JOIN languages l
              ON hr.main_language = l.name
            WHERE 1=1
              {f"AND {condition_string}" if condition_string else ""}
            GROUP BY 1, 2
        ) sub
        ORDER BY
            CASE commit_bucket
                WHEN '< 1 month'     THEN 1
                WHEN '1-3 months'    THEN 2
                WHEN '3-6 months'    THEN 3
                WHEN '6-9 months'    THEN 4
                WHEN '9-12 months'   THEN 5
                WHEN '12-15 months'  THEN 6
                WHEN '15-18 months'  THEN 7
                WHEN '18-21 months'  THEN 8
                WHEN '21-24 months'  THEN 9
                ELSE                   10
            END
        """
        stmt = text(sql)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)




@cache.memoize()
def fetch_multilang_usage(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
        WITH language_counts AS (
            SELECT
                gea.repo_id,
                COUNT(DISTINCT gea.language) AS language_count
            FROM go_enry_analysis gea
            JOIN languages l ON gea.language = l.name
            WHERE gea.percent_usage > 0
              AND l.type = 'programming'
            GROUP BY gea.repo_id
        ),
        bucketed_data AS (
            SELECT
                hr.classification_label,
                CASE
                    WHEN lc.language_count BETWEEN 1 AND 9 
                        THEN CAST(lc.language_count AS TEXT) || ' language' || 
                             CASE WHEN lc.language_count > 1 THEN 's' ELSE '' END
                    ELSE '10+ languages'
                END AS language_bucket
            FROM language_counts lc
            JOIN harvested_repositories hr
                ON lc.repo_id = hr.repo_id
            {f"WHERE {condition_string}" if condition_string else ""}
        )
        SELECT
            classification_label,
            language_bucket,
            COUNT(*) AS repo_count
        FROM bucketed_data
        GROUP BY classification_label, language_bucket
        ORDER BY
            classification_label,
            CASE 
                WHEN language_bucket = '10+ languages' THEN 10
                ELSE CAST(SPLIT_PART(language_bucket, ' ', 1) AS INTEGER)
            END
        """
        stmt = text(sql)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)



def fetch_cloc(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            SELECT 
                cloc.language AS main_language,
                SUM(cloc.blank) AS blank_lines,
                SUM(cloc.comment) AS comment_lines,
                SUM(cloc.code) AS total_lines_of_code,
                COUNT(*) AS source_code_file_count
            FROM cloc_metrics cloc
            JOIN languages l ON cloc.language = l.name
            JOIN harvested_repositories hr ON cloc.repo_id = hr.repo_id
            WHERE cloc.language IS NOT NULL 
              AND cloc.language != 'SUM'
              AND l.type = 'programming'
              {f'AND {condition_string}' if condition_string else ''}
            GROUP BY cloc.language
            ORDER BY total_lines_of_code DESC
            LIMIT 10
        """

        stmt = text(base_query)
        df = pd.read_sql(stmt, engine, params=param_dict)

        numeric_columns = ["blank_lines", "comment_lines", "total_lines_of_code", "source_code_file_count"]
        for column in numeric_columns:
            if column in df.columns:
                df[column] = df[column].apply(lambda x: int(x) if pd.notnull(x) else None)

        return df

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


def fetch_contribution_activity(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                hr.clone_url_ssh AS repo_url,
                rm.number_of_contributors AS contributors,
                rm.total_commits AS commits,
                rm.repo_size_bytes AS repo_size,
                hr.app_id,
                hr.browse_url AS web_url,
                hr.transaction_cycle AS tc,
                hr.component_id,
                hr.component_name,
                hr.repo_name,
                hr.repo_slug,
                hr.host_name,
                hr.main_language,
                hr.all_languages,
                hr.classification_label,
                hr.scope,
                rm.repo_age_days,
                rm.file_count,
                lz.total_nloc AS total_lines_of_code
            FROM harvested_repositories hr
            LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
            LEFT JOIN lizard_summary lz ON hr.repo_id = lz.repo_id
            JOIN languages l ON hr.main_language = l.name
            WHERE l.type = 'programming'
        """

        if condition_string:
            base_query += f" AND {condition_string}"

        logger.debug("Executing contributors/commits/size query:")
        logger.debug(base_query)
        logger.debug("With parameters:")
        logger.debug(param_dict)

        stmt = text(base_query)
        df = pd.read_sql(stmt, engine, params=param_dict)

        df["app_id"] = df["app_id"].apply(deduplicate_comma_separated_values)
        df["repo_age_human"] = df["repo_age_days"].apply(human_readable_age)
        df["total_lines_of_code"] = df["total_lines_of_code"].apply(
            lambda x: f"{int(x):,}" if pd.notnull(x) else None
        )

        return df

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

def fetch_language_distribution(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = f"""
            WITH top_languages AS (
                SELECT hr.main_language
                FROM harvested_repositories hr
                JOIN languages l ON hr.main_language = l.name
                WHERE l.type = 'programming'
                {f"AND {condition_string}" if condition_string else ""}
                GROUP BY hr.main_language
                ORDER BY COUNT(*) DESC
                LIMIT 10
            )
            SELECT 
                hr.main_language, 
                hr.classification_label,
                COUNT(*) AS repo_count
            FROM harvested_repositories hr
            JOIN languages l ON hr.main_language = l.name
            JOIN top_languages tl ON hr.main_language = tl.main_language
            WHERE l.type = 'programming'
            {f"AND {condition_string}" if condition_string else ""}
            GROUP BY hr.main_language, hr.classification_label
        """

        logger.debug("Executing top 10 language distribution query:")
        logger.debug(base_query)
        logger.debug("With parameters:")
        logger.debug(param_dict)

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)



@cache.memoize()
def fetch_package_types(filters=None):
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                sd.package_type,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories crm ON crm.repo_id = sd.repo_id
        """

        if condition_string:
            base_query += f" WHERE {condition_string}"

        base_query += " GROUP BY sd.package_type ORDER BY repo_count DESC LIMIT 10"

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)


def fetch_code_contributors(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            WITH top_languages AS (
                SELECT 
                    hr.main_language,
                    COUNT(DISTINCT hr.repo_id) AS total_repos
                FROM harvested_repositories hr
                JOIN languages l ON hr.main_language = l.name
                WHERE hr.main_language != 'SUM' AND l.type = 'programming'
                GROUP BY hr.main_language
                ORDER BY total_repos DESC
                LIMIT 15
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
            JOIN top_languages tl ON hr.main_language = tl.main_language
            JOIN languages l ON hr.main_language = l.name
            WHERE l.type = 'programming'
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
