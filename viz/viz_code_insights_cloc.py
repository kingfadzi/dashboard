import plotly.express as px
import pandas as pd
from dash import dcc


def render_code_volume_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="language",
        y="code_lines",
        title="Code Volume by Language",
        labels={"language": "Language", "code_lines": "Lines of Code"}
    )
    return dcc.Graph(id="code-volume-chart", figure=fig)


def render_file_count_chart(df: pd.DataFrame):
    fig = px.bar(
        df,
        x="language",
        y="total_files",
        title="File Count by Language",
        labels={"language": "Language", "total_files": "File Count"}
    )
    return dcc.Graph(id="file-count-chart", figure=fig)


def render_code_composition_chart(df: pd.DataFrame):
    df_melted = df.melt(id_vars="language", value_vars=["code", "comment", "blank"],
                        var_name="type", value_name="lines")
    fig = px.bar(
        df_melted,
        x="language",
        y="lines",
        color="type",
        title="Code vs Comment Composition",
        labels={"language": "Language", "lines": "Line Count", "type": "Segment"}
    )
    return dcc.Graph(id="code-composition-chart", figure=fig)


def render_code_file_scatter_chart(df: pd.DataFrame):
    fig = px.scatter(
        df,
        x="files",
        y="code",
        color="language",
        title="Code vs File Count (Unbalanced Usage)",
        labels={"files": "File Count", "code": "Lines of Code", "language": "Language"}
    )
    return dcc.Graph(id="code-file-scatter-chart", figure=fig)
