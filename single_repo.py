import dash
from dash import Dash, html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import datetime

# Set Plotly theme
pio.templates.default = "plotly_white"

# Initialize Dash app
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# Sample data (replace with actual extracted profile data)
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
    'Main Language': 'Python',
    'Other Languages': ['HTML', 'Shell'],
    'Frameworks': ['Flask', 'Jinja2'],
    'Build Tool': 'Poetry',
    'Runtime Version': 'Python 3.9',
    'Language Percentages': {
        'Python': 85,
        'HTML': 10,
        'Shell': 5,
    },
    'Dockerfile': True,
    'CI/CD Present': True,
    'Cloud Native Score': 65,
    'Health Scores': {
        'Code Quality': 80,
        'Security': 40,
        'Modernization': 60,
        'IaC Readiness': 50,
    },
    'Cyclomatic Complexity Avg': 3.5,
    'Cyclomatic Complexity Max': 12,
    'Comment Density': 12,
    'Monolith Risk': 'Low',
    'Dependencies': [
        {'Name': 'Flask', 'Version': '1.0', 'Age (Years)': 5},
        {'Name': 'Werkzeug', 'Version': '0.16.1', 'Age (Years)': 4}
    ],
    'Outdated Dependencies %': 50,
    'Vulnerabilities': [
        {'CVE': 'GHSA-vc8w-jr9v-vj7f', 'Severity': 'Critical', 'Description': 'Example vulnerability description.'},
    ],
    'Critical Vuln Count': 1,
    'Single Developer Risk': False,
    'DevOps Best Practices': True,
    'Commits Last 12 Months': [5, 10, 8, 15, 9, 12, 6, 14, 11, 7, 13, 10]
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

# Language pie chart
def create_language_pie(language_data):
    labels = list(language_data.keys())
    values = list(language_data.values())
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title='Language Distribution')
    return fig

# Commit activity sparkline
def create_commit_sparkline(commits):
    months = pd.date_range(end=datetime.date.today(), periods=12, freq='M').strftime('%b').tolist()
    fig = go.Figure(go.Scatter(x=months, y=commits, mode='lines+markers'))
    fig.update_layout(title='Commits in Last 12 Months', height=250)
    return fig

# App layout
app.layout = html.Div([
    html.H2(f"{profile_data['Repo ID']} Repository Profile"),
    
    html.Div([
        html.Span(f"Status: {profile_data['Status']}", 
                 className='badge bg-success' if profile_data['Status'] == 'ACTIVE' else 'badge bg-secondary'),
        html.Span('Security Risk', className='badge bg-danger') if profile_data['Security Risk'] else None,
        html.Span('EOL Risk', className='badge bg-warning') if profile_data['EOL Risk'] else None,
        html.Span('Tech Debt Risk', className='badge bg-info') if profile_data['Tech Debt Risk'] else None,
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
    
    html.H4('Technology Stack'),
    html.Div([
        html.P(f"Main Language: {profile_data['Main Language']}", style={'fontWeight': 'bold'}),
        html.P("Other Languages: ", style={'fontWeight': 'bold'}),
        *[html.Span(lang, className='badge bg-secondary', style={'marginRight': '5px'}) for lang in profile_data['Other Languages']],
        html.P("Frameworks: ", style={'fontWeight': 'bold', 'marginTop': '10px'}),
        *[html.Span(fw, className='badge bg-info', style={'marginRight': '5px'}) for fw in profile_data['Frameworks']],
        html.P(f"Build Tool: {profile_data['Build Tool']}", style={'marginTop': '10px'}),
        html.P(f"Runtime: {profile_data['Runtime Version']}", style={'marginBottom': '20px'}),
        dcc.Graph(figure=create_language_pie(profile_data['Language Percentages']))
    ], className='mb-4'),
    
    html.H4('Modernization Readiness'),
    html.P(f"Dockerfile Present: {'Yes' if profile_data['Dockerfile'] else 'No'}"),
    html.P(f"CI/CD Pipeline Present: {'Yes' if profile_data['CI/CD Present'] else 'No'}"),
    html.P(f"Cloud Native Score: {profile_data['Cloud Native Score']}%"),
    
    html.H4('Code Quality'),
    html.P(f"Average Cyclomatic Complexity: {profile_data['Cyclomatic Complexity Avg']}", style={'marginBottom': '5px'}),
    html.P(f"Max Cyclomatic Complexity: {profile_data['Cyclomatic Complexity Max']}", style={'marginBottom': '5px'}),
    html.P(f"Comment Density: {profile_data['Comment Density']}%", style={'marginBottom': '5px'}),
    html.P(f"Monolith Risk: {profile_data['Monolith Risk']}"),
    
    html.H4('Dependency Health'),
    dash_table.DataTable(
        data=profile_data['Dependencies'],
        columns=[{'name': i, 'id': i} for i in ['Name', 'Version', 'Age (Years)']],
        style_table={'overflowX': 'auto'}
    ),
    html.P(f"Outdated Dependencies: {profile_data['Outdated Dependencies %']}%", style={'marginTop': '10px'}),
    
    html.H4('Security Posture'),
    dash_table.DataTable(
        data=profile_data['Vulnerabilities'],
        columns=[{'name': i, 'id': i} for i in ['CVE', 'Severity', 'Description']],
        style_table={'overflowX': 'auto'}
    ),
    html.P(f"Critical Vulnerability Count: {profile_data['Critical Vuln Count']}", style={'marginTop': '10px'}),
    
    html.H4('Compliance Metrics'),
    html.P(f"Single Developer Risk: {'Yes' if profile_data['Single Developer Risk'] else 'No'}"),
    html.P(f"DevOps Best Practices Followed: {'Yes' if profile_data['DevOps Best Practices'] else 'No'}"),
    
    html.H4('Recent Activity'),
    dcc.Graph(figure=create_commit_sparkline(profile_data['Commits Last 12 Months'])),
    
    html.H4('Health Overview'),
    dcc.Graph(figure=create_health_chart(profile_data['Health Scores'])),
    
], style={'padding': '20px'})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)