from dash.dependencies import Input, Output
from data.fetch_overview_kpis import fetch_overview_kpis
from utils.filter_utils import extract_filter_dict_from_store

def format_number_short(value):
    if value is None:
        return "0"
    try:
        n = int(value)
        if n >= 1_000_000:
            return f"{n/1_000_000:.1f}M"
        if n >= 1_000:
            return f"{n/1_000:.0f}K"
        return str(n)
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

        return (
            # Repos
            kpi.get("total_repos", 0),
            f"A:{kpi.get('active', 0)} · I:{kpi.get('inactive', 0)}",

            # Recent Updates
            kpi.get("recently_updated", 0),
            f"New:{kpi.get('new_repos', 0)} · 30d",

            # Solo Devs
            kpi.get("solo_contributor", 0),
            f"All:{kpi.get('total_contributors', 0)}",

            # LOC
            format_number_short(kpi.get("loc")),
            f"Files:{format_number_short(kpi.get('source_files'))} · Repos:{kpi.get('total_repos', 0)}",

            # Branching
            kpi.get("branch_sprawl", 0),
            ">10 branches",

            # Build Tools
            kpi.get("build_tool_detected", 0),
            f"Mod:{kpi.get('modules', 0)} · NoTool:{kpi.get('without_tool', 0)}",

            # Runtimes
            kpi.get("runtime_detected", 0),
            f"Langs:{kpi.get('languages', 0)}",

            # CI/CD (total + breakdown)
            kpi.get("cicd_total", 0),
            f"BP:{kpi.get('bitbucket_pipelines', 0)} · GL:{kpi.get('gitlab_ci', 0)} · J:{kpi.get('jenkins', 0)}",

            # Source Hosts
            kpi.get("sources_total", 0),
            "Hosts",
        )
