import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
import plotly.graph_objects as go

# --- Instead of using helper, let's define the bar inside this section ---
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

# --- Main Renderer ---
def render(profile_data):
    """
    Renders Dependency Category Analysis with full-width bar chart and full table including category.
    """

    # 1. Read Dependencies
    dependencies = profile_data.get('Dependencies', [])

    if not dependencies:
        return dbc.Card(
            dbc.CardBody([
                html.H4('Dependency Category Analysis', className='card-title mb-4'),
                html.P("No dependency data available.", className="text-muted")
            ]),
            className="mb-4 shadow-sm"
        )

    dependencies_df = pd.DataFrame(dependencies)

    # 2. Build Chart
    category_bar = create_dependency_category_bar(dependencies_df)

    # 3. Build Full Subcategories Table
    top_subcategories_age = (
        dependencies_df
        .groupby(['category', 'sub_category'])
        .agg(
            packages=('name', 'count'),
            avg_age=('age', 'mean')
        )
        .sort_values(by='packages', ascending=False)
        .reset_index()
        .head(10)  # <-- Top 10 now since we have more granularity
    )

    # 4. Return layout
    return dbc.Card(
        dbc.CardBody([
            html.H4('Dependency Category Analysis', className='card-title mb-4'),

            # Full-width Bar Chart
            html.Div([
                html.H6('Category Distribution', className='text-muted mb-2'),
                dcc.Graph(
                    figure=category_bar,
                    config={
                        'displayModeBar': False,  # no zoom
                        'staticPlot': False       # no panning
                    },
                    style={"height": "350px"}
                ),
            ], className="mb-4"),

            # Full-width Table
            html.Div([
                html.H6('Top Subcategories by Packages', className='text-muted mb-3'),
                dash_table.DataTable(
                    data=[
                        {
                            "Category": row['category'],
                            "Subcategory": row['sub_category'],
                            "Packages": row['packages'],
                            "Avg Age (Years)": f"{row['avg_age']:.1f}"
                        }
                        for _, row in top_subcategories_age.iterrows()
                    ],
                    columns=[
                        {"name": "Category", "id": "Category"},
                        {"name": "Subcategory", "id": "Subcategory"},
                        {"name": "Packages", "id": "Packages"},
                        {"name": "Avg Age (Years)", "id": "Avg Age (Years)"},
                    ],
                    style_cell={
                        "fontSize": "0.8rem",
                        "padding": "5px",
                        "textAlign": "left"
                    },
                    style_as_list_view=True,
                    style_table={"overflowX": "auto"},
                    style_header={
                        "backgroundColor": "rgb(240,240,240)",
                        "fontWeight": "bold"
                    },
                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{Avg Age (Years)} >= 5', 'column_id': 'Avg Age (Years)'},
                            'backgroundColor': 'rgba(255, 0, 0, 0.1)',
                            'color': 'red',
                            'fontWeight': 'bold'
                        },
                        {
                            'if': {'filter_query': '{Avg Age (Years)} >= 3 && {Avg Age (Years)} < 5', 'column_id': 'Avg Age (Years)'},
                            'backgroundColor': 'rgba(255,165,0,0.1)',
                            'color': 'orange'
                        },
                        {
                            'if': {'filter_query': '{Avg Age (Years)} < 3', 'column_id': 'Avg Age (Years)'},
                            'backgroundColor': 'rgba(0,255,0,0.1)',
                            'color': 'green'
                        },
                    ],
                )
            ]),
        ]),
        className="mb-4 shadow-sm"
    )