import pandas as pd
import plotly.express as px

from components.chart_style import stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
from utils.formattting import human_readable_size


# 1. Total Cyclomatic Complexity
@stacked_bar_chart_style(x_col="ccn_bucket", y_col="repo_count")
def render_total_ccn_chart(df: pd.DataFrame):
    ccn_order = ["< 100", "100-299", "300-599", "600+"]
    df["ccn_bucket"] = pd.Categorical(df["ccn_bucket"], categories=ccn_order, ordered=True)
    df = df.sort_values("ccn_bucket")

    fig = px.bar(
        df,
        x="ccn_bucket",
        y="repo_count",
        color="language_group",
        labels={
            "ccn_bucket": "Cyclomatic Complexity",
            "repo_count": "Repository Count",
            "language_group": "Language Group"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, df

# 2. Function Count
@stacked_bar_chart_style(x_col="function_bucket", y_col="repo_count")
def render_function_count_chart(df: pd.DataFrame):
    bucket_order = ["< 10", "10-49", "50-199", "200+"]
    df["function_bucket"] = pd.Categorical(df["function_bucket"], categories=bucket_order, ordered=True)
    df = df.sort_values("function_bucket")

    fig = px.bar(
        df,
        x="function_bucket",
        y="repo_count",
        color="language_group",
        labels={
            "function_bucket": "Function Count",
            "repo_count": "Repository Count",
            "language_group": "Language Group"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, df

# 3. Total NLOC
@stacked_bar_chart_style(x_col="nloc_bucket", y_col="repo_count")
def render_total_nloc_chart(df: pd.DataFrame):
    bucket_order = ["< 1K", "1K–4.9K", "5K–9.9K", "10K+"]
    df["nloc_bucket"] = pd.Categorical(df["nloc_bucket"], categories=bucket_order, ordered=True)
    df = df.sort_values("nloc_bucket")

    fig = px.bar(
        df,
        x="nloc_bucket",
        y="repo_count",
        color="language_group",
        labels={
            "nloc_bucket": "Non-Commented LOC (NLOC)",
            "repo_count": "Repository Count",
            "language_group": "Language Group"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, df


# 4. Scatter: Function Count vs Total Complexity
def render_ccn_vs_function_count_chart(df: pd.DataFrame):
    df = df.copy()
    df["code_size_bytes"] = pd.to_numeric(df["code_size_bytes"], errors="coerce").fillna(0)
    df["avg_ccn"] = df["total_ccn"] / df["function_count"]
    df = df[df["function_count"] > 0]

    # Strip outliers for function count only
    function_threshold = df["function_count"].quantile(0.98)
    df = df[df["function_count"] <= function_threshold]

    # Format repo size for hover
    df["repo_size_human"] = df["code_size_bytes"].apply(human_readable_size)

    # Size color ticks
    min_size = df["code_size_bytes"].min()
    max_size = df["code_size_bytes"].max()
    tickvals = [min_size, max_size/4, max_size/2, 3*max_size/4, max_size]
    ticktext = [human_readable_size(v) for v in tickvals]

    fig = px.scatter(
        df,
        x="function_count",
        y="avg_ccn",
        size="code_size_bytes",
        color="code_size_bytes",
        hover_name="repo_name",
        color_continuous_scale=NEUTRAL_COLOR_SEQUENCE,
        labels={
            "function_count": "Function Count",
            "avg_ccn": "Average Cyclomatic Complexity",
            "code_size_bytes": "Repo Size (Bytes)",
            "repo_size_human": "Repo Size"
        },
        hover_data={
            "repo_name": True,
            "repo_size_human": True,
            "code_size_bytes": False,
            "avg_ccn": True,
            "function_count": True
        }
    )

    fig.update_layout(
        template="plotly_white",
        dragmode=False,
        autosize=True,
        margin=dict(t=40, b=40, l=20, r=20),
        coloraxis_colorbar=dict(
            title=dict(text="Repository Size", side="top", font=dict(size=14)),
            tickvals=tickvals,
            ticktext=ticktext,
            tickfont=dict(size=10)
        )
    )

    fig.update_traces(marker=dict(opacity=0.7))
    return fig
