import pandas as pd

def viz_table_data(df):
    if df.empty:
        return []

    # Sort repos by total commits descending
    df = df.sort_values(by="total_commits", ascending=False)

    # Format repo_id as link if web_url is valid
    if "repo_id" in df.columns and "web_url" in df.columns:
        df["repo_id"] = df.apply(
            lambda row: (
                f'<a href="{row["web_url"]}" target="_blank" style="text-decoration:none; color:#007bff;">{row["repo_id"]}</a>'
                if pd.notnull(row["web_url"]) and row["web_url"].strip() not in ["", "#"]
                else row["repo_id"]
            ),
            axis=1,
        )

    # Format last_commit_date
    if "last_commit_date" in df.columns and pd.api.types.is_datetime64_any_dtype(df["last_commit_date"]):
        df["last_commit_date"] = df["last_commit_date"].dt.strftime("%Y-%m-%d")

    # Format numbers with thousands separator
    numeric_columns = ["total_commits", "number_of_contributors"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")

    return df.to_dict("records")
