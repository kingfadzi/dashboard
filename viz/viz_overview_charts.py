import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.chart_style import stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
from utils.formattting import human_readable_size

@stacked_bar_chart_style(x_col="activity_status", y_col="repo_count")
def render_repo_status_chart(filtered_df: pd.DataFrame):
    aggregated_df = filtered_df.groupby(
        ["activity_status", "host_name"], as_index=False
    )["repo_count"].sum()

    aggregated_df["activity_status"] = aggregated_df["activity_status"].str.capitalize()

    fig = px.bar(
        aggregated_df,
        x="activity_status",
        y="repo_count",
        color="host_name",
        barmode="stack",
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        labels={
            "activity_status": "Activity Status",
            "repo_count": "Repository Count",
            "host_name": "Host"
        }
    )

    return fig, aggregated_df


@stacked_bar_chart_style(x_col="classification_label", y_col="repo_count")
def render_repo_size_chart(filtered_df: pd.DataFrame):
    # Set fixed size ordering
    filtered_df["classification_label"] = pd.Categorical(
        filtered_df["classification_label"],
        categories=["Tiny", "Small", "Medium", "Large", "Massive"],
        ordered=True
    )
    filtered_df = filtered_df.sort_values("classification_label")

    fig = px.bar(
        filtered_df,
        x="classification_label",
        y="repo_count",
        color="language_group",
        text="repo_count",
        labels={
            "classification_label": "Repo Size",
            "repo_count": "Repository Count",
            "language_group": "Language Group"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, filtered_df


def render_vulnerabilities_chart(filtered_df):

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

def render_standards_issues_chart(filtered_df):

    return px.bar(
        filtered_df,
        x="category",
        y="repo_count",
        labels={
            "category": "Issue Category",
            "repo_count": "Repository Count",
        },
        color="category",
    ).update_layout(
        template="plotly_white",
        title={"x": 0.5},
        dragmode=False,
        showlegend=False
    )

def render_appserver_chart(filtered_df):
    if filtered_df.empty:
        return px.bar(
            title="No App Server Data Found"
        )

    return px.bar(
        filtered_df,
        x="iac_type",
        y="repo_count",
        labels={"iac_type": "App Server", "repo_count": "Repository Count"},
        color="iac_type"
    ).update_layout(
        xaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        title={"text": "Top Application Servers", "x": 0.5},
        xaxis_title=None,
        dragmode=False,
        showlegend=False
    )

def render_package_type_chart(df):
    if df.empty:
        return px.bar(title=None)

    df["package_type"] = df["package_type"].fillna("Unknown").replace("", "Unknown")

    return px.bar(
        df,
        x="package_type",
        y="repo_count",
        color="package_type",
        labels={
            "package_type": "Package Type",
            "repo_count": "Repository Count"
        },
    ).update_layout(
        xaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        title=None,
        xaxis_title=None,
        dragmode=False,
        showlegend=False
    )

def render_language_contributors_heatmap(filtered_df: pd.DataFrame):
    # Define SQL-style bucket order
    bucket_order = [
        "0-1",
        "2-5",
        "6-10",
        "11-20",
        "21-50",
        "51-100",
        "101-500"
    ]

    # Apply categorical sort
    filtered_df["contributor_bucket"] = pd.Categorical(
        filtered_df["contributor_bucket"], categories=bucket_order, ordered=True
    )
    filtered_df = filtered_df.sort_values("contributor_bucket")

    # Pivot to form heatmap
    heatmap_data = filtered_df.pivot(
        index="contributor_bucket",
        columns="language",
        values="repo_count"
    ).fillna(0)

    z_data = heatmap_data.values
    x_labels = heatmap_data.columns.tolist()
    y_labels = heatmap_data.index.tolist()
    text_data = [[f"{int(val)}" for val in row] for row in z_data]

    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=x_labels,
        y=y_labels,
        text=text_data,
        texttemplate="%{text}",
        colorscale=NEUTRAL_COLOR_SEQUENCE,
        showscale=False
    ))

    fig.update_layout(
        title={"x": 0.5},
        template="plotly_white",
        dragmode=False,
        xaxis_title="Language",
        yaxis_title="Number of Contributors"
    )

    return fig




def render_iac_chart(filtered_df):
    if filtered_df.empty:
        return {"data": []}

    fig = px.bar(
        filtered_df,
        x="iac_type",
        y="repo_count",
        labels={"iac_type": "IaC Framework", "repo_count": "Repositories"},
        color="iac_type"
    )

    fig.update_layout(
        xaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        title_text="Top 20 IaC Frameworks",
        title_x=0.5,
        xaxis_title=None,
        yaxis_title="Repositories",
        dragmode=False,
        showlegend=False,
        height=450,
        margin=dict(t=60, b=100)
    )
    fig.update_layout(
        xaxis_title=None,
        title=None
    )
    return fig

def render_dev_frameworks_chart(df):
    if df.empty:
        return px.bar(title="No Developer Framework Data Found")

    # Normalize empty strings or None to "Unclassified"
    df["framework"] = df["framework"].fillna("Unclassified").replace("", "Unclassified")

    return px.bar(
        df,
        x="framework",
        y="repo_count",
        labels={"framework": "Framework", "repo_count": "Repository Count"},
        color="framework"
    ).update_layout(
        xaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        title=None,
        xaxis_title=None,
        dragmode=False,
        showlegend=False
    )

def render_multilang_chart(df):

    fig = px.bar(
        df,
        x="language_bucket",
        y="repo_count",
        color="language_bucket",
        labels={
            "language_bucket": "Number of Languages per Repo",
            "repo_count": "Repository Count"
        },

    )
    fig.update_layout(
        showlegend=False,
        template="plotly_white",
        xaxis=dict(categoryorder="total descending"),
        title_x=0.5,
        dragmode=False
    )
    return fig


@stacked_bar_chart_style(x_col="main_language", y_col="count")
def render_cloc_chart(filtered_df: pd.DataFrame):
    melted_df = filtered_df.melt(
        id_vars="main_language",
        value_vars=[
            "blank_lines",
            "comment_lines",
            "total_lines_of_code",
            "source_code_file_count"
        ],
        var_name="metric",
        value_name="count"
    )

    fig = px.bar(
        melted_df,
        x="main_language",
        y="count",
        color="metric",
        labels={
            "main_language": "Language",
            "count": "Lines of Code",
            "metric": "Metric Type"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis=dict(categoryorder="total descending", title=None),
        legend_title=None,
        dragmode=False,
        yaxis=dict(tickformat=",")
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{y:,} lines<extra></extra>"
    )

    return fig, melted_df


def render_contribution_scatter(filtered_df: pd.DataFrame):
    filtered_df["repo_size"] = filtered_df["repo_size"].fillna(0)
    filtered_df["repo_size_human"] = filtered_df["repo_size"].apply(human_readable_size)

    # Truncate long hover fields
    def truncate(text, max_len=60):
        return text if pd.isna(text) or len(str(text)) <= max_len else str(text)[:max_len] + "..."

    filtered_df["web_url"] = filtered_df["web_url"].apply(lambda x: truncate(x, 60))
    filtered_df["all_languages"] = filtered_df["all_languages"].apply(lambda x: truncate(x, 60))

    # Setup size scale ticks
    min_size = filtered_df["repo_size"].min()
    max_size = filtered_df["repo_size"].max()
    tickvals = [min_size, max_size / 4, max_size / 2, 3 * max_size / 4, max_size]
    ticktext = [human_readable_size(val) for val in tickvals]

    fig = px.scatter(
        filtered_df,
        x="contributors",
        y="commits",
        size="repo_size",
        size_max=60,
        color="repo_size",
        color_continuous_scale=NEUTRAL_COLOR_SEQUENCE,
        labels={
            "main_language": "Main Language",
            "repo_size_human": "Size",
            "repo_age_human": "Age",
            "contributors": "Number of Contributors",
            "commits": "Total Commits",
            "web_url": "URL",
            "all_languages": "Languages Used",
            "total_lines_of_code": "LOC",
            "file_count": "File Count",
        },
        hover_data={
            "main_language": True,
            "repo_size_human": True,
            "repo_size": False,
            "web_url": True,
            "repo_age_human": True,
            "app_id": True,
            "tc": True,
            "component_id": True,
            "all_languages": True,
            "file_count": True,
            "total_lines_of_code": True
        },
    )

    fig.update_layout(
        template="plotly_white",
        dragmode="zoom",
        autosize=True,
        margin=dict(l=50, r=150, t=50, b=50),
        coloraxis_colorbar=dict(
            title=dict(
                text="Repository Size",
                side="top",
                font=dict(size=14),
            ),
            tickvals=tickvals,
            ticktext=ticktext,
        ),
        legend=dict(
            font=dict(size=12),
            itemsizing="trace",
        ),
    )

    return fig

def render_primary_language_chart(filtered_df):

    return px.bar(
        filtered_df,
        x="main_language",
        y="repo_count",
        labels={
            "main_language": "Language",
            "repo_count": "Repository Count"
        },
    ).update_layout(
        dragmode=False,
        xaxis_title="",
        yaxis_title="Repository Count",
    )

def render_commit_buckets_chart(df):
    if "commit_bucket" not in df.columns or "repo_count" not in df.columns:
        raise KeyError("Required columns 'commit_bucket' and 'repo_count' are missing in the DataFrame.")

    fig = px.bar(
        df,
        x="commit_bucket",
        y="repo_count",
        color="commit_bucket",
        labels={
            "commit_bucket": "Commit Recency",
            "repo_count": "Repository Count",
        },
    )
    fig.update_layout(
        showlegend=False,
        template="plotly_white",
        title_x=0.5,
        xaxis=dict(
            categoryorder="array",
            categoryarray=[
                "< 1 month", "1-3 months", "3-6 months", "6-9 months",
                "9-12 months", "12-18 months", "18-24 months", "24+ months"
            ],
        ),
        yaxis=dict(title="Repository Count"),
        dragmode=False,
    )
    return fig