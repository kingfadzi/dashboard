# callbacks/viz_table_data.py

import pandas as pd

def viz_table_data(df):
    if df.empty:
        return []

    df = df.sort_values(by="commits", ascending=False)

    # Format Repo Name as a clickable link that opens in a new tab
    if "repo_id" in df.columns and "web_url" in df.columns:
        df["repo_id"] = df.apply(
            lambda row: f"[{row['repo_id']}]({row['web_url']} \"target=_blank\")"
            if pd.notnull(row["web_url"]) and row["web_url"].strip() not in ["", "#"]
            else row["repo_id"],
            axis=1,
        )

    # Format Last Commit Date as 'YYYY-MM-DD'
    if "last_commit" in df.columns and pd.api.types.is_datetime64_any_dtype(df["last_commit"]):
        df["last_commit"] = df["last_commit"].dt.strftime("%Y-%m-%d")

    # Format Numeric Columns with Comma Separators
    numeric_columns = ["commits", "contributors"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")

    return df.to_dict("records")