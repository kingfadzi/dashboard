import dash_bootstrap_components as dbc
from dash import html

def render(profile_data):
    repo_name = profile_data.get("Repo ID", "Unknown")
    browse_url = profile_data.get("Browse URL", "#")
    vcs_hostname = profile_data.get("VCS Hostname", "Unknown")
    last_updated = profile_data.get("Last Updated", "Unknown")

    fields = {
        "App ID": profile_data.get("Department AppID", "Unknown"),
        "Department": profile_data.get("Department", "Unknown"),
        "Team": profile_data.get("Team", "Unknown"),
        "Product Owner": profile_data.get("Product Owner", "Unknown"),
        "VCS Hostname": vcs_hostname,
        "Repository URL": html.A(
            browse_url,
            href=browse_url,
            target="_blank",
            style={"textDecoration": "none", "color": "#0d6efd", "fontSize": "0.85rem"}
        ),
        "Last Updated": last_updated,
    }

    investment_status = profile_data.get("Investment Status", "Unknown")
    investment_color = "success" if investment_status.lower() == "invest" else "warning"

    table_rows = []
    for label, value in fields.items():
        table_rows.append(
            html.Tr([
                html.Td(label, style={"fontWeight": "bold", "fontSize": "0.85rem", "width": "35%"}),
                html.Td(value if isinstance(value, html.A) else str(value), style={"fontSize": "0.85rem"}),
            ])
        )

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