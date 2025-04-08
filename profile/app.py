import urllib.parse
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Import your sections (in the exact order you requested)
import sections.section_kpis as section_kpis
import sections.section_tech_stack as section_tech_stack
import sections.section_modernization as section_modernization
import sections.section_code_quality as section_code_quality
import sections.section_git_activity_hygiene as section_git_activity_hygiene
import sections.section_eol_risks as section_eol_risks
import sections.section_dependency_risk_summary as section_dependency_risk_summary

# Import the profile loader from services (no duplication here):
from services.profile_loader import load_profile
import sections.section_bio as bio


# Database info
DATABASE_URL = "postgresql://postgres:postgres@192.168.1.188:5432/gitlab-usage"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Initialize Dash
app = Dash(__name__, use_pages=False, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback for reading repo_id from URL
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'search')
)
def render_page_content(search):
    params = urllib.parse.parse_qs(search.lstrip('?'))
    repo_id = params.get('repo_id', [None])[0]

    if not repo_id:
        return html.Div([
            html.H3("No repo_id provided in the URL."),
            html.P("Try: http://<your-host>:8050/?repo_id=vulnerable-apps/secDevLabs")
        ])


    session = SessionLocal()
    try:
        profile_data = load_profile(session, repo_id)
    except Exception as e:
        session.close()
        return html.Div([
            html.H3("Error loading repo profile"),
            html.Pre(str(e))
        ])
    session.close()

    # Render sections in the exact original order
    return html.Div([
        bio.render(profile_data),
        section_kpis.render(profile_data),
        section_tech_stack.render(profile_data),
        section_modernization.render(profile_data),
        section_code_quality.render(profile_data),
        section_git_activity_hygiene.render(profile_data),
        section_dependency_risk_summary.render(profile_data),
        section_eol_risks.render(profile_data),


    ], style={"padding": "20px"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
