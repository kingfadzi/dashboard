from dash import html, dcc
import dash_bootstrap_components as dbc
import helpers

def render(profile_data):
    build_tool = profile_data.get('Build Tool', '-')
    runtime_version = profile_data.get('Runtime Version', '-')
    frameworks = profile_data.get('Frameworks', [])

    return dbc.Card(
        dbc.CardBody([
            html.H4('Technology Stack', className='card-title mb-4'),


            dbc.Row([
                dbc.Col(html.Small('Build Tool:', className='text-muted'), width="auto"),
                dbc.Col(html.Span(build_tool, style={"fontWeight": "bold", "fontSize": "0.9rem"}), width="auto"),
                dbc.Col(html.Small('Runtime Version:', className='text-muted ms-4'), width="auto"),
                dbc.Col(html.Span(runtime_version, style={"fontWeight": "bold", "fontSize": "0.9rem"}), width="auto"),
            ], align="center", className="mb-4"),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=helpers.create_language_bar(profile_data.get('Language Percentages', {})),
                        config={'displayModeBar': False}
                    )
                ], width=8),
                dbc.Col([
                    html.H6('Frameworks', className='text-muted'),
                    html.Div(
                        [html.Span(fw, className='badge bg-info me-2 mb-2', style={"fontSize": "0.8rem"}) for fw in frameworks]
                        if frameworks else html.Small('No frameworks detected.', className="text-muted")
                    )
                ], width=4)
            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )