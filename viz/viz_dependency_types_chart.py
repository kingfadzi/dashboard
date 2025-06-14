import plotly.express as px

def viz_package_type_distribution_chart(df):
    if df.empty:
        return px.bar(title=None)

    df["package_type"] = df["package_type"].fillna("Unknown").replace("", "Unknown")

    return px.bar(
        df,
        x="package_type",
        y="package_count",
        color="package_type",
        labels={"package_type": "Package Type", "package_count": "Package Count"},
    ).update_layout(
        xaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        title=None,
        xaxis_title=None,
        dragmode=False,
        showlegend=False
    )
