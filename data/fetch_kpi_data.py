import pandas as pd
from sqlalchemy import text
from data.cache_instance import cache
from data.db_connection import engine
from data.build_filter_conditions import build_filter_conditions


def short_format(num):
    if not num:
        return "0"
    val = float(num)
    if val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.1f}B"
    elif val >= 1_000_000:
        return f"{val / 1_000_000:.1f}M"
    elif val >= 1_000:
        return f"{val / 1_000:.1f}K"
    else:
        return f"{val:.0f}"


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


@cache.memoize()
def fetch_kpi_data(filters=None):
    condition_string, param_dict = build_filter_conditions(filters)

    sql = """
    SELECT
        hr.repo_id,
        rm.total_commits,
        rm.number_of_contributors,
        rm.active_branch_count,
        rm.last_commit_date,
        rm.repo_size_bytes,
        ls.total_nloc,
        ls.avg_ccn,
        ls.function_count,
        ls.total_ccn
    FROM harvested_repositories hr
    LEFT JOIN repo_metrics rm ON hr.repo_id = rm.repo_id
    LEFT JOIN lizard_summary ls ON hr.repo_id = ls.repo_id
    """
    if condition_string:
        sql += f" WHERE {condition_string}"

    df = pd.read_sql(text(sql), engine, params=param_dict)
    if df.empty:
        return {}

    now = pd.Timestamp.now()
    df["repo_age_days"] = (now - pd.to_datetime(df["last_commit_date"], errors="coerce")).dt.days
    df["lines_per_function"] = df["total_nloc"] / df["function_count"]
    df = df.replace([float("inf"), -float("inf")], pd.NA)

    result = {}

    def summarize_metric(df, column, formatter=short_format, size=False):
        series = df[column].dropna()
        if series.empty:
            return {
                "median": "0",
                "iqr": "0",
                "stddev": "0",
                "outlier_count": 0
            }

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        filtered = series[(series >= lower) & (series <= upper)]
        outlier_count = series.size - filtered.size

        if filtered.empty:
            filtered = series
            outlier_count = 0  # fallback disables outlier count

        print(f"{column}: using {len(filtered)} of {len(series)} rows (excluded {outlier_count})")

        median = filtered.median()
        stddev = filtered.std()

        return {
            "median": human_readable_size(median) if size else formatter(median),
            "iqr": human_readable_size(iqr) if size else formatter(iqr),
            "stddev": human_readable_size(stddev) if size else formatter(stddev),
            "outlier_count": int(outlier_count)
        }

    result["commits"] = summarize_metric(df, "total_commits")
    result["contributors"] = summarize_metric(df, "number_of_contributors")
    result["branches"] = summarize_metric(df, "active_branch_count")
    result["repo_age_days"] = summarize_metric(df, "repo_age_days")
    result["loc"] = summarize_metric(df, "total_nloc")
    result["repo_size"] = summarize_metric(df, "repo_size_bytes", size=True)
    result["lines_per_function"] = summarize_metric(df, "lines_per_function")

    df_ccn = df[["avg_ccn", "function_count", "total_ccn"]].dropna()
    result["avg_ccn"] = {
        "median": f"{df_ccn['avg_ccn'].median():.1f}" if not df_ccn.empty else "0.0",
        "function_count": short_format(df_ccn["function_count"].sum()),
        "total_cyclomatic_complexity": short_format(df_ccn["total_ccn"].sum())
    }
    result["total_repos"] = f"{df['repo_id'].dropna().nunique():,}"
    return result
