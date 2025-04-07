from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    # Safely extract values with defaults if they are None or missing
    dockerfile_present = profile_data.get('Dockerfile', False)
    ci_cd_present = profile_data.get('CI/CD Present', False)
    iac_config_present = profile_data.get('IaC Config Present', False)
    deprecated_apis_found = profile_data.get('Deprecated APIs Found', 0)
    hardcoded_secrets_found = profile_data.get('Hardcoded Secrets Found', 0)
    other_modernization_findings = profile_data.get('Other Modernization Findings', 0)

    return dbc.Card(
        dbc.CardBody([
            html.H4('Modernization Readiness', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.H6('Dockerfile', className='text-muted'),
                    html.Span(
                        "Present" if dockerfile_present else "Missing",
                        className=f"badge {'bg-success' if dockerfile_present else 'bg-danger'}",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('CI/CD Pipeline', className='text-muted'),
                    html.Span(
                        "Present" if ci_cd_present else "Missing",
                        className=f"badge {'bg-success' if ci_cd_present else 'bg-danger'}",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('IaC/Cloud Config', className='text-muted'),
                    html.Span(
                        "Present" if iac_config_present else "Missing",
                        className=f"badge {'bg-success' if iac_config_present else 'bg-danger'}",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),
            ], className="g-3 mb-4"),

            html.H5('Modernization Findings', className='mt-2 mb-3'),

            dbc.Row([
                dbc.Col([
                    html.H6('Deprecated APIs', className='text-muted'),
                    html.Span(
                        f"{deprecated_apis_found}",
                        className="badge bg-warning",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('Hardcoded Secrets', className='text-muted'),
                    html.Span(
                        f"{hardcoded_secrets_found}",
                        className="badge bg-danger",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('Other Modernization Issues', className='text-muted'),
                    html.Span(
                        f"{other_modernization_findings}",
                        className="badge bg-info",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),
            ], className="g-3")
        ]),
        className="mb-4 shadow-sm"
    )
