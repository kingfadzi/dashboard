import dash_bootstrap_components as dbc
from dash import html


def render(profile_data):
    def combine_name_id(name, uid):
        return f"{name} ({uid})" if name and uid and uid != "Unknown" else name or uid or "Unknown"

    def combine_app_id_name(app_id, name):
        # Display application name with App ID in parentheses if both are available
        if name and app_id and name != "Unknown":
            return f"{name} ({app_id})"
        return name or app_id or "Unknown"

    repo_name = profile_data.get("Repo ID", "Unknown")
    vcs_hostname = profile_data.get("VCS Hostname", "Unknown")
    browse_url = profile_data.get("Browse URL", "#")
    investment_status = profile_data.get("House Position", "Unknown")

    status = investment_status.lower()
    investment_color = {
        "invest":  "success",
        "maintain":"info",
        "divest":  "warning",
        "cease":   "danger"
    }.get(status, "secondary")

    short_description = profile_data.get("Short Description", "")

    def info_card(title, fields_dict):
        rows = [
            html.Tr([
                html.Td(label, className="fw-bold", style={"width": "45%", "fontSize": "0.75rem", "padding": "0.25rem"}),
                html.Td(
                    value if isinstance(value, (html.A, dbc.Badge, html.Span, html.Div)) else str(value),
                    style={"fontSize": "0.75rem", "padding": "0.25rem"}
                )
            ]) for label, value in fields_dict.items()
        ]
        return dbc.Card(
            dbc.CardBody([
                html.Small(title, className="text-muted fw-bold d-block mb-2"),
                dbc.Table(html.Tbody(rows), className="table-sm table-borderless mb-0", style={"width": "100%"})
            ]),
            className="h-100 shadow-sm p-2"
        )

    # Build cards with App ID included in the application name
    cards = [
        info_card("Application", {
            "VCS": html.A(
                vcs_hostname,
                href=browse_url,
                target="_blank",
                style={"textDecoration": "none", "fontSize": "0.75rem"}
            ),
            "Name": combine_app_id_name(
                profile_data.get("App ID"),
                profile_data.get("Business Application Name")
            ),
            "App Type": profile_data.get("Application Type", "Unknown"),
            "Architecture": profile_data.get("Architecture Type", "Unknown"),
            "Hosting": profile_data.get("Architecture Hosting", "Unknown"),
        }),
        info_card("Business", {
            "Application": combine_app_id_name(
                profile_data.get("App ID"),
                profile_data.get("Business Application Name")
            ),
            "TC": profile_data.get("Owning Transaction Cycle", "Unknown"),
            "Resilience": profile_data.get("Resilience Category", "Unknown"),
            "Tier": profile_data.get("Application Tier", "Unknown"),
            "Investment": dbc.Badge(
                investment_status,
                color=investment_color,
                className="p-1",
                style={"fontSize": "0.65rem"}
            ),
        }),
        info_card("People / Tech", {
            "Product Owner": combine_name_id(
                profile_data.get("Product Owner"),
                profile_data.get("Product Owner ID")
            ),
            "System Architect": combine_name_id(
                profile_data.get("System Architect"),
                profile_data.get("System Architect ID")
            ),
            "CTO": profile_data.get("CTO", "Unknown"),
            "Business Owner": combine_name_id(
                profile_data.get("Business Owner"),
                profile_data.get("Business Owner ID")
            ),
        })
    ]

    # Short description card
    description_card = dbc.Card(
        dbc.CardBody([
            html.Small("Short Description", className="text-muted fw-bold d-block mb-2"),
            html.Div(
                short_description or "No description available.",
                style={
                    "whiteSpace": "pre-wrap",
                    "backgroundColor": "#f8f9fa",
                    "borderLeft": "4px solid #dee2e6",
                    "padding": "0.75rem",
                    "borderRadius": "4px",
                    "fontSize": "0.75rem"
                }
            )
        ]),
        className="shadow-sm mb-4"
    )

    return html.Div([
        html.H2(repo_name, className="mb-4", style={"fontWeight": "bold", "fontSize": "1.4rem"}),

        # Short description first under heading
        description_card,

        dbc.Row(
            [dbc.Col(card, md=4) for card in cards],
            className="gx-3 gy-3 mb-4"
        ),
    ])
