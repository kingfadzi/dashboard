from dash import html, dcc
import dash_bootstrap_components as dbc
import helpers

def render(profile_data):
    return dbc.Card(
        dbc.CardBody([
            html.H4('Technology Stack', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.H6('Frameworks', className='text-muted'),
                    html.Div([
                        *[html.Span(fw, className='badge bg-info me-2 mb-2', style={"fontSize": "0.8rem"}) for fw in profile_data.get('Frameworks', [])]
                    ]) if profile_data.get('Frameworks') else html.P('No frameworks detected.', className='text-muted'),

                    html.Hr(),

                    html.H6('Build Tool', className='text-muted'),
                    html.P(profile_data.get('Build Tool') or '-', style={"fontWeight": "bold", "fontSize": "0.9rem"}),

                    html.H6('Runtime Version', className='text-muted'),
                    html.P(profile_data.get('Runtime Version') or '-', style={"fontWeight": "bold", "fontSize": "0.9rem"}),
                ], width=6),

                dbc.Col([
                    dcc.Graph(
                        figure=helpers.create_language_bar(profile_data.get('Language Percentages', {})),
                        config={'displayModeBar': False}
                    )
                ], width=6),
            ])
        ]),
        className="mb-4 shadow-sm"
    )