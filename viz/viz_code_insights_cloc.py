import plotly.express as px
import pandas as pd
from dash import dcc

from components.chart_style import stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE


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
    fig = px.scatter(
        df,
        x="files",
        y="code",
        size="code_size_bytes",
        color="classification_label",
        labels={
            "files": "File Count",
            "code": "Lines of Code",
            "code_size_bytes": "Repo Size (Bytes)",
            "classification_label": "Size"
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        hover_name="repo_name"
    )
    fig.update_layout(
        dragmode=False,
        margin=dict(t=40, b=40, l=20, r=20)
    )
    return fig

