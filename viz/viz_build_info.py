import plotly.express as px
import plotly.graph_objects as go

# 1. Detection Coverage by Tool
def render_detection_coverage_chart(df):
    fig = go.Figure()

    statuses = df["detection_status"].unique()
    tools = sorted(df["tool"].unique())

    for status in statuses:
        filtered = df[df["detection_status"] == status]
        visible = "legendonly" if status == "No Modules Detected" else True
        fig.add_trace(go.Bar(
            x=filtered["tool"],
            y=filtered["repo_count"],
            name=status,
            visible=visible,
        ))

    fig.update_layout(
        barmode="stack",
        xaxis_title=None,
        yaxis_title="Repository Count",
        title=None
    )
    return fig

# 2. Module Count Buckets
def render_module_count_chart(df):
    fig = px.bar(
        df,
        x="module_bucket",
        y="repo_count",
        labels={"module_bucket": "Module Count Range", "repo_count": "Repository Count"},
    )
    fig.update_layout(title=None)
    return fig

# 3. Repos per Tool and Variant
def render_repos_per_tool_variant_chart(df):
    fig = px.bar(
        df,
        x="variant",
        y="repo_count",
        color="tool",
        barmode="group",
        labels={"variant": "Build Tool Variant", "tool": "Language Tool", "repo_count": "Repository Count"},
    )
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title=None)
    return fig

# 4. Status by Tool
def render_status_by_tool_chart(df):
    fig = px.bar(
        df,
        x="tool",
        y="repo_count",
        color="status",
        barmode="stack",
        labels={"tool": "Language (tool)", "status": "Status", "repo_count": "Repository Count"},
    )
    fig.update_layout(title=None)
    return fig

# 5. Runtime Versions by Tool
def render_runtime_versions_chart(df):
    df = df.sort_values("repo_count", ascending=False)
    fig = px.bar(
        df,
        x="runtime_version",
        y="repo_count",
        color="variant",
        barmode="stack",
        labels={"runtime_version": "Runtime Version", "variant": "Build Tool Variant", "repo_count": "Repository Count"},
    )
    fig.update_xaxes(tickangle=45)
    fig.update_layout(title=None)
    return fig

# 6. Runtime Fragmentation by Tool
def render_runtime_fragmentation_chart(df):
    fig = px.bar(
        df,
        x="tool",
        y="version_count",
        labels={"tool": "Language (tool)", "version_count": "Distinct Runtime Versions"},
    )
    fig.update_layout(title=None)
    return fig

# 7. Confidence Distribution
def render_confidence_distribution_chart(df):
    fig = px.bar(
        df,
        x="confidence",
        y="repo_count",
        labels={"confidence": "Confidence Level", "repo_count": "Repository Count"},
    )
    fig.update_xaxes(categoryorder="array", categoryarray=["high", "medium", "low", "unknown"])
    fig.update_layout(title=None)
    return fig
