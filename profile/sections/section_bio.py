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
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H2(repo_name, className="mb-2", style={"fontWeight": "bold"}),
                        html.A(
                            "View Repository",
                            href=clone_url if clone_url != "Unknown" else "#",
                            target="_blank",
                            className="btn btn-primary btn-sm mb-3",
                            style={"fontSize": "0.8rem"}
                        ),
                        html.Div([
                            dbc.Badge(f"App ID: {department_appid}", color="info", className="me-2 mb-2", pill=True),
                            dbc.Badge(f"Product Owner: {product_owner}", color="secondary", className="me-2 mb-2", pill=True),
                            dbc.Badge(f"Investment Status: {investment_status}", color="success" if investment_status.lower() == "active" else "warning", className="me-2 mb-2", pill=True),
                        ], style={"fontSize": "0.85rem"})
                    ])
                ], width=12, lg=8),

            ], align="center"),
        ]),
        className="mb-4 shadow-sm"
    )