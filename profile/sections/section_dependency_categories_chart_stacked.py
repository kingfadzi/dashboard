from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

def render(profile_data):
    dependencies = profile_data.get('Dependencies', [])
    
    if not dependencies:
        return dbc.Card(
            dbc.CardBody([
                html.H4('Dependency Categories (Stacked)', className='card-title mb-4'),
                html.P('No dependencies available.', className='text-muted')
            ]),
            className="mb-4 shadow-sm"
        )

    # Create DataFrame
    df = pd.DataFrame(dependencies)

    if df.empty:
        return html.Div()

    # Group by category and subcategory
    grouped = df.groupby(['category', 'sub_category']).size().reset_index(name='count')

    categories = grouped['category'].unique()

    fig = go.Figure()

    # For each subcategory, create a bar trace
    for subcat in grouped['sub_category'].unique():
        filtered = grouped[grouped['sub_category'] == subcat]
        fig.add_trace(go.Bar(
            y=filtered['category'],
            x=filtered['count'],
            name=subcat,
            orientation='h'
        ))

    fig.update_layout(
        barmode='stack',
        margin=dict(t=20, b=20, l=20, r=20),
        height=450,
        xaxis_title="Number of Dependencies",
        yaxis_title="Category",
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return dbc.Card(
        dbc.CardBody([
            html.H4('Dependency Categories (Stacked)', className='card-title mb-4'),
            dcc.Graph(figure=fig, config={'displayModeBar': False}),
        ]),
        className="mb-4 shadow-sm"
    )