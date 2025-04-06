from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

def render(profile_data):
    # Prepare dependencies
    dependencies = profile_data.get('Dependencies', [])
    if not dependencies:
        return html.Div("No dependency data available.")
    
    df = pd.DataFrame(dependencies)
    
    if df.empty or 'category' not in df.columns or 'sub_category' not in df.columns:
        return html.Div("Invalid dependency structure.")

    # Group for stacked chart
    stacked_data = (
        df.groupby(['category', 'sub_category'])
        .size()
        .reset_index(name='count')
    )

    # Create pivot table for stacking
    pivot = stacked_data.pivot(index='category', columns='sub_category', values='count').fillna(0)

    fig = go.Figure()

    # Add each subcategory as a separate color bar
    for sub_category in pivot.columns:
        fig.add_trace(go.Bar(
            y=pivot.index,
            x=pivot[sub_category],
            name=sub_category,
            orientation='h',
            hovertemplate=f"<b>{sub_category}</b><br>Packages: %{{x}}<extra></extra>",
        ))

    fig.update_layout(
        barmode='stack',
        height=400,
        margin=dict(t=10, b=10, l=40, r=10),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title="Number of Packages",
            fixedrange=True  # <--- disable x-axis zoom
        ),
        yaxis=dict(
            title="Category",
            fixedrange=True  # <--- disable y-axis zoom
        ),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
    )

    # Config: no toolbar, allow hover
    config = {
        'displayModeBar': False,
        'staticPlot': False  # hover works
    }

    return dbc.Card(
        dbc.CardBody([
            html.H4('Dependency Category Breakdown', className='card-title mb-4'),
            dcc.Graph(figure=fig, config=config)
        ]),
        className="mb-4 shadow-sm"
    )