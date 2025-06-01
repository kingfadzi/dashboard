import plotly.express as px
import pandas as pd
import re

def normalize_version(version):
    if not version:
        return "unknown"
    match = re.match(r"(\d+\.\d+)", version)
    return match.group(1) if match else version

def render_spring_version_chart(df, title):
    df = df.copy()
    df["normalized_version"] = df["version"].apply(normalize_version)
    grouped = df.groupby("normalized_version").agg({"repo_count": "sum"}).reset_index()

    fig = px.bar(
        grouped,
        x="normalized_version",
        y="repo_count",
        labels={"normalized_version": "Version", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        title=None,
        margin=dict(t=10),
        dragmode=False,
        xaxis_title=None,
        yaxis_title="Repository Count",
    )
    fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)
    return fig