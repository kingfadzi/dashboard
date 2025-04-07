from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

SEVERITY_ORDER = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}

def render(profile_data):
    findings = profile_data.get('Semgrep Findings', [])

    if not findings:
        return html.Div("No static code risks available.")

    df = pd.DataFrame(findings)

    if df.empty or 'category' not in df.columns or 'subcategory' not in df.columns or 'severity' not in df.columns:
        return html.Div("Invalid code risk data structure.")

    df['severity_weight'] = df['severity'].map(SEVERITY_ORDER).fillna(0)

    agg = (
        df.groupby(['category', 'subcategory'])
        .agg(findings=('severity', 'count'), highest_severity_weight=('severity_weight', 'max'))
        .reset_index()
    )

    agg = agg.sort_values(by=['highest_severity_weight', 'findings'], ascending=[False, False])

    pivot = agg.pivot(index='category', columns='subcategory', values='findings').fillna(0)

    fig = go.Figure()

    for subcategory in pivot.columns:
        fig.add_trace(go.Bar(
            y=pivot.index,
            x=pivot[subcategory],
            name=subcategory,
            orientation='h',
            hovertemplate=f"<b>{subcategory}</b><br>Findings: %{{x}}<extra></extra>",
        ))

    fig.update_layout(
        barmode='stack',
        height=400,
        margin=dict(t=10, b=10, l=40, r=10),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            title="Findings",
            fixedrange=True
        ),
        yaxis=dict(
            title="Category",
            fixedrange=True
        ),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
    )

    config = {
        'displayModeBar': False,
        'staticPlot': False
    }

    return dbc.Card(
        dbc.CardBody([
            html.H4('Static Code Risk by Category', className='card-title mb-4'),

            dcc.Graph(figure=fig, config=config),

            html.H5('Top Risky Subcategories', className='mt-4 mb-3'),

            dash_table.DataTable(
                data=agg[['category', 'subcategory', 'findings']].to_dict('records'),
                columns=[
                    {"name": "Category", "id": "category"},
                    {"name": "Subcategory", "id": "subcategory"},
                    {"name": "Findings", "id": "findings"},
                ],
                style_cell={"fontSize": "0.8rem", "padding": "4px"},
                style_table={"overflowX": "auto"},
                style_as_list_view=True,
                style_header={"backgroundColor": "rgb(240,240,240)", "fontWeight": "bold"},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                    {
                        'if': {
                            'filter_query': '{findings} >= 5',
                            'column_id': 'findings'
                        },
                        'color': 'red',
                        'fontWeight': 'bold'
                    }
                ],
            )
        ]),
        className="mb-4 shadow-sm"
    )