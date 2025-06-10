import plotly.express as px
import pandas as pd
from dash import dcc

from components.chart_style import stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE


@stacked_bar_chart_style(x_col="size_bucket", y_col="repo_count")
def render_avg_file_size_chart(df: pd.DataFrame):

    size_order = ["< 500B", "500B - 1KB", "1KB - 5KB", "5KB - 20KB", "20KB+"]
    df["size_bucket"] = pd.Categorical(df["size_bucket"], categories=size_order, ordered=True)
    df = df.sort_values("size_bucket")

    fig = px.bar(
        df,
        x="size_bucket",
        y="repo_count",
        color="language_group",
        labels={
            "size_bucket": "Avg File Size",
            "language_group": "Language Group",
            "repo_count": "Repository Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, df


@stacked_bar_chart_style(x_col="dominance_bucket", y_col="repo_count")
def render_contributor_dominance_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="dominance_bucket",
        y="repo_count",
        color="language_group",
        labels={
            "dominance_bucket": "Top Contributor Share",
            "repo_count": "Repository Count",
            "language_group": "Language Group"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, df



def render_branch_sprawl_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="branch_bucket",
        y="repo_count",
        #title="Branch Sprawl (Active Branch Count)",
        labels={"branch_bucket": "Branch Count Bucket", "repo_count": "Repo Count"},
    )
    fig.update_layout(
        dragmode=False
        
    )
    return dcc.Graph(id="branch-sprawl-chart", figure=fig)


def render_repo_age_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="age_bucket",
        y="repo_count",
        #title="Repository Age Buckets",
        labels={"age_bucket": "Repo Age", "repo_count": "Repo Count"},
    )
    fig.update_layout(
        dragmode=False
        
    )
    return dcc.Graph(id="repo-age-chart", figure=fig)
