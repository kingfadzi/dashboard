from dash import html, dcc
import dash_bootstrap_components as dbc
import helpers

def render(profile_data):
    return dbc.Card(
        dbc.CardBody([
            html.H4('Technology Stack', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.H6('Main Language', className='text-muted'),
                    html.Span(profile_data['Main Language'], className='badge bg-primary mb-2', style={"fontSize": "0.9rem"}),
                    html.Hr(),

                    html.H6('Other Languages', className='text-muted'),
                    html.Div([
                        *[html.Span(lang, className='badge bg-secondary me-2 mb-2', style={"fontSize": "0.8rem"}) for lang in profile_data['Other Languages']]
                    ]),
                    html.Hr(),

                    html.H6('Frameworks', className='text-muted'),
                    html.Div([
                        *[html.Span(fw, className='badge bg-info me-2 mb-2', style={"fontSize": "0.8rem"}) for fw in profile_data['Frameworks']]
                    ]),
                    html.Hr(),

                    html.H6('Build Tool', className='text-muted'),
                    html.P(profile_data['Build Tool'], style={"fontWeight": "bold", "fontSize": "0.9rem"}),

                    html.H6('Runtime Version', className='text-muted'),
                    html.P(profile_data['Runtime Version'], style={"fontWeight": "bold", "fontSize": "0.9rem"}),
                ], width=6),

                dbc.Col([
                    dcc.Graph(
                        figure=helpers.create_language_pie(profile_data['Language Percentages']),
                        config={'displayModeBar': False}
                    )
                ], width=6),
            ])
        ]),
        className="mb-4 shadow-sm"
    )