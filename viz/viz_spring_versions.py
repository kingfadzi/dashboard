import plotly.express as px
from components.chart_style import standard_chart_style
from components.colors import NEUTRAL_COLOR_SEQUENCE

@standard_chart_style
def render_spring_version_chart(df, title=None):
    df = df.copy()

    df["version_bucket"] = (
        df["version_bucket"]
        .str.strip()
        .fillna("Invalid / Unrecognized")
    )

    df = df.groupby(["version_bucket", "host_name"], as_index=False)["repo_count"].sum()
    df["repo_count"] = df["repo_count"].astype(int)
    df["text_label"] = df["repo_count"].astype(str)

    fig = px.bar(
        df,
        x="version_bucket",
        y="repo_count",
        color="host_name",
        text="text_label",
        labels={
            "version_bucket": "Version",
            "repo_count": "Repository Count",
            "host_name": "Host",
        },
        color_discrete_sequence=NEUTRAL_COLOR_SEQUENCE
    )

    fig.update_traces(textposition="outside")
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
