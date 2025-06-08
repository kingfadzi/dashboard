# callbacks/repo_profile_callbacks.py

import urllib.parse
from dash import Input, Output, callback, html
from dash.exceptions import PreventUpdate
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

from data.fetch_repo_profile import fetch_repo_profile, fetch_harvested_repo, classify_language_from_db

def register_repo_profile_callbacks(app):
    @app.callback(
        Output("repo-profile-content", "children"),
        Input("url", "search"),
    )
    def update_repo_profile_content(search):
        if not search:
            raise PreventUpdate

        params = urllib.parse.parse_qs(search.lstrip("?"))
        repo_id = params.get("repo_id", [None])[0]

        if not repo_id:
            return html.Div([
                html.H3("No repo_id provided."),
                html.P("Please provide a repo_id in the URL parameters."),
            ])

        try:
            profile_data = fetch_repo_profile(repo_id)
            harvested_repo = fetch_harvested_repo(repo_id)
            app_id = harvested_repo.get("app_id")
            main_language = harvested_repo.get("main_language")
            language_group = classify_language_from_db(main_language)
        except Exception as e:
            return html.Div([
                html.H3("Error loading profile"),
                html.Pre(str(e))
            ])

        children = []

        if app_id:
            children.append(bio.render(profile_data))

        children.append(section_kpis.render(profile_data))

        if language_group not in {"no_language", "markup_or_data", "other_programming"}:
            children.extend([
                section_modernization.render(profile_data),
                section_tech_stack.render(profile_data),
                section_code_quality.render(profile_data),
                section_git_activity_hygiene.render(profile_data),
                section_dependency_risk_summary.render(profile_data),
                section_eol_risks.render(profile_data),
            ])

        return html.Div(children, style={"padding": "20px"})
