from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

def render(profile_data):
    findings = profile_data.get('Semgrep Findings', [])

    if not findings:
        return html.Div("No static code risks available.")

    df = pd.DataFrame(findings)

    if df.empty or 'subcategory' not in df.columns or 'severity' not in df.columns:
        return html.Div("Invalid static code risk data.")

    # Only Critical, High, Medium
    df = df[df['severity'].isin(['Critical', 'High', 'Medium'])]

    # Group
    agg = df.groupby(['subcategory', 'severity']).size().unstack(fill_value=0)

    # Sort by severity priority
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

    # Build rows
    rows = []
    for subcategory, row in top_agg.iterrows():
        badges = []

        for severity in ['Critical', 'High', 'Medium']:
            count = int(row.get(severity, 0))
            if count > 0:
                badges.append(
                    html.Div([
                        html.Span('●', style={'color': severity_colors.get(severity, 'gray'), 'fontSize': '1.2rem', 'marginRight': '6px'}),
                        html.Span(f"{severity}: {count}", style={'fontSize': '0.85rem'})
                    ], style={"display": "flex", "alignItems": "center", "marginRight": "10px"})
                )

        rows.append(
            dbc.Row([
                dbc.Col(html.Span(subcategory, style={"fontWeight": "bold"}), width=6),
                dbc.Col(html.Div(badges, style={"display": "flex", "flexWrap": "wrap"}), width=6),
            ], className="mb-2 align-items-center")
        )

    return dbc.Card(
        dbc.CardBody([
            html.H4('Top Code Risks by Category', className='card-title mb-4'),
            html.Div(rows)
        ]),
        className="mb-4 shadow-sm"
    )