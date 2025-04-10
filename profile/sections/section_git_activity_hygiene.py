from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    recent_commit_dates = profile_data.get('Recent Commit Dates', [])
    last_updated = profile_data.get('Last Updated', 'Unknown')

    # Calculate metrics safely
    total_commits = profile_data.get('Total Commits', 0)
    top_contributor_commits = profile_data.get('Top Contributor Commits', 0)
    file_count = profile_data.get('File Count', 1)
    repo_size_mb = profile_data.get('Repo Size (MB)', 0)

    # Derived metrics
    commits_per_file = total_commits / max(file_count, 1)
    size_per_file = repo_size_mb / max(file_count, 1)
    single_dev_percent = (top_contributor_commits / total_commits) * 100 if total_commits > 0 else 0

    commits_last_90_days = sum(
        1 for date in recent_commit_dates
        if is_within_last_n_days(date, 90)
    )

    rows = [
        {
            "risk": "Single Developer Risk",
            "status": risk_badge(single_dev_percent, thresholds=(50, 75), reverse=True, low_label="High", high_label="Low"),
            "details": f"{single_dev_percent:.1f}% commits from 1 developer"
        },
        {
            "risk": "Repository Bloat Risk",
            "status": risk_badge(size_per_file, thresholds=(0.5, 1.0), reverse=True, low_label="High", high_label="Low"),
            "details": f"{size_per_file:.2f} MB per file"
        },
        {
            "risk": "Code Growth Health",
            "status": risk_badge(commits_per_file, thresholds=(0.5, 1.0), low_label="Low", high_label="High"),
            "details": f"{commits_per_file:.1f} commits per file"
        },
        {
            "risk": "Dormancy Risk",
            "status": risk_badge(commits_last_90_days, thresholds=(5, 10), reverse=False, low_label="High", high_label="Low"),
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

def risk_badge(value, thresholds=(50, 75), reverse=False, low_label="High", high_label="Good"):
    if value is None:
        return "-"

    if reverse:
        if value < thresholds[0]:
            color = "success"
            label = high_label
        elif value < thresholds[1]:
            color = "warning"
            label = "Moderate"
        else:
            color = "danger"
            label = low_label
    else:
        if value > thresholds[1]:
            color = "success"
            label = high_label
        elif value > thresholds[0]:
            color = "warning"
            label = "Moderate"
        else:
            color = "danger"
            label = low_label

    return dbc.Badge(label, color=color, className="me-1", pill=True)
