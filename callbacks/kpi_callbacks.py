from dash.dependencies import Input, Output
from data.fetch_overview_kpis import fetch_overview_kpis
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

            Output("kpi-old-repos", "children"),
            Output("kpi-old-repos-subtext", "children"),

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

            Output("kpi-dockerfiles", "children"),
            Output("kpi-dockerfiles-subtext", "children"),

            Output("kpi-docker-compose", "children"),
            Output("kpi-docker-compose-subtext", "children"),

            Output("kpi-helm-charts", "children"),
            Output("kpi-helm-charts-subtext", "children"),

            Output("kpi-sources", "children"),
            Output("kpi-sources-subtext", "children"),
        ],
        [Input("default-filter-store", "data")],
    )
    def update_kpi_values(store_data):
        filters = extract_filter_dict_from_store(store_data)
        kpi = fetch_overview_kpis(filters)

        # Basic repo metrics
        total_repos    = kpi.get("total_repos", 0)
        active         = kpi.get("active", 0)
        inactive       = kpi.get("inactive", 0)
        recently_updated = kpi.get("recently_updated", 0)
        new_repos        = kpi.get("new_repos", 0)
        old_repos        = kpi.get("old_repos", 0)
        massive_repos    = kpi.get("massive_repos", 0)

        # Contributors & branches
        solo            = kpi.get("solo_contributor", 0)
        total_contribs  = kpi.get("total_contributors", 0)
        branch_sprawl   = kpi.get("branch_sprawl", 0)

        # Build, runtime, language
        build_detected  = kpi.get("build_tool_detected", 0)
        modules         = kpi.get("modules", 0)
        without_tool    = kpi.get("without_tool", 0)
        runtime_detected = kpi.get("runtime_detected", 0)
        languages        = kpi.get("languages", 0)

        # CI/CD & IaC
        cicd_total = kpi.get("cicd_total", 0)
        ap         = kpi.get("azure_pipelines", 0)
        bp         = kpi.get("bitbucket_pipelines", 0)
        gl         = kpi.get("gitlab_ci", 0)
        jenkins    = kpi.get("jenkins", 0)

        dockerfiles    = kpi.get("dockerfiles", 0)
        docker_compose = kpi.get("docker_compose", 0)
        helm_charts    = kpi.get("helm_charts", 0)

        # Source hosts and code
        sources_total = kpi.get("sources_total", 0)
        loc             = kpi.get("loc", 0)
        source_files    = kpi.get("source_files", 0)

        return (
            # Total repos
            format_with_commas(total_repos),
            f"Active: {format_number_si(active)} · Inactive: {format_number_si(inactive)}",

            # Recent updates
            format_with_commas(recently_updated),
            f"New: {format_number_si(new_repos)} · 30d",

            # Old Repos
            format_with_commas(old_repos),
            ">1yr",

            # Massive Repos
            format_with_commas(massive_repos),
            "classification=Massive",

            # Solo contributors
            format_with_commas(solo),
            f"All: {format_number_si(total_contribs)}",

            # LOC (main uses SI as before), subtext updated
            format_number_si(loc),
            f"Files: {format_number_si(source_files)} · Repos: {format_number_si(total_repos)}",

            # Branch sprawl
            format_with_commas(branch_sprawl),
            ">10 branches",

            # Build tools
            format_with_commas(build_detected),
            f"Mod: {format_number_si(modules)} · NoTool: {format_number_si(without_tool)}",

            # Runtimes
            format_with_commas(runtime_detected),
            f"Langs: {format_number_si(languages)}",

            # CI/CD
            format_with_commas(cicd_total),
            f"AP: {format_number_si(ap)} · BP: {format_number_si(bp)} · GL: {format_number_si(gl)} · J: {format_number_si(jenkins)}",

            # Dockerfiles
            format_with_commas(dockerfiles),
            "Dockerfile",

            # Docker Compose
            format_with_commas(docker_compose),
            "docker-compose.yml",

            # Helm Charts
            format_with_commas(helm_charts),
            "Helm",

            # Source hosts
            format_with_commas(sources_total),
            "Hosts",
        )