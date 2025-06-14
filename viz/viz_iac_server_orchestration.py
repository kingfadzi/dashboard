import plotly.express as px
import pandas as pd

from components.chart_style import standard_chart_style, stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
import plotly.graph_objects as go

@stacked_bar_chart_style(x_col="framework", y_col="repo_count")
def render_iac_server_orchestration_chart(df: pd.DataFrame):
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available",
            xaxis=dict(title="Framework", visible=True),
            yaxis=dict(title="Repository Count", visible=True),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        return fig, df  # maintain contract with decorator

    fig = px.bar(
        df,
        x="framework",
        y="repo_count",
        color="classification_label",  # Stripe by repo size
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        labels={
            "framework": "Framework",
            "repo_count": "Repository Count",
            "classification_label": "Repo Size"
        },
        barmode="stack"
    )

    return fig, df