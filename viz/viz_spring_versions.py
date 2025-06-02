import plotly.express as px

import plotly.express as px

def render_spring_version_chart(df, title=None):
    df = df.copy()

    # Normalize version buckets and handle missing values
    df["version_bucket"] = (
        df["version_bucket"]
        .str.strip()  # Remove leading/trailing whitespace
        .fillna("Invalid / Unrecognized")
    )

    # Ensure unique combinations by aggregating (if needed)
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
    )

    fig.update_traces(textposition="outside")
    fig.update_yaxes(
        tickformat=".0f",
        tickmode="auto",
        automargin=True,
        ticks="outside"
    )

    fig.update_layout(
        barmode="stack",
        margin=dict(t=10),
        dragmode=False,
        xaxis_title=None,
        yaxis_title="Repository Count",
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        xaxis={'categoryorder': 'category ascending'}  # Enforce consistent ordering
    )

    return fig
