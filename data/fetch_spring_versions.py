import pandas as pd
import logging
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.build_filter_conditions import build_filter_conditions
from univers.versions import MavenVersion

logger = logging.getLogger(__name__)

def classify_framework_version_bucket(version: str) -> str:
    try:
        mv = MavenVersion(version)
        if mv >= MavenVersion("7.0.0"):
            return "7.x"
        elif MavenVersion("6.0.0") <= mv < MavenVersion("7.0.0"):
            return "6.2.x – 6.0.x"
        elif mv == MavenVersion("5.3.0") or (MavenVersion("5.3.0") <= mv < MavenVersion("5.4.0")):
            return "5.3.x"
        elif MavenVersion("5.1.0") <= mv < MavenVersion("5.3.0"):
            return "5.2.x – 5.1.x"
        else:
            return "Legacy < 5.1"
    except Exception as e:
        logger.warning(f"[Spring Framework] Invalid version '{version}': {e}")
        return "Invalid / Unrecognized"

def classify_boot_version_bucket(version: str) -> str:
    try:
        mv = MavenVersion(version)
        if mv >= MavenVersion("4.0.0"):
            return "4.x"
        elif MavenVersion("3.4.0") <= mv < MavenVersion("3.6.0"):
            return "3.5.x – 3.4.x"
        elif MavenVersion("3.0.0") <= mv < MavenVersion("3.4.0"):
            return "3.3.x – 3.0.x"
        elif mv == MavenVersion("2.7.0") or (MavenVersion("2.7.0") <= mv < MavenVersion("2.8.0")):
            return "2.7.x"
        elif MavenVersion("2.0.0") <= mv < MavenVersion("2.7.0"):
            return "2.6.x – 2.0.x"
        elif mv < MavenVersion("2.0.0"):
            return "Legacy < 2.0"
        else:
            return "Invalid / Unrecognized"
    except Exception as e:
        logger.warning(f"[Spring Boot] Invalid version '{version}': {e}")
        return "Invalid / Unrecognized"

@cache.memoize()
def fetch_spring_framework_versions(filters=None):
    def query_data(condition_string, param_dict, group_id, bucket_fn):
        sql = f"""
            SELECT 
                sd.normalized_version AS version,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd.group_id = :group_id
            {f"AND {condition_string}" if condition_string else ""}
            GROUP BY sd.normalized_version
            ORDER BY repo_count DESC
        """
        params = param_dict.copy()
        params["group_id"] = group_id
        df = pd.read_sql(text(sql), engine, params=params)
        df["version_bucket"] = df["version"].apply(bucket_fn)
        df_grouped = (
            df.groupby("version_bucket", as_index=False)["repo_count"]
            .sum()
            .sort_values("repo_count", ascending=False)
        )
        return df_grouped

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df_core = query_data(condition_string, param_dict, "org.springframework", classify_framework_version_bucket)
    df_boot = query_data(condition_string, param_dict, "org.springframework.boot", classify_boot_version_bucket)
    return df_core, df_boot
