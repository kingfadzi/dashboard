import plotly.express as px

def viz_semgrep_findings(filtered_df):

    return px.bar(
        filtered_df,
        x="category",
        y="repo_count",
        labels={
            "category": "Issue Category",
            "repo_count": "Repository Count",
        },
        color="category",
    ).update_layout(
        template="plotly_white",
        title={"x": 0.5},
        dragmode=False,
        showlegend=False
    )
