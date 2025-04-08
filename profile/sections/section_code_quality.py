from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    # Safely extract values with defaults
    lines_of_code = profile_data.get('Lines of Code', 0)
    comment_lines = profile_data.get('Comment Lines', 0)
    blank_lines = profile_data.get('Blank Lines', 0)
    size_label = profile_data.get('Classification Label', "not detected")
    avg_ccn_value = profile_data.get('Avg Cyclomatic Complexity', 0)
    total_ccn_value = profile_data.get('Total Cyclomatic Complexity', 0)
    total_functions = profile_data.get('Total Functions', 0)

    # Correct comment density calculation (using only CLOC metrics)
    if lines_of_code + comment_lines > 0:
        comment_density = (comment_lines / (lines_of_code + comment_lines)) * 100
    else:
        comment_density = 0

    # Correct blank line density (still using CLOC)
    if lines_of_code + comment_lines + blank_lines > 0:
        blank_line_ratio = (blank_lines / (lines_of_code + comment_lines + blank_lines)) * 100
    else:
        blank_line_ratio = 0

    # Size classification coloring
    if size_label.lower() in ['tiny', 'small']:
        size_color = "success"
    elif size_label.lower() in ['medium', 'non-code']:
        size_color = "warning"
    else:
        size_color = "danger"

    # Metric color coding
    avg_ccn_color = "success" if avg_ccn_value < 4 else "warning" if avg_ccn_value <= 6 else "danger"
    total_ccn_color = "success" if total_ccn_value < 1500 else "warning" if total_ccn_value <= 3000 else "danger"
    comment_color = "success" if comment_density >= 15 else "warning" if comment_density >= 8 else "danger"
    blank_color = "success" if blank_line_ratio < 10 else "warning" if blank_line_ratio <= 20 else "danger"
    function_color = "success" if total_functions < 500 else "warning" if total_functions <= 2000 else "danger"

    return dbc.Card(
        dbc.CardBody([
            html.H4('Code Metrics Overview', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H6('Size Rating', className='text-muted mb-1'),
                        html.Span(
                            size_label,
                            className=f"badge bg-{size_color}",
                            style={"fontSize": "1rem", "padding": "6px"}
                        ),
                    ], className="mb-4"),

                    html.Div([
                        html.H6('Blank Line Ratio', className='text-muted mb-1'),
                        html.Span(
                            f"{blank_line_ratio:.1f}%",
                            className=f"badge bg-{blank_color}",
                            style={"fontSize": "1rem", "padding": "6px"}
                        ),
                    ], className="mb-4"),
                ], width=12, md=4),

                dbc.Col([
                    html.Div([
                        html.H6('Avg Cyclomatic Complexity', className='text-muted mb-1'),
                        html.Span(
                            f"{avg_ccn_value:.1f}",
                            className=f"badge bg-{avg_ccn_color}",
                            style={"fontSize": "1rem", "padding": "6px"}
                        ),
                    ], className="mb-4"),

                    html.Div([
                        html.H6('Total Cyclomatic Complexity', className='text-muted mb-1'),
                        html.Span(
                            f"{total_ccn_value:,}",
                            className=f"badge bg-{total_ccn_color}",
                            style={"fontSize": "1rem", "padding": "6px"}
                        ),
                    ], className="mb-4"),
                ], width=12, md=4),

                dbc.Col([
                    html.Div([
                        html.H6('Comment Density', className='text-muted mb-1'),
                        html.Span(
                            f"{comment_density:.1f}%",
                            className=f"badge bg-{comment_color}",
                            style={"fontSize": "1rem", "padding": "6px"}
                        ),
                    ], className="mb-4"),

                    html.Div([
                        html.H6('Function Count', className='text-muted mb-1'),
                        html.Span(
                            f"{total_functions:,}",
                            className=f"badge bg-{function_color}",
                            style={"fontSize": "1rem", "padding": "6px"}
                        ),
                    ], className="mb-4"),
                ], width=12, md=4),
            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )
