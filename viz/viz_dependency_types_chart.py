import plotly.express as px

def viz_package_type_distribution_chart(df):
    if df.empty:
        return px.pie(names=[], values=[], title="No Package Type Data Found")

    df["package_type"] = df["package_type"].fillna("Unknown").replace("", "Unknown")

    return px.pie(
        df,
        names="package_type",
        values="package_count",
        title="Package Type Distribution (Syft Dependencies)",
        hole=0.3  # donut chart style
    ).update_traces(
        textposition="inside",
        textinfo="percent+label"
    ).update_layout(
        template="plotly_white",
        title={"x": 0.5},
        showlegend=True,
        dragmode=False
    )