from dash import Input, Output
from dash.exceptions import PreventUpdate

from data.overview.fetch_overview_kpis import fetch_overview_kpis
from utils.filter_utils import extract_filter_dict_from_store


def format_with_commas(value):
    if value is None:
        return "0"
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return "0"


def format_number_si(value):
    if value is None:
        return "0"
    try:
        num = float(value)
        for unit in ("", "K", "M", "B", "T"):
            if abs(num) < 1000:
                return f"{num:.0f}{unit}" if unit == "" else f"{num:.1f}{unit}"
            num /= 1000.0
        return f"{num:.1f}E"
    except (ValueError, TypeError):
        return "0"


def register_kpi_callbacks(app):
    @app.callback(
        [
            Output("kpi-total-repos", "children"),
            Output("kpi-total-repos-subtext", "children"),

            Output("kpi-avg-commits", "children"),
            Output("kpi-avg-commits-subtext", "children"),

            Output("kpi-oldest-repos", "children"),
            Output("kpi-oldest-repos-subtext", "children"),

            Output("kpi-massive-repos", "children"),
            Output("kpi-massive-repos-subtext", "children"),

            Output("kpi-avg-contributors", "children"),
            Output("kpi-avg-contributors-subtext", "children"),

            Output("kpi-avg-loc", "children"),
            Output("kpi-avg-loc-subtext", "children"),

            Output("kpi-branches", "children"),
            Output("kpi-branches-subtext", "children"),

            Output("kpi-build-tools", "children"),
            Output("kpi-build-tools-subtext", "children"),

            Output("kpi-runtime", "children"),
            Output("kpi-runtime-subtext", "children"),

            Output("kpi-cicd", "children"),
            Output("kpi-cicd-subtext", "children"),

            Output("kpi-container", "children"),
            Output("kpi-container-subtext", "children"),

            Output("kpi-sources", "children"),
            Output("kpi-sources-subtext", "children"),
        ],
        [Input("default-filter-store", "data")],
    )
    def update_kpi_values(store_data):
        filters = extract_filter_dict_from_store(store_data)
        kpi = fetch_overview_kpis(filters)

        # Massive repo breakdown subtext
        massive_subtext = (
            f"Code: {format_number_si(kpi.get('massive_code'))} · "
            f"Data: {format_number_si(kpi.get('massive_markup_or_data'))} · "
            f"None: {format_number_si(kpi.get('massive_no_language'))}"
        )

        # Lang group subtext
        lang_group_subtext = (
            f"Code: {format_number_si(kpi.get('lang_group_code'))} · "
            f"Data: {format_number_si(kpi.get('lang_group_markup_or_data'))} · "
            f"None: {format_number_si(kpi.get('lang_group_no_language'))}"
        )

        return (
            # Total Repos
            format_with_commas(kpi.get("total_repos")),
            lang_group_subtext,

            # Updates
            format_with_commas(kpi.get("new_repos")),
            f"Recent: {format_number_si(kpi.get('recently_updated'))} · 30d",

            # Oldest Repos
            format_with_commas(kpi.get("repos_3y")),
            f">3y: {format_number_si(kpi.get('repos_5y'))} · 10y: {format_number_si(kpi.get('repos_10y'))}",

            # Massive Repos
            format_with_commas(kpi.get("massive_repos")),
            massive_subtext,

            # Contributors
            format_with_commas(kpi.get("solo_contributor")),
            f"All: {format_number_si(kpi.get('total_contributors'))}",

            # LOC
            format_number_si(kpi.get("loc")),
            f"Files: {format_number_si(kpi.get('source_files'))} · Repos: {format_number_si(kpi.get('total_repos'))}",

            # Branches
            format_with_commas(kpi.get("branch_sprawl")),
            ">10 branches",

            # Build tools
            format_with_commas(kpi.get("build_tool_detected")),
            f"Modules: {format_number_si(kpi.get('modules'))} · NoTool: {format_number_si(kpi.get('without_tool'))}",

            # Runtime
            format_with_commas(kpi.get("runtime_detected")),
            f"Languages: {format_number_si(kpi.get('languages'))}",

            # CI/CD
            format_with_commas(kpi.get("cicd_total")),
            f"GitLab: {format_number_si(kpi.get('gitlab_ci'))} · Jenkins: {format_number_si(kpi.get('jenkins'))}",

            # Containers
            format_with_commas(kpi.get("dockerfiles")),
            f"Helm: {format_number_si(kpi.get('helm_charts'))} · Compose: {format_number_si(kpi.get('docker_compose'))}",

            # Sources
            format_with_commas(kpi.get("sources_total")),
            f"GitLab: {format_number_si(kpi.get('gitlab'))} · Bitbucket: {format_number_si(kpi.get('bitbucket'))}",
        )
