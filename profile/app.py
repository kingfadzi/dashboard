from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from services.profile_loader import load_profile

# Database connection
DATABASE_URL = "postgresql://postgres:postgres@192.168.1.188:5432/gitlab-usage"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Initialize Dash app
app = Dash(__name__, use_pages=False, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout: Location + page content
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# URL-based callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'search')
)
def render_page_content(search):
    import urllib.parse
    params = urllib.parse.parse_qs(search.lstrip('?'))
    repo_id = params.get('repo_id', [None])[0]

    if not repo_id:
        return html.Div([
            html.H3("No repo_id provided in the URL."),
            html.P("Example: http://your-dashboard:8050/?repo_id=CTFd")
        ])

    session = SessionLocal()

    try:
        profile_data = load_profile(session, repo_id)
    except Exception as e:
        session.close()
        return html.Div([
            html.H3(f"Error loading repo profile"),
            html.Pre(str(e))
        ])

    session.close()

    return html.Div([
        section_kpis.render(profile_data),
        section_tech_stack.render(profile_data),
        section_modernization.render(profile_data),
        section_code_metrics.render(profile_data),
        section_dependencies.render(profile_data),
        section_dependency_categories_chart_stacked.render(profile_data),
        section_dependency_risk_summary.render(profile_data),
        section_vulnerabilities.render(profile_data),
        section_eol.render(profile_data),
        section_code_risks_by_category.render(profile_data),
        section_compliance.render(profile_data),
        section_recent_activity.render(profile_data),
        section_health_overview.render(profile_data),
    ], style={"padding": "20px"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)