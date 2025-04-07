from dash import html, dcc
import dash_bootstrap_components as dbc
import helpers

def render(profile_data):
    frameworks = profile_data.get('Frameworks', [])
    build_tool = profile_data.get('Build Tool', '-')
    runtime_version = profile_data.get('Runtime Version', '-')

    return dbc.Cardfrom dash import html, dcc
import dash_bootstrap_components as dbc
import helpers

def render(profile_data):
    main_language = profile_data.get('Main Language', 'Unknown')
    build_tool = profile_data.get('Build Tool', 'N/A') or 'N/A'
    runtime_version = profile_data.get('Runtime Version', 'N/A') or 'N/A'
    frameworks = profile_data.get('Frameworks', [])

    return dbc.Card(
        dbc.CardBody([
            html.H4('Technology Stack', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col(html.Small('Build Tool:', className='text-muted'), width="auto"),
                        dbc.Col(html.Span(build_tool, style={"fontWeight": "bold", "fontSize": "0.9rem"})),
                    ], align="center", className="mb-2"),

                    dbc.Row([
                        dbc.Col(html.Small('Runtime Version:', className='text-muted'), width="auto"),
                        dbc.Col(html.Span(runtime_version, style={"fontWeight": "bold", "fontSize": "0.9rem"})),
                    ], align="center", className="mb-4"),

                    html.H6('Frameworks', className='text-muted'),
                    html.Div([
                        html.Div(
                            html.Span(fw, className='badge bg-info me-2 mb-2', style={"fontSize": "0.8rem"}),
                            style={"display": "inline-block"}
                        )
                        for fw in frameworks
                    ]) if frameworks else html.Div(
                        html.Small("No frameworks detected.", className="text-muted"),
                        className="mb-2"
                    ),
                ], width=4),

                dbc.Col([
                    dcc.Graph(
                        figure=helpers.create_language_bar(profile_data.get('Language Percentages', {})),
                        config={'displayModeBar': False}
                    )
                ], width=8),
            ])
        ]),
        className="mb-4 shadow-sm"
    )