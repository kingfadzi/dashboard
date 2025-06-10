from components.chart_style import standard_chart_style
from components.chart_style import stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.graph_objects import Figure, Bar

@standard_chart_style
def render_dependency_detection_chart(df):
    return px.bar(
        df,
        x="status",
        y="repo_count",
        color="status",
        text="repo_count",
        labels={"status": "", "repo_count": "Repository Count"},
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

@stacked_bar_chart_style(x_col="language_group", y_col="repo_count")
def render_iac_detection_chart(df):
    fig = px.bar(
        df,
        x="language_group",
        y="repo_count",
        color="status",
        labels={
            "language_group": "Language Group",
            "repo_count": "Repository Count",
            "status": "IaC Detection"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )
    return fig, df



@stacked_bar_chart_style(x_col="language_group", y_col="repo_count")
def render_xeol_detection_chart(df):
    fig = px.bar(
        df,
        x="language_group",
        y="repo_count",
        color="size",
        labels={
            "language_group": "",
            "size": "Repo Size",
            "repo_count": "Repository Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )
    return fig, df

@standard_chart_style
def render_package_type_distribution_chart(df):
    fig = px.bar(
        df,
        x="package_type",
        y="repo_count",
        color="package_type",
        orientation="v",
        text="repo_count",
        labels={"package_type": "Package Type", "repo_count": "Repository Count"},
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_layout(
        showlegend=False,
        xaxis=dict(
            showticklabels=True,
            title="",
            categoryorder="total descending"
        ),
        yaxis=dict(title="Repository Count")
    )

    return fig




@stacked_bar_chart_style(x_col="sub_category", y_col="repo_count")
def render_subcategory_distribution_chart(df):
    fig = px.bar(
        df,
        x="sub_category",
        y="repo_count",
        color="package_type",
        labels={
            "sub_category": "",
            "repo_count": "Repository Count",
            "package_type": "Package Type"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )
    return fig, df


@stacked_bar_chart_style(x_col="dep_bucket", y_col="repo_count")
def render_dependency_volume_chart(df):
    fig = px.bar(
        df,
        x="dep_bucket",
        y="repo_count",
        color="package_type",  # now stripe by package_type
        labels={
            "dep_bucket": "Dependency Count",
            "repo_count": "Repository Count",
            "package_type": "Package Type"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )
    return fig, df



@stacked_bar_chart_style(x_col="eol_state", y_col="repo_count")
def render_xeol_top_products_chart(df):
    fig = px.bar(
        df,
        x="eol_state",
        y="repo_count",
        color="artifact_type",
        labels={
            "eol_state": "",
            "repo_count": "Repository Count",
            "artifact_type": "Artifact Type"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )
    return fig, df

from components.chart_style import standard_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
import plotly.express as px

@stacked_bar_chart_style(x_col="artifact_name", y_col="repo_count")
def render_top_expired_xeol_products_chart(df):
    df = df.copy()
    df["artifact_type"] = df["artifact_type"].fillna("Unknown")
    df["artifact_name"] = df["artifact_name"].fillna("Unknown").str.slice(0, 40)
    df = df.sort_values("repo_count", ascending=False)

    fig = px.bar(
        df,
        x="artifact_name",
        y="repo_count",
        color="artifact_type",
        labels={
            "artifact_name": "Artifact / Product",
            "artifact_type": "Artifact Type",
            "repo_count": "Repository Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    fig.update_layout(
        xaxis=dict(type="category", tickangle=45)
    )

    return fig, df



def render_dependency_detection_heatmap(df):
    # 1) Define the “canonical” order for languages and statuses
    full_language_order = [
        "no_language",
        "markup_or_data",
        "other_programming",
        "dotnet",
        "go",
        "javascript",
        "python",
        "java",
    ]
    full_status_order = ["Detected", "None Detected"]

    # 2) Pivot so that rows = language_group, columns = detection_status
    heatmap_data = df.pivot_table(
        index="language_group",
        columns="detection_status",
        values="repo_count",
        aggfunc="sum",
        fill_value=0
    )

    # 3) Keep only whatever languages/statuses actually appear, but in the order we want
    existing_languages = [lang for lang in full_language_order if lang in heatmap_data.index]
    existing_statuses  = [st   for st   in full_status_order   if st   in heatmap_data.columns]

    heatmap_data = heatmap_data.reindex(
        index=existing_languages,
        columns=existing_statuses,
        fill_value=0
    )

    # 4) Extract z, x, y; force integer labels
    z = heatmap_data.values
    x = heatmap_data.columns.tolist()   # e.g. ["Detected", "None Detected"]
    y = heatmap_data.index.tolist()     # e.g. ["no_language", "markup_or_data", …, "java"]
    text = np.vectorize(lambda v: str(int(v)))(z)

    # 5) Build the Heatmap (no textposition required; texttemplate centers it)
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
        xaxis_title="Dependency Detection Status",
        yaxis_title="Language Group",
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig


from plotly import express as px
from components.chart_style import standard_chart_style

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
    fig.update_xaxes(showticklabels=True)
    return fig