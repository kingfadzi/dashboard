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
    'Deprecated APIs Found': 3,
    'Hardcoded Secrets Found': 2,
    'Other Modernization Findings': 8,
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
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        textinfo='percent+label',  # show % + language name inside
        insidetextorientation='radial'  # nice radial text
    )])
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),  # remove wasted space
        showlegend=False  # <--- REMOVE LEGEND
    )
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
    
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Repo Size (MB)", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Repo Size (MB)']} MB", className="text-center"),
                            html.Small(f"Files={profile_data['File Count']}", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Lines of Code", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Lines of Code']:,}", className="text-center"),
                            html.Small("All Files", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Contributors", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Contributors']}", className="text-center"),
                            html.Small("Active contributors", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Active Branches", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Active Branch Count']}", className="text-center"),
                            html.Small("Main + Dev", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Repo Age", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(f"{profile_data['Repo Age (Years)']}y", className="text-center"),
                            html.Small(f"Since {profile_data['Last Commit Date'][:4]}", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Activity Status", className="text-center bg-light", style={"fontSize": "0.8rem"}),
                        dbc.CardBody([
                            html.H4(profile_data['Activity Status'], className="text-center"),
                            html.Small("Based on commits", className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                        ])
                    ],
                    className="mb-4"
                )
            ),
        ],
        className="mb-4 mt-2",
        justify="around"
    ),
    
      html.Div([
      dbc.Card(
          dbc.CardBody([
              html.H4('Technology Stack', className='card-title mb-4'),
  
              dbc.Row([
                  dbc.Col([
                      html.H6('Main Language', className='text-muted'),
                      html.Span(profile_data['Main Language'], className='badge bg-primary', style={"fontSize": "0.9rem"}),
                      html.Hr(),
  
                      html.H6('Other Languages', className='text-muted'),
                      html.Div([
                          *[html.Span(lang, className='badge bg-secondary me-2', style={"fontSize": "0.8rem"}) for lang in profile_data['Other Languages']]
                      ]),
                      html.Hr(),
  
                      html.H6('Frameworks', className='text-muted'),
                      html.Div([
                          *[html.Span(fw, className='badge bg-info me-2', style={"fontSize": "0.8rem"}) for fw in profile_data['Frameworks']]
                      ]),
                      html.Hr(),
  
                      html.H6('Build Tool', className='text-muted'),
                      html.P(profile_data['Build Tool'], style={"fontWeight": "bold"}),
  
                      html.H6('Runtime Version', className='text-muted'),
                      html.P(profile_data['Runtime Version'], style={"fontWeight": "bold"}),
                  ], width=6),
  
                  dbc.Col([
                      dcc.Graph(figure=create_language_pie(profile_data['Language Percentages']), config={'displayModeBar': False})
                  ], width=6),
              ])
          ]),
          className="mb-4 shadow-sm"
      )
  ]),
    
    html.Div([
    dbc.Card(
        dbc.CardBody([
            html.H4('Modernization Readiness', className='card-title mb-4'),

            dbc.Row([
                dbc.Col([
                    html.H6('Dockerfile', className='text-muted'),
                    html.Span(
                        "Present" if profile_data['Dockerfile'] else "Missing",
                        className=f"badge {'bg-success' if profile_data['Dockerfile'] else 'bg-danger'}",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('CI/CD Pipeline', className='text-muted'),
                    html.Span(
                        "Present" if profile_data['CI/CD Present'] else "Missing",
                        className=f"badge {'bg-success' if profile_data['CI/CD Present'] else 'bg-danger'}",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),
            ], className="g-3 mb-4"),

            html.H5('Modernization Findings', className='mt-2 mb-3'),

            dbc.Row([
                dbc.Col([
                    html.H6('Deprecated APIs', className='text-muted'),
                    html.Span(
                        f"{profile_data['Deprecated APIs Found']}",
                        className="badge bg-warning",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('Hardcoded Secrets', className='text-muted'),
                    html.Span(
                        f"{profile_data['Hardcoded Secrets Found']}",
                        className="badge bg-danger",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),

                dbc.Col([
                    html.H6('Other Modernization Issues', className='text-muted'),
                    html.Span(
                        f"{profile_data['Other Modernization Findings']}",
                        className="badge bg-info",
                        style={"fontSize": "0.9rem"}
                    )
                ], width=4),
            ], className="g-3")
        ]),
        className="mb-4 shadow-sm"
    )
]),
    
    html.Div([
    dbc.Card(
        dbc.CardBody([
            html.H4('Code Quality', className='card-title mb-4'),

            dbc.Row([
                # Average Cyclomatic Complexity
                dbc.Col([
                    html.H6('Avg Cyclomatic Complexity', className='text-muted'),
                    dbc.Progress(
                        value=min(profile_data['Cyclomatic Complexity Avg'] * 10, 100),
                        color="info",
                        style={"height": "20px"},
                        striped=True,
                        animated=True,
                    ),
                    html.Small(
                        f"{profile_data['Cyclomatic Complexity Avg']:.1f} (lower is better)",
                        className="text-muted d-block text-center mt-2",
                        style={"fontSize": "0.7rem"}
                    )
                ], width=6),

                # Max Cyclomatic Complexity
                dbc.Col([
                    html.H6('Max Cyclomatic Complexity', className='text-muted'),
                    html.Div([
                        html.Span(
                            f"{profile_data['Cyclomatic Complexity Max']}",
                            className=f"badge {'bg-danger' if profile_data['Cyclomatic Complexity Max'] > 10 else 'bg-warning' if profile_data['Cyclomatic Complexity Max'] > 5 else 'bg-success'}",
                            style={"fontSize": "1.2rem", "padding": "8px"}
                        ),
                        html.Small(
                            "in any single function",
                            className="text-muted d-block text-center mt-2",
                            style={"fontSize": "0.7rem"}
                        )
                    ], className="text-center")
                ], width=6),
            ], className="g-4 mb-4"),

            dbc.Row([
                # Comment Density
                dbc.Col([
                    html.H6('Comment Density', className='text-muted'),
                    dbc.Progress(
                        value=profile_data['Comment Density'],
                        color="success" if profile_data['Comment Density'] > 10 else "warning",
                        style={"height": "20px"},
                        striped=True,
                        animated=True,
                    ),
                    html.Small(
                        f"{profile_data['Comment Density']}% of lines are comments",
                        className="text-muted d-block text-center mt-2",
                        style={"fontSize": "0.7rem"}
                    )
                ], width=6),

                # Monolith Risk
                dbc.Col([
                    html.H6('Monolith Risk', className='text-muted'),
                    html.Div([
                        html.Span(
                            profile_data['Monolith Risk'],
                            className=f"badge {'bg-success' if profile_data['Monolith Risk'] == 'Low' else 'bg-warning' if profile_data['Monolith Risk'] == 'Medium' else 'bg-danger'}",
                            style={"fontSize": "1.2rem", "padding": "8px"}
                        ),
                        html.Small(
                            "based on size and structure",
                            className="text-muted d-block text-center mt-2",
                            style={"fontSize": "0.7rem"}
                        )
                    ], className="text-center")
                ], width=6),
            ], className="g-4")
        ]),
        className="mb-4 shadow-sm"
    )
]),
    
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