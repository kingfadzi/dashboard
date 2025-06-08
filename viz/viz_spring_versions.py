import re

import pandas as pd
import plotly.express as px
from components.chart_style import standard_chart_style, status_chart_style, stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE

@stacked_bar_chart_style(x_col="version_bucket", y_col="repo_count")
def render_spring_version_chart(df, title=None):
    df = df.copy()

    # Clean and fill empty buckets
    df["version_bucket"] = (
        df["version_bucket"]
        .astype(str)
        .str.strip()
        .replace("", "Invalid")
        .fillna("Invalid")
    )

    # Prefix numeric-looking buckets with 'v'
    def prefix_if_numeric(value):
        return f"v{value}" if re.fullmatch(r"\d+(\.\d+)*", value) else value

    df["version_bucket"] = df["version_bucket"].apply(prefix_if_numeric)

    # Group and sum
    df = df.groupby(["version_bucket", "host_name"], as_index=False)["repo_count"].sum()
    df["repo_count"] = df["repo_count"].astype(int)

    # Preserve sorted order
    ordered_versions = df["version_bucket"].drop_duplicates().sort_values(key=lambda s: s.str.extract(r"(\d+(?:\.\d+)*)")[0].astype(float, errors='ignore')).tolist()
    df["version_bucket"] = pd.Categorical(df["version_bucket"], categories=ordered_versions, ordered=True)

    fig = px.bar(
        df,
        x="version_bucket",
        y="repo_count",
        color="host_name",
        labels={
            "version_bucket": "Version",
            "repo_count": "Repository Count",
            "host_name": "Host",
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, df
