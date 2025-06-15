import plotly.express as px

from components.chart_style import stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE


def viz_trivy_vulnerabilities(filtered_df):

    return px.bar(
        filtered_df,
        x="severity",
        y="repo_count",
        labels={
            "severity": "Severity Level",
            "repo_count": "Repository Count",
        },
        color="severity",  # Color bars by severity
    ).update_layout(
        template="plotly_white",
        title={"x": 0.5},  # Center the title
        dragmode=False,
        showlegend=False
    )

@stacked_bar_chart_style(x_col="severity", y_col="repo_count")
def render_repo_count_by_trivy_severity_chart(df):
    df = df.copy()
    df["severity"] = df["severity"].fillna("Unknown")
    df = df.sort_values("repo_count", ascending=False)

    fig = px.bar(
        df,
        x="severity",
        y="repo_count",
        color="severity",
        labels={
            "severity": "",
            "repo_count": "Repository Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    return fig, df

@stacked_bar_chart_style(x_col="resource_type", y_col="repo_count")
def render_repo_count_by_trivy_resource_type_chart(df):
    df = df.copy()
    df["resource_type"] = df["resource_type"].fillna("Unknown")
    df["severity"] = df["severity"].fillna("Unknown")
    df = df.sort_values("repo_count", ascending=False)

    fig = px.bar(
        df,
        x="resource_type",
        y="repo_count",
        color="severity",
        labels={
            "resource_type": "",
            "severity": "Severity",
            "repo_count": "Repository Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_layout(xaxis=dict(type="category", tickangle=45))
    return fig, df

@stacked_bar_chart_style(x_col="severity", y_col="repo_count")
def render_repo_count_by_fix_status_chart(df):
    df = df.copy()
    df["severity"] = df["severity"].fillna("Unknown")
    df["fix_status"] = df["fix_status"].fillna("Unknown")
    df = df.sort_values("repo_count", ascending=False)

    fig = px.bar(
        df,
        x="severity",
        y="repo_count",
        color="fix_status",
        labels={
            "severity": "",
            "fix_status": "Fix Status",
            "repo_count": "Repository Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_layout(xaxis=dict(type="category", tickangle=45))
    return fig, df

@stacked_bar_chart_style(x_col="product", y_col="repo_count")
def render_top_trivy_repo_impact_chart(df):
    df = df.copy()
    df["product"] = df["product"].fillna("Unknown").str.slice(0, 40)
    df["severity"] = df["severity"].fillna("Unknown")

    df = df.sort_values(["repo_count", "product"], ascending=[False, True])

    fig = px.bar(
        df,
        x="product",
        y="repo_count",
        color="severity",
        labels={
            "product": "Product",
            "severity": "Severity",
            "repo_count": "Affected Repositories"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    fig.update_layout(
        xaxis=dict(type="category", tickangle=45)
    )

    return fig, df

