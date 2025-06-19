import pandas as pd
from data.cache_instance import cache
from data.buildtools.build_filter_conditions import build_filter_conditions
from data.shared_kpi_query import fetch_kpi_totals


def fetch_code_insights_kpis(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        return fetch_kpi_totals(condition_string, param_dict)

    condition_string, param_dict = build_filter_conditions(filters, alias="hr")
    df = query_data(condition_string, param_dict)

    return {
        "total_repos": int(df["total_repos"] or 0),
        "code_repos": int(df["code_repos"] or 0),
        "markup_data_repos": int(df["markup_data_repos"] or 0),
        "no_language_repos": int(df["no_language_repos"] or 0),
        "files": int(df["total_files"] or 0),
        "functions": int(df["total_functions"] or 0),
        "loc": int(df["total_loc"] or 0),
    }
