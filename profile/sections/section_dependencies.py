from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    # Badge Colors
    outdated_color = "success" if profile_data['Outdated Dependencies %'] < 10 else "warning" if profile_data['Outdated Dependencies %'] <= 40 else "danger"
    vulnerable_color = "success" if profile_data['Vulnerable Dependencies %'] < 10 else "warning" if profile_data['Vulnerable Dependencies %'] <= 40 else "danger"
    critical_color = "success" if profile_data['Critical Vuln Count'] == 0 else "danger"
    eol_color = "success" if profile_data['EOL Packages Found'] == 0 else "danger"

    return dbc.Card(
        dbc.CardBody([
            html.H4('Dependency Health Overview', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6('Total Dependencies', className='text-muted mb-1'),
                        html.H5(f"{profile_data['Total Dependencies']:,}", className="text-center"),
                    ])
                ], width=12, md=4),

                dbc.Col([
                    html.Div([
                        html.H6('Outdated Dependencies (%)', className='text-muted mb-1'),
                        html.Span(f"{profile_data['Outdated Dependencies %']}%", className=f"badge bg-{outdated_color}", style={"fontSize": "1rem", "padding": "6px"})
                    ])
                ], width=12, md=4),

                dbc.Col([
                    html.Div([
                        html.H6('Vulnerable Dependencies (%)', className='text-muted mb-1'),
                        html.Span(f"{profile_data['Vulnerable Dependencies %']}%", className=f"badge bg-{vulnerable_color}", style={"fontSize": "1rem", "padding": "6px"})
                    ])
                ], width=12, md=4),
            ], className="g-4 mb-4"),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6('Critical Vulnerabilities', className='text-muted mb-1'),
                        html.Span(f"{profile_data['Critical Vuln Count']}", className=f"badge bg-{critical_color}", style={"fontSize": "1rem", "padding": "6px"})
                    ])
                ], width=12, md=4),

                dbc.Col([
                    html.Div([
                        html.H6('EOL Packages Found', className='text-muted mb-1'),
                        html.Span(f"{profile_data['EOL Packages Found']}", className=f"badge bg-{eol_color}", style={"fontSize": "1rem", "padding": "6px"})
                    ])
                ], width=12, md=4),

                dbc.Col([
                    html.Div([
                        html.H6('Dependency Managers', className='text-muted mb-1'),
                        html.Div([
                            *[html.Span(dm, className="badge bg-primary me-2", style={"fontSize": "0.8rem"}) for dm in profile_data['Dependency Managers Used']]
                        ])
                    ])
                ], width=12, md=4),
            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )