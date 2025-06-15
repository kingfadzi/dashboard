import pandas as pd
from sqlalchemy import text
from data.db_connection import engine
from data.buildtools.build_filter_conditions import build_filter_conditions
from data.cache_instance import cache


def clean_classification_label(label):
    if isinstance(label, str):
        if "->" in label:
            return label.split("->", 1)[1].strip()
        return label.strip()
    return label


def fetch_classification_data(filters=None):
    @cache.memoize()
    def query_data(condition_string, param_dict):
        sql = """
        SELECT classification_label, COUNT(*) AS repo_count
        FROM harvested_repositories
        """
        if condition_string:
            sql += f" WHERE {condition_string}"
        sql += " GROUP BY classification_label"

        stmt = text(sql)
        df = pd.read_sql(stmt, engine, params=param_dict)

        df['classification_value'] = df['classification_label'].apply(clean_classification_label)

        df = df.groupby('classification_value', as_index=False)['repo_count'].sum()

        # Rename back to classification_label for consistency
        df.rename(columns={'classification_value': 'classification_label'}, inplace=True)

        return df

    condition_string, param_dict = build_filter_conditions(filters)
    return query_data(condition_string, param_dict)
