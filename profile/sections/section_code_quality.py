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

    # Size Rating Badge
    size_label = profile_data['Classification Label']
    if size_label.lower() in ['tiny', 'small']:
        size_color = "success"
    elif size_label.lower() in ['medium', 'non-code']:
        size_color = "warning"
    else:
        size_color = "danger"

    # Cyclomatic Complexity Badge
    avg_ccn_label = classify_avg_ccn(profile_data['Avg Cyclomatic Complexity'])
    avg_ccn_color = "success" if avg_ccn_label == "Good" else "warning" if avg_ccn_label == "Moderate" else "danger"

    # Total CCN Badge
    total_ccn_label = classify_total_ccn(profile_data['Total Cyclomatic Complexity'])
    total_ccn_color = "success" if total_ccn_label == "Low Risk" else "warning" if total_ccn_label == "Medium Risk" else "danger"

    # Comment Quality Badge
    comment_quality_label = classify_comment_quality(comment_ratio)
    comment_quality_color = "success" if comment_quality_label == "Excellent" else "warning" if comment_quality_label == "Moderate" else "danger"

    # Function Density Badge
    function_density_label = classify_function_density(profile_data['Total Functions'])
    function_density_color = "success" if function_density_label == "Small Codebase" else "warning" if function_density_label == "Medium Codebase" else "danger"

    return dbc.Card(
        dbc.CardBody([
            html.H4('Code Metrics Overview', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.H6('Size Rating', className='text-muted'),
                    html.Div([
                        html.Span(size_label, className=f"badge bg-{size_color}", style={"fontSize": "1rem", "padding": "6px"}),
                    ], className="text-center mb-4"),

                    html.H6('Blank Lines', className='text-muted'),
                    html.Div([
                        html.H5(f"{profile_data['Blank Lines']:,}", className="text-center"),
                        dbc.Tooltip("Blank or empty lines from CLOC", target="blank-lines", placement="top"),
                    ], id="blank-lines"),
                ], width=12, md=4),

                dbc.Col([
                    html.H6('Complexity Level', className='text-muted'),
                    html.Div([
                        html.Span(avg_ccn_label, className=f"badge bg-{avg_ccn_color}", style={"fontSize": "1rem", "padding": "6px"}),
                    ], className="text-center mb-4"),

                    html.H6('Overall Complexity', className='text-muted'),
                    html.Div([
                        html.Span(total_ccn_label, className=f"badge bg-{total_ccn_color}", style={"fontSize": "1rem", "padding": "6px"}),
                        dbc.Tooltip("Sum of all CCN (via Lizard)", target="total-ccn", placement="top"),
                    ], id="total-ccn", className="text-center"),
                ], width=12, md=4),

                dbc.Col([
                    html.H6('Comment Quality', className='text-muted'),
                    html.Div([
                        html.Span(comment_quality_label, className=f"badge bg-{comment_quality_color}", style={"fontSize": "1rem", "padding": "6px"}),
                    ], className="text-center mb-4"),

                    html.H6('Function Density', className='text-muted'),
                    html.Div([
                        html.Span(function_density_label, className=f"badge bg-{function_density_color}", style={"fontSize": "1rem", "padding": "6px"}),
                        dbc.Tooltip("Total number of functions (via Lizard)", target="total-funcs", placement="top"),
                    ], id="total-funcs", className="text-center"),
                ], width=12, md=4),
            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )