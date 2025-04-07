from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    # Safely retrieve values with defaults
    outdated_dependencies = profile_data.get('Outdated Dependencies %', 0)
    vulnerable_dependencies = profile_data.get('Vulnerable Dependencies %', 0)
    critical_vuln_count = profile_data.get('Critical Vuln Count', 0)
    eol_packages_found = profile_data.get('EOL Packages Found', 0)
    total_dependencies = profile_data.get('Total Dependencies', 0)
    dependency_managers_used = profile_data.get('Dependency Managers Used', [])

    # Badge Colors
    outdated_color = "success" if outdated_dependencies < 10 else "warning" if outdated_dependencies <= 40 else "danger"
    vulnerable_color = "success" if vulnerable_dependencies < 10 else "warning" if vulnerable_dependencies <= 40 else "danger"
    critical_color = "success" if critical_vuln_count == 0 else "danger"
    eol_color = "success" if eol_packages_found == 0 else "danger"

    return dbc.Card(
        dbc.CardBody([
            html.H4('Dependency Health Overview', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6('Total Dependencies', className='text-muted mb-1'),
                        html.Span(f"{total_dependencies:,}", className="badge bg-primary", style={"fontSize": "1rem", "padding": "6px"})
                    ])
                ], width=12, md=4),

                dbc.Col([
                    html.Div([
                        html.H6('Outdated Dependencies (%)', className='text-muted mb-1'),
                        html.Span(f"{outdated_dependencies}%", className=f"badge bg-{outdated_color}", style={"fontSize": "1rem", "padding": "6px"})
                    ])
                ], width=12, md=4),

                dbc.Col([
                    html.Div([
                        html.H6('Vulnerable Dependencies (%)', className='text-muted mb-1'),
                        html.Span(f"{vulnerable_dependencies}%", className=f"badge bg-{vulnerable_color}", style={"fontSize": "1rem", "padding": "6px"})
                    ])
                ], width=12, md=4),
            ], className="g-4 mb-4"),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6('Critical Vulnerabilities', className='text-muted mb-1'),
                        html.Span(f"{critical_vuln_count}", className=f"badge bg-{critical_color}", style={"fontSize": "1rem", "padding": "6px"})
                    ])
                ], width=12, md=4),

                dbc.Col([
                    html.Div([
                        html.H6('EOL Packages Found', className='text-muted mb-1'),
                        html.Span(f"{eol_packages_found}", className=f"badge bg-{eol_color}", style={"fontSize": "1rem", "padding": "6px"})
                    ])
                ], width=12, md=4),

                dbc.Col([
                    html.Div([
                        html.H6('Dependency Managers', className='text-muted mb-1'),
                        html.Div([
                            *[html.Span(dm, className="badge bg-primary me-2", style={"fontSize": "0.8rem"}) for dm in dependency_managers_used]
                        ])
                    ])
                ], width=12, md=4),
            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )
