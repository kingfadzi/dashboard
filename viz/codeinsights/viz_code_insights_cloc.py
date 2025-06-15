import plotly.express as px
import pandas as pd
from dash import dcc

from components.chart_style import stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE
from utils.formattting import human_readable_size


@stacked_bar_chart_style(x_col="language", y_col="lines")
def render_code_composition_chart(df: pd.DataFrame):
    df_melted = df.melt(
        id_vars="language",
        value_vars=["code", "comment", "blank"],
        var_name="type",
        value_name="lines"
    )

    fig = px.bar(
        df_melted,
        x="language",
        y="lines",
        color="type",
        labels={
            "language": "Language",
            "lines": "Line Count",
            "type": "Segment"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack"
    )

    return fig, df_melted



def render_code_file_scatter_chart(df: pd.DataFrame):
    # Filter valid and positive values
    df = df[df["code"].notnull() & df["code_size_bytes"].notnull()]
    df = df[(df["code"] > 0) & (df["code_size_bytes"] > 0)]

    # Remove top 5% LOC outliers
    threshold = df["code"].quantile(0.95)
    df = df[df["code"] <= threshold]

    # Human-readable repo size
    df["repo_size"] = df["code_size_bytes"]
    df["repo_size_human"] = df["repo_size"].apply(human_readable_size)

    # Tick scale setup
    min_size = df["repo_size"].min()
    max_size = df["repo_size"].max()
    tickvals = [min_size, max_size/4, max_size/2, 3*max_size/4, max_size]
    ticktext = [human_readable_size(v) for v in tickvals]

    fig = px.scatter(
        df,
        x="files",
        y="code",
        size="repo_size",
        size_max=60,
        color="repo_size",
        color_continuous_scale=NEUTRAL_COLOR_SEQUENCE,
        labels={
            "files": "File Count",
            "code": "Lines of Code",
            "repo_size": "Repo Size (Bytes)",
            "repo_size_human": "Repo Size"
        },
        hover_name="repo_name",
        hover_data={
            "repo_size_human": True,
            "repo_size": False,
            "code": True,
            "files": True
        },
    )

    fig.update_layout(
        dragmode=False,
        margin=dict(t=40, b=40, l=20, r=20),
        coloraxis_colorbar=dict(
            title=dict(
                text="Repo Size",
                side="top",
                font=dict(size=14),
            ),
            tickvals=tickvals,
            ticktext=ticktext,
            tickfont=dict(size=10)
        )
    )

    fig.update_yaxes(title="Lines of Code", type="linear")

    return fig





