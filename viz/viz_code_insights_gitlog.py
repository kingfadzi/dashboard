import plotly.express as px
import pandas as pd
from dash import dcc


def render_avg_file_size_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="size_bucket",
        y="repo_count",
        #title="Average File Size (code_size / file_count)",
        labels={"size_bucket": "Avg File Size", "repo_count": "Repo Count"},
    )
    return dcc.Graph(id="avg-file-size-chart", figure=fig)


def render_contributor_dominance_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="dominance_bucket",
        y="repo_count",
        #title="Contributor Dominance (Top Contributor % of Commits)",
        labels={"dominance_bucket": "Ownership Bucket", "repo_count": "Repo Count"},
    )
    return dcc.Graph(id="contributor-dominance-chart", figure=fig)


def render_branch_sprawl_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="branch_bucket",
        y="repo_count",
        #title="Branch Sprawl (Active Branch Count)",
        labels={"branch_bucket": "Branch Count Bucket", "repo_count": "Repo Count"},
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
    return dcc.Graph(id="repo-age-chart", figure=fig)
