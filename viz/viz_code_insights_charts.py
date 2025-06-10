import pandas as pd
import plotly.express as px
from dash import dcc

from components.chart_style import stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE


@stacked_bar_chart_style(x_col="language", y_col="repo_count")
def render_role_distribution_chart(df: pd.DataFrame):
    df["repo_count"] = pd.to_numeric(df["repo_count"], errors="coerce").fillna(0)

    # Keep only top 20 languages by total repo_count
    top_langs = df.groupby("language")["repo_count"].sum().nlargest(20).index
    df = df[df["language"].isin(top_langs)]

    fig = px.bar(
        df,
        x="language",
        y="repo_count",
        color="language_role",
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack",
        text="repo_count",
        labels={
            "language": "",
            "repo_count": "Repository Count"
        },
    )
    return fig, df



import plotly.graph_objects as go
import numpy as np

def render_language_mixed_chart(df):
    # Sort for consistent layout
    df = df.sort_values("avg_percent_usage", ascending=False)

    # Log-scale repo count for line
    df["log_repo_count"] = df["repo_count"].apply(lambda x: round(np.log10(x + 1), 2))

    fig = go.Figure()

    # Bar chart: avg percent usage
    fig.add_trace(go.Bar(
        x=df["language"],
        y=df["avg_percent_usage"],
        name="Avg % Usage",
        yaxis="y1",
        marker_color="#636EFA"
    ))

    # Line chart: log repo count
    fig.add_trace(go.Scatter(
        x=df["language"],
        y=df["log_repo_count"],
        name="Log(Repo Count)",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="#EF553B", width=3),
        marker=dict(size=6)
    ))

    # Layout with dual axes
    fig.update_layout(
        title=None,
        xaxis=dict(title="Language"),
        yaxis=dict(title="Avg % Usage", side="left", range=[0, 100]),
        yaxis2=dict(
            title="Log10(Repo Count)",
            overlaying="y",
            side="right",
            showgrid=False,
            #range=[0, 5]
        ),
        legend=dict(x=0.5, y=1.15, xanchor="center", orientation="h"),
        margin=dict(t=40, b=20, l=40, r=40),
        dragmode=False
    )

    return dcc.Graph(id="language-mixed-chart", figure=fig)


