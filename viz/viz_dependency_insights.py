import plotly.express as px

import plotly.graph_objects as go
import numpy as np
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


def render_no_deps_heatmap(df):
    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No-dependency Repositories",
            xaxis_title="Language Group",
            yaxis_title="Contributors Bucket",
            margin=dict(l=60, r=20, t=60, b=60),
        )
        return fig

    full_y_order = ['0', '1-5', '6-10', '11-20', '21+']
    full_x_order = [
        "java",
        "python",
        "javascript",
        "go",
        "dotnet",
        "other_programming",
        "markup_or_data",
        "no_language"
    ]

    heatmap_df = df.pivot_table(
        index="contributors_bucket",
        columns="language_group",
        values="repos_without_dependencies",
        aggfunc="sum",
        fill_value=0
    )

    heatmap_df = heatmap_df.reindex(index=full_y_order, columns=full_x_order, fill_value=0)

    z = heatmap_df.values
    x = heatmap_df.columns.tolist()
    y = heatmap_df.index.tolist()
    text = np.vectorize(lambda v: str(int(v)))(z)

    fig = go.Figure(go.Heatmap(
        z=z,
        x=x,
        y=y,
        text=text,
        texttemplate="%{text}",
        textfont={"size": 12},
        colorscale=NEUTRAL_COLOR_SEQUENCE,
        showscale=False
    ))

    fig.update_layout(
        title="",
        xaxis_title="",
        yaxis_title="Number of Contributors",
        margin=dict(l=20, r=20, t=40, b=40)
    )

    return fig
