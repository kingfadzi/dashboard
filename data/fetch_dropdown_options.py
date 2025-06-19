import pandas as pd
from data.db_connection import engine


def fetch_dropdown_options():
    query = """
    SELECT DISTINCT 
        host_name, 
        activity_status, 
        transaction_cycle, 
        main_language, 
        classification_label
    FROM harvested_repositories
    """
    df = pd.read_sql(query, engine)
    return {
        "host_names": sorted(df["host_name"].dropna().unique().tolist()),
        "activity_statuses": sorted(df["activity_status"].dropna().unique().tolist()),
        "tcs": sorted(df["transaction_cycle"].dropna().unique().tolist()),
        "languages": sorted(df["main_language"].dropna().unique().tolist()),
        "classification_labels": sorted(df["classification_label"].dropna().unique().tolist()),
    }