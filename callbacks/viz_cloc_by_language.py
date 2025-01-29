import plotly.express as px

def viz_cloc_by_language(filtered_df):

    melted_df = filtered_df.melt(
        id_vars="main_language",
        value_vars=["blank_lines", "comment_lines", "total_lines_of_code", "source_code_file_count"],
        var_name="metric",
        value_name="count"
    )

    fig = px.bar(
        melted_df,
        x="main_language",
        y="count",
        color="metric",
        labels={
            "main_language": "Language",
            "count": "Lines of code",
            "metric": "Metric Type",
        },
        barmode="stack",
    ).update_layout(
        template="plotly_white",
        xaxis=dict(categoryorder="total descending", title=None),
        legend_title=None,  # Remove the legend title
        dragmode=False,
        yaxis=dict(tickformat=",")
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{y:,} lines<extra></extra>"
    )

    return fig
