import pandas as pd
from data.db_connection import engine

def fetch_filter_options(column_name):
    query = f"""
        SELECT DISTINCT {column_name}
        FROM harvested_repositories
        WHERE {column_name} IS NOT NULL
        ORDER BY {column_name} ASC
    """
    df = pd.read_sql(query, engine)
    return [{"label": row[column_name], "value": row[column_name]} for _, row in df.iterrows()]
