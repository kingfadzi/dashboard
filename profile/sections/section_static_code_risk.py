from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

def render(profile_data):
    findings = profile_data.get('Semgrep Findings', [])

    if not findings:
        return html.Div("No static code risks available.")

    df = pd.DataFrame(findings)

    if df.empty or 'category' not in df.columns or 'subcategory' not in df.columns or 'severity' not in df.columns:
        return html.Div("Invalid static code risk data.")

    # Focus only on Critical, High, Medium
    df = df[df['severity'].isin(['Critical', 'High', 'Medium'])]

    # Group by subcategory and severity
    agg = df.groupby(['subcategory', 'severity']).size().unstack(fill_value=0)

    # Sort: Critical > High > Medium findings
    agg['sort_key'] = (
        agg.get('Critical', 0) * 1000 +
        agg.get('High', 0) * 100 +
        agg.get('Medium', 0)
    )
    agg = agg.sort_values('sort_key', ascending=False).drop(columns=['sort_key'])

    # Limit to top 5 risky subcategories
    top_agg = agg.head(5)

    # Generate rows with badges
    rows = []
    for subcategory, row in top_agg.iterrows():
        badges = []

        if row.get('Critical', 0) > 0:
            badges.append(dbc.Badge(f"Critical {int(row['Critical'])}", color="danger", className="me-1", pill=True))
        if row.get('High', 0) > 0:
            badges.append(dbc.Badge(f"High {int(row['High'])}", color="warning", className="me-1", pill=True))
        if row.get('Medium', 0) > 0:
            badges.append(dbc.Badge(f"Medium {int(row['Medium'])}", color="secondary", className="me-1", pill=True))

        rows.append(
            dbc.Row([
                dbc.Col(html.Span(subcategory, style={"fontWeight": "bold"}), width=6),
                dbc.Col(badges, width=6),
            ], className="mb-2 align-items-center")
        )

    return dbc.Card(
        dbc.CardBody([
            html.H4('Top Code Risks by Category', className='card-title mb-4'),
            html.Div(rows)
        ]),
        className="mb-4 shadow-sm"
    )