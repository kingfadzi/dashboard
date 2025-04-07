from dash import html, dash_table
import dash_bootstrap_components as dbc

def render(profile_data):
    rows = [
        {
            "Risk Factor": "Single Developer Risk",
            "Status": status_badge(profile_data['Single Developer %'], thresholds=(50, 75)),
            "Details": f"{profile_data['Single Developer %']}% commits from 1 dev"
        },
        {
            "Risk Factor": "Repository Bloat Risk",
            "Status": status_badge(profile_data['Repo Size per File (MB)'], thresholds=(0.5, 1.0), reverse=True),
            "Details": f"{profile_data['Repo Size per File (MB)']:.2f} MB per file"
        },
        {
            "Risk Factor": "Code Growth Health",
            "Status": status_badge(profile_data['Commits-to-Files Ratio'], thresholds=(0.5, 1.0)),
            "Details": f"{profile_data['Commits-to-Files Ratio']:.1f} commits per file"
        },
        {
            "Risk Factor": "Dormancy Risk",
            "Status": status_badge(profile_data['Days Since Last Commit'], thresholds=(90, 180), reverse=True),
            "Details": f"{profile_data['Days Since Last Commit']} days since last commit"
        }
    ]

    return dbc.Card(
        dbc.CardBody([
            html.H4('Repository Activity & Hygiene', className='card-title mb-4'),

            dash_table.DataTable(
                columns=[
                    {"name": "Risk Factor", "id": "Risk Factor"},
                    {"name": "Status", "id": "Status", "presentation": "markdown"},
                    {"name": "Details", "id": "Details"},
                ],
                data=rows,
                style_cell={
                    "fontFamily": "system-ui, sans-serif",
                    "fontSize": "0.8rem",
                    "textAlign": "left",
                    "padding": "8px",
                },
                style_table={"overflowX": "auto"},
                style_as_list_view=True,
                style_header={
                    "backgroundColor": "rgb(240,240,240)", 
                    "fontWeight": "bold",
                    "textAlign": "left"
                },
                style_data_conditional=[
                    {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248,248,248)"},
                ],
            )
        ]),
        className="mb-4 shadow-sm"
    )

def status_badge(value, thresholds=(50, 75), reverse=False):
    """Helper to return colored badge-style label based on thresholds."""
    if reverse:
        if value < thresholds[0]:
            color, label = "danger", "High"
        elif value < thresholds[1]:
            color, label = "warning", "Moderate"
        else:
            color, label = "success", "Good"
    else:
        if value > thresholds[1]:
            color, label = "success", "Good"
        elif value > thresholds[0]:
            color, label = "warning", "Moderate"
        else:
            color, label = "danger", "High"

    return f"![{label}](https://placehold.co/12x12/{badge_color(color)}/transparent.png) {label}"

def badge_color(level):
    colors = {
        "success": "28a745",  # green
        "warning": "ffc107",  # orange
        "danger": "dc3545",   # red
    }
    return colors.get(level, "6c757d")