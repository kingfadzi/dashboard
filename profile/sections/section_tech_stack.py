from dash import html, dcc
import dash_bootstrap_components as dbc
import profile.helpers as helpers


def render(profile_data):
    build_envs = profile_data.get("Build Environment", [])
    frameworks = profile_data.get("Frameworks", [])
    iac_frameworks = profile_data.get("IaC Frameworks", [])

    # === Build Tool Table Rows ===
    build_tool_rows = []
    if build_envs:
        header = html.Thead(html.Tr([
            html.Th("Build Tool"),
            html.Th("Variant"),
            html.Th("Tool Version"),
            html.Th("Runtime Version")
        ]))

        body = html.Tbody([
            html.Tr([
                html.Td(env.get("Build Tool", "-")),
                html.Td(env.get("Variant", "-")),
                html.Td(env.get("Tool Version", "-")),
                html.Td(env.get("Runtime Version", "-")),
            ])
            for env in build_envs
        ])

        build_tool_table = dbc.Table([header, body], bordered=True, hover=True, size="sm", responsive=True)
    else:
        build_tool_table = html.Small("No build environments detected.", className="text-muted")

    return dbc.Card(
        dbc.CardBody([
            html.H4('Technology Stack', className='card-title mb-4'),

            # === Build Tools & Runtimes Table ===
            html.Div([
                html.Small("Build Tools & Runtimes", className="text-muted d-block mb-2"),
                build_tool_table
            ], style={
                "marginBottom": "2rem",
                "padding": "1rem",
                "borderLeft": "4px solid #5dade2",
                "backgroundColor": "#f8f9fa",
                "borderRadius": "6px"
            }),

            # === STACKED TECH LAYERS ===
            html.Div([
                # Languages Layer
                html.Div([
                    html.Small("Languages", className="text-muted d-block mb-1"),
                    dcc.Graph(
                        figure=helpers.create_language_bar(profile_data.get('Language Percentages', {})),
                        config={'displayModeBar': False}
                    )
                ], style={
                    "marginBottom": "2rem",
                    "padding": "1rem",
                    "borderLeft": "4px solid #9b59b6",
                    "backgroundColor": "#fafafa",
                    "borderRadius": "6px"
                }),

                # Dev Frameworks Layer
                html.Div([
                    html.Small("Dev Frameworks", className="text-muted d-block mb-2"),
                    html.Div(
                        [html.Span(fw, className='badge me-2 mb-2', style={
                            "fontSize": "0.8rem",
                            "backgroundColor": "#9b59b6",
                            "color": "white"
                        }) for fw in frameworks]
                        if frameworks else html.Small('No dev frameworks detected.', className="text-muted")
                    )
                ], style={
                    "marginBottom": "2rem",
                    "padding": "1rem",
                    "borderLeft": "4px solid #7d3c98",
                    "backgroundColor": "#f9f9f9",
                    "borderRadius": "6px"
                }),

                # IaC Frameworks Layer
                html.Div([
                    html.Small("Infrastructure-as-Code", className="text-muted d-block mb-2"),
                    html.Div(
                        [html.Span(fw, style={
                            "display": "inline-block",
                            "padding": "4px 10px",
                            "margin": "4px 6px 0 0",
                            "backgroundColor": "#e3f2fd",
                            "borderRadius": "20px",
                            "fontSize": "0.75rem",
                            "fontWeight": "500",
                            "color": "#0d47a1",
                            "border": "1px solid #90caf9"
                        }) for fw in iac_frameworks]
                        if iac_frameworks else html.Small('No IaC frameworks detected.', className="text-muted")
                    )
                ], style={
                    "padding": "1rem",
                    "borderLeft": "4px solid #1e88e5",
                    "backgroundColor": "#f0f8ff",
                    "borderRadius": "6px"
                })
            ])
        ]),
        className="mb-4 shadow-sm"
    )
