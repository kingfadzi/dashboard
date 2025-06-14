import plotly.express as px
import pandas as pd
from dash import dcc

import plotly.express as px

from components.chart_style import stacked_bar_chart_style, standard_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE


@standard_chart_style
def render_markup_language_usage_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="language",
        y="repo_count",
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        labels={"language": "", "repo_count": "Repository Count"},
    )
    # Add values on top of each bar
    fig.update_traces(
        text=df["repo_count"],
        texttemplate="%{text:.0f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="%{x}<br>Repos: %{y}",
    )
    fig.update_layout(
        dragmode=False,
        xaxis_tickfont=dict(size=10),
        title=None,
        margin=dict(t=40, b=20, l=20, r=20),
    )
    fig.update_xaxes(showticklabels=True)
    return fig

