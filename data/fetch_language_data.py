import logging
import pandas as pd
from sqlalchemy import text

from data.build_filter_conditions import build_filter_conditions
from data.db_connection import engine
from data.cache_instance import cache
from data.sql_filter_utils import build_repo_filter_conditions

logger = logging.getLogger(__name__)

def fetch_language_data(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                main_language, 
                COUNT(*) AS repo_count
            FROM harvested_repositories
        """
        if condition_string:
            base_query += f" WHERE {condition_string}"

        base_query += " GROUP BY main_language"

        logger.debug("Executing language data query:")
        logger.debug(base_query)
        logger.debug("With parameters:")
        logger.debug(param_dict)

        stmt = text(base_query)
        return pd.read_sql(stmt, engine, params=param_dict)

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)
