from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    # Helper for warning badges
    def warning_badge(show):
        if show:
            return html.Span("⚠️", style={"marginLeft": "5px", "fontSize": "1.2rem"})
        return None

    return dbc.Card(
        dbc.CardBody([
            html.H4('Code Metrics', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.H6('Lines of Code (NLOC)', className='text-muted'),
                    html.Div([
                        html.H4(f"{profile_data['Total NLOC']:,}", className="text-center mb-3"),
                        dbc.Tooltip("Non-blank, non-comment lines of code (from CLOC)", target="nloc", placement="top"),
                    ], id="nloc"),

                    html.H6('Blank Lines', className='text-muted'),
                    html.Div([
                        html.H5(f"{profile_data['Blank Lines']:,}", className="text-center mb-3"),
                        dbc.Tooltip("Blank or empty lines (from CLOC)", target="blank-lines", placement="top"),
                    ], id="blank-lines"),

                    html.H6('Comment Lines', className='text-muted'),
                    html.Div([
                        html.H5(f"{profile_data['Comment Lines']:,}", className="text-center"),
                        dbc.Tooltip("Lines containing only comments (from CLOC)", target="comment-lines", placement="top"),
                    ], id="comment-lines"),
                ], width=12, md=4),

                dbc.Col([
                    html.H6('Avg Cyclomatic Complexity', className='text-muted'),
                    dbc.Progress(
                        value=min(profile_data['Avg Cyclomatic Complexity'] * 10, 100),
                        color="info" if profile_data['Avg Cyclomatic Complexity'] <= 5 else "danger",
                        style={"height": "20px"},
                        striped=True,
                        animated=True,
                        className="mb-3 mt-2"
                    ),
                    html.Small(
                        html.Span([
                            f"{profile_data['Avg Cyclomatic Complexity']:.1f} (lower is better)",
                            warning_badge(profile_data['Avg Cyclomatic Complexity'] > 5)
                        ]),
                        className="text-muted d-block text-center mb-4",
                        style={"fontSize": "0.7rem"}
                    ),

                    html.H6('Total Cyclomatic Complexity', className='text-muted'),
                    html.Div([
                        html.H5([
                            f"{profile_data['Total Cyclomatic Complexity']:,}",
                            warning_badge(profile_data['Total Cyclomatic Complexity'] > 3000)
                        ], className="text-center"),
                        dbc.Tooltip("Sum of CCN across all functions (from Lizard)", target="total-ccn", placement="top"),
                    ], id="total-ccn")
                ], width=12, md=4),

                dbc.Col([
                    html.H6('Total Tokens', className='text-muted'),
                    html.Div([
                        html.H5(f"{profile_data['Total Tokens']:,}", className="text-center mb-4"),
                        dbc.Tooltip("Sum of parsed code tokens (from Lizard)", target="total-tokens", placement="top"),
                    ], id="total-tokens"),

                    html.H6('Total Functions', className='text-muted'),
                    html.Div([
                        html.H5([
                            f"{profile_data['Total Functions']:,}",
                            warning_badge(profile_data['Total Functions'] > 2000)
                        ], className="text-center"),
                        dbc.Tooltip("Total number of functions/methods detected", target="total-funcs", placement="top"),
                    ], id="total-funcs"),
                ], width=12, md=4),
            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )