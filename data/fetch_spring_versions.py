import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.build_filter_conditions import build_filter_conditions

@cache.memoize()
def fetch_spring_framework_versions(filters=None):
    def query_data(condition_string, param_dict, group_id):
        sql = f"""
            SELECT 
                CASE 
                    WHEN sd.version ~ '^\\d+\\.\\d+' 
                        THEN SPLIT_PART(sd.version, '.', 1) || '.' || SPLIT_PART(sd.version, '.', 2)
                    ELSE 'not detected'
                END AS major_minor,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd.group_id = :group_id
            {f"AND {condition_string}" if condition_string else ""}
            GROUP BY major_minor
            ORDER BY repo_count DESC
        """
        param_dict["group_id"] = group_id
        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df_core = query_data(condition_string, param_dict.copy(), "org.springframework")
    df_boot = query_data(condition_string, param_dict.copy(), "org.springframework.boot")
    return df_core, df_boot