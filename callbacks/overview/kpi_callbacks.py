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

        return (
            # Total repos
            format_with_commas(kpi.get("total_repos", 0)),
            f"Active: {format_number_si(kpi.get('active'))} · Inactive: {format_number_si(kpi.get('inactive'))}",

            # Updates
            format_with_commas(kpi.get("recently_updated", 0)),
            f"New: {format_number_si(kpi.get('new_repos'))} · 30d",

            # Oldest repos
            format_with_commas(kpi.get("old_repos_total", 0)),
            f"3y: {format_number_si(kpi.get('repos_3y'))} · 4y: {format_number_si(kpi.get('repos_4y'))} · 5y: {format_number_si(kpi.get('repos_5y'))}",

            # Massive repos
            format_with_commas(kpi.get("massive_repos", 0)),
            f">500K LOC",

            # Contributors
            format_with_commas(kpi.get("solo_contributor", 0)),
            f"All: {format_number_si(kpi.get('total_contributors'))}",

            # LOC
            format_number_si(kpi.get("loc")),
            f"Files: {format_number_si(kpi.get('source_files'))} · Repos: {format_number_si(kpi.get('total_repos'))}",

            # Branches
            format_with_commas(kpi.get("branch_sprawl", 0)),
            ">10 branches",

            # Build tools
            format_with_commas(kpi.get("build_tool_detected", 0)),
            f"Modules: {format_number_si(kpi.get('modules'))} · NoTool: {format_number_si(kpi.get('without_tool'))}",

            # Runtime
            format_with_commas(kpi.get("runtime_detected", 0)),
            f"Languages: {format_number_si(kpi.get('languages'))}",

            # CI/CD
            format_with_commas(kpi.get("cicd_total", 0)),
            f"GL: {format_number_si(kpi.get('gitlab_ci'))} · Jenkins: {format_number_si(kpi.get('jenkins'))}",

            # Containerization
            format_with_commas(kpi.get("dockerfiles", 0)),
            f"Helm: {format_number_si(kpi.get('helm_charts'))} · Compose: {format_number_si(kpi.get('docker_compose'))}",

            # Sources
            format_with_commas(kpi.get("sources_total", 0)),
            "Hosts",
        )