from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

def render(profile_data):
    findings = profile_data.get('Semgrep Findings', [])

    if not findings:
        return dbc.Card(
            dbc.CardBody([
                html.H4('Top Code Risks by Category', className='card-title mb-4'),
                html.P('No static code risks available.', className='text-muted')
            ]),
            className="mb-4 shadow-sm"
        )

    df = pd.DataFrame(findings)

    if df.empty or 'subcategory' not in df.columns or 'severity' not in df.columns:
        return dbc.Card(
            dbc.CardBody([
                html.H4('Top Code Risks by Category', className='card-title mb-4'),
                html.P('Invalid static code risk data.', className='text-muted')
            ]),
            className="mb-4 shadow-sm"
        )

    # Only Critical, High, Medium
    df = df[df['severity'].isin(['Critical', 'High', 'Medium'])]

    # Group and aggregate
    agg = df.groupby(['subcategory', 'severity']).size().unstack(fill_value=0)

    # Sorting
    agg['sort_key'] = (
        agg.get('Critical', 0) * 1000 +
        agg.get('High', 0) * 100 +
        agg.get('Medium', 0)
    )
    agg = agg.sort_values('sort_key', ascending=False).drop(columns=['sort_key'])
    top_agg = agg.head(5)

    severity_colors = {
        'Critical': 'red',
        'High': 'orange',
        'Medium': 'gold'
    }

    # Build table rows
    table_rows = []
    for subcategory, row in top_agg.iterrows():
        badges = []
        for severity in ['Critical', 'High', 'Medium']:
            count = int(row.get(severity, 0))
            if count > 0:
                badges.append(
                    html.Div([
                        html.Span(
                            '●',
                            style={
                                'color': severity_colors.get(severity, 'gray'),
                                'fontSize': '1.2rem',
                                'textShadow': '0px 0px 3px rgba(0,0,0,0.5)',
                                'marginRight': '5px',
                                'lineHeight': '1'
                            }
                        ),
                        html.Span(
                            f"{severity}: {count}",
                            style={"fontSize": "0.85rem"}
                        )
                    ], style={"display": "flex", "alignItems": "center", "marginRight": "10px"})
                )

        table_rows.append(
            html.Tr([
                html.Td(subcategory),
                html.Td(html.Div(badges, style={"display": "flex", "flexWrap": "wrap"})),
            ])
        )

    table_header = html.Thead(html.Tr([
        html.Th("Category"),
        html.Th("Findings"),
    ]))

    table_body = html.Tbody(table_rows)

    return dbc.Card(
        dbc.CardBody([
            html.H4('Top Code Risks by Category', className='card-title mb-4'),
            dbc.Table(
                children=[table_header, table_body],
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
                className="table-striped table-bordered",
            )
        ]),
        className="mb-4 shadow-sm"
    )