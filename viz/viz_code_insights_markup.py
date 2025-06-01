import plotly.express as px
import pandas as pd
from dash import dcc

import plotly.express as px

def render_markup_language_usage_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="language",
        y="repo_count",
        labels={"language": "", "repo_count": "Repository Count"},
    )
    # Add values on top of each bar
    fig.update_traces(
        text=df["repo_count"],
        texttemplate="%{text:.0f}",
        textposition="outside",
        cliponaxis=False
    )
    fig.update_layout(
        dragmode=False,
        xaxis_title=None,
        title=None,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    fig.update_traces(hovertemplate="%{x}<br>Repos: %{y}")
    return fig
