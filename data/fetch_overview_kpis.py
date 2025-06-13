from sqlalchemy import text
import pandas as pd
from data.cache_instance import cache
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions

def fetch_overview_kpis(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        query = f"""
            WITH base AS (
                SELECT hr.repo_id, hr.activity_status, hr.host_name,
                       rm.last_commit_date, rm.repo_age_days
                FROM harvested_repositories hr
                LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
                WHERE 1=1
                {f'AND {condition_string}' if condition_string else ''}
            )
            SELECT
                -- Repository counts
                (SELECT COUNT(*) FROM base) AS total_repos,
                (SELECT COUNT(*) FROM base WHERE activity_status = 'ACTIVE') AS active,
                (SELECT COUNT(*) FROM base WHERE activity_status = 'INACTIVE') AS inactive,
                -- Activity
                (SELECT COUNT(*) FROM base WHERE last_commit_date >= NOW() - INTERVAL '30 days') AS recently_updated,
                (SELECT COUNT(*) FROM base WHERE repo_age_days <= 30) AS new_repos,
                -- Build tool / runtime
                (SELECT COUNT(DISTINCT bcc.repo_id) FROM build_config_cache bcc JOIN base USING (repo_id) WHERE tool IS NOT NULL) AS build_tool_detected,
                (SELECT COUNT(*) FROM build_config_cache bcc JOIN base USING (repo_id)) AS modules,
                (SELECT COUNT(*) FROM build_config_cache bcc JOIN base USING (repo_id) WHERE tool IS NULL) AS without_tool,
                (SELECT COUNT(DISTINCT bcc.repo_id) FROM build_config_cache bcc JOIN base USING (repo_id) WHERE runtime_version IS NOT NULL) AS runtime_detected,
                (SELECT COUNT(DISTINCT ga.language) FROM go_enry_analysis ga JOIN base USING (repo_id)) AS languages,
                -- CI/CD breakdown
                (SELECT COUNT(DISTINCT iac.repo_id) FROM iac_components iac JOIN base USING (repo_id)
                    WHERE framework IN ('Azure Pipelines', 'Bitbucket Pipelines', 'GitLab CI', 'Jenkins')) AS cicd_total,
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'Azure Pipelines') AS azure_pipelines,
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'Bitbucket Pipelines') AS bitbucket_pipelines,
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'GitLab CI') AS gitlab_ci,
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'Jenkins') AS jenkins,
                -- Source hosts count
                (SELECT COUNT(DISTINCT host_name) FROM base) AS sources_total,
                -- Code metrics
                (SELECT SUM(code) FROM cloc_metrics cm JOIN base USING (repo_id) WHERE cm.language != 'SUM') AS loc,
                (SELECT SUM(files) FROM cloc_metrics cm JOIN base USING (repo_id) WHERE cm.language != 'SUM') AS source_files,
              -- Contributors & branches
                (SELECT COUNT(DISTINCT rm.repo_id) FROM repo_metrics rm JOIN base USING (repo_id) WHERE number_of_contributors = 1) AS solo_contributor,
                (SELECT SUM(rm.number_of_contributors) FROM repo_metrics rm JOIN base USING (repo_id)) AS total_contributors,
                (SELECT COUNT(*) FROM repo_metrics rm JOIN base USING (repo_id) WHERE active_branch_count > 10) AS branch_sprawl;
        """
        return pd.read_sql(text(query), engine, params=param_dict).iloc[0].to_dict()

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)