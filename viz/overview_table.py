import pandas as pd

def viz_table_data(df):
    if df.empty:
        return []

    df = df.sort_values(by="total_commits", ascending=False)

    if "repo_id" in df.columns and "web_url" in df.columns:
        df["repo_id"] = df.apply(
            lambda row: f"[{row['repo_id']}]({row['web_url']})"
            if pd.notnull(row["web_url"]) and row["web_url"].strip() not in ["", "#"]
            else row["repo_id"],
            axis=1,
        )

    if "last_commit_date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["last_commit_date"]):
        df["last_commit_date"] = df["last_commit_date"].dt.strftime("%Y-%m-%d")

    for col in ["total_commits", "number_of_contributors"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")

    return df.to_dict("records")