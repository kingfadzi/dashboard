import plotly.express as px

# 1. Total Cyclomatic Complexity
def render_total_ccn_chart(df):
    fig = px.bar(
        df,
        x="ccn_bucket",
        y="repo_count",
        title="Total Cyclomatic Complexity (Architectural Risk)",
        labels={"ccn_bucket": "Complexity Bucket", "repo_count": "Repo Count"},
    )
    return fig

# 2. Function Count
def render_function_count_chart(df):
    fig = px.bar(
        df,
        x="function_bucket",
        y="repo_count",
        title="Function Count (Modularity vs Monoliths)",
        labels={"function_bucket": "Function Count Bucket", "repo_count": "Repo Count"},
    )
    return fig

# 3. Total NLOC
def render_total_nloc_chart(df):
    fig = px.bar(
        df,
        x="nloc_bucket",
        y="repo_count",
        title="Non-Commented Code Volume (NLOC)",
        labels={"nloc_bucket": "NLOC Bucket", "repo_count": "Repo Count"},
    )
    return fig

# 4. Scatter: Function Count vs Total Complexity
def render_ccn_vs_function_count_chart(df):
    fig = px.scatter(
        df,
        x="function_count",
        y="total_ccn",
        title="Function Count vs Total Complexity",
        labels={"function_count": "Function Count", "total_ccn": "Total CCN"},
        hover_name="repo_id",
    )
    fig.update_traces(marker=dict(size=7, opacity=0.7))
    return fig
