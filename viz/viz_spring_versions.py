import plotly.express as px

def render_spring_version_chart(df, title=None):
    df = df.copy()
    df["version"] = df["version"].fillna("not detected")

    fig = px.bar(
        df,
        x="framework",
        y="repo_count",
        color="version",
        labels={
            "framework": "Framework",
            "version": "Version",
            "repo_count": "Repository Count"
        },
    )
    fig.update_layout(
        title=title,
        barmode="stack",
        margin=dict(t=10),
        dragmode=False,
        xaxis_title=None,
        yaxis_title="Repository Count",
        xaxis_fixedrange=True,
        yaxis_fixedrange=True
    )
    return fig