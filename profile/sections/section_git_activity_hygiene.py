from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    rows = [
        {
            "risk": "Single Developer Risk",
            "status": risk_badge(profile_data['Single Developer %'], (50, 75)),
            "details": f"{profile_data['Single Developer %']}% commits from 1 dev"
        },
        {
            "risk": "Repository Bloat Risk",
            "status": risk_badge(profile_data['Repo Size per File (MB)'], (0.5, 1.0), reverse=True),
            "details": f"{profile_data['Repo Size per File (MB)']:.2f} MB per file"
        },
        {
            "risk": "Code Growth Health",
            "status": risk_badge(profile_data['Commits-to-Files Ratio'], (0.5, 1.0)),
            "details": f"{profile_data['Commits-to-Files Ratio']:.1f} commits per file"
        },
        {
            "risk": "Dormancy Risk",
            "status": risk_badge(profile_data['Days Since Last Commit'], (90, 180), reverse=True),
            "details": f"{profile_data['Days Since Last Commit']} days since last commit"
        }
    ]

    table_header = [
        html.Thead(html.Tr([
            html.Th("Risk Factor"),
            html.Th("Status"),
            html.Th("Details"),
        ]))
    ]

    table_body = [
        html.Tbody([
            html.Tr([
                html.Td(row["risk"]),
                html.Td(row["status"]),
                html.Td(row["details"]),
            ]) for row in rows
        ])
    ]

    return dbc.Card(
        dbc.CardBody([
            html.H4('Repository Activity & Hygiene', className='card-title mb-4'),
            dbc.Table(
                children=table_header + table_body,
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
                className="table-striped table-bordered",
            )
        ]),
        className="mb-4 shadow-sm"
    )

def risk_badge(value, thresholds=(50, 75), reverse=False):
    """Helper to return a Bootstrap badge for risk levels."""
    if reverse:
        if value < thresholds[0]:
            color = "danger"
            label = "High"
        elif value < thresholds[1]:
            color = "warning"
            label = "Moderate"
        else:
            color = "success"
            label = "Good"
    else:
        if value > thresholds[1]:
            color = "success"
            label = "Good"
        elif value > thresholds[0]:
            color = "warning"
            label = "Moderate"
        else:
            color = "danger"
            label = "High"

    return dbc.Badge(label, color=color, className="me-1", pill=True)