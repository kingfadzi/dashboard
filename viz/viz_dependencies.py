import plotly.express as px

import plotly.express as px

import plotly.express as px

def render_dependency_detection_chart(df):
    fig = px.bar(
        df,
        x="status",
        y="repo_count",
        color="status",
        labels={"status": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        showlegend=True,
        #margin=dict(l=40, r=10, t=10, b=20),  # left margin gives space for y-axis label
        xaxis=dict(showticklabels=False, title=""),
        yaxis=dict(title="Repository Count", automargin=True),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        ),
    )
    fig.update_yaxes(rangemode="nonnegative", fixedrange=True)
    return fig



def render_iac_detection_chart(df):
    fig = px.bar(
        df,
        x="status",
        y="repo_count",
        color="status",
        labels={"status": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        showlegend=True,
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
        labels={"status": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        showlegend=True,
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
        labels={"package_type": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        xaxis_title="Repository Count",
        legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center", font=dict(size=10))
    )
    return fig

def render_top_packages_chart(df):
    fig = px.bar(
        df,
        x="package_name",
        y="count",
        labels={"package_name": "Package", "count": "Occurrences"},
    )
    fig.update_layout(
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
        labels={"framework": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        xaxis_title="Repository Count",
        legend=dict(orientation="h", y=1.02, x=0.5, xanchor="center", font=dict(size=10))
    )
    return fig

def render_dependency_volume_chart(df):
    fig = px.bar(
        df,
        x="dep_bucket",
        y="repo_count",
        labels={"dep_bucket": "Dependency Count", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        xaxis_title="Dependency Count",
        legend=dict(
            orientation="h",
            y=1.02,
            x=0.5,
            xanchor="center",
            font=dict(size=10)
        )
    )
    return fig



def render_xeol_top_products_chart(df):
    fig = px.bar(
        df,
        y="product_name",
        x="repo_count",
        orientation="h",
        labels={"product_name": "", "repo_count": "Repository Count"},
    )
    fig.update_layout()
    return fig


def render_xeol_exposure_bucketed_chart(df):
    fig = px.bar(
        df,
        x="bucket",
        y="repo_count",
        color="artifact_type",
        barmode="stack",
        labels={
            "bucket": "EOL Artifact Count",
            "repo_count": "Repository Count",
            "artifact_type": "Artifact Type",
        },
    )
    fig.update_layout(
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
    fig.update_layout()
    return fig

def render_iac_adoption_by_framework_count_chart(df):
    fig = px.bar(
        df,
        x="framework_bucket",
        y="repo_count",
        labels={
            "framework_bucket": "Frameworks Used per Repo",
            "repo_count": "Repository Count",
        },
    )
    fig.update_layout(
        xaxis_title="Frameworks Used per Repository",
        showlegend=False
    )
    return fig


