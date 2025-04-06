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

    # Mapping severities to colors
    severity_colors = {
        'Critical': 'danger',
        'High': 'warning',
        'Medium': 'info',
        'Low': 'secondary'
    }

    def severity_badge(severity):
        color = severity_colors.get(severity, 'secondary')
        return dbc.Badge(severity, color=color, className="me-1", pill=True)

    def source_badge(source):
        if source == 'G':
            return dbc.Badge("G", color="primary", className="me-1", pill=True)
        elif source == 'T':
            return dbc.Badge("T", color="info", className="me-1", pill=True)
        else:
            return html.Span('')

    table_data = []
    for vuln in vulnerabilities:
        table_data.append({
            'package': vuln['package'],
            'version': vuln['version'],
            'severity_badge': severity_badge(vuln['severity']),
            'fix_version': vuln['fix_version'] if vuln['fix_version'] else '-',
            'source_badge': source_badge(vuln['source'])
        })

    columns = [
        {"name": "Package", "id": "package"},
        {"name": "Version", "id": "version"},
        {"name": "Severity", "id": "severity_badge", "presentation": "markdown"},
        {"name": "Fix Version", "id": "fix_version"},
        {"name": "Source", "id": "source_badge", "presentation": "markdown"},
    ]

    return dbc.Card(
        dbc.CardBody([
            html.H4('Vulnerability Overview', className='card-title mb-4'),
            dash_table.DataTable(
                columns=columns,
                data=[{
                    "package": row['package'],
                    "version": row['version'],
                    "severity_badge": str(row['severity_badge']),
                    "fix_version": row['fix_version'],
                    "source_badge": str(row['source_badge'])
                } for row in table_data],
                style_cell={"fontSize": "0.8rem", "padding": "4px", "textAlign": "left"},
                style_table={"overflowX": "auto"},
                style_as_list_view=True,
                style_header={"backgroundColor": "rgb(240,240,240)", "fontWeight": "bold"},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                ],
            )
        ]),
        className="mb-4 shadow-sm"
    )