from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

def render(profile_data):
    vulnerabilities = profile_data.get('Vulnerabilities', [])

    if not vulnerabilities:
        return dbc.Card(
            dbc.CardBody([
                html.H4('Vulnerability Overview', className='card-title mb-4'),
                html.P('No vulnerabilities found.', className='text-muted')
            ]),
            className="mb-4 shadow-sm"
        )

    # Mapping severities to Bootstrap colors
    severity_colors = {
        'Critical': 'danger',
        'High': 'warning',
        'Medium': 'info',
        'Low': 'secondary'
    }

    def severity_badge(severity):
        color = severity_colors.get(severity, 'secondary')
        return dbc.Badge(severity, color=color, pill=True)

    def source_badge(source):
        if source == 'G':
            return dbc.Badge("G", color="primary", pill=True)
        elif source == 'T':
            return dbc.Badge("T", color="info", pill=True)
        else:
            return html.Span('')

    table_rows = []
    for vuln in vulnerabilities:
        table_rows.append({
            'package': vuln['package'],
            'version': vuln['version'],
            'severity': severity_badge(vuln['severity']),
            'fix_version': vuln['fix_version'] if vuln['fix_version'] else '-',
            'source': source_badge(vuln['source']),
        })

    return dbc.Card(
        dbc.CardBody([
            html.H4('Vulnerability Overview', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Table(
                            # Table header
                            [html.Thead(html.Tr([
                                html.Th("Package"),
                                html.Th("Version"),
                                html.Th("Severity"),
                                html.Th("Fix Version"),
                                html.Th("Source"),
                            ]))] +

                            # Table body
                            [html.Tbody([
                                html.Tr([
                                    html.Td(row['package']),
                                    html.Td(row['version']),
                                    html.Td(row['severity']),
                                    html.Td(row['fix_version']),
                                    html.Td(row['source']),
                                ]) for row in table_rows
                            ])],
                            bordered=True,
                            hover=True,
                            responsive=True,
                            size="sm",
                            className="table-striped table-bordered",
                        )
                    ])
                ])
            ])
        ]),
        className="mb-4 shadow-sm"
    )