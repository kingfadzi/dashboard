import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.build_filter_conditions import build_filter_conditions

@cache.memoize()
def fetch_spring_framework_versions(filters=None):
    def query_data(condition_string, param_dict, framework_name):
        sql = f"""
            SELECT 
                sd.version,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd.framework ILIKE :framework
            {f"AND {condition_string}" if condition_string else ""}
            GROUP BY sd.version
            ORDER BY repo_count DESC
        """
        param_dict["framework"] = framework_name
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df_core = query_data(condition_string, param_dict.copy(), "spring core")
    df_boot = query_data(condition_string, param_dict.copy(), "spring boot core")
    return df_core, df_boot