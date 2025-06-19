import os
import logging

from sqlalchemy import text
import pandas as pd
from data.cache_instance import cache
from data.db_connection import engine
from data.buildtools.build_filter_conditions import build_filter_conditions
from data.shared_kpi_query import fetch_kpi_totals

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
        param_dict["gitlab_host"]    = f"%{GITLAB_HOSTNAME}%"
        param_dict["bitbucket_host"] = f"%{BITBUCKET_HOSTNAME}%"

        query = f"""
            WITH base AS (
                SELECT
                    hr.repo_id,
                    hr.app_id,
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
                    b.repo_id,
                    CASE
                        WHEN LOWER(l.type) = 'programming' THEN 'code'
                        WHEN LOWER(l.type) IN ('markup','data') THEN 'data'
                        ELSE 'none'
                    END AS lang_group
                FROM base b
                LEFT JOIN languages l
                  ON LOWER(b.main_language) = LOWER(l.name)
                WHERE b.classification_label = 'Massive'
            )
            SELECT
                -- Total repos
                (SELECT COUNT(*) FROM base) AS total_repos,
                (SELECT COUNT(*) FROM base
                   WHERE app_id IS NOT NULL AND TRIM(app_id) <> ''
                ) AS repos_with_appid,
                (SELECT COUNT(*) FROM base
                   WHERE app_id IS NULL OR TRIM(app_id) = ''
                ) AS repos_without_appid,

                -- Activity
                (SELECT COUNT(*) FROM base
                   WHERE last_commit_date >= NOW() - INTERVAL '30 days'
                ) AS recently_updated,
                (SELECT COUNT(*) FROM base
                   WHERE repo_age_days <= 30
                ) AS new_repos,

                -- Age buckets
                (SELECT COUNT(*) FROM base WHERE repo_age_days > 1095) AS repos_3y,
                (SELECT COUNT(*) FROM base WHERE repo_age_days > 1825) AS repos_5y,
                (SELECT COUNT(*) FROM base WHERE repo_age_days > 3650) AS repos_10y,

                -- Massive classification
                (SELECT COUNT(*) FROM base
                   WHERE classification_label = 'Massive'
                ) AS massive_repos,
                (SELECT COUNT(*) FROM massive_lang_groups
                   WHERE lang_group = 'code'
                ) AS massive_code,
                (SELECT COUNT(*) FROM massive_lang_groups
                   WHERE lang_group = 'data'
                ) AS massive_data,
                (SELECT COUNT(*) FROM massive_lang_groups
                   WHERE lang_group = 'none'
                ) AS massive_none,

                -- Build tool / runtime
                (SELECT COUNT(DISTINCT bcc.repo_id)
                   FROM build_config_cache bcc
                   JOIN base USING (repo_id)
                   WHERE bcc.tool IS NOT NULL
                ) AS build_tool_detected,
                (SELECT COUNT(*) FROM build_config_cache bcc
                   JOIN base USING (repo_id)
                ) AS modules,
                -- **FIXED**: repos without any tool detected
                (SELECT COUNT(*) FROM base b
                   WHERE NOT EXISTS (
                     SELECT 1
                       FROM build_config_cache bcc
                      WHERE bcc.repo_id = b.repo_id
                        AND bcc.tool IS NOT NULL
                   )
                ) AS without_tool,
                (SELECT COUNT(DISTINCT bcc.repo_id)
                   FROM build_config_cache bcc
                   JOIN base USING (repo_id)
                   WHERE runtime_version IS NOT NULL
                ) AS runtime_detected,

                -- Language count (programming only)
                (SELECT COUNT(DISTINCT ga.language)
                   FROM go_enry_analysis ga
                   JOIN languages l ON ga.language = l.name
                   JOIN base USING (repo_id)
                   WHERE l.type = 'programming'
                ) AS languages,

                -- CI/CD breakdown
                (SELECT COUNT(DISTINCT iac.repo_id)
                   FROM iac_components iac JOIN base USING (repo_id)
                   WHERE framework IN ('Azure Pipelines', 'Bitbucket Pipelines', 'GitLab CI', 'Jenkins')
                ) AS cicd_total,
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

                -- Contributors & branches
                (SELECT COUNT(DISTINCT rm.repo_id)
                   FROM repo_metrics rm JOIN base USING (repo_id)
                   WHERE number_of_contributors = 1
                ) AS solo_contributor,
                (SELECT SUM(rm.number_of_contributors)
                   FROM repo_metrics rm JOIN base USING (repo_id)
                ) AS total_contributors,
                (SELECT COUNT(*) FROM repo_metrics rm JOIN base USING (repo_id) WHERE active_branch_count > 10) AS branch_sprawl;
        """

        # execute
        results = pd.read_sql(text(query), engine, params=param_dict).iloc[0].to_dict()

        # append shared LOC / file / function KPIs
        shared_kpis = fetch_kpi_totals(condition_string, param_dict)
        results.update({
            "loc":                 int(shared_kpis["total_loc"]       or 0),
            "source_files":        int(shared_kpis["total_files"]     or 0),
            "functions":           int(shared_kpis["total_functions"] or 0),
            "code_repos":          int(shared_kpis["code_repos"]            or 0),
            "markup_data_repos":   int(shared_kpis["markup_data_repos"]     or 0),
            "no_language_repos":   int(shared_kpis["no_language_repos"]     or 0),
        })

        # ensure ints for the new metric
        results["without_tool"] = int(results.get("without_tool", 0))

        return results

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)


