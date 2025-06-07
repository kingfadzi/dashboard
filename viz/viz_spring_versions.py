import plotly.express as px
from components.chart_style import standard_chart_style, status_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE

@status_chart_style
def render_spring_version_chart(df, title=None):
    df = df.copy()

    df["version_bucket"] = (
        df["version_bucket"]
        .str.strip()
        .fillna("Invalid / Unrecognized")
    )

    df = df.groupby(["version_bucket", "host_name"], as_index=False)["repo_count"].sum()
    df["repo_count"] = df["repo_count"].astype(int)

    fig = px.bar(
        df,
        x="version_bucket",
        y="repo_count",
        color="host_name",
        labels={
            "version_bucket": "Version",
            "repo_count": "Repository Count",
            "host_name": "Host",
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    # Hide individual stack labels, we'll annotate totals in the decorator
    fig.update_traces(text=None)

    fig.update_yaxes(
        tickformat=".0f",
        tickmode="auto",
        automargin=True,
        ticks="outside",
        title_text="Repository Count"
    )
    fig.update_xaxes(
        categoryorder="category ascending",
        showticklabels=True
    )
    fig.update_layout(barmode="stack")

    return fig

