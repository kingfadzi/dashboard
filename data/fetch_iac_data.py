import logging
import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.sql_filter_utils import build_repo_filter_conditions

logger = logging.getLogger(__name__)

def fetch_iac_data(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                ic.framework AS iac_type,
                COUNT(DISTINCT ic.repo_id) AS repo_count
            FROM iac_components ic
            JOIN harvested_repositories hr ON hr.repo_id = ic.repo_id
            JOIN repo_metrics rm ON rm.repo_id = ic.repo_id
        """

        if condition_string:
            base_query += f" WHERE {condition_string}"

        base_query += " GROUP BY ic.framework ORDER BY repo_count DESC LIMIT 20"

        logger.debug("Executing IaC data query:")
        logger.debug(base_query)
        logger.debug("With parameters:")
        logger.debug(param_dict)

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)

@cache.memoize()
def fetch_iac_server_orchestration_usage(filters=None):
    def query_data(condition_string, param_dict):
        sql = f"""
            SELECT 
                ic.framework,
                COUNT(DISTINCT ic.repo_id) AS repo_count
            FROM iac_components ic
            JOIN harvested_repositories hr ON ic.repo_id = hr.repo_id
            WHERE ic.sub_category ILIKE ANY (
                ARRAY['application servers', 'kubernetes orchestration']
            )
            {f"AND {condition_string}" if condition_string else ""}
            GROUP BY ic.framework
            ORDER BY repo_count DESC
        """

        logger.debug("Executing IaC server/orchestration query:")
        logger.debug(sql)
        logger.debug("With parameters:")
        logger.debug(param_dict)

        return pd.read_sql(text(sql), engine, params=param_dict)

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)