import urllib.parse
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Sections
import profile.sections.section_kpis as section_kpis
import profile.sections.section_tech_stack as section_tech_stack
import profile.sections.section_modernization as section_modernization
import profile.sections.section_code_quality as section_code_quality
import profile.sections.section_git_activity_hygiene as section_git_activity_hygiene
import profile.sections.section_dependency_risk_summary as section_dependency_risk_summary
import profile.sections.section_eol_risks as section_eol_risks
import profile.sections.section_bio as bio

# Service
from profile.services.profile_loader import load_profile

# Database
DATABASE_URL = "postgresql://postgres:postgres@192.168.1.188:5432/gitlab-usage"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Register the page
dash.register_page(
    __name__,
    path="/repo",  # The page will be available at /repo?repo_id=...
    name="Repository Profile",
    title="Repository Profile"
)

layout = html.Div([
    dcc.Location(id='repo-url', refresh=False),
    html.Div(id='repo-profile-content')
])

# Callback to render based on URL parameter
@dash.callback(
    Output('repo-profile-content', 'children'),
    Input('repo-url', 'search')
)
def render_repo_profile(search):
    if not search:
        return html.Div([
            html.H3("No repo_id provided."),
            html.P("Please provide a repo_id in the URL parameters."),
        ])

    params = urllib.parse.parse_qs(search.lstrip('?'))
    repo_id = params.get('repo_id', [None])[0]

    if not repo_id:
        return html.Div([
            html.H3("No repo_id provided."),
            html.P("Please provide a repo_id in the URL parameters."),
        ])

    session = SessionLocal()
    try:
        profile_data = load_profile(session, repo_id)
    except Exception as e:
        return html.Div([
            html.H3("Error loading profile"),
            html.Pre(str(e))
        ])
    finally:
        session.close()

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
