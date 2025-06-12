from dash import html
import dash_bootstrap_components as dbc

def render(profile_data):
    def kpi_card(title, main, sub):
        return dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(title, className="text-center bg-light", style={"fontSize": "0.8rem"}),
                    dbc.CardBody([
                        html.H4(main, className="text-center"),
                        html.Small(sub, className="text-center text-muted d-block", style={"fontSize": "0.7rem"})
                    ])
                ],
                className="mb-4 shadow-sm"
            ),
            xs=12, sm=6, md=4, lg=3
        )

    return dbc.Row(
        [
            kpi_card("Total Repositories", profile_data["total_repos"], f"Active: {profile_data['active']} · Inactive: {profile_data['inactive']}"),
            kpi_card("Recently Updated", profile_data["recently_updated"], f"New: {profile_data['new_repos']} · Total: {profile_data['total_repos']}"),
            kpi_card("Build Tool Coverage", profile_data["build_tool_detected"], f"Modules: {profile_data['modules']} · Unknown: {profile_data['without_tool']}"),
            kpi_card("Runtime Version Coverage", profile_data["runtime_detected"], f"Langs: {profile_data['languages']} · With Tool: {profile_data['build_tool_detected']}"),
            kpi_card("CI/CD Detected", profile_data["cicd_total"], f"Jenkins: {profile_data['jenkins']} · GH Actions: {profile_data['gha']} · TeamCity: {profile_data['teamcity']}"),
            kpi_card("Sources Connected", profile_data["sources_total"], f"GitHub: {profile_data['github']} · GitLab: {profile_data['gitlab']} · Bitbucket: {profile_data['bitbucket']}"),
            kpi_card("Lines of Code", f"{profile_data['loc']:,}", f"Source Files: {profile_data['source_files']} · Repos: {profile_data['total_repos']}"),
            kpi_card("Solo-Contributor Repos", profile_data["solo_contributor"], f"Contributors: {profile_data['total_contributors']} · Tracked: {profile_data['total_repos']}"),
            kpi_card("Branch Complexity", profile_data["branch_sprawl"], f">10 branches · Across {profile_data['total_repos']} repos"),
        ],
        className="g-3 mb-4",
        justify="around"
    )