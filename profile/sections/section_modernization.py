import dash_bootstrap_components as dbc
from dash import html

def render(profile_data):
    semgrep_findings = profile_data.get('Semgrep Findings', [])
    modernization_signals = profile_data.get('Modernization Signals', {})

    severity_rank = {
        "error": 3,    # Highest priority
        "warning": 2,
        "info": 1,
        "unlabeled": 0
    }

    severity_color = {
        "error": "danger",     # Red
        "warning": "warning",  # Orange
        "info": "primary"      # Blue
    }

    # Group findings by category
    category_data = {}

    for finding in semgrep_findings:
        category = finding.get('category', 'Unknown')
        severity = finding.get('severity', 'unlabeled').lower()

        if category not in category_data:
            category_data[category] = {"count": 0, "highest_severity": severity}
        category_data[category]["count"] += 1

        # Update highest severity if necessary
        current_rank = severity_rank.get(severity, 0)
        existing_rank = severity_rank.get(category_data[category]["highest_severity"], 0)
        if current_rank > existing_rank:
            category_data[category]["highest_severity"] = severity

    # Sort by count
    top_categories = sorted(category_data.items(), key=lambda x: x[1]['count'], reverse=True)[:3]

    semgrep_cols = []
    for category, data in top_categories:
        semgrep_cols.append(
            dbc.Col([
                html.H6(f"{category.title()} Issues", className='text-muted'),
                dbc.Badge(
                    f"{data['count']}",
                    color=severity_color.get(data["highest_severity"], "secondary"),
                    className="p-2",
                    style={"fontSize": "1.0rem"}
                )
            ], width=4)
        )

    if not semgrep_cols:
        semgrep_cols = [dbc.Col(html.P('No static code risks detected.', className="text-muted"))]

    return dbc.Card(
        dbc.CardBody([
            html.H4('Modernization Readiness', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.H6('Dockerfile', className='text-muted'),
                    html.Span(
                        "Present" if modernization_signals.get('Dockerfile', False) else "Missing",
                        className=f"badge {'bg-success' if modernization_signals.get('Dockerfile', False) else 'bg-danger'}",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('CI/CD Pipeline', className='text-muted'),
                    html.Span(
                        "Present" if modernization_signals.get('CI/CD Pipeline', False) else "Missing",
                        className=f"badge {'bg-success' if modernization_signals.get('CI/CD Pipeline', False) else 'bg-danger'}",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('IaC Config', className='text-muted'),
                    html.Span(
                        "Present" if modernization_signals.get('IaC Config', False) else "Missing",
                        className=f"badge {'bg-success' if modernization_signals.get('IaC Config', False) else 'bg-danger'}",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),
            ], className="g-3 mb-4"),

            dbc.Row(semgrep_cols, className="g-3"),
        ]),
        className="mb-4 shadow-sm"
    )