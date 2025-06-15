import pandas as pd
import plotly.express as px
from dash import dcc

from components.chart_style import stacked_bar_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE


@stacked_bar_chart_style(x_col="language", y_col="repo_count")
def render_role_distribution_chart(df: pd.DataFrame):
    df["repo_count"] = pd.to_numeric(df["repo_count"], errors="coerce").fillna(0)

    # Keep only top 20 languages by total repo_count
    top_langs = df.groupby("language")["repo_count"].sum().nlargest(20).index
    df = df[df["language"].isin(top_langs)]

    fig = px.bar(
        df,
        x="language",
        y="repo_count",
        color="language_role",
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE,
        barmode="stack",
        text="repo_count",
        labels={
            "language": "",
            "repo_count": "Repository Count"
        },
    )
    return fig, df



from dash import dcc
import plotly.graph_objects as go

def render_language_metrics_heatmap(df):
    metric_rows = [
        "avg_percent_usage",
        "repo_count",
        "primary_language_count",
        "avg_code_per_file"
    ]

    df = df[["language"] + metric_rows]
    z_data = df[metric_rows].values.T

    text_data = []
    for i, metric in enumerate(metric_rows):
        row = []
        for val in z_data[i]:
            if metric == "avg_percent_usage":
                row.append(f"{int(round(val))}%")
            else:
                row.append(f"{int(round(val)):,}")
        text_data.append(row)

    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=df["language"],
        y=metric_rows,
        text=text_data,
        texttemplate="%{text}",
        colorscale=NEUTRAL_COLOR_SEQUENCE,
        showscale=False
    ))

    fig.update_layout(
        title=None,
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(t=20, b=20, l=20, r=20),
        dragmode=False
    )

    return dcc.Graph(id="language-metrics-heatmap", figure=fig)




