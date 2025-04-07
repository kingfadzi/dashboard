from dash import html, dcc
import dash_bootstrap_components as dbc
import helpers

def render(profile_data):
    frameworks = profile_data.get('Frameworks', [])
    build_tool = profile_data.get('Build Tool', '-')
    runtime_version = profile_data.get('Runtime Version', '-')

    return dbc.Card(
        dbc.CardBody([
            html.H4('Technology Stack', className='card-title mb-4'),

            # Build tool and runtime version at top
            dbc.Row([
                dbc.Col([
                    html.H6('Build Tool', className='text-muted mb-1'),
                    html.P(build_tool, style={"fontWeight": "bold", "fontSize": "0.9rem"}),
                ], width=6),
                dbc.Col([
                    html.H6('Runtime Version', className='text-muted mb-1'),
                    html.P(runtime_version, style={"fontWeight": "bold", "fontSize": "0.9rem"}),
                ], width=6),
            ], className="mb-4"),

            # Language bar chart and frameworks
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=helpers.create_language_bar(profile_data.get('Language Percentages', {})),
                        config={'displayModeBar': False}
                    )
                ], width=8),

                dbc.Col([
                    html.H6('Frameworks', className='text-muted mb-2'),
                    html.Div(
                        [
                            html.Span(fw, className='badge bg-info me-1 mb-1', style={"fontSize": "0.8rem"})
                            for fw in frameworks
                        ] if frameworks else html.P("No frameworks detected.", className="text-muted"),
                        style={"display": "flex", "flexWrap": "wrap"}
                    )
                ], width=4),
            ])
        ]),
        className="mb-4 shadow-sm"
    )