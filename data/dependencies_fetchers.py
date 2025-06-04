import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache
from data.sql_filter_utils import build_repo_filter_conditions


# 1. Syft Dependency Coverage
def fetch_dependency_detection_coverage(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
            SELECT 
                sub.status,
                sub.main_language,
                sub.classification_label,
                COUNT(*) AS repo_count
            FROM (
                SELECT
                    hr.repo_id,
                    hr.main_language,
                    hr.classification_label,
                    CASE 
                        WHEN sd.repo_id IS NULL THEN 'None'
                        ELSE 'Detected'
                    END AS status
                FROM harvested_repositories hr
                LEFT JOIN syft_dependencies sd ON hr.repo_id = sd.repo_id  
                {where_clause}
                GROUP BY hr.repo_id, sd.repo_id, hr.main_language, hr.classification_label
            ) sub
            GROUP BY sub.status, sub.main_language, sub.classification_label
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)




# 2. IaC Component Coverage
def fetch_iac_detection_coverage(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
            SELECT status, COUNT(*) AS repo_count
            FROM (
                SELECT
                    hr.repo_id,
                    CASE WHEN ic.repo_id IS NULL THEN 'No IaC Detected'
                         ELSE 'IaC Detected'
                    END AS status
                FROM harvested_repositories hr
                LEFT JOIN iac_components ic ON hr.repo_id = ic.repo_id
                LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
                {where_clause}
                GROUP BY hr.repo_id, ic.repo_id
            ) sub
            GROUP BY status
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)


# 3. Xeol EOL Coverage
def fetch_xeol_detection_coverage(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
            SELECT status, COUNT(*) AS repo_count
            FROM (
                SELECT
                    hr.repo_id,
                    CASE WHEN x.repo_id IS NULL THEN 'No EOL Detected'
                         ELSE 'EOL Artifacts Detected'
                    END AS status
                FROM harvested_repositories hr
                LEFT JOIN xeol_results x ON hr.repo_id = x.repo_id
                {where_clause}
                GROUP BY hr.repo_id, x.repo_id
            ) sub
            GROUP BY status
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_package_type_distribution(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT sd.package_type, COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            {where_clause}
            GROUP BY sd.package_type
            ORDER BY repo_count DESC
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_subcategory_distribution(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            WITH subcat_totals AS (
                SELECT 
                    sd.sub_category,
                    COUNT(DISTINCT sd.repo_id) AS total_repo_count
                FROM syft_dependencies sd
                JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
                WHERE sd.sub_category IS NOT NULL AND sd.sub_category <> ''
                {extra_where}
                GROUP BY sd.sub_category
            ),
            top_subcategories AS (
                SELECT sub_category
                FROM subcat_totals
                ORDER BY total_repo_count DESC
                LIMIT 15
            )
            SELECT 
                sd.sub_category,
                sd.package_type,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            JOIN top_subcategories ts ON sd.sub_category = ts.sub_category
            WHERE sd.package_type IS NOT NULL AND sd.package_type <> ''
            {extra_where}
            GROUP BY sd.sub_category, sd.package_type
            ORDER BY sd.sub_category, repo_count DESC
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_dependency_volume_buckets(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                CASE
                    WHEN dep_count = 0 THEN '0'
                    WHEN dep_count <= 10 THEN '1–10'
                    WHEN dep_count <= 50 THEN '11–50' 
                    WHEN dep_count <= 100 THEN '51–100'
                    ELSE '100+'
                END AS dep_bucket,
                main_language,
                COUNT(*) AS repo_count
            FROM (
                SELECT 
                    hr.repo_id,
                    hr.main_language,
                    COUNT(sd.id) AS dep_count
                FROM harvested_repositories hr
                LEFT JOIN syft_dependencies sd ON hr.repo_id = sd.repo_id
                JOIN cloc_metrics cloc ON hr.repo_id = cloc.repo_id
                JOIN languages ON cloc.language = languages.name
                WHERE languages.type = 'programming'
                {extra_where}
                GROUP BY hr.repo_id, hr.main_language
            ) sub
            GROUP BY dep_bucket, main_language
            ORDER BY MIN(dep_count)
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_xeol_top_products(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                CASE
                    WHEN x.eol_date IS NULL THEN 'unknown'
                    WHEN CAST(x.eol_date AS DATE) < CURRENT_DATE THEN 'past_eol'
                    WHEN CAST(x.eol_date AS DATE) BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '180 days' THEN 'near_eol'
                    ELSE 'future_eol'
                END AS eol_state,
                x.artifact_type,
                COUNT(DISTINCT x.repo_id) AS repo_count
            FROM xeol_results x
            JOIN harvested_repositories hr ON x.repo_id = hr.repo_id
            WHERE x.product_name IS NOT NULL
            {extra_where}
            GROUP BY eol_state, x.artifact_type
            ORDER BY eol_state, artifact_type
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)


@cache.memoize()
def fetch_iac_category_summary(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                ic.category,
                COUNT(DISTINCT ic.framework) AS framework_count,
                COUNT(DISTINCT ic.repo_id) AS repo_count
            FROM iac_components ic
            JOIN harvested_repositories hr ON ic.repo_id = hr.repo_id
            {where_clause}
            GROUP BY ic.category
            ORDER BY repo_count DESC
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    df = query_data(condition_string, param_dict)
    return df if not df.empty else pd.DataFrame(columns=["category", "framework_count", "repo_count"])



@cache.memoize()
def fetch_iac_adoption_by_framework_count(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                framework_bucket,
                classification_label,
                COUNT(*) AS repo_count
            FROM (
                SELECT
                    hr.repo_id,
                    hr.classification_label,
                    COUNT(DISTINCT ic.framework) AS framework_count,
                    CASE
                        WHEN COUNT(DISTINCT ic.framework) = 0 THEN '0 (none)'
                        WHEN COUNT(DISTINCT ic.framework) = 1 THEN '1'
                        WHEN COUNT(DISTINCT ic.framework) BETWEEN 2 AND 4 THEN '2–4'
                        WHEN COUNT(DISTINCT ic.framework) BETWEEN 5 AND 7 THEN '5–7'
                        ELSE '8+'
                    END AS framework_bucket
                FROM harvested_repositories hr
                LEFT JOIN iac_components ic ON hr.repo_id = ic.repo_id
                {where_clause}
                GROUP BY hr.repo_id, hr.classification_label
            ) sub
            GROUP BY framework_bucket, classification_label
            ORDER BY
                CASE framework_bucket
                    WHEN '0 (none)' THEN 1
                    WHEN '1' THEN 2
                    WHEN '2–4' THEN 3
                    WHEN '5–7' THEN 4
                    ELSE 5
                END,
                classification_label
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)



@cache.memoize()
def fetch_top_expired_xeol_products(filters=None):
    def query_data(condition_string, param_dict):
        sql = """
            SELECT
                x.artifact_name,
                x.artifact_type,
                x.artifact_version,  -- NEW
                COUNT(DISTINCT x.repo_id) AS repo_count
            FROM xeol_results x
            JOIN harvested_repositories hr ON x.repo_id = hr.repo_id
            WHERE x.artifact_name IS NOT NULL
              AND x.eol_date IS NOT NULL
              AND CAST(x.eol_date AS DATE) < CURRENT_DATE
              {extra_where}
            GROUP BY x.artifact_name, x.artifact_type, x.artifact_version  
            ORDER BY repo_count DESC
            LIMIT 10
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)








