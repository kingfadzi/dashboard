import plotly.express as px
import pandas as pd

def render_iac_server_orchestration_chart(df: pd.DataFrame):
    if df.empty:
        return px.bar(title="No data available")

    fig = px.bar(
        df,
        x="framework",
        y="repo_count",
        labels={"framework": "Framework", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        height=400,
        title=None,
        margin=dict(t=10),
        dragmode=False,
        xaxis_title=None,
        yaxis_title="Repository Count",
    )
    fig.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)
    return fig