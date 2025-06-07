import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache
from utils.sql_filter_utils import build_repo_filter_conditions


# 1. Syft Dependency Coverage
def fetch_dependency_detection_by_language(filters=None):
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
                  WHEN hr.main_language IS NULL OR LOWER(hr.main_language) = 'no language' THEN 'no_language'
                  WHEN LOWER(l.type) IN ('markup', 'data') THEN 'markup_or_data'
                  WHEN LOWER(l.type) = 'programming' THEN 'other_programming'
                  ELSE 'unknown'
                END AS language_group,

                -- 2) Determine detection status
                CASE
                  WHEN sd.repo_id IS NULL THEN 'None Detected'
                  ELSE 'Detected'
                END AS detection_status,

                COUNT(DISTINCT hr.repo_id) AS repo_count

            FROM harvested_repositories hr
            LEFT JOIN syft_dependencies sd
              ON hr.repo_id = sd.repo_id
            LEFT JOIN languages l
              ON LOWER(hr.main_language) = LOWER(l.name)
            {where_clause}
            GROUP BY language_group, detection_status
        """
        where_clause = f"WHERE {condition_string}" if condition_string else ""
        stmt = text(sql.format(where_clause=where_clause))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)





# 2. IaC Component Coverage (striped by language group)
def fetch_iac_detection_coverage(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
            WITH repo_language_group AS (
                SELECT
                    hr.repo_id,
                    CASE WHEN EXISTS (
                        SELECT 1
                        FROM iac_components ic 
                        WHERE ic.repo_id = hr.repo_id
                        AND (
                            ic.subcategory ILIKE 'compute services%%' OR
                            ic.subcategory ILIKE 'container%%' OR
                            ic.subcategory ILIKE 'kubernetes%%' OR
                            ic.subcategory ILIKE 'network security controls%%' OR
                            ic.subcategory ILIKE 'policy as code%%' OR
                            ic.subcategory ILIKE 'scaling%%' OR
                            ic.subcategory ILIKE 'storage services%%'
                        )
                        LIMIT 1
                    ) THEN 'IaC Detected' ELSE 'No IaC Detected' END AS status,
                    CASE
                        WHEN LOWER(hr.main_language) = 'java' THEN 'java'
                        WHEN LOWER(hr.main_language) = 'python' THEN 'python'
                        WHEN LOWER(hr.main_language) IN ('javascript', 'typescript') THEN 'javascript'
                        WHEN LOWER(hr.main_language) IN ('c#', 'f#', 'vb.net', 'visual basic') THEN 'dotnet'
                        WHEN LOWER(hr.main_language) IN ('go', 'golang') THEN 'go'
                        ELSE NULL
                    END AS language_group
                FROM harvested_repositories hr
                WHERE 
                    LOWER(hr.main_language) IN ('java', 'python', 'go', 'golang', 
                                                 'javascript', 'typescript', 
                                                 'c#', 'f#', 'vb.net', 'visual basic')
                    {condition_fragment}
            )
            SELECT
                status,
                language_group,
                COUNT(*) AS repo_count
            FROM repo_language_group
            WHERE language_group IS NOT NULL
            GROUP BY status, language_group
            ORDER BY status, language_group
        """
        condition_fragment = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(condition_fragment=condition_fragment))
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
            LIMIT 5
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
            WITH filtered_data AS (
                SELECT 
                    sd.sub_category,
                    sd.package_type,
                    sd.repo_id
                FROM syft_dependencies sd
                JOIN harvested_repositories hr 
                  USING (repo_id)
                WHERE 
                    sd.sub_category <> ''
                    AND sd.package_type <> ''
                    AND LOWER(sd.category) NOT IN (
                        'other',
                        'utility libraries',
                        'utilities & libraries',
                        'serialization',
                        'development tools',
                        'development & testing tools',
                        'developer tooling',
                        'build, dependency management & deployment tools'
                    )
                    {extra_where}
            ),

            subcat_totals AS (
                SELECT 
                    sub_category,
                    COUNT(DISTINCT repo_id) AS total_repo_count
                FROM filtered_data
                GROUP BY sub_category
            ),

            top_subcategories AS (
                SELECT sub_category
                FROM subcat_totals
                ORDER BY total_repo_count DESC
                LIMIT 15
            )

            SELECT 
                fd.sub_category,
                fd.package_type,
                COUNT(DISTINCT fd.repo_id) AS repo_count
            FROM filtered_data fd
            JOIN top_subcategories ts 
              USING (sub_category)
            GROUP BY fd.sub_category, fd.package_type
            ORDER BY fd.sub_category, repo_count DESC
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
            WITH dependency_buckets AS (
                SELECT 
                    hr.repo_id,
                    COUNT(sd.id) AS dep_count,
                    CASE
                        WHEN COUNT(sd.id) BETWEEN 1 AND 10 THEN '1–10'
                        WHEN COUNT(sd.id) BETWEEN 11 AND 20 THEN '11–20'
                        WHEN COUNT(sd.id) BETWEEN 21 AND 30 THEN '21–30'
                        WHEN COUNT(sd.id) BETWEEN 31 AND 40 THEN '31–40'
                        WHEN COUNT(sd.id) BETWEEN 41 AND 50 THEN '41–50'
                        WHEN COUNT(sd.id) BETWEEN 51 AND 100 THEN '51–100'
                        ELSE '101+'
                    END AS dep_bucket
                FROM harvested_repositories hr
                JOIN syft_dependencies sd USING (repo_id)
                {extra_where}
                GROUP BY hr.repo_id
                HAVING COUNT(sd.id) > 0
            )

            SELECT
                db.dep_bucket,
                COALESCE(sd.package_type, 'None') AS package_type,
                COUNT(DISTINCT db.repo_id) AS repo_count
            FROM dependency_buckets db
            JOIN syft_dependencies sd USING (repo_id)
            GROUP BY db.dep_bucket, sd.package_type
            ORDER BY 
                ARRAY_POSITION(
                    ARRAY['1–10', '11–20', '21–30', '31–40', '41–50', '51–100', '101+'],
                    db.dep_bucket
                ),
                repo_count DESC;
        """
        extra_where = f"WHERE {condition_string}" if condition_string else ""
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


@cache.memoize()
def fetch_no_deps_heatmap_data(filters=None):
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
              CASE
                WHEN LOWER(hr.main_language) = 'java' THEN 'java'
                WHEN LOWER(hr.main_language) = 'python' THEN 'python'
                WHEN LOWER(hr.main_language) IN ('javascript', 'typescript') THEN 'javascript'
                WHEN LOWER(hr.main_language) IN ('c#', 'f#', 'vb.net', 'visual basic') THEN 'dotnet'
                WHEN LOWER(hr.main_language) IN ('go', 'golang') THEN 'go'
                WHEN LOWER(hr.main_language) = 'no language' OR hr.main_language IS NULL THEN 'no_language'
                WHEN LOWER(lt.type) IN ('markup', 'data') THEN 'markup_or_data'
                WHEN LOWER(lt.type) = 'programming' THEN 'other_programming'
                ELSE 'unknown'
              END AS language_group,
              cb.contributors_bucket,
              COUNT(DISTINCT hr.repo_id) AS repos_without_dependencies
            FROM harvested_repositories hr
            JOIN contributor_buckets cb ON hr.repo_id = cb.repo_id
            LEFT JOIN syft_dependencies sd ON hr.repo_id = sd.repo_id
            LEFT JOIN languages lt ON LOWER(hr.main_language) = LOWER(lt.name)
            WHERE sd.repo_id IS NULL
            {extra_where}
            GROUP BY language_group, cb.contributors_bucket
            ORDER BY language_group,
              CASE cb.contributors_bucket
                WHEN '0' THEN 0
                WHEN '1-5' THEN 1
                WHEN '6-10' THEN 2
                WHEN '11-20' THEN 3
                ELSE 4
              END;
        """
        extra_where = f"AND {condition_string}" if condition_string else ""
        stmt = text(sql.format(extra_where=extra_where))
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)






