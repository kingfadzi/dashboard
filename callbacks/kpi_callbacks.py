from dash import Input, Output
from utils.filter_utils import extract_filter_dict_from_store
from data.fetch_overview_kpis import fetch_overview_kpis


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

            Output("kpi-sources", "children"),
            Output("kpi-sources-subtext", "children"),
        ],
        [Input("default-filter-store", "data")],
    )
    def update_kpi_values(store_data):
        filters = extract_filter_dict_from_store(store_data)
        kpi = fetch_overview_kpis(filters)

        total_repos = kpi.get("total_repos", 0)
        active = kpi.get("active", 0)
        inactive = kpi.get("inactive", 0)

        recently_updated = kpi.get("recently_updated", 0)
        new_repos = kpi.get("new_repos", 0)

        solo = kpi.get("solo_contributor", 0)
        total_contribs = kpi.get("total_contributors", 0)

        loc = kpi.get("loc", 0)
        source_files = kpi.get("source_files", 0)

        branch_sprawl = kpi.get("branch_sprawl", 0)

        build_detected = kpi.get("build_tool_detected", 0)
        modules = kpi.get("modules", 0)
        without_tool = kpi.get("without_tool", 0)

        runtime_detected = kpi.get("runtime_detected", 0)
        languages = kpi.get("languages", 0)

        cicd_total = kpi.get("cicd_total", 0)
        bp = kpi.get("bitbucket_pipelines", 0)
        gl = kpi.get("gitlab_ci", 0)
        jenkins = kpi.get("jenkins", 0)

        sources_total = kpi.get("sources_total", 0)

        return (
            format_with_commas(total_repos),
            f"Active: {format_number_si(active)} · Inactive: {format_number_si(inactive)}",

            format_with_commas(recently_updated),
            f"New: {format_number_si(new_repos)} · 30d",

            format_with_commas(solo),
            f"All: {format_number_si(total_contribs)}",

            format_number_si(loc),
            f"Files: {format_number_si(source_files)} · Repos: {format_number_si(total_repos)}",

            format_with_commas(branch_sprawl),
            ">10 branches",

            format_with_commas(build_detected),
            f"Modules: {format_number_si(modules)} · NoTool: {format_number_si(without_tool)}",

            format_with_commas(runtime_detected),
            f"Languages: {format_number_si(languages)}",

            format_with_commas(cicd_total),
            f"GitLab: {format_number_si(gl)} · Jenkins: {format_number_si(jenkins)}",

            format_with_commas(sources_total),
            "Hosts",
        )