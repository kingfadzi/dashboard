import plotly.express as px

from components.chart_style import standard_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE

@standard_chart_style
def render_middleware_subcategory_chart(df):
    fig = px.bar(
        df,
        x="framework",
        y="repo_count",
        color="main_language",
        text="repo_count",
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        labels={
            "framework": "Framework",
            "repo_count": "Repository Count",
            "main_language": "Language"
        },
    )

    fig.update_traces(
        texttemplate="%{text}",
        textposition="inside",
        textfont_size=12
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title=None,
        yaxis_title="Repository Count",
        xaxis_tickangle=-45
    )

    return fig

import plotly.graph_objects as go
import pandas as pd

def render_no_deps_heatmap(df: pd.DataFrame):

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No-dependency Repositories",
            xaxis_title="Build Tool Variant",
            yaxis_title="Contributors Bucket",
            margin=dict(l=60, r=20, t=60, b=60),
        )
        return fig

    # Pivot into 2D format: contributors_bucket (rows) × build_tool_variant (cols)
    pivot_df = df.pivot(
        index="contributors_bucket",
        columns="build_tool_variant",
        values="repos_without_dependencies"
    ).fillna(0)

    # Ensure row and column order
    pivot_df = pivot_df.reindex(['0', '1-5', '6-10', '11-20', '21+'], axis=0)
    pivot_df = pivot_df.reindex(sorted(pivot_df.columns), axis=1)

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns.tolist(),
            y=pivot_df.index.tolist(),
            colorscale="Viridis",
            colorbar=dict(title="# Repos (No Dependencies)"),
            hovertemplate="<b>Variant:</b> %{x}<br><b>Contributors:</b> %{y}<br><b>Repos:</b> %{z}<extra></extra>"
        )
    )

    fig.update_layout(
        title="Repositories Without Dependencies<br>(By Build Tool Variant & Contributors)",
        xaxis_title="Build Tool Variant",
        yaxis_title="Contributors Bucket",
        margin=dict(l=60, r=20, t=80, b=60)
    )

    return fig
