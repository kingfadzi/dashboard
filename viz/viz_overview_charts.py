import plotly.express as px

from utils.formattting import human_readable_size

def render_repo_status_chart(filtered_df):

    aggregated_df = filtered_df.groupby(
        ["activity_status", "host_name"], as_index=False
    )["repo_count"].sum()
    aggregated_df["activity_status"] = aggregated_df["activity_status"].str.capitalize()

    color_map = {"Active": "green", "Inactive": "red"}

    fig = px.bar(
        aggregated_df,
        x="activity_status",
        y="repo_count",
        color="host_name",
        barmode="stack",
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )

    for trace in fig.data:
        if trace.name in color_map:
            trace.marker.color = color_map[trace.name]

    fig.update_layout(
        dragmode=False,
        xaxis_title="",
        yaxis_title="Repository Count",
        legend_title="Host Name",
    )

    return fig

def render_repo_size_chart(filtered_df):

    fig = px.bar(
        filtered_df,
        x="classification_label",
        y="repo_count",
        text="repo_count"
    )

    fig.update_traces(
        textposition="outside",
        textfont_size=10
    )

    fig.update_layout(
        showlegend=False,
        title={"x": 0.5},
        xaxis_title="",
        yaxis_title="Repository Count",
        dragmode=False
    )

    return fig

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

def render_language_contributors_heatmap(filtered_df):
    heatmap_data = filtered_df.pivot(
        index="contributor_bucket",
        columns="language",
        values="repo_count"
    ).fillna(0)

    return px.imshow(
        heatmap_data,
        text_auto=True,
        labels={
            "x": "Language",
            "y": "Number of contributors",
            "color": "Repository Count",
        },
        color_continuous_scale="Viridis",
    ).update_layout(
        title={"x": 0.5},
        template="plotly_white",
        dragmode=False,
        xaxis_title=None,
    )


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


def render_cloc_chart(filtered_df):

    melted_df = filtered_df.melt(
        id_vars="main_language",
        value_vars=["blank_lines", "comment_lines", "total_lines_of_code", "source_code_file_count"],
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
            "count": "Lines of code",
            "metric": "Metric Type",
        },
        barmode="stack",
    ).update_layout(
        template="plotly_white",
        xaxis=dict(categoryorder="total descending", title=None),
        legend_title=None,  # Remove the legend title
        dragmode=False,
        yaxis=dict(tickformat=",")
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{y:,} lines<extra></extra>"
    )

    return fig

def render_contribution_scatter(filtered_df):
    filtered_df["repo_size"] = filtered_df["repo_size"].fillna(0)
    filtered_df["repo_size_human"] = filtered_df["repo_size"].apply(human_readable_size)

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