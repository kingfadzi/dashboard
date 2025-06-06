import plotly.express as px

import plotly.graph_objects as go
import numpy as np
from components.chart_style import standard_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE

@standard_chart_style
def render_middleware_subcategory_chart(df):
    fig = px.bar(
        df,
        x="framework",
        y="repo_count",
        color="main_language",
        text="repo_count",
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        labels={
            "framework": "Framework",
            "repo_count": "Repository Count",
            "main_language": "Language"
        },
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textfont_size=12
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title=None,
        yaxis_title="Repository Count",
        xaxis_tickangle=-45
    )

    return fig


def render_no_deps_heatmap(df):
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No-dependency Repositories",
            xaxis_title="Language Group",
            yaxis_title="Contributors Bucket",
            margin=dict(l=60, r=20, t=60, b=60),
        )
        return fig

    full_y_order = ['0', '1-5', '6-10', '11-20', '21+']
    full_x_order = [
        "java",
        "python",
        "javascript",
        "go",
        "dotnet",
        "other_programming",
        "markup_or_data",
        "no_language"
    ]

    heatmap_df = df.pivot_table(
        index="contributors_bucket",
        columns="language_group",
        values="repos_without_dependencies",
        aggfunc="sum",
        fill_value=0
    )

    heatmap_df = heatmap_df.reindex(index=full_y_order, columns=full_x_order, fill_value=0)

    z = heatmap_df.values
    x = heatmap_df.columns.tolist()
    y = heatmap_df.index.tolist()
    text = np.vectorize(lambda v: str(int(v)))(z)

    fig = go.Figure(go.Heatmap(
        z=z,
        x=x,
        y=y,
        text=text,
        texttemplate="%{text}",
        textfont={"size": 12},
        colorscale=NEUTRAL_COLOR_SEQUENCE,
        showscale=False
    ))

    fig.update_layout(
        title="",
        xaxis_title="",
        yaxis_title="Number of Contributors",
        margin=dict(l=20, r=20, t=40, b=40)
    )

    return fig

def render_with_deps_by_variant(df):
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="Repositories With Dependencies",
            xaxis_title="Build Tool Variant",
            yaxis_title="Contributors Bucket",
            margin=dict(l=60, r=20, t=60, b=60),
        )
        return fig

    full_y_order = ['0', '1-5', '6-10', '11-20', '21+']
    full_x_order = sorted(df['build_tool_variant'].dropna().unique())

    heatmap_df = df.pivot_table(
        index="contributors_bucket",
        columns="build_tool_variant",
        values="repo_count",
        aggfunc="sum",
        fill_value=0
    )

    heatmap_df = heatmap_df.reindex(index=full_y_order, columns=full_x_order, fill_value=0)

    z = heatmap_df.values
    x = heatmap_df.columns.tolist()
    y = heatmap_df.index.tolist()
    text = np.vectorize(lambda v: str(int(v)))(z)

    fig = go.Figure(go.Heatmap(
        z=z,
        x=x,
        y=y,
        text=text,
        texttemplate="%{text}",
        textfont={"size": 12},
        colorscale=NEUTRAL_COLOR_SEQUENCE,
        showscale=False
    ))

    fig.update_layout(
        title="",
        xaxis_title="",
        yaxis_title="Number of Contributors",
        margin=dict(l=20, r=20, t=40, b=40)
    )

    return fig

@standard_chart_style
def render_avg_deps_per_package_type_chart(df):
    df["package_type"] = df["package_type"].fillna("Unknown").replace("", "Unknown")

    fig = px.bar(
        df,
        x="package_type",
        y="avg_dependencies_per_repo",
        color="package_type",
        text="avg_dependencies_per_repo",
        labels={
            "package_type": "Package Type",
            "avg_dependencies_per_repo": "Avg Dependencies / Repo"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside"
    )

    fig.update_layout(
        showlegend=False,
        xaxis=dict(
            showticklabels=True,
            title="",
            categoryorder="total descending"
        ),
        yaxis=dict(title="Avg Dependencies / Repo")
    )

    return fig


def render_no_dependency_repo_scatter(df):
    if df.empty:
        return px.scatter(
            title="No data available",
            labels={
                "contributor_count": "Contributors",
                "total_commits": "Total Commits",
                "repo_size_mb": "Repo Size (MB)",
                "language_group": "Language Group",
                "build_tools": "Build Tools"
            }
        )

    fig = px.scatter(
        df,
        x="contributor_count",
        y="total_commits",
        size="repo_size_mb",
        color="language_group",
        hover_name="repo_id",
        hover_data=["repo_size_mb", "build_tools"],
        labels={
            "contributor_count": "Contributors",
            "total_commits": "Total Commits",
            "repo_size_mb": "Repo Size (MB)",
            "language_group": "Language Group",
            "build_tools": "Build Tools"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
    )

    fig.update_traces(
        marker=dict(
            sizemode="area",
            sizeref=2. * df["repo_size_mb"].max() / (50.0**2),
            sizemin=6,
            line=dict(width=0.5, color="DarkSlateGrey")
        )
    )

    fig.update_layout(
        xaxis_title="Contributors",
        yaxis_title="Total Commits",
        showlegend=True,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig
