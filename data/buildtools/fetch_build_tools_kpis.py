import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions
from data.shared_kpi_query import fetch_kpi_totals


def fetch_build_tools_kpis(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):

        shared_kpis = fetch_kpi_totals(condition_string, param_dict)

        tool_sql = f"""
            WITH base AS (
                SELECT hr.repo_id
                FROM harvested_repositories hr
                {f"WHERE {condition_string}" if condition_string else ""}
            )
            SELECT
                COUNT(*) AS repos,
                COUNT(DISTINCT b.variant) AS variants,
                COUNT(DISTINCT b.runtime_version) AS runtimes,
                COUNT(DISTINCT CASE WHEN b.repo_id IS NULL OR b.tool IS NULL THEN a.repo_id END) AS no_tool
            FROM base a
            LEFT JOIN build_config_cache b ON a.repo_id = b.repo_id
        """
        tool_df = pd.read_sql(text(tool_sql), engine, params=param_dict)

        return {
            "repos": int(tool_df["repos"].iloc[0] or 0),
            "variants": int(tool_df["variants"].iloc[0] or 0),
            "runtimes": int(tool_df["runtimes"].iloc[0] or 0),
            "no_tool": int(tool_df["no_tool"].iloc[0] or 0),
            "code_repos": int(shared_kpis.get("code_repos", 0)),
            "no_language_repos": int(shared_kpis.get("no_language_repos", 0)),
            "markup_data_repos": int(shared_kpis.get("markup_data_repos", 0)),
        }

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    return query_data(condition_string, param_dict)
