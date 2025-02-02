# callbacks/viz_table_data.py

import pandas as pd

def viz_table_data(df):
    if df.empty:
        return []

    df = df.sort_values(by="commits", ascending=False)

    if "last_commit" in df.columns and pd.api.types.is_datetime64_any_dtype(df["last_commit"]):
        df["last_commit"] = df["last_commit"].dt.strftime("%Y-%m-%d")

    numeric_columns = ["commits", "contributors"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:,}" if pd.notnull(x) else "")

    return df.to_dict("records")