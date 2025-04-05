import dash
from dash import html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# Sample data (replace with your actual extracted profile data)
profile_data = {
    'Repo ID': 'CTFd',
    'Status': 'ACTIVE',
    'Security Risk': True,
    'EOL Risk': False,
    'Repo Size (MB)': 25,
    'File Count': 929,
    'Lines of Code': 106417,
    'Contributors': 149,
    'Repo Age (Years)': 10,
    'Health Scores': {
        'Code Quality': 80,
        'Security': 40,
        'Modernization': 60,
    },
    'Vulnerabilities': [
        {'CVE': 'GHSA-vc8w-jr9v-vj7f', 'Severity': 'Critical'},
    ],
    'Dependencies': []  # Populate if available
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Health overview chart
def create_health_chart(health_scores):
    categories = list(health_scores.keys())
    scores = list(health_scores.values())
    fig = go.Figure(go.Bar(
        x=scores,
        y=categories,
        orientation='h',
        marker_color=['green' if s > 70 else 'orange' if s > 50 else 'red' for s in scores]
    ))
    fig.update_layout(title='Health Overview', xaxis=dict(range=[0, 100]))
    return fig

# App layout
app.layout = html.Div([
    html.H2(f"{profile_data['Repo ID']} Repository Profile"),
    
    html.Div([
        html.Span(
            f"Status: {profile_data['Status']}",
            className='badge bg-success' if profile_data['Status'] == 'ACTIVE' else 'badge bg-secondary'
        ),
        html.Span('Security Risk', className='badge bg-danger') if profile_data['Security Risk'] else None,
        html.Span('EOL Risk', className='badge bg-warning') if profile_data['EOL Risk'] else None,
    ], style={'display': 'flex', 'gap': '10px', 'marginBottom': '20px'}),
    
    dbc.CardGroup([
        dbc.Card(dbc.CardBody([html.H5('Repo Size (MB)'), html.P(profile_data['Repo Size (MB)'])])),
        dbc.Card(dbc.CardBody([html.H5('Files'), html.P(profile_data['File Count'])])),
        dbc.Card(dbc.CardBody([html.H5('Lines of Code'), html.P(profile_data['Lines of Code'])])),
        dbc.Card(dbc.CardBody([html.H5('Contributors'), html.P(profile_data['Contributors'])])),
        dbc.Card(dbc.CardBody([html.H5('Repo Age'), html.P(f"{profile_data['Repo Age (Years)']} years")])),
    ], className='mb-4'),
    
    dcc.Graph(figure=create_health_chart(profile_data['Health Scores'])),
    
    dbc.Alert("Critical vulnerabilities detected.", color='danger') if profile_data['Security Risk'] else None,
    
    dbc.Button("Show Details", id="collapse-button", className="mb-3", color="primary"),
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            html.H5('Dependencies'),
            dash_table.DataTable(
                data=profile_data['Dependencies'],
                columns=[{'name': i, 'id': i} for i in ['Name', 'Version']] if profile_data['Dependencies'] else [],
                style_table={'overflowX': 'auto'}
            ),
            html.H5('Vulnerabilities'),
            dash_table.DataTable(
                data=profile_data['Vulnerabilities'],
                columns=[{'name': i, 'id': i} for i in ['CVE', 'Severity']],
                style_table={'overflowX': 'auto'}
            ),
        ])),
        id="collapse",
    )
])

# Callbacks
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)