import plotly.express as px

def render_dependency_detection_chart(df):
    fig = px.bar(
        df,
        x="status",
        y="repo_count",
        color="status",
        title="Dependency Detection Coverage",
        labels={"status": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        showlegend=True,
        height=400,
        xaxis=dict(showticklabels=False, title=""),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )
    return fig

def render_iac_detection_chart(df):
    fig = px.bar(
        df,
        x="status",
        y="repo_count",
        color="status",
        title="IaC Component Detection Coverage",
        labels={"status": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        showlegend=True,
        height=400,
        xaxis=dict(showticklabels=False, title=""),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )
    return fig

def render_xeol_detection_chart(df):
    fig = px.bar(
        df,
        x="status",
        y="repo_count",
        color="status",
        title="EOL Artifact Detection Coverage",
        labels={"status": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        showlegend=True,
        height=400,
        xaxis=dict(showticklabels=False, title=""),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )
    return fig

import plotly.express as px

def render_package_type_distribution_chart(df):
    fig = px.bar(
        df,
        y="package_type",
        x="repo_count",
        orientation="h",
        title="Package Type Distribution",
        labels={"package_type": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        height=400,
        xaxis_title="",
        legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center", font=dict(size=10))
    )
    return fig

def render_top_packages_chart(df):
    fig = px.bar(
        df,
        x="package_name",
        y="count",
        title="Top Packages Across Repositories",
        labels={"package_name": "Package", "count": "Occurrences"},
    )
    fig.update_layout(
        height=400,
        xaxis_tickangle=45,
        xaxis_title="",
        legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center", font=dict(size=10))
    )
    return fig

def render_framework_distribution_chart(df):
    fig = px.bar(
        df,
        y="framework",
        x="repo_count",
        orientation="h",
        title="Framework Usage Distribution",
        labels={"framework": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        height=400,
        xaxis_title="",
        legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center", font=dict(size=10))
    )
    return fig

def render_dependency_volume_chart(df):
    fig = px.bar(
        df,
        x="dep_bucket",
        y="repo_count",
        title="Dependency Volume per Repository",
        labels={"dep_bucket": "Dependency Count", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        height=400,
        xaxis_title="",
        legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center", font=dict(size=10))
    )
    return fig



def render_xeol_top_products_chart(df):
    fig = px.bar(
        df,
        y="product_name",
        x="repo_count",
        orientation="h",
        title="Top Products with EOL Risk",
        labels={"product_name": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(height=400)
    return fig


def render_xeol_exposure_bucketed_chart(df):
    fig = px.bar(
        df,
        x="bucket",
        y="repo_count",
        color="artifact_type",
        barmode="stack",
        title="EOL Exposure per Repo (Bucketed by Artifact Type)",
        labels={
            "bucket": "EOL Artifact Count",
            "repo_count": "Repository Count",
            "artifact_type": "Artifact Type",
        },
    )
    fig.update_layout(
        height=450,
        xaxis_title="EOL Artifact Count per Repository",
        legend=dict(
            orientation="h",
            y=1.15,  # above chart
            x=0.5,
            xanchor="center",
            font=dict(size=10),
            bgcolor="rgba(255,255,255,0.8)"
        ),
        margin=dict(t=100)  # space for title + legend
    )
    return fig


def render_iac_framework_usage_chart(df):
    fig = px.bar(
        df,
        y="framework",
        x="repo_count",
        orientation="h",
        title="IaC Framework Usage",
        labels={"framework": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(height=400)
    return fig

def render_iac_adoption_by_framework_count_chart(df):
    fig = px.bar(
        df,
        x="framework_bucket",
        y="repo_count",
        title="IaC Adoption by Framework Count",
        labels={
            "framework_bucket": "Frameworks Used per Repo",
            "repo_count": "Repository Count",
        },
    )
    fig.update_layout(
        height=400,
        xaxis_title="Frameworks Used per Repository",
        showlegend=False
    )
    return fig


