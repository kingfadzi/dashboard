import plotly.express as px

def render_markup_language_usage_chart(df):
    fig = px.bar(
        df,
        x="language",
        y="repo_count",
        labels={"language": "", "repo_count": "Repository Count"},
    )
    fig.update_layout(
        height=400,
        margin=dict(t=10),
        xaxis_title=None,
        yaxis_title="Repository Count",
        title=None,
        dragmode=False,
    )
    fig.update_traces(hovertemplate="%{x}<br>Repos: %{y}")
    fig.update_layout(
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
    )
    return fig