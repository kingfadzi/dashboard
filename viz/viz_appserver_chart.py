import plotly.express as px

def viz_appserver_chart(filtered_df):
    if filtered_df.empty:
        return px.bar(
            title="No App Server Data Found"
        )

    return px.bar(
        filtered_df,
        x="iac_type",
        y="repo_count",
        labels={"iac_type": "App Server", "repo_count": "Repository Count"},
        color="iac_type"
    ).update_layout(
        xaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        title={"text": "Top Application Servers", "x": 0.5},
        xaxis_title=None,
        dragmode=False,
        showlegend=False
    )