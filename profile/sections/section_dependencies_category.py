from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from helpers import create_dependency_category_bar

def render(dependencies_df, top_subcategories_age):
    def color_for_age(age):
        if age < 3:
            return "success"
        elif age <= 5:
            return "warning"
        else:
            return "danger"

    return dbc.Card(
        dbc.CardBody([
            html.H4('Dependency Category Analysis', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=create_dependency_category_bar(dependencies_df),
                        config={'displayModeBar': False}
                    )
                ], width=6),

                dbc.Col([
                    html.H6('Top Subcategories (by Package Count)', className='text-muted mb-3'),
                    dash_table.DataTable(
                        data=[
                            {
                                "Subcategory": row['sub_category'],
                                "Packages": row['packages'],
                                "Avg Age": f"{row['avg_age']:.1f} yrs"
                            }
                            for _, row in top_subcategories_age.iterrows()
                        ],
                        columns=[
                            {"name": "Subcategory", "id": "Subcategory"},
                            {"name": "Packages", "id": "Packages"},
                            {"name": "Avg Age", "id": "Avg Age"},
                        ],
                        style_cell={"fontSize": "0.8rem", "padding": "4px", "textAlign": "left"},
                        style_as_list_view=True,
                        style_table={"overflowX": "auto"},
                        style_header={"backgroundColor": "rgb(240,240,240)", "fontWeight": "bold"},
                        style_data_conditional=[
                            {
                                'if': {
                                    'filter_query': '{Avg Age} >= 5',
                                    'column_id': 'Avg Age'
                                },
                                'backgroundColor': 'rgba(255, 0, 0, 0.1)',
                                'color': 'red',
                                'fontWeight': 'bold'
                            },
                            {
                                'if': {
                                    'filter_query': '{Avg Age} >= 3 && {Avg Age} < 5',
                                    'column_id': 'Avg Age'
                                },
                                'backgroundColor': 'rgba(255,165,0,0.1)',
                                'color': 'orange'
                            },
                            {
                                'if': {
                                    'filter_query': '{Avg Age} < 3',
                                    'column_id': 'Avg Age'
                                },
                                'backgroundColor': 'rgba(0,255,0,0.1)',
                                'color': 'green'
                            },
                        ],
                    )
                ], width=6),
            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )