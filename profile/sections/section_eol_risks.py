from dash import html
import dash_bootstrap_components as dbc
import datetime

def render(profile_data):
    eol_results = profile_data.get('EOL Results', [])

    if not eol_results:
        return dbc.Card(
            dbc.CardBody([
                html.H4('End of Life Risks', className='card-title mb-4'),
                html.P('No EOL risks detected.', className='text-muted')
            ]),
            className="mb-4 shadow-sm"
        )

    def eol_badge(eol_date_str):
        try:
            eol_date = datetime.datetime.strptime(eol_date_str, '%Y-%m-%d').date()
            today = datetime.date.today()

            if eol_date < today:
                color = "danger"
                label = "EOL Passed"
            elif (eol_date - today).days <= 365:
                color = "warning"
                label = "EOL Soon"
            else:
                color = "success"
                label = "Supported"
        except Exception:
            color = "secondary"
            label = "Unknown"

        return dbc.Badge(label, color=color, className="me-1", pill=True)

    table_header = [
        html.Thead(html.Tr([
            html.Th("Artifact"),
            html.Th("Version"),
            html.Th("EOL Status"),
            html.Th("Latest Release"),
        ]))
    ]

    table_body = [
        html.Tbody([
            html.Tr([
                html.Td(item.get('artifact_name', 'Unknown')),
                html.Td(item.get('artifact_version', '-')),
                html.Td(eol_badge(item.get('eol_date', None))),
                html.Td(item.get('latest_release', '-')),
            ]) for item in eol_results
        ])
    ]

    return dbc.Card(
        dbc.CardBody([
            html.H4('End of Life Risks', className='card-title mb-4'),
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