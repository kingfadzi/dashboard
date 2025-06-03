import plotly.express as px
import pandas as pd

from components.chart_style import standard_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
import plotly.graph_objects as go

@standard_chart_style
def render_iac_server_orchestration_chart(df: pd.DataFrame):
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available",
            xaxis=dict(title="Framework", visible=True),
            yaxis=dict(title="Repository Count", visible=True),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        return fig

    fig = px.bar(
        df,
        x="framework",
        y="repo_count",
        text="repo_count",
        color="main_language",  # Language stripe
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        labels={
            "framework": "Framework",
            "repo_count": "Repository Count",
            "main_language": "Main Language"
        },
        barmode="stack"
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textfont_size=12
    )

    fig.update_layout(
        title=None,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title=None,
        yaxis_title="Repository Count",
        dragmode=False,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True
    )

    fig.update_xaxes(showticklabels=True)

    return fig

