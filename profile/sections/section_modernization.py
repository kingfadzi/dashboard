import dash_bootstrap_components as dbc
from dash import html

def render(profile_data):
    # Semgrep Issues Count - count the top 3 issues
    semgrep_issues = profile_data.get('Semgrep Findings', [])
    
    if not semgrep_issues:
        return dbc.Card(
            dbc.CardBody([
                html.H4('Modernization Readiness', className='card-title mb-4'),
                html.P('No Semgrep issues detected.', className='text-muted')
            ]),
            className="mb-4 shadow-sm"
        )
    
    # Aggregating semgrep issues by category
    category_count = {}
    for issue in semgrep_issues:
        category = issue.get('category', 'Unknown')
        if category not in category_count:
            category_count[category] = 0
        category_count[category] += 1

    # Sorting by the most frequent issues
    top_issues = sorted(category_count.items(), key=lambda x: x[1], reverse=True)[:3]

    # Build the badges for the top issues
    issue_badges = []
    for category, count in top_issues:
        issue_badges.append(
            html.Span(f"{category}: {count}", className="badge bg-info me-2", style={"fontSize": "0.9rem"})
        )

    # Build the Modernization Readiness Card
    return dbc.Card(
        dbc.CardBody([
            html.H4('Modernization Readiness', className='card-title mb-4'),

            # The first row for Dockerfile, CI/CD, etc.
            dbc.Row([
                dbc.Col([
                    html.H6('Dockerfile', className='text-muted'),
                    html.Span(
                        "Present" if profile_data.get('Dockerfile', False) else "Missing",
                        className=f"badge {'bg-success' if profile_data.get('Dockerfile', False) else 'bg-danger'}",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('CI/CD Pipeline', className='text-muted'),
                    html.Span(
                        "Present" if profile_data.get('CI/CD Present', False) else "Missing",
                        className=f"badge {'bg-success' if profile_data.get('CI/CD Present', False) else 'bg-danger'}",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('IaC Config', className='text-muted'),
                    html.Span(
                        "Present" if profile_data.get('IaC Config Present', False) else "Missing",
                        className=f"badge {'bg-success' if profile_data.get('IaC Config Present', False) else 'bg-danger'}",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),
            ], className="g-3 mb-4"),

            # The second row for Semgrep Issues Count
            html.H5("Semgrep Issues (Top 3)", className="mt-3 mb-2"),
            html.Div(issue_badges),

        ]),
        className="mb-4 shadow-sm"
    )