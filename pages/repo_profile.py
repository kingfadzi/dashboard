import urllib.parse
from dash import html
from data.fetch_repo_profile import fetch_repo_profile

# Sections
import profile.sections.section_bio as bio
import profile.sections.section_kpis as section_kpis
import profile.sections.section_tech_stack as section_tech_stack
import profile.sections.section_modernization as section_modernization
import profile.sections.section_code_quality as section_code_quality
import profile.sections.section_git_activity_hygiene as section_git_activity_hygiene
import profile.sections.section_dependency_risk_summary as section_dependency_risk_summary
import profile.sections.section_eol_risks as section_eol_risks

def render_repo_profile_content(search: str):
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

    try:
        profile_data = fetch_repo_profile(repo_id)
    except Exception as e:
        return html.Div([
            html.H3("Error loading profile"),
            html.Pre(str(e))
        ])

    return html.Div([
        bio.render(profile_data),
        section_kpis.render(profile_data),
        section_modernization.render(profile_data),
        section_tech_stack.render(profile_data),
        section_code_quality.render(profile_data),
        section_git_activity_hygiene.render(profile_data),
        section_dependency_risk_summary.render(profile_data),
        section_eol_risks.render(profile_data),
    ], style={"padding": "20px"})