from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    return dbc.Card(
        dbc.CardBody([
            html.H4('Code Quality', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.H6('Avg Cyclomatic Complexity', className='text-muted'),
                    dbc.Progress(
                        value=min(profile_data['Cyclomatic Complexity Avg'] * 10, 100),
                        color="info",
                        style={"height": "20px"},
                        striped=True,
                        animated=True,
                        className="mt-2"
                    ),
                    html.Small(
                        f"{profile_data['Cyclomatic Complexity Avg']:.1f} (lower is better)",
                        className="text-muted d-block text-center mt-2",
                        style={"fontSize": "0.7rem"}
                    )
                ], width=6),

                dbc.Col([
                    html.H6('Max Cyclomatic Complexity', className='text-muted'),
                    html.Div([
                        html.Span(
                            f"{profile_data['Cyclomatic Complexity Max']}",
                            className=f"badge {'bg-danger' if profile_data['Cyclomatic Complexity Max'] > 10 else 'bg-warning' if profile_data['Cyclomatic Complexity Max'] > 5 else 'bg-success'}",
                            style={"fontSize": "1.2rem", "padding": "8px"}
                        ),
                        html.Small(
                            "Highest complexity function",
                            className="text-muted d-block text-center mt-2",
                            style={"fontSize": "0.7rem"}
                        )
                    ], className="text-center")
                ], width=6),
            ], className="g-4 mb-4"),

            dbc.Row([
                dbc.Col([
                    html.H6('Comment Density', className='text-muted'),
                    dbc.Progress(
                        value=profile_data['Comment Density'],
                        color="success" if profile_data['Comment Density'] > 10 else "warning",
                        style={"height": "20px"},
                        striped=True,
                        animated=True,
                        className="mt-2"
                    ),
                    html.Small(
                        f"{profile_data['Comment Density']}% of lines are comments",
                        className="text-muted d-block text-center mt-2",
                        style={"fontSize": "0.7rem"}
                    )
                ], width=6),

                dbc.Col([
                    html.H6('Monolith Risk', className='text-muted'),
                    html.Div([
                        html.Span(
                            profile_data['Monolith Risk'],
                            className=f"badge {'bg-success' if profile_data['Monolith Risk'] == 'Low' else 'bg-warning' if profile_data['Monolith Risk'] == 'Medium' else 'bg-danger'}",
                            style={"fontSize": "1.2rem", "padding": "8px"}
                        ),
                        html.Small(
                            "Based on repo structure",
                            className="text-muted d-block text-center mt-2",
                            style={"fontSize": "0.7rem"}
                        )
                    ], className="text-center")
                ], width=6),
            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )