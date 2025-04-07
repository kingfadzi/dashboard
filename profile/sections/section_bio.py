import dash_bootstrap_components as dbc
from dash import html

def render(profile_data):
    repo_name = profile_data.get("Repo Name", "Unknown")
    clone_url = profile_data.get("Clone URL", "Unknown")
    department_appid = profile_data.get("Department AppID", "Unknown")
    product_owner = profile_data.get("Product Owner", "Unknown")
    investment_status = profile_data.get("Investment Status", "Unknown")

    return dbc.Card(
        dbc.CardBody([
            html.H4("Repository Bio", className="card-title mb-4"),
            html.Div([
                html.H6("Repo Name", className="text-muted"),
                html.P(repo_name, style={"fontWeight": "bold"})
            ], className="mb-3"),
            html.Div([
                html.H6("Repository URL", className="text-muted"),
                html.A(clone_url, href=clone_url, target="_blank", style={"fontWeight": "bold"})
                if clone_url != "Unknown" else
                html.Span("Unknown", style={"fontWeight": "bold"})
            ], className="mb-3"),
            html.Div([
                html.H6("Department AppID", className="text-muted"),
                html.P(department_appid, style={"fontWeight": "bold"})
            ], className="mb-3"),
            html.Div([
                html.H6("Product Owner", className="text-muted"),
                html.P(product_owner, style={"fontWeight": "bold"})
            ], className="mb-3"),
            html.Div([
                html.H6("Investment Status", className="text-muted"),
                html.P(investment_status, style={"fontWeight": "bold"})
            ], className="mb-3"),
        ]),
        className="mb-4 shadow-sm"
    )