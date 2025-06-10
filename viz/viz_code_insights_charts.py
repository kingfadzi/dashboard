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



def render_language_bubble_chart(df):
    fig = px.scatter(
        df,
        x="avg_percent_usage",
        y="avg_code_per_file",
        size="log_repo_count",
        color="language",
        hover_name="language",
        size_max=60,
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        labels={
            "avg_percent_usage": "Avg % Usage",
            "avg_code_per_file": "Avg Code per File",
            "primary_language_count": "Primary Language Count",
            "log_repo_count": "Repo Count (log10)"
        }
    )

    fig.update_layout(
        title=None,
        xaxis_title="Avg % Usage (per repo)",
        yaxis_title="Avg Code per File",
        margin=dict(t=40, b=20, l=20, r=20),
        dragmode=False
    )

    return dcc.Graph(id="language-bubble-chart", figure=fig)

