import plotly.express as px

def viz_dependency_types_chart(df):
    if df.empty:
        return px.bar(title="No Dependency Type Data Found")

    df["sub_category"] = df["sub_category"].fillna("Unclassified").replace("", "Unclassified")

    return px.bar(
        df,
        x="sub_category",
        y="repo_count",
        labels={"sub_category": "Dependency Type", "repo_count": "Repository Count"},
        color="sub_category"
    ).update_layout(
        xaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        title={"text": "Top Dependency Types", "x": 0.5},
        xaxis_title=None,
        dragmode=False,
        showlegend=False
    )