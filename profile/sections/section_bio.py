import dash_bootstrap_components as dbc
from dash import html

def render(profile_data):
    repo_name = profile_data.get("Repo Name", "Unknown")
    clone_url = profile_data.get("Clone URL", "#")
    department_appid = profile_data.get("Department AppID", "Unknown")
    product_owner = profile_data.get("Product Owner", "Unknown")
    investment_status = profile_data.get("Investment Status", "Unknown")

    # Color badge only for Investment Status
    investment_color = "success" if investment_status.lower() == "active" else "warning"

    return dbc.Card(
        dbc.CardBody([
            html.H2(repo_name, className="mb-3", style={"fontWeight": "bold"}),

            html.A(
                "View Repository",
                href=clone_url,
                target="_blank",
                className="btn btn-primary btn-sm mb-4",
                style={"fontSize": "0.8rem"}
            ),

            dbc.Row([
                dbc.Col([
                    html.P("App ID", className="text-muted mb-1", style={"fontSize": "0.8rem"}),
                    html.P(department_appid, style={"fontWeight": "500", "fontSize": "1rem"}),
                ], width=4),

                dbc.Col([
                    html.P("Product Owner", className="text-muted mb-1", style={"fontSize": "0.8rem"}),
                    html.P(product_owner, style={"fontWeight": "500", "fontSize": "1rem"}),
                ], width=4),

                dbc.Col([
                    html.P("Investment Status", className="text-muted mb-1", style={"fontSize": "0.8rem"}),
                    dbc.Badge(investment_status, color=investment_color, className="p-2", style={"fontSize": "0.9rem"})
                ], width=4),
            ], className="mb-2"),
        ]),
        className="mb-4 shadow-sm"
    )