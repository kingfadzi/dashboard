import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.build_filter_conditions import build_filter_conditions

@cache.memoize()
def fetch_spring_framework_versions(filters=None):
    def query_data(condition_string, param_dict, group_prefix):
        sql = f"""
            SELECT 
                sd.version,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd.package_type = 'java-archive'
              AND sd.package_name LIKE :group_prefix
              {f"AND {condition_string}" if condition_string else ""}
            GROUP BY sd.version
            ORDER BY repo_count DESC
        """
        param_dict["group_prefix"] = f"{group_prefix}:%"
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df_core = query_data(condition_string, param_dict.copy(), "org.springframework")
    df_boot = query_data(condition_string, param_dict.copy(), "org.springframework.boot")
    return df_core, df_boot