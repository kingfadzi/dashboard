from dash import html, dcc
import dash_bootstrap_components as dbc
import helpers

def render(profile_data):
    frameworks = profile_data.get('Frameworks', [])
    build_tool = profile_data.get('Build Tool')
    runtime_version = profile_data.get('Runtime Version')

    language_percentages = profile_data.get('Language Percentages', {})

    return dbc.Card(
        dbc.CardBody([
            html.H4('Technology Stack', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H6('Frameworks', className='text-muted'),
                            html.Div([
                                *[html.Span(fw, className='badge bg-info me-2 mb-2', style={"fontSize": "0.8rem"}) for fw in frameworks]
                            ]) if frameworks else html.P('No frameworks detected.', className='text-muted', style={"fontSize": "0.85rem"}),
                        ], width=4),

                        dbc.Col([
                            html.H6('Build Tool', className='text-muted'),
                            html.P(build_tool or '-', style={"fontWeight": "bold", "fontSize": "0.85rem"}),
                        ], width=4),

                        dbc.Col([
                            html.H6('Runtime Version', className='text-muted'),
                            html.P(runtime_version or '-', style={"fontWeight": "bold", "fontSize": "0.85rem"}),
                        ], width=4),
                    ], className="mb-4 g-2"),

                    dcc.Graph(
                        figure=helpers.create_language_bar(language_percentages),
                        config={'displayModeBar': False}
                    )
                ], width=8, style={"margin": "0 auto"}),
            ]),
        ]),
        className="mb-4 shadow-sm"
    )