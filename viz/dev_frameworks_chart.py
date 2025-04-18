import plotly.express as px

def dev_frameworks_chart(df):
    if df.empty:
        return px.bar(title="No Developer Framework Data Found")

    return px.bar(
        df,
        x="framework",
        y="repo_count",
        labels={"framework": "Framework", "repo_count": "Repository Count"},
        color="framework"
    ).update_layout(
        xaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        title={"text": "Top Developer Frameworks", "x": 0.5},
        xaxis_title=None,
        dragmode=False,
        showlegend=False
    )