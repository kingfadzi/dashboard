def create_dependency_category_bar(dependencies_df):
    category_counts = dependencies_df['category'].value_counts()

    colors = [
        "#AEC6CF", "#FFB347", "#CFCFC4", "#B39EB5", "#F49AC2",
        "#FDFD96", "#84B6F4", "#FF6961", "#CB99C9", "#FFD1DC"
    ]

    fig = go.Figure(go.Bar(
        y=category_counts.index,
        x=category_counts.values,
        orientation='h',
        marker=dict(
            color=colors * (len(category_counts) // len(colors) + 1)  # Repeat safely
        ),
        text=category_counts.values,
        textposition='auto',
    ))

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=10, b=10, l=10, r=10),
        height=350,
        xaxis_title="Dependencies",
        yaxis_title="Category",
        showlegend=False,
        dragmode=False,
    )

    return fig