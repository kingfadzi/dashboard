import dash_bootstrap_components as dbc
from dash import html

def render(profile_data):
    # Fetch values
    repo_name = profile_data.get("Repo Name", "Unknown")
    clone_url = profile_data.get("Clone URL", "#")

    fields = {
        "App ID": profile_data.get("Department AppID", "Unknown"),
        "Department": profile_data.get("Department", "Unknown"),
        "Team": profile_data.get("Team", "Unknown"),
        "Product Owner": profile_data.get("Product Owner", "Unknown"),
    }

    investment_status = profile_data.get("Investment Status", "Unknown")
    investment_color = "success" if investment_status.lower() == "active" else "warning"

    # Build the fields table
    table_rows = []
    for label, value in fields.items():
        table_rows.append(
            html.Tr([
                html.Td(label, style={"fontWeight": "bold", "fontSize": "0.85rem", "width": "35%"}),
                html.Td(value, style={"fontSize": "0.85rem"}),
            ])
        )

    # Add Investment Status separately (with badge)
    table_rows.append(
        html.Tr([
            html.Td("Investment Status", style={"fontWeight": "bold", "fontSize": "0.85rem"}),
            html.Td(
                dbc.Badge(investment_status, color=investment_color, className="p-2", style={"fontSize": "0.75rem"}),
            )
        ])
    )

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

            dbc.Table(
                table_rows,
                bordered=False,
                hover=False,
                size="sm",
                className="table-borderless",
            )
        ]),
        className="mb-4 shadow-sm"
    )