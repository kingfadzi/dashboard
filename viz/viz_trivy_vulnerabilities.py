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

@stacked_bar_chart_style(x_col="resource_type", y_col="repo_count")
def render_trivy_repos_by_resource_type_chart(df):
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
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    fig.update_layout(
        xaxis=dict(type="category", tickangle=45)
    )

    return fig, df



@stacked_bar_chart_style(x_col="pkg_name", y_col="vuln_count")
def render_top_trivy_packages_by_severity_chart(df):
    df = df.copy()
    df["severity"] = df["severity"].fillna("Unknown")

    # Save full name for hover, truncate for axis
    df["pkg_name_full"] = df["pkg_name"].fillna("Unknown")
    df["pkg_name"] = df["pkg_name_full"].str.slice(0, 20) + "…"
    df = df.sort_values("vuln_count", ascending=False)

    fig = px.bar(
        df,
        x="pkg_name",
        y="vuln_count",
        color="severity",
        labels={
            "pkg_name": "",
            "severity": "Severity",
            "vuln_count": "Vulnerability Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack",
        hover_name="pkg_name_full"  # show full package name on hover
    )

    fig.update_layout(
        xaxis=dict(type="category", tickangle=45)
    )

    return fig, df






@stacked_bar_chart_style(x_col="severity", y_col="vuln_count")
def render_trivy_fix_status_by_severity_chart(df):
    df = df.copy()
    df["severity"] = df["severity"].fillna("Unknown")
    df["fix_status"] = df["fix_status"].fillna("Unknown")
    df = df.sort_values("vuln_count", ascending=False)

    fig = px.bar(
        df,
        x="severity",
        y="vuln_count",
        color="fix_status",
        labels={
            "severity": "",
            "fix_status": "Fix Availability",
            "vuln_count": "Vulnerability Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    fig.update_layout(
        xaxis=dict(type="category", tickangle=45)
    )

    return fig, df

