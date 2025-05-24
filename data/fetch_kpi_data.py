import pandas as pd
from sqlalchemy import text
from data.cache_instance import cache
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions

def human_readable_size(size_in_bytes):
    if size_in_bytes is None:
        size_in_bytes = 0
    if size_in_bytes < 1024:
        return f"{size_in_bytes:.2f} B"
    elif size_in_bytes < 1024**2:
        return f"{(size_in_bytes / 1024):.2f} KB"
    elif size_in_bytes < 1024**3:
        return f"{(size_in_bytes / (1024**2)):.2f} MB"
    else:
        return f"{(size_in_bytes / (1024**3)):.2f} GB"

def short_format(num):
    """
    Convert a number into short form with one decimal place:
    K for thousands, M for millions, B for billions.
    Numbers below 1000 are shown as an integer.
    """
    if not num:
        return "0"
    if isinstance(num, str):
        try:
            num = float(num.replace(",", ""))
        except Exception:
            return str(num)
    val = float(num)
    if val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.1f}B"
    elif val >= 1_000_000:
        return f"{val / 1_000_000:.1f}M"
    elif val >= 1_000:
        return f"{val / 1_000:.1f}K"
    else:
        return f"{val:.0f}"

@cache.memoize()
def fetch_kpi_data(filters=None):
    condition_string, param_dict = build_filter_conditions(filters)

    sql = """
    SELECT
        COUNT(*)::bigint AS total_repos,
        
        AVG(total_commits) AS avg_commits,
        MIN(total_commits) AS min_commits,
        MAX(total_commits) AS max_commits,
        
        AVG(number_of_contributors) AS avg_contributors,
        MIN(number_of_contributors) AS min_contributors,
        MAX(number_of_contributors) AS max_contributors,
        
        AVG(total_lines_of_code) AS avg_loc,
        MIN(total_lines_of_code) AS min_loc,
        MAX(total_lines_of_code) AS max_loc,
        
        AVG(avg_cyclomatic_complexity) AS avg_ccn,
        
        AVG(repo_size_bytes) AS avg_repo_size,
        MIN(repo_size_bytes) AS min_repo_size,
        MAX(repo_size_bytes) AS max_repo_size,
        
        SUM(CASE WHEN iac_dockerfile IS NOT NULL THEN iac_dockerfile ELSE 0 END) AS dockerfiles,
        
        SUM(total_token_count) AS total_token_count,
        SUM(function_count) AS function_count,
        SUM(total_cyclomatic_complexity) AS total_cyclomatic_complexity
    FROM combined_repo_metrics_api
    """

    if condition_string:
        sql += f" WHERE {condition_string}"

    df = pd.read_sql(text(sql), engine, params=param_dict)

    if df.empty:
        return {
            "total_repos": "0",
            "avg_commits": {"value": "0", "min": "0", "max": "0"},
            "avg_contributors": {"value": "0", "min": "0", "max": "0"},
            "avg_loc": {"value": "0", "min": "0", "max": "0"},
            "avg_ccn": {
                "value": "0",
                "function_count": "0",
                "total_cyclomatic_complexity": "0",
            },
            "avg_repo_size": {"value": "0.00 B", "min": "0.00 B", "max": "0.00 B"},
            "dockerfiles": "0"
        }

    row = df.iloc[0]

    total_repos = f"{(row['total_repos'] or 0):,.0f}"
    avg_commits = f"{(row['avg_commits'] or 0):,.0f}"
    avg_contributors = f"{(row['avg_contributors'] or 0):,.0f}"
    avg_loc = f"{(row['avg_loc'] or 0):,.0f}"
    avg_ccn = f"{(row['avg_ccn'] or 0):,.1f}"
    dockerfiles = f"{(row['dockerfiles'] or 0):,.0f}"

    avg_repo_size_str = human_readable_size(row['avg_repo_size'])
    min_repo_size_str = human_readable_size(row['min_repo_size'])
    max_repo_size_str = human_readable_size(row['max_repo_size'])

    min_commits = short_format(row['min_commits'] or 0)
    max_commits = short_format(row['max_commits'] or 0)
    min_contributors = short_format(row['min_contributors'] or 0)
    max_contributors = short_format(row['max_contributors'] or 0)
    min_loc = short_format(row['min_loc'] or 0)
    max_loc = short_format(row['max_loc'] or 0)

    formatted_function_count = short_format(row['function_count'] or 0)
    formatted_total_ccn = short_format(row['total_cyclomatic_complexity'] or 0)

    return {
        "total_repos": total_repos,
        "avg_commits": {
            "value": avg_commits,
            "min": min_commits,
            "max": max_commits,
        },
        "avg_contributors": {
            "value": avg_contributors,
            "min": min_contributors,
            "max": max_contributors,
        },
        "avg_loc": {
            "value": avg_loc,
            "min": min_loc,
            "max": max_loc,
        },
        "avg_ccn": {
            "value": avg_ccn,
            "function_count": formatted_function_count,
            "total_cyclomatic_complexity": formatted_total_ccn,
        },
        "avg_repo_size": {
            "value": avg_repo_size_str,
            "min": min_repo_size_str,
            "max": max_repo_size_str,
        },
        "dockerfiles": dockerfiles,
    }
