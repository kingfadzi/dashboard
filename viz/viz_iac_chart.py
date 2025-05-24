import plotly.express as px

def viz_iac_chart(filtered_df):
    if filtered_df.empty:
        return {"data": []}

    fig = px.bar(
        filtered_df,
        x="iac_type",
        y="repo_count",
        labels={"iac_type": "IaC Framework", "repo_count": "Repositories"},
        color="iac_type"
    )

    fig.update_layout(
        xaxis=dict(categoryorder="total descending"),
        template="plotly_white",
        title_text="Top 20 IaC Frameworks",
        title_x=0.5,
        xaxis_title=None,
        yaxis_title="Repositories",
        dragmode=False,
        showlegend=False,
        height=450,
        margin=dict(t=60, b=100)
    )

    return fig