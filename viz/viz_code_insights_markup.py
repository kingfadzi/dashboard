import plotly.express as px
import pandas as pd
from dash import dcc

def render_markup_language_usage_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="language",
        y="repo_count",
        labels={"language": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        height=400,
        margin=dict(t=10, b=50),
        xaxis_title=None,
        yaxis_title="Repository Count",
        title=None,
        dragmode=False,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
    )
    fig.update_traces(hovertemplate="%{x}<br>Repos: %{y}")
    return dcc.Graph(id="markup-language-usage-chart", figure=fig, config={"displayModeBar": False})
