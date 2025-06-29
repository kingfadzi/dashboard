import re
import pandas as pd
import logging
from sqlalchemy import text
from data.db_connection import engine
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions
from univers.versions import SemverVersion

logger = logging.getLogger(__name__)

# Only allow strings like 1.2, 1.2.3, 1.2.3-alpha, 1.2.3+build
SEMVER_LIKE_RE = re.compile(r"^\d+(\.\d+){1,2}([-+][\w.\-]+)?$")

def is_valid_version_string(v: str) -> bool:
    return isinstance(v, str) and v.strip() and SEMVER_LIKE_RE.match(v.strip())

def get_version_bucket(version: str) -> str:
    if not is_valid_version_string(version):
        logger.warning(f"[Version] Unrecognized version format: {version!r}")
        return "Invalid"

    try:
        sv = SemverVersion(version)
        return f"{sv.major}.{sv.minor}"
    except Exception as e:
        logger.warning(f"[Version] Failed to parse version '{version}': {e}")
        return "Invalid"

@cache.memoize()
def fetch_spring_framework_versions(filters=None):
    def query_data(condition_string, param_dict, group_id):
        sql = f"""
            SELECT 
                sd.normalized_version AS version,
                hr.host_name,
                COUNT(DISTINCT sd.repo_id) AS repo_count
            FROM syft_dependencies sd
            JOIN harvested_repositories hr ON sd.repo_id = hr.repo_id
            WHERE sd.group_id = :group_id
            {f"AND {condition_string}" if condition_string else ""}
            GROUP BY sd.normalized_version, hr.host_name
            ORDER BY repo_count DESC            
        """
        params = param_dict.copy()
        params["group_id"] = group_id

        df = pd.read_sql(text(sql), engine, params=params)
        df["repo_count"] = df["repo_count"].fillna(0).astype(int)
        df["version_bucket"] = df["version"].apply(get_version_bucket)

        df_grouped = (
            df.groupby(["version_bucket", "host_name"], as_index=False)["repo_count"]
            .sum()
        )

        # Calculate total repo_count per version_bucket
        top_versions = (
            df_grouped.groupby("version_bucket", as_index=False)["repo_count"]
            .sum()
            .sort_values("repo_count", ascending=False)
            .head(10)["version_bucket"]
            .tolist()
        )

        # Filter to only top 10 version buckets
        df_grouped = df_grouped[df_grouped["version_bucket"].isin(top_versions)]

        df_grouped["repo_count"] = df_grouped["repo_count"].astype(int)
        return df_grouped

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df_core = query_data(condition_string, param_dict, "org.springframework")
    df_boot = query_data(condition_string, param_dict, "org.springframework.boot")
    return df_core, df_boot

