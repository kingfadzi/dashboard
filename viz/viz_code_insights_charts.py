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



import pandas as pd
import plotly.express as px
from dash import dcc

def render_language_metrics_heatmap(df):
    # Sort by dominance
    df = df.sort_values("avg_percent_usage", ascending=False)

    # Select and round key metrics
    metric_cols = [
        "avg_percent_usage",
        "repo_count",
        "primary_language_count",
        "avg_code_per_file"
    ]
    df_melted = df[["language"] + metric_cols].melt(
        id_vars="language",
        var_name="Metric",
        value_name="Value"
    )

    # Round values for display
    df_melted["Value"] = df_melted["Value"].round(2)

    # Pivot to wide format for imshow
    pivoted = df_melted.pivot(index="Metric", columns="language", values="Value")

    # Plot heatmap with real values
    fig = px.imshow(
        pivoted,
        text_auto=True,
        color_continuous_scale="Viridis",
        aspect="auto"
    )

    fig.update_layout(
        title="Language Metrics Heatmap",
        xaxis_title="Language",
        yaxis_title=None,
        margin=dict(t=40, b=20, l=20, r=20),
        dragmode=False
    )

    return dcc.Graph(id="language-metrics-heatmap", figure=fig)



