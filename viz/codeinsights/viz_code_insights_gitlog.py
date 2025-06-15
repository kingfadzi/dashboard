import plotly.express as px
import pandas as pd
from dash import dcc

from components.chart_style import stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE


@stacked_bar_chart_style(x_col="size_bucket", y_col="repo_count")
def render_avg_file_size_chart(df: pd.DataFrame):
    size_order = [
        "0–1KB", "1–2KB", "2–4KB", "4–6KB", "6–8KB",
        "8–10KB", "10–12KB", "12–14KB", "14–16KB", "16–20KB", "20KB+"
    ]

    # Normalize dashes
    df["size_bucket"] = df["size_bucket"].str.replace("-", "–").str.strip()
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
    dominance_order = [
        "0–10%", "10–20%", "20–30%", "30–40%", "40–50%",
        "50–60%", "60–70%", "70–80%", "80–90%", "90–100%"
    ]
    df = df[df["dominance_bucket"].isin(dominance_order)]
    df["dominance_bucket"] = pd.Categorical(df["dominance_bucket"], categories=dominance_order, ordered=True)
    df = df.sort_values("dominance_bucket")

    fig = px.bar(
        df,
        x="dominance_bucket",
        y="repo_count",
        color="language_group",
        labels={
            "dominance_bucket": "Top Contributor % of Commits",
            "repo_count": "Repository Count",
            "language_group": "Language Group"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, df




@stacked_bar_chart_style(x_col="branch_bucket", y_col="repo_count")
def render_branch_sprawl_chart(df: pd.DataFrame):
    branch_order = [
        "Only 1", "2-5", "6-8", "9-15", "16-20",
        "21-30", "31-40", "41-60", "61-80", "80+"
    ]
    df["branch_bucket"] = df["branch_bucket"].replace({"1": "Only 1"})
    df["branch_bucket"] = pd.Categorical(df["branch_bucket"], categories=branch_order, ordered=True)
    df = df.sort_values("branch_bucket")

    fig = px.bar(
        df,
        x="branch_bucket",
        y="repo_count",
        color="language_group",
        labels={
            "branch_bucket": "Active Branch Count",
            "repo_count": "Repository Count",
            "language_group": "Language Group"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, df



@stacked_bar_chart_style(x_col="age_bucket", y_col="repo_count")
def render_repo_age_chart(df: pd.DataFrame):
    age_order = [
        "<1 month", "1-3 months", "3-6 months", "6-12 months",
        "1-2 years", "2-3 years", "3-4 years", "4-5 years",
        "5-7 years", "7+ years"
    ]
    df["age_bucket"] = pd.Categorical(df["age_bucket"], categories=age_order, ordered=True)
    df = df.sort_values("age_bucket")

    fig = px.bar(
        df,
        x="age_bucket",
        y="repo_count",
        color="classification_label",
        labels={
            "age_bucket": "Repository Age",
            "classification_label": "Size",
            "repo_count": "Repository Count"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, df

