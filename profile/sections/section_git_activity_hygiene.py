from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    recent_commit_dates = profile_data.get('Recent Commit Dates', [])
    last_updated = profile_data.get('Last Updated', 'Unknown')

    commits_last_90_days = sum(
        1 for date in recent_commit_dates
        if is_within_last_n_days(date, 90)
    )

    rows = [
        {
            "risk": "Single Developer Risk",
            "status": risk_badge(profile_data.get('Single Developer %', 0), (50, 75)),
            "details": f"{profile_data.get('Single Developer %', 0)}% commits from 1 developer"
        },
        {
            "risk": "Repository Bloat Risk",
            "status": risk_badge(profile_data.get('Repo Size (MB)', 0) / max(profile_data.get('File Count', 1), 1), (0.5, 1.0), reverse=True),
            "details": f"{profile_data.get('Repo Size (MB)', 0) / max(profile_data.get('File Count', 1), 1):.2f} MB per file"
        },
        {
            "risk": "Code Growth Health",
            "status": risk_badge(profile_data.get('Total Commits', 0) / max(profile_data.get('File Count', 1), 1), (0.5, 1.0)),
            "details": f"{profile_data.get('Total Commits', 0) / max(profile_data.get('File Count', 1), 1):.1f} commits per file"
        },
        {
            "risk": "Dormancy Risk",
            "status": risk_badge(commits_last_90_days, (5, 10)),
            "details": html.Span([
                f"{commits_last_90_days} commits in last 90 days ",
                html.Small(f"(as of {last_updated.split('T')[0]})", className="text-muted")
            ])
        }
    ]

    table_header = html.Thead(html.Tr([
        html.Th("Risk Factor"),
        html.Th("Status"),
        html.Th("Details"),
    ]))

    table_body = html.Tbody([
        html.Tr([
            html.Td(row["risk"]),
            html.Td(row["status"]),
            html.Td(row["details"]),
        ]) for row in rows
    ])

    return dbc.Card(
        dbc.CardBody([
            html.H4('Repository Activity & Hygiene', className='card-title mb-4'),
            dbc.Table(
                children=[table_header, table_body],
                bordered=True,
                hover=True,
                responsive=True,
                size="sm",
                className="table-striped table-bordered",
            ),
        ]),
        className="mb-4 shadow-sm"
    )

def is_within_last_n_days(date_str, n_days):
    from datetime import datetime, timezone, timedelta
    if not date_str:
        return False
    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        cutoff = datetime.now(timezone.utc) - timedelta(days=n_days)
        return dt >= cutoff
    except Exception:
        return False


def risk_badge(value, thresholds=(50, 75), reverse=False):
    if value is None:
        return "-"
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
