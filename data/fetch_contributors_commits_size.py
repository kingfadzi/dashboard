import logging
import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.sql_filter_utils import build_repo_filter_conditions

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def human_readable_age(days):
    if days < 7:
        return f"{days} days"
    elif days < 30:
        return f"{days // 7} weeks"
    elif days < 365:
        return f"{days // 30} months"
    else:
        return f"{days // 365} years"


def deduplicate_comma_separated_values(values):
    if not values:
        return ""
    unique_values = set(values.split(","))
    return ",".join(sorted(unique_values))


def fetch_contributors_commits_size(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        base_query = """
            SELECT 
                hr.clone_url_ssh AS repo_url,
                rm.number_of_contributors AS contributors,
                rm.total_commits AS commits,
                rm.repo_size_bytes AS repo_size,
                hr.app_id,
                hr.browse_url AS web_url,
                hr.transaction_cycle AS tc,
                hr.component_id,
                hr.component_name,
                hr.repo_name,
                hr.repo_slug,
                hr.host_name,
                hr.main_language,
                hr.all_languages,
                hr.classification_label,
                hr.scope,
                rm.repo_age_days,
                rm.file_count,
                lz.total_nloc AS total_lines_of_code
            FROM harvested_repositories hr
            LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
            LEFT JOIN lizard_summary lz ON hr.repo_id = lz.repo_id
            JOIN languages l ON hr.main_language = l.name
            WHERE l.type = 'programming'
        """

        if condition_string:
            base_query += f" AND {condition_string}"

        logger.debug("Executing contributors/commits/size query:")
        logger.debug(base_query)
        logger.debug("With parameters:")
        logger.debug(param_dict)

        stmt = text(base_query)
        df = pd.read_sql(stmt, engine, params=param_dict)

        df["app_id"] = df["app_id"].apply(deduplicate_comma_separated_values)
        df["repo_age_human"] = df["repo_age_days"].apply(human_readable_age)
        df["total_lines_of_code"] = df["total_lines_of_code"].apply(
            lambda x: f"{int(x):,}" if pd.notnull(x) else None
        )

        return df

    condition_string, param_dict = build_repo_filter_conditions(filters)
    return query_data(condition_string, param_dict)
