from dash import html, dcc
import dash_bootstrap_components as dbc
import helpers

def render(profile_data):
    # Safely extract values with defaults if they are None or missing
    main_language = profile_data.get('Main Language', "not detected")
    other_languages = profile_data.get('Other Languages', [])
    frameworks = profile_data.get('Frameworks', [])
    build_tool = profile_data.get('Build Tool', "not detected")
    runtime_version = profile_data.get('Runtime Version', "not detected")
    language_percentages = profile_data.get('Language Percentages', {})

    return dbc.Card(
        dbc.CardBody([
            html.H4('Technology Stack', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.H6('Main Language', className='text-muted'),
                    html.Span(
                        main_language,
                        className='badge bg-primary mb-2',
                        style={"fontSize": "0.9rem"}
                    ),
                    html.Hr(),

                    html.H6('Other Languages', className='text-muted'),
                    html.Div([
                        *[html.Span(lang, className='badge bg-secondary me-2 mb-2', style={"fontSize": "0.8rem"})
                          for lang in other_languages]
                    ]),
                    html.Hr(),

                    html.H6('Frameworks', className='text-muted'),
                    html.Div([
                        *[html.Span(fw, className='badge bg-info me-2 mb-2', style={"fontSize": "0.8rem"})
                          for fw in frameworks]
                    ]),
                    html.Hr(),

                    html.H6('Build Tool', className='text-muted'),
                    html.P(build_tool, style={"fontWeight": "bold", "fontSize": "0.9rem"}),

                    html.H6('Runtime Version', className='text-muted'),
                    html.P(runtime_version, style={"fontWeight": "bold", "fontSize": "0.9rem"}),
                ], width=6),

                dbc.Col([
                    dcc.Graph(
                        figure=helpers.create_language_pie(language_percentages),
                        config={'displayModeBar': False}
                    )
                ], width=6),
            ])
        ]),
        className="mb-4 shadow-sm"
    )
