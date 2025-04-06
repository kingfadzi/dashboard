from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    return dbc.Card(
        dbc.CardBody([
            html.H4('Modernization Readiness', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.H6('Dockerfile', className='text-muted'),
                    html.Span(
                        "Present" if profile_data['Dockerfile'] else "Missing",
                        className=f"badge {'bg-success' if profile_data['Dockerfile'] else 'bg-danger'}",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('CI/CD Pipeline', className='text-muted'),
                    html.Span(
                        "Present" if profile_data['CI/CD Present'] else "Missing",
                        className=f"badge {'bg-success' if profile_data['CI/CD Present'] else 'bg-danger'}",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),
            ], className="g-3 mb-4"),

            html.H5('Modernization Findings', className='mt-2 mb-3'),

            dbc.Row([
                dbc.Col([
                    html.H6('Deprecated APIs', className='text-muted'),
                    html.Span(
                        f"{profile_data['Deprecated APIs Found']}",
                        className="badge bg-warning",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('Hardcoded Secrets', className='text-muted'),
                    html.Span(
                        f"{profile_data['Hardcoded Secrets Found']}",
                        className="badge bg-danger",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('Other Findings', className='text-muted'),
                    html.Span(
                        f"{profile_data['Other Modernization Findings']}",
                        className="badge bg-info",
                        style={"fontSize": "0.9rem", "padding": "5px 10px"}
                    )
                ], width=4),
            ], className="g-3")
        ]),
        className="mb-4 shadow-sm"
    )