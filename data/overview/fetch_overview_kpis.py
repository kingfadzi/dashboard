import os
import logging

from sqlalchemy import text
import pandas as pd
from data.cache_instance import cache
from data.db_connection import engine
from data.buildtools.build_filter_conditions import build_filter_conditions

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

GITLAB_HOSTNAME = os.environ.get("GITLAB_HOSTNAME", "gitlab")
BITBUCKET_HOSTNAME = os.environ.get("BITBUCKET_HOSTNAME", "bitbucket")

logger.info(f"GITLAB_HOSTNAME: {GITLAB_HOSTNAME}")
logger.info(f"BITBUCKET_HOSTNAME: {BITBUCKET_HOSTNAME}")


def fetch_overview_kpis(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        param_dict["gitlab_host"] = f"%{GITLAB_HOSTNAME}%"
        param_dict["bitbucket_host"] = f"%{BITBUCKET_HOSTNAME}%"

        query = f"""
            WITH base AS (
                SELECT
                    hr.repo_id,
                    hr.activity_status,
                    hr.host_name,
                    hr.main_language,
                    hr.classification_label,
                    rm.last_commit_date,
                    rm.repo_age_days
                FROM harvested_repositories hr
                LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
                WHERE 1=1
                {f'AND {condition_string}' if condition_string else ''}
            ),
            massive_lang_groups AS (
                SELECT
                    hr.repo_id,
                    CASE
                        WHEN l.type = 'programming' THEN 'code'
                        WHEN LOWER(hr.main_language) = 'no language' THEN 'no_language'
                        WHEN LOWER(l.type) IN ('markup', 'data') THEN 'markup_or_data'
                        ELSE 'unknown'
                    END AS lang_group
                FROM base hr
                LEFT JOIN languages l ON LOWER(hr.main_language) = LOWER(l.name)
                WHERE hr.classification_label = 'Massive'
            ),
            all_lang_groups AS (
                SELECT
                    hr.repo_id,
                    CASE
                        WHEN l.type = 'programming' THEN 'code'
                        WHEN LOWER(hr.main_language) = 'no language' THEN 'no_language'
                        WHEN LOWER(l.type) IN ('markup', 'data') THEN 'markup_or_data'                        
                        ELSE 'unknown'
                    END AS lang_group
                FROM base hr
                LEFT JOIN languages l ON LOWER(hr.main_language) = LOWER(l.name)
            )

            SELECT
                -- Total repo count
                (SELECT COUNT(*) FROM base) AS total_repos,

                -- Lang group distribution (distinct repos)
                (SELECT COUNT(DISTINCT repo_id) FROM all_lang_groups WHERE lang_group = 'code') AS lang_group_code,
                (SELECT COUNT(DISTINCT repo_id) FROM all_lang_groups WHERE lang_group = 'markup_or_data') AS lang_group_markup_or_data,
                (SELECT COUNT(DISTINCT repo_id) FROM all_lang_groups WHERE lang_group = 'no_language') AS lang_group_no_language,
                (SELECT COUNT(DISTINCT repo_id) FROM all_lang_groups WHERE lang_group = 'unknown') AS lang_group_unknown,

                -- Activity
                (SELECT COUNT(*) FROM base WHERE last_commit_date >= NOW() - INTERVAL '30 days') AS recently_updated,
                (SELECT COUNT(*) FROM base WHERE repo_age_days <= 30) AS new_repos,

                -- Age buckets
                (SELECT COUNT(*) FROM base WHERE repo_age_days > 1095) AS repos_3y,
                (SELECT COUNT(*) FROM base WHERE repo_age_days > 1825) AS repos_5y,
                (SELECT COUNT(*) FROM base WHERE repo_age_days > 3650) AS repos_10y,

                -- Massive classification breakdown
                (SELECT COUNT(*) FROM base WHERE classification_label = 'Massive') AS massive_repos,
                (SELECT COUNT(DISTINCT repo_id) FROM massive_lang_groups WHERE lang_group = 'code') AS massive_code,
                (SELECT COUNT(DISTINCT repo_id) FROM massive_lang_groups WHERE lang_group = 'markup_or_data') AS massive_markup_or_data,
                (SELECT COUNT(DISTINCT repo_id) FROM massive_lang_groups WHERE lang_group = 'no_language') AS massive_no_language,

                -- Build tool / runtime
                (SELECT COUNT(DISTINCT bcc.repo_id) FROM build_config_cache bcc JOIN base USING (repo_id) WHERE tool IS NOT NULL) AS build_tool_detected,
                (SELECT COUNT(*) FROM build_config_cache bcc JOIN base USING (repo_id)) AS modules,
                (SELECT COUNT(*) FROM build_config_cache bcc JOIN base USING (repo_id) WHERE tool IS NULL) AS without_tool,
                (SELECT COUNT(DISTINCT bcc.repo_id) FROM build_config_cache bcc JOIN base USING (repo_id) WHERE runtime_version IS NOT NULL) AS runtime_detected,

                -- Language count (programming only)
                (SELECT COUNT(DISTINCT ga.language)
                 FROM go_enry_analysis ga
                 JOIN languages l ON ga.language = l.name
                 JOIN base USING (repo_id)
                 WHERE l.type = 'programming') AS languages,

                -- CI/CD breakdown
                (SELECT COUNT(DISTINCT iac.repo_id) FROM iac_components iac JOIN base USING (repo_id)
                    WHERE framework IN ('Azure Pipelines', 'Bitbucket Pipelines', 'GitLab CI', 'Jenkins')) AS cicd_total,
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'Azure Pipelines') AS azure_pipelines,
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'Bitbucket Pipelines') AS bitbucket_pipelines,
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'GitLab CI') AS gitlab_ci,
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'Jenkins') AS jenkins,

                -- IaC: Docker & Helm
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'Dockerfile') AS dockerfiles,
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'docker-compose') AS docker_compose,
                (SELECT COUNT(*) FROM iac_components iac JOIN base USING (repo_id) WHERE framework = 'Helm Charts') AS helm_charts,

                -- Source hosts count
                (SELECT COUNT(DISTINCT host_name) FROM base) AS sources_total,
                (SELECT COUNT(*) FROM base WHERE host_name ILIKE :gitlab_host) AS gitlab,
                (SELECT COUNT(*) FROM base WHERE host_name ILIKE :bitbucket_host) AS bitbucket,

                -- Code metrics (programming only)
                (SELECT SUM(cm.code)
                 FROM cloc_metrics cm
                 JOIN languages l ON cm.language = l.name
                 JOIN base USING (repo_id)
                 WHERE cm.language != 'SUM' AND l.type = 'programming') AS loc,

                (SELECT SUM(cm.files)
                 FROM cloc_metrics cm
                 JOIN languages l ON cm.language = l.name
                 JOIN base USING (repo_id)
                 WHERE cm.language != 'SUM' AND l.type = 'programming') AS source_files,

                -- Contributors & branches
                (SELECT COUNT(DISTINCT rm.repo_id) FROM repo_metrics rm JOIN base USING (repo_id)
                    WHERE number_of_contributors = 1) AS solo_contributor,
                (SELECT SUM(rm.number_of_contributors) FROM repo_metrics rm JOIN base USING (repo_id)) AS total_contributors,
                (SELECT COUNT(*) FROM repo_metrics rm JOIN base USING (repo_id) WHERE active_branch_count > 10) AS branch_sprawl;
        """
        return pd.read_sql(text(query), engine, params=param_dict).iloc[0].to_dict()

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)
