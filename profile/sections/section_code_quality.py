from dash import html
import dash_bootstrap_components as dbc
from helpers import (
    classify_avg_ccn,
    classify_comment_quality,
    classify_function_density,
    classify_total_ccn,
)

def render(profile_data):
    comment_ratio = (profile_data['Comment Lines'] / profile_data['Total NLOC']) * 100

    # Badge color for Size Rating
    size_label = profile_data['Classification Label']
    if size_label.lower() in ['tiny', 'small']:
        size_badge_color = "success"
    elif size_label.lower() in ['medium', 'non-code']:
        size_badge_color = "warning"
    else:
        size_badge_color = "danger"

    return dbc.Card(
        dbc.CardBody([
            html.H4('Code Metrics Overview', className='card-title mb-4'),

            dbc.Row([
                # Column 1: Size Rating and Blank Lines
                dbc.Col([
                    html.H6('Size Rating', className='text-muted'),
                    html.Div([
                        html.Span(
                            profile_data['Classification Label'],
                            className=f"badge bg-{size_badge_color}",
                            style={"fontSize": "1.0rem", "padding": "8px"}
                        )
                    ], className="text-center mb-3"),

                    html.H6('Blank Lines', className='text-muted'),
                    html.Div([
                        html.H5(f"{profile_data['Blank Lines']:,}", className="text-center"),
                        dbc.Tooltip("Total blank lines detected (via CLOC)", target="blank-lines", placement="top"),
                    ], id="blank-lines")
                ], width=12, md=4),

                # Column 2: Complexity Level and Total CCN
                dbc.Col([
                    html.H6('Complexity Level', className='text-muted'),
                    html.Div([
                        html.H5(
                            classify_avg_ccn(profile_data['Avg Cyclomatic Complexity']),
                            className="text-center mb-3"
                        )
                    ]),
                    
                    html.H6('Overall Complexity', className='text-muted'),
                    html.Div([
                        html.H5(
                            classify_total_ccn(profile_data['Total Cyclomatic Complexity']),
                            className="text-center"
                        ),
                        dbc.Tooltip("Sum of all function complexities (via Lizard)", target="total-ccn", placement="top"),
                    ], id="total-ccn"),
                ], width=12, md=4),

                # Column 3: Comments and Function Density
                dbc.Col([
                    html.H6('Comment Quality', className='text-muted'),
                    html.Div([
                        html.H5(
                            classify_comment_quality(comment_ratio),
                            className="text-center mb-3"
                        )
                    ]),

                    html.H6('Function Density', className='text-muted'),
                    html.Div([
                        html.H5(
                            classify_function_density(profile_data['Total Functions']),
                            className="text-center"
                        ),
                        dbc.Tooltip("Number of functions/methods detected (via Lizard)", target="total-funcs", placement="top"),
                    ], id="total-funcs")
                ], width=12, md=4),
            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )