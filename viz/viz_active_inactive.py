import plotly.express as px

def viz_active_inactive(filtered_df):

    aggregated_df = filtered_df.groupby(
        ["activity_status", "host_name"], as_index=False
    )["repo_count"].sum()
    aggregated_df["activity_status"] = aggregated_df["activity_status"].str.capitalize()

    color_map = {"Active": "green", "Inactive": "red"}

    fig = px.bar(
        aggregated_df,
        x="activity_status",
        y="repo_count",
        color="host_name",
        barmode="stack",
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )

    for trace in fig.data:
        if trace.name in color_map:
            trace.marker.color = color_map[trace.name]

    fig.update_layout(
        dragmode=False,
        xaxis_title="",
        yaxis_title="Repository Count",
        legend_title="Host Name",
    )

    return fig
