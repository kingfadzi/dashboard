import os
import pandas as pd
from sqlalchemy import text
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions
from data.shared_kpi_query import fetch_kpi_totals
from data.db_connection import engine

@cache.memoize()
def fetch_status_kpis(filters=None):
    """
    Fetch overview KPIs including analysis status counts.
    """
    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    param_dict["gitlab_host"]    = f"%{os.environ.get('GITLAB_HOSTNAME','gitlab')}%"
    param_dict["bitbucket_host"] = f"%{os.environ.get('BITBUCKET_HOSTNAME','bitbucket')}%"

    query = f"""
    WITH base AS (
        SELECT
            hr.repo_id,
            hr.app_id,
            hr.activity_status,
            hr.host_name,
            hr.main_language,
            hr.classification_label,
            hr.status AS analysis_status,
            rm.last_commit_date,
            rm.repo_age_days
        FROM harvested_repositories hr
        LEFT JOIN repo_metrics rm USING (repo_id)
        WHERE 1=1 {f'AND {condition_string}' if condition_string else ''}
    )
    SELECT
        COUNT(*) FILTER (WHERE analysis_status = 'FETCHED')     AS waiting,
        COUNT(*) FILTER (WHERE analysis_status = 'in_progress') AS in_progress,
        COUNT(*) FILTER (WHERE analysis_status = 'SUCCESS')     AS completed,
        COUNT(*) FILTER (WHERE analysis_status = 'FAILURE')     AS failed
    FROM base;
    """
    results = pd.read_sql(text(query), engine, params=param_dict).iloc[0].to_dict()
    # Append shared LOC / file / function KPIs
    shared = fetch_kpi_totals(condition_string, param_dict)
    results.update(
        loc               = int(shared.get("total_loc")          or 0),
        source_files      = int(shared.get("total_files")        or 0),
        functions         = int(shared.get("total_functions")    or 0),
        code_repos        = int(shared.get("code_repos")         or 0),
        markup_data_repos = int(shared.get("markup_data_repos")  or 0),
        no_language_repos = int(shared.get("no_language_repos")  or 0)
    )
    return results
