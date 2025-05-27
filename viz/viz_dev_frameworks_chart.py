import plotly.express as px

def viz_dev_frameworks_chart(df):
    if df.empty:
        return px.bar(title="No Developer Framework Data Found")

    # Normalize empty strings or None to "Unclassified"
    df["framework"] = df["framework"].fillna("Unclassified").replace("", "Unclassified")

    return px.bar(
        df,
        x="framework",
        y="repo_count",
        labels={"framework": "Framework", "repo_count": "Repository Count"},
        color="framework"
    ).update_layout(
        xaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        title=None,
        xaxis_title=None,
        dragmode=False,
        showlegend=False
    )