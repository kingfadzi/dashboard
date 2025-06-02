import plotly.express as px

def render_outdated_library_chart(df):
    fig = px.bar(
        df,
        x="package_name",
        y="version_count",
        labels={"package_name": "Package", "version_count": "Distinct Versions"},
    )
    fig.update_layout(margin=dict(t=10), xaxis_tickangle=-45)
    return fig

def render_legacy_version_chart(df):
    fig = px.bar(
        df,
        x="major_minor",
        y="repo_count",
        labels={"major_minor": "Version Group", "repo_count": "Repository Count"},
    )
    fig.update_layout(margin=dict(t=10), xaxis_tickangle=-30)
    return fig

def render_junit_version_chart(df):
    fig = px.bar(
        df,
        x="version",
        y="repo_count",
        labels={"version": "JUnit Version", "repo_count": "Repository Count"},
    )
    fig.update_layout(margin=dict(t=10), xaxis_tickangle=-30)
    return fig

def render_dependency_count_chart(df):
    fig = px.histogram(
        df,
        x="dep_count",
        nbins=30,
        labels={"dep_count": "Dependency Count"},
    )
    fig.update_layout(margin=dict(t=10))
    return fig

def render_frameworks_per_repo_chart(df):
    fig = px.histogram(
        df,
        x="framework_count",
        nbins=10,
        labels={"framework_count": "Frameworks per Repo"},
    )
    fig.update_layout(margin=dict(t=10))
    return fig