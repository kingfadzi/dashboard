import plotly.express as px

def viz_heatmap(filtered_df):

    heatmap_data = filtered_df.pivot(
        index="contributor_bucket",
        columns="commit_bucket",
        values="repo_count",
    ).fillna(0)

    return px.imshow(
        heatmap_data,
        text_auto=True,
    ).update_layout(dragmode=False, title={"x": 0.5})
