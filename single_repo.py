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
    'Tech Debt Risk': True,
    'Repo Size (MB)': 25,
    'File Count': 929,
    'Lines of Code': 106417,
    'Contributors': 149,
    'Repo Age (Years)': 10,
    'Last Commit Date': '2024-12-27',
    'Activity Status': 'ACTIVE',
    'Active Branch Count': 1,
    'Health Scores': {
        'Code Quality': 80,
        'Security': 40,
        'Modernization': 60,
        'IaC Readiness': 50,
    },
    'Vulnerabilities': [
        {'CVE': 'GHSA-vc8w-jr9v-vj7f', 'Severity': 'Critical', 'Description': 'Example vulnerability description.'},
    ],
    'Dependencies': [
        {'Name': 'Flask', 'Version': '1.0'},
        {'Name': 'Werkzeug', 'Version': '0.16.1'},
    ],
    'Build Info': {
        'Build Tool': 'Poetry',
        'Runtime Version': 'Python 3.9'
    },
    'IaC Details': {
        'Dockerfile': True,
        'Terraform': False,
        'Kubernetes': False
    }
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
        html.Span('Tech Debt Risk', className='badge bg-info') if profile_data.get('Tech Debt Risk') else None,
    ], style={'display': 'flex', 'gap': '10px', 'marginBottom': '20px'}),
    
    dbc.CardGroup([
        dbc.Card(dbc.CardBody([html.H5('Repo Size (MB)'), html.P(profile_data['Repo Size (MB)'])])),
        dbc.Card(dbc.CardBody([html.H5('Files'), html.P(profile_data['File Count'])])),
        dbc.Card(dbc.CardBody([html.H5('Lines of Code'), html.P(profile_data['Lines of Code'])])),
        dbc.Card(dbc.CardBody([html.H5('Contributors'), html.P(profile_data['Contributors'])])),
        dbc.Card(dbc.CardBody([html.H5('Active Branches'), html.P(profile_data['Active Branch Count'])])),
        dbc.Card(dbc.CardBody([html.H5('Repo Age'), html.P(f"{profile_data['Repo Age (Years)']} years")])),
        dbc.Card(dbc.CardBody([html.H5('Last Commit Date'), html.P(profile_data['Last Commit Date'])])),
        dbc.Card(dbc.CardBody([html.H5('Activity Status'), html.P(profile_data['Activity Status'])])),
    ], className='mb-4'),
    
    dcc.Graph(figure=create_health_chart(profile_data['Health Scores'])),
    
    dbc.Alert("Critical vulnerabilities detected.", color='danger') if profile_data['Security Risk'] else None,
    
    dbc.Button("Show Full Details", id="collapse-button", className="mb-3", color="primary"),
    dbc.Collapse(
        dbc.Card(dbc.CardBody([
            dcc.Tabs([
                dcc.Tab(label='Dependencies', children=[
                    dash_table.DataTable(
                        data=profile_data['Dependencies'],
                        columns=[{'name': i, 'id': i} for i in ['Name', 'Version']],
                        style_table={'overflowX': 'auto'}
                    )
                ]),
                dcc.Tab(label='Vulnerabilities', children=[
                    dash_table.DataTable(
                        data=profile_data['Vulnerabilities'],
                        columns=[{'name': i, 'id': i} for i in ['CVE', 'Severity', 'Description']],
                        style_table={'overflowX': 'auto'}
                    )
                ]),
                dcc.Tab(label='Build Info', children=[
                    html.P(f"Build Tool: {profile_data['Build Info']['Build Tool']}"),
                    html.P(f"Runtime Version: {profile_data['Build Info']['Runtime Version']}")
                ]),
                dcc.Tab(label='IaC Details', children=[
                    html.P(f"Dockerfile: {'Present' if profile_data['IaC Details']['Dockerfile'] else 'Missing'}"),
                    html.P(f"Terraform: {'Present' if profile_data['IaC Details']['Terraform'] else 'Missing'}"),
                    html.P(f"Kubernetes: {'Present' if profile_data['IaC Details']['Kubernetes'] else 'Missing'}")
                ]),
            ])
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)