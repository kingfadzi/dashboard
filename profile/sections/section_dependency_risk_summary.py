from dash import html
import dash_bootstrap_components as dbc
from collections import Counter

def render(profile_data):
    dependencies = profile_data.get('Dependencies', [])
    vulnerabilities = profile_data.get('Vulnerabilities', [])

    total_dependencies = len(dependencies)

    # Build unique vulnerable packages
    vulnerable_packages = set()
    package_severities = {}

    for v in vulnerabilities:
        pkg = v.get('package')
        version = v.get('version')
        severity = v.get('severity')
        if pkg and version:
            key = (pkg, version)
            vulnerable_packages.add(key)
            existing_sev = package_severities.get(key)
            if existing_sev:
                severity_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
                if severity_order.get(severity, 0) > severity_order.get(existing_sev, 0):
                    package_severities[key] = severity
            else:
                package_severities[key] = severity

    total_vulnerable_packages = len(vulnerable_packages)

    severity_counter = Counter(package_severities.values())

    fix_ready_packages = set()
    for v in vulnerabilities:
        pkg = v.get('package')
        version = v.get('version')
        fix_version = v.get('fix_version')
        if pkg and version and (pkg, version) in vulnerable_packages:
            if fix_version and fix_version not in ('None', '-', ''):
                fix_ready_packages.add((pkg, version))

    fix_ready_count = len(fix_ready_packages)
    fix_ready_percent = round((fix_ready_count / max(total_vulnerable_packages, 1)) * 100, 1)

    return dbc.Card(
        dbc.CardBody([
            html.H4('Dependency Risk Summary', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6('Total Dependencies', className='text-muted mb-2'),
                        dbc.Badge(
                            f"{total_dependencies}",
                            color="primary",
                            className="p-2 mb-2",
                            style={"fontSize": "1rem"}
                        ),
                    ])
                ], width=4),

                dbc.Col([
                    html.Div([
                        html.H6('Vulnerable Dependencies', className='text-muted mb-2'),
                        dbc.Badge(
                            f"{total_vulnerable_packages}",
                            color="danger",
                            className="p-2 mb-2",
                            style={"fontSize": "1rem"}
                        ),
                        html.Div([
                            html.Span(f"Critical: {severity_counter.get('Critical', 0)}", style={"marginRight": "10px"}),
                            html.Span(f"High: {severity_counter.get('High', 0)}", style={"marginRight": "10px"}),
                            html.Span(f"Medium: {severity_counter.get('Medium', 0)}", style={"marginRight": "10px"}),
                            html.Span(f"Low: {severity_counter.get('Low', 0)}"),
                        ], className="text-muted mt-2", style={"fontSize": "0.75rem", "display": "flex", "flexWrap": "wrap"})
                    ])
                ], width=4),

                dbc.Col([
                    html.Div([
                        html.H6('Fix Readiness', className='text-muted mb-2'),
                        dbc.Badge(
                            f"{fix_ready_percent}%",
                            color="success",
                            className="p-2 mb-2",
                            style={"fontSize": "1rem"}
                        ),
                        html.Div([
                            html.Small(f"{fix_ready_count} of {total_vulnerable_packages} vulnerable packages", className="d-block"),
                        ], className="text-muted mt-2", style={"fontSize": "0.75rem"})
                    ])
                ], width=4),
            ], className="g-4"),
        ]),
        className="mb-4 shadow-sm"
    )
