import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table 
from helpers import create_dependency_category_bar

def render(profile_data):
    """
    Render Dependency Category Analysis with a full-width bar chart and a table underneath.
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

    # 2. Build Horizontal Bar Chart
    category_bar = create_dependency_category_bar(dependencies_df)

    # 3. Top Subcategories Table
    top_subcategories_age = (
        dependencies_df
        .groupby('sub_category')
        .agg(
            packages=('name', 'count'),
            avg_age=('age', 'mean')
        )
        .sort_values(by='packages', ascending=False)
        .reset_index()
        .head(5)
    )

    # 4. Final layout
    return dbc.Card(
        dbc.CardBody([
            html.H4('Dependency Category Analysis', className='card-title mb-4'),

            # Bar Chart Full Width
            html.Div([
                html.H6('Category Distribution', className='text-muted mb-2'),
                dcc.Graph(
                    figure=category_bar,
                    config={'displayModeBar': False},
                    style={"height": "350px"}
                ),
            ], className="mb-4"),

            # Table Full Width
            html.Div([
                html.H6('Top Subcategories by Packages', className='text-muted mb-3'),
                dash_table.DataTable(
                    data=[
                        {
                            "Subcategory": row['sub_category'],
                            "Packages": row['packages'],
                            "Avg Age (Years)": f"{row['avg_age']:.1f}"
                        }
                        for _, row in top_subcategories_age.iterrows()
                    ],
                    columns=[
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